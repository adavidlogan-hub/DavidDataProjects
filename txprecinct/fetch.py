"""The one fetch client every agent, script, and the poller uses.

Guarantees:
  * honest User-Agent from config
  * robots.txt respected (RFC 9309: 4xx means allow all; 5xx or unreachable means disallow all)
  * per-host rate limits from config/fetch.toml, enforced across processes
  * 20 second timeout, 2 retries with exponential backoff, then a logged failure
  * every response cached with timestamp and SHA-256; bodies stored once per hash
  * cached pages are returned instead of refetched unless the caller asks otherwise
  * conditional requests (ETag / If-Modified-Since) when refreshing a cached URL
"""
from __future__ import annotations

import email.utils
import os
import ssl
import time
import urllib.error
import urllib.request
import urllib.robotparser
from dataclasses import dataclass, field
from urllib.parse import quote, urlsplit, urlunsplit

from .config import FetchConfig, HostClass, load_config
from .ratelimit import HostLimiter
from .store import Store

RETRYABLE_STATUS = {408, 429, 500, 502, 503, 504}
_PATH_SAFE = "/%:@!$&'()*+,;=-._~"
_QUERY_SAFE = "/%:@!$&'()*+,;=-._~?"


def normalize_url(url: str) -> str:
    """Percent-encode characters that cannot appear in a request line (spaces, control
    characters, non-ASCII) without touching existing escapes. Drops the fragment."""
    p = urlsplit(url.strip())
    return urlunsplit((p.scheme.lower(), p.netloc, quote(p.path, safe=_PATH_SAFE),
                       quote(p.query, safe=_QUERY_SAFE), ""))


@dataclass
class FetchResult:
    url: str
    status: int | None
    body: bytes | None
    content_hash: str | None
    fetched_at: float
    from_cache: bool = False
    not_modified: bool = False
    error: str | None = None
    headers: dict = field(default_factory=dict)
    final_url: str | None = None
    attempts: int = 0

    @property
    def ok(self) -> bool:
        return self.error is None and self.body is not None

    def text(self, encoding: str = "utf-8") -> str:
        if self.body is None:
            raise RuntimeError(f"no body for {self.url}: {self.error}")
        return self.body.decode(encoding, errors="replace")


