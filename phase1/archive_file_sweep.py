"""Archived results-file sweep (targeted pass 3).

The Wayback Machine keeps the original server's Last-Modified header with every
capture, so a report file captured days after an election still shows when the
county uploaded it. For each county host in the targets file this script lists
archived results files (PDF, CSV, spreadsheets, text, and vendor results pages)
captured from election day to 21 days after, for each of the three elections,
replays the earliest capture of each distinct file version, and records:
original Last-Modified and Date headers, PDF CreationDate and ModDate, printed
date-times and a text sample from the first pages (PDFs), "Website Updated"
style strings (HTML), and whether the upload time or a printed time falls on
election night (7 PM to 3 AM local). Raw replays under 30 MB are saved.

All requests go through the fetch module (archive.org: 1 request per 2 s,
robots.txt, cache). Facts only; deciding results is left to the checklist rules.

    python -m phase1.archive_file_sweep --targets phase1/targeted/sweep_targets.json --out phase1/targeted/sweep
"""
from __future__ import annotations

import argparse
import email.utils
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from phase1.pdf_probe import pdf_info  # noqa: E402

# Election day (local date) and the UTC offset in force on election night.
ELECTIONS = {
    "2024_general": ("2024-11-05", -6),
    "2026_primary": ("2026-03-03", -6),
    "2026_runoff": ("2026-05-26", -5),
}
WINDOW_DAYS = 21
FILE_MIME = r"(application/pdf|text/csv|text/plain|application/vnd.*|application/octet-stream|application/zip|application/x-zip.*|application/json|text/xml|application/xml)"
HTML_MIME = r"(text/html|application/json|text/xml|application/xml)"
KEYWORDS = r"(?i).*(elect|result|precinct|pct|canvass|cumul|unofficial|official|sovc|statement|summary|vote|returns|tally|report|general|primary|runoff|2024|2026).*"
SCORE = [(r"(?i)precinct|pct|sovc|statement.of.votes|canvass", 4), (r"(?i)unofficial|cumulative|election.?night|night|final", 2),
         (r"(?i)general|primary|runoff|nov|mar|may|2024|2026", 1), (r"(?i)result|summary|report", 1)]
UPDATED_RE = re.compile(r"(?i)(website updated|last updated|updated|as of|report generated|run date|printed)[^0-9]{0,40}"
                        r"(\d{1,2}/\d{1,2}/\d{2,4}[ ,]+\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)?)")
PRINTED_FMT = ("%m/%d/%Y %I:%M %p", "%m/%d/%Y %I:%M:%S %p", "%m/%d/%Y %H:%M", "%m/%d/%y %I:%M %p")
SAVE_LIMIT = 30 * 1024 * 1024
MAX_FILE_REPLAYS_PER_ELECTION = 12
MAX_PAGE_REPLAYS_PER_ELECTION = 4


def night_bounds(election: str) -> tuple[datetime, datetime, int]:
    day, off = ELECTIONS[election]
    d = datetime.strptime(day, "%Y-%m-%d")
    return d + timedelta(hours=19), d + timedelta(days=1, hours=3), off


def local_from_http(value: str | None, off: int) -> datetime | None:
    if not value:
        return None
    try:
        dt = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone(timedelta(hours=off))).replace(tzinfo=None)


def parse_printed(s: str) -> datetime | None:
    s = re.sub(r"\s+", " ", s.replace(",", " ")).strip()
    for f in PRINTED_FMT:
        try:
            return datetime.strptime(s.upper(), f)
        except ValueError:
            continue
    return None


def score(url: str) -> int:
    return sum(w for rx, w in SCORE if re.search(rx, url))


