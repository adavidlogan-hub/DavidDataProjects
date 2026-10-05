"""Find each county's election and results pages, and fingerprint the results platform.

Starts from the SOS-listed county website (data/seed_counties.csv), follows links
whose text or URL mentions elections or results, up to a small per-county page
budget, and records every candidate results link with the page it was found on.
The platform field is a fingerprint of what the links show, never a guess:

  clarity_style   link to *.clarityelections.com
  sos_feed_only   only results link found points at the SOS results site
  county_pdfs     results links are PDFs (or other documents) on a county host
  vendor_hosted   results link on a configured vendor host other than Clarity
  homegrown       results pages (HTML) on the county's own host
  unknown         nothing conclusive found

Output: data/link_discovery.csv and data/link_discovery.json (all candidates).

    python -m phase1.discover_links [--only Harris,Dallas] [--workers 20] [--budget 8]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from txprecinct.fetch import FetchClient  # noqa: E402

DATA = Path(__file__).resolve().parent.parent / "data"
ELECTION_RE = re.compile(r"elect|vot(e|er|ing)|ballot", re.I)
RESULTS_RE = re.compile(r"result|returns|canvass|cumulative|precinct|summary|\benr\b|clarityelections|"
                        r"texas-election\.com", re.I)
DOC_RE = re.compile(r"\.(pdf|xlsx?|csv|txt|docx?)(\?|$)", re.I)
SOS_RESULTS_HOSTS = ("results.texas-election.com", "sos.state.tx.us", "sos.texas.gov")
SKIP_RE = re.compile(r"^(mailto:|tel:|javascript:|#)", re.I)


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self._href = None
        self._text: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self._href = dict(attrs).get("href")
            self._text = []

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._href is not None:
            self.links.append((self._href.strip(), " ".join("".join(self._text).split())))
            self._href = None


def extract_links(base_url: str, body: bytes) -> list[tuple[str, str]]:
    p = LinkParser()
    try:
        p.feed(body.decode("utf-8", errors="replace"))
    except Exception as e:  # malformed HTML: keep what was parsed, note nothing else
        print(f"warn: parse error on {base_url}: {e}", file=sys.stderr)
    out = []
    for href, text in p.links:
        if not href or SKIP_RE.match(href):
            continue
        out.append((urljoin(base_url, href), text))
    return out


def fingerprint(candidates: list[dict], county_hosts: set[str], vendor_suffixes: tuple[str, ...]) -> tuple[str, str]:
    """Return (platform, evidence_url)."""
    def host(u):
        return (urlsplit(u).hostname or "").lower()
    for c in candidates:
        if host(c["url"]).endswith("clarityelections.com"):
            return "clarity_style", c["url"]
    for c in candidates:
        h = host(c["url"])
        if any(h == s or h.endswith("." + s) for s in vendor_suffixes) and RESULTS_RE.search(c["url"] + " " + c["text"]):
            return "vendor_hosted", c["url"]
    county_results = [c for c in candidates if host(c["url"]) in county_hosts]
    docs = [c for c in county_results if DOC_RE.search(c["url"])]
    pages = [c for c in county_results if not DOC_RE.search(c["url"])]
    if docs and len(docs) >= len(pages):
        return "county_pdfs", docs[0]["url"]
    if pages:
        return "homegrown", pages[0]["url"]
    sos = [c for c in candidates if any(host(c["url"]).endswith(s) for s in SOS_RESULTS_HOSTS)]
    if sos:
        return "sos_feed_only", sos[0]["url"]
    return "unknown", ""


def discover(client: FetchClient, county: str, start: str, budget: int, vendor_suffixes) -> dict:
    rec = {"county": county, "start_url": start, "pages_fetched": [], "errors": [], "election_pages": [],
           "candidates": []}
    if not start:
        rec["platform"], rec["platform_evidence"] = "unknown", ""
        rec["note"] = "SOS lists no county website"
        return rec
    county_hosts = {(urlsplit(start).hostname or "").lower()}
    queue, seen, fetched = [(start, 0)], {start}, 0
    while queue and fetched < budget:
        url, depth = queue.pop(0)
        r = client.get(url, purpose=f"discover:{county}")
        fetched += 1
        if not r.ok:
            rec["errors"].append({"url": url, "error": r.error, "status": r.status})
            continue
        final = r.final_url or url
        county_hosts.add((urlsplit(final).hostname or "").lower())
        rec["pages_fetched"].append({"url": url, "final_url": final, "content_hash": r.content_hash})
        ctype = (r.headers.get("content-type") or "").lower()
        if "html" not in ctype and ctype:
            continue
        for link, text in extract_links(final, r.body):
            if link in seen:
                continue
            blob = link + " " + text
            if RESULTS_RE.search(blob) and ELECTION_RE.search(blob + " " + final) or \
               urlsplit(link).hostname and urlsplit(link).hostname.endswith(("clarityelections.com",) + SOS_RESULTS_HOSTS):
                seen.add(link)
                rec["candidates"].append({"url": link, "text": text[:160], "found_on": final, "depth": depth + 1})
                h = (urlsplit(link).hostname or "").lower()
                if depth < 2 and not DOC_RE.search(link) and (h in county_hosts or ELECTION_RE.search(h)):
                    queue.append((link, depth + 1))
            elif ELECTION_RE.search(blob) and depth < 1:
                seen.add(link)
                rec["election_pages"].append({"url": link, "text": text[:160], "found_on": final})
                h = (urlsplit(link).hostname or "").lower()
                if h in county_hosts or ELECTION_RE.search(h):
                    queue.insert(0, (link, depth + 1))
    rec["platform"], rec["platform_evidence"] = fingerprint(rec["candidates"], county_hosts, vendor_suffixes)
    return rec


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=20)
    ap.add_argument("--budget", type=int, default=8, help="max pages fetched per county")
    a = ap.parse_args(argv)
    seed = list(csv.DictReader(open(DATA / "seed_counties.csv", encoding="utf-8")))
    assert len(seed) == 254, f"seed has {len(seed)} rows"
    only = {c.strip() for c in a.only.split(",") if c.strip()}
    rows = [r for r in seed if not only or r["county"] in only]
    client = FetchClient(agent="discover-links")
    vendor = client.cfg.host_classes["vendor"].suffixes
    t0, results = time.time(), []
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(discover, client, r["county"], r["county_website_sos"], a.budget, vendor): r["county"]
                for r in rows}
        for f in as_completed(futs):
            try:
                results.append(f.result())
            except Exception as e:  # one county's crash is recorded loudly, not allowed to stop the other 253
                results.append({"county": futs[f], "start_url": "", "platform": "unknown", "platform_evidence": "",
                                "candidates": [], "pages_fetched": [], "election_pages": [],
                                "errors": [{"url": "", "error": f"CRASH {type(e).__name__}: {e}", "status": None}]})
            print(f"{len(results)}/{len(rows)} {futs[f]}: {results[-1]['platform']}", flush=True)
    results.sort(key=lambda r: r["county"])
    out_json = DATA / ("link_discovery.json" if not only else "link_discovery_partial.json")
    out_json.write_text(json.dumps({"generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                    "elapsed_seconds": round(time.time() - t0, 1), "counties": results}, indent=2))
    with open(out_json.with_suffix(".csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["county", "start_url", "platform", "platform_evidence", "n_candidates", "top_candidates",
                    "pages_fetched", "errors"])
        for r in results:
            w.writerow([r["county"], r["start_url"], r["platform"], r["platform_evidence"], len(r["candidates"]),
                        " | ".join(c["url"] for c in r["candidates"][:5]), len(r["pages_fetched"]),
                        " | ".join(f"{e['url']}: {e['error']}" for e in r["errors"][:3])])
    print(json.dumps({"counties": len(results), "elapsed_seconds": round(time.time() - t0, 1),
                      "by_platform": {p: sum(r["platform"] == p for r in results)
                                      for p in sorted({r["platform"] for r in results})}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