class FetchClient:
    def __init__(self, config: FetchConfig | None = None, agent: str = "unknown"):
        self.cfg = config or load_config()
        self.agent = agent
        self.store = Store(self.cfg.state_dir)
        lease = self.cfg.timeout_seconds * 2 + 30
        self.limiter = HostLimiter(self.store, self.cfg.global_max_concurrency, lease)
        self._robots_mem: dict[str, tuple[float, urllib.robotparser.RobotFileParser]] = {}
        self._opener = self._build_opener()

    def _build_opener(self) -> urllib.request.OpenerDirector:
        cafile = self.cfg.ca_bundle or os.environ.get("SSL_CERT_FILE") or None
        ctx = ssl.create_default_context(cafile=cafile) if cafile else ssl.create_default_context()
        return urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))

    # Public API ------------------------------------------------------------
    def get(self, url: str, *, use_cache: bool = True, max_age: float | None = None,
            conditional: bool = True, purpose: str = "") -> FetchResult:
        """Fetch url. Returns the cached copy when use_cache and fresh enough."""
        url = normalize_url(url)
        parts = urlsplit(url)
        if parts.scheme not in ("http", "https") or not parts.hostname:
            raise ValueError(f"unsupported URL: {url!r}")
        cached = self.store.latest_ok(url)
        if cached is not None and use_cache and (max_age is None or time.time() - cached["fetched_at"] <= max_age):
            return self._result_from_row(cached, from_cache=True)

        host = parts.hostname.lower()
        hc = self.cfg.classify(host)
        if self.cfg.respect_robots and not self._robots_allows(url, parts, hc):
            rec = self._base_rec(url, host, hc, purpose)
            rec.update(error="robots_disallowed_or_unreachable", attempts=0)
            self.store.record_fetch(rec, ok=False)
            return FetchResult(url=url, status=None, body=None, content_hash=None,
                               fetched_at=rec["fetched_at"], error=rec["error"])

        extra = {}
        if conditional and cached is not None:
            if cached["etag"]:
                extra["If-None-Match"] = cached["etag"]
            if cached["last_modified"]:
                extra["If-Modified-Since"] = cached["last_modified"]
        return self._fetch_with_retries(url, host, hc, extra, cached, purpose)

    # Internals -------------------------------------------------------------
    def _base_rec(self, url: str, host: str, hc: HostClass, purpose: str) -> dict:
        return {"url": url, "host": host, "host_class": hc.name, "fetched_at": time.time(),
                "agent": self.agent, "purpose": purpose}

    def _fetch_with_retries(self, url, host, hc, extra_headers, cached, purpose) -> FetchResult:
        attempts = 1 + self.cfg.retries
        last_err = None
        last_status = None
        for attempt in range(attempts):
            slot = self.limiter.acquire(host, hc)
            t0 = time.time()
            try:
                status, body, headers, final_url, err = self._raw_request(url, extra_headers)
            finally:
                self.limiter.release(slot)
            elapsed_ms = int((time.time() - t0) * 1000)
            rec = self._base_rec(url, host, hc, purpose)
            rec.update(status=status, elapsed_ms=elapsed_ms, attempts=attempt + 1, final_url=final_url)

            if status == 304 and cached is not None:
                rec.update(content_hash=cached["content_hash"], content_type=cached["content_type"],
                           etag=headers.get("etag") or cached["etag"],
                           last_modified=headers.get("last-modified") or cached["last_modified"])
                self.store.record_fetch(rec, ok=True)
                res = self._result_from_row(cached, from_cache=False)
                res.not_modified, res.status, res.fetched_at, res.attempts = True, 304, rec["fetched_at"], attempt + 1
                return res

            if err is None and status is not None and 200 <= status < 300 and body is not None:
                h = self.store.put_blob(body)
                rec.update(content_hash=h, content_type=headers.get("content-type"),
                           etag=headers.get("etag"), last_modified=headers.get("last-modified"))
                self.store.record_fetch(rec, ok=True)
                return FetchResult(url=url, status=status, body=body, content_hash=h,
                                   fetched_at=rec["fetched_at"], headers=headers,
                                   final_url=final_url, attempts=attempt + 1)

            last_err = err or f"HTTP {status}"
            last_status = status
            if status == 429:
                self.limiter.backoff(host, self._backoff_429(hc, headers, attempt))
            retryable = err is not None or status in RETRYABLE_STATUS
            if not retryable or attempt == attempts - 1:
                # Keep a non-2xx body if one came back; it is raw evidence too.
                if body:
                    rec["content_hash"] = self.store.put_blob(body)
                rec["error"] = last_err
                self.store.record_fetch(rec, ok=False)
                return FetchResult(url=url, status=last_status, body=None, content_hash=rec.get("content_hash"),
                                   fetched_at=rec["fetched_at"], error=last_err, headers=headers,
                                   final_url=final_url, attempts=attempt + 1)
            if status != 429:
                time.sleep(self.cfg.retry_backoff_base_seconds * (2 ** attempt))
        raise AssertionError("unreachable: retry loop must return")

    def _backoff_429(self, hc: HostClass, headers: dict, attempt: int) -> float:
        ra = headers.get("retry-after")
        if ra:
            try:
                return max(float(ra), 1.0)
            except ValueError:
                dt = email.utils.parsedate_to_datetime(ra)
                if dt is not None:
                    return max(dt.timestamp() - time.time(), 1.0)
        base = hc.backoff_on_429_seconds
        return base * (2 ** attempt) if hc.exponential_backoff else base

    def _raw_request(self, url: str, extra_headers: dict):
        """Returns (status, body, headers, final_url, error). Never raises for HTTP/network errors."""
        headers = {"User-Agent": self.cfg.user_agent, "Accept": "*/*", **extra_headers}
        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with self._opener.open(req, timeout=self.cfg.timeout_seconds) as resp:
                body = resp.read()
                return resp.status, body, {k.lower(): v for k, v in resp.headers.items()}, resp.geturl(), None
        except urllib.error.HTTPError as e:
            try:
                body = e.read()
            except Exception:
                body = None
            hdrs = {k.lower(): v for k, v in (e.headers.items() if e.headers else [])}
            return e.code, body, hdrs, url, None
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            reason = getattr(e, "reason", e)
            return None, None, {}, url, f"{type(e).__name__}: {reason}"

    def _result_from_row(self, row, from_cache: bool) -> FetchResult:
        body = self.store.get_blob(row["content_hash"])
        return FetchResult(url=row["url"], status=row["status"], body=body, content_hash=row["content_hash"],
                           fetched_at=row["fetched_at"], from_cache=from_cache, final_url=row["final_url"],
                           headers={"etag": row["etag"], "last-modified": row["last_modified"],
                                    "content-type": row["content_type"]})

    def _robots_allows(self, url: str, parts, hc: HostClass) -> bool:
        origin = f"{parts.scheme}://{parts.netloc}"
        host = parts.netloc.lower()
        now = time.time()
        mem = self._robots_mem.get(host)
        if mem and mem[0] > now:
            return mem[1].can_fetch(self.cfg.user_agent, url)
        row = self.store.get_robots(host)
        if row is not None:
            ttl = self.cfg.robots_failure_cache_seconds if row["error"] else self.cfg.robots_cache_seconds
            if now - row["checked_at"] <= ttl:
                rp = self._parser_from(row["status"], row["body"], row["error"])
                self._robots_mem[host] = (row["checked_at"] + ttl, rp)
                return rp.can_fetch(self.cfg.user_agent, url)
        # Same retry policy as page fetches: a transient refusal must not be cached as "disallow all".
        for attempt in range(1 + self.cfg.retries):
            slot = self.limiter.acquire(parts.hostname.lower(), hc)
            try:
                status, body, _h, _f, err = self._raw_request(origin + "/robots.txt", {})
            finally:
                self.limiter.release(slot)
            if err is None and status is not None and status >= 500:
                err = f"HTTP {status}"
            if status == 429:
                err = "HTTP 429"
            if err is None or attempt == self.cfg.retries:
                break
            time.sleep(self.cfg.retry_backoff_base_seconds * (2 ** attempt))
        text = body.decode("utf-8", errors="replace") if body else None
        self.store.put_robots(host, status, text, err)
        if err:
            rec = self._base_rec(origin + "/robots.txt", parts.hostname.lower(), hc, "robots")
            rec.update(status=status, attempts=1, error=err)
            self.store.record_fetch(rec, ok=False)
        rp = self._parser_from(status, text, err)
        ttl = self.cfg.robots_failure_cache_seconds if err else self.cfg.robots_cache_seconds
        self._robots_mem[host] = (now + ttl, rp)
        return rp.can_fetch(self.cfg.user_agent, url)

    @staticmethod
    def _parser_from(status, body, error) -> urllib.robotparser.RobotFileParser:
        rp = urllib.robotparser.RobotFileParser()
        if error:
            rp.disallow_all = True
        elif status is not None and 400 <= status < 500:
            rp.allow_all = True
        elif status is not None and 200 <= status < 300:
            rp.parse((body or "").splitlines())
        else:
            rp.disallow_all = True
        return rp