def cdx_url(prefix: str, election: str, mime: str, first_day: int = 0, days: int = WINDOW_DAYS) -> str:
    day, off = ELECTIONS[election]
    start = datetime.strptime(day, "%Y-%m-%d") - timedelta(hours=off) + timedelta(days=first_day)  # local midnight in UTC
    end = start + timedelta(days=days)
    return ("https://web.archive.org/cdx/search/cdx?url=" + quote(prefix, safe="") + "&matchType=prefix&output=json"
            f"&from={start:%Y%m%d%H%M%S}&to={end:%Y%m%d%H%M%S}"
            "&fl=timestamp,original,statuscode,mimetype,digest,length&filter=statuscode:200"
            f"&filter=mimetype:{quote(mime, safe='')}&filter=original:{quote(KEYWORDS, safe='')}&limit=3000")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", help="comma-separated counties")
    ap.add_argument("--chunk-days", type=int, default=WINDOW_DAYS,
                    help="split each CDX query into windows of this many days (smaller queries finish within the fetch timeout)")
    a = ap.parse_args(argv)
    from txprecinct.fetch import FetchClient
    c = FetchClient(agent="archive-file-sweep")
    targets = json.loads(Path(a.targets).read_text())
    only = set(a.only.split(",")) if a.only else None
    out_root = Path(a.out)
    t0 = time.time()
    summary = {}
    for county, spec in targets.items():
        if only and county not in only:
            continue
        cdir = out_root / county.replace(" ", "_")
        cdir.mkdir(parents=True, exist_ok=True)
        rec = {"county": county, "spec": spec, "swept_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
               "window_days": WINDOW_DAYS, "elections": {}}
        for election in ELECTIONS:
            n0, n1, off = night_bounds(election)
            rows, cdx_log = [], []
            chunks = [(d, min(a.chunk_days, WINDOW_DAYS - d)) for d in range(0, WINDOW_DAYS, a.chunk_days)]
            for prefix in spec.get("file_prefixes", []):
                for d0, nd in chunks:
                    u = cdx_url(prefix, election, FILE_MIME, d0, nd)
                    r = c.get(u, purpose=f"sweep:cdx:{county}")
                    got = json.loads(r.text() or "[]")[1:] if r.ok else []
                    cdx_log.append({"cdx_url": u, "error": r.error, "rows": len(got)})
                    rows += [("file", *g) for g in got]
            for prefix in spec.get("page_prefixes", []):
                got = []
                for d0, nd in chunks[:max(1, -(-2 // a.chunk_days))]:  # pages: first 2 days only
                    u = cdx_url(prefix, election, HTML_MIME, d0, nd)
                    r = c.get(u, purpose=f"sweep:cdx:{county}")
                    part = json.loads(r.text() or "[]")[1:] if r.ok else []
                    cdx_log.append({"cdx_url": u, "error": r.error, "rows": len(part)})
                    got += part
                # Results pages change often; keep only captures within 2 days of election day.
                cutoff = (n0 - timedelta(hours=19) + timedelta(days=2) - timedelta(hours=off)).strftime("%Y%m%d%H%M%S")
                rows += [("page", *g) for g in got if g[0] <= cutoff]
            # One entry per distinct version (url without query, digest), earliest capture.
            versions: dict = {}
            for kind, ts, orig, status, mime, digest, length in sorted(rows, key=lambda x: x[1]):
                key = (re.sub(r"\?.*$", "", orig).lower(), digest)
                versions.setdefault(key, {"kind": kind, "timestamp_utc": ts, "original": orig, "mimetype": mime,
                                          "digest": digest, "length": length})
            vlist = sorted(versions.values(), key=lambda v: (-score(v["original"]), v["timestamp_utc"]))
            replays = []
            pick = ([v for v in vlist if v["kind"] == "file"][:MAX_FILE_REPLAYS_PER_ELECTION]
                    + [v for v in vlist if v["kind"] == "page"][:MAX_PAGE_REPLAYS_PER_ELECTION])
            for v in pick:
                rr = c.get(f"https://web.archive.org/web/{v['timestamp_utc']}id_/{v['original']}",
                           purpose=f"sweep:replay:{county}")
                body = rr.body or b""
                lm_local = local_from_http(rr.headers.get("x-archive-orig-last-modified"), off)
                ent = dict(v, replay_error=rr.error, bytes=len(body),
                           sha256=hashlib.sha256(body).hexdigest() if body else None,
                           orig_last_modified=rr.headers.get("x-archive-orig-last-modified"),
                           orig_date=rr.headers.get("x-archive-orig-date"),
                           orig_last_modified_local=lm_local.strftime("%Y-%m-%d %H:%M:%S") if lm_local else None,
                           upload_on_election_night=bool(lm_local and n0 <= lm_local <= n1))
                printed: list[str] = []
                if rr.ok and body[:5] == b"%PDF-":
                    info = pdf_info(body)
                    ent.update(info)
                    printed = info.get("printed_datetimes_first_streams", [])
                elif rr.ok:
                    text = body.decode("utf-8", "replace")
                    ent["updated_strings"] = [" ".join(m) for m in UPDATED_RE.findall(text)][:10]
                    printed = [m[1] for m in UPDATED_RE.findall(text)]
                    ent["text_sample"] = re.sub(r"\s+", " ", re.sub(r"(?s)<script.*?</script>|<style.*?</style>|<[^>]+>", " ", text))[:3000]
                pts = [p for p in (parse_printed(s) for s in printed) if p]
                ent["printed_on_election_night"] = any(n0 <= p <= n1 for p in pts)
                if rr.ok and body and len(body) < SAVE_LIMIT:
                    ext = ".pdf" if body[:5] == b"%PDF-" else (".html" if "html" in (v["mimetype"] or "") else ".bin")
                    name = f"{election}_{v['timestamp_utc']}_{hashlib.sha256(v['original'].encode()).hexdigest()[:10]}{ext}"
                    (cdir / name).write_bytes(body)
                    ent["saved_file"] = name
                replays.append(ent)
            rec["elections"][election] = {"cdx": cdx_log, "versions_found": len(versions),
                                          "versions": list(versions.values())[:400], "replays": replays}
        (cdir / "index.json").write_text(json.dumps(rec, indent=1))
        flags = [(e, r["original"]) for e, d in rec["elections"].items() for r in d["replays"]
                 if r["upload_on_election_night"] or r["printed_on_election_night"]]
        summary[county] = {"versions": {e: d["versions_found"] for e, d in rec["elections"].items()},
                           "replays": sum(len(d["replays"]) for d in rec["elections"].values()),
                           "night_flags": flags}
        print(json.dumps({"county": county, **summary[county]}), flush=True)
    (out_root / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps({"elapsed_s": round(time.time() - t0, 1), "counties": len(summary)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
