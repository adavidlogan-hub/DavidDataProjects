"""Report the timestamps inside archived or local PDFs.

For each URL, the Wayback CDX index is searched (path prefix, query string
ignored, any capture time) through the fetch module, so rate limits, robots.txt,
and the cache apply. The earliest capture with HTTP 200 is replayed and the
archive's record of the original server's Last-Modified and Date headers is
reported, plus the PDF's own CreationDate and ModDate and any date-time strings
printed in the page text. Raw PDFs under 90 MB are saved to --out-dir.

    python -m phase1.pdf_probe --urls-file phase1/targeted/pdf_urls.txt --out-dir phase1/targeted/pdfs
    python -m phase1.pdf_probe --file ..\\large-archive-files\\some.pdf
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zlib
from pathlib import Path
from urllib.parse import quote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

INFO_RE = re.compile(rb"/(CreationDate|ModDate|Title|Producer|Creator)\s*\(([^)]{0,200})\)")
STREAM_RE = re.compile(rb"stream\r?\n(.*?)\r?\nendstream", re.S)
PRINTED_RE = re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM|am|pm)?")
SAVE_LIMIT = 90 * 1024 * 1024


def pdf_info(data: bytes, stream_cap: int = 400) -> dict:
    out: dict = {}
    for k, v in INFO_RE.findall(data):
        out.setdefault(k.decode(), v.decode("latin-1", "replace"))
    printed: list[str] = []
    precinct_words = 0
    sample = ""
    for i, m in enumerate(STREAM_RE.finditer(data)):
        if i >= stream_cap:
            break
        try:
            txt = zlib.decompress(m.group(1)).decode("latin-1", "replace")
        except zlib.error:
            continue
        precinct_words += len(re.findall(r"(?i)precinct", txt))
        if len(sample) < 6000:
            sample += " ".join(re.findall(r"\(((?:[^()\\]|\\.)*)\)\s*Tj", txt)) + " | "
        for s in PRINTED_RE.findall(txt):
            if s not in printed:
                printed.append(s)
    out["printed_datetimes_first_streams"] = printed[:20]
    out["precinct_word_count_first_streams"] = precinct_words
    out["text_sample_first_streams"] = sample[:6000]
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", action="append", default=[])
    ap.add_argument("--urls-file")
    ap.add_argument("--file", action="append", default=[])
    ap.add_argument("--out-dir")
    a = ap.parse_args(argv)
    for f in a.file:
        data = Path(f).read_bytes()
        print(json.dumps({"file": f, "bytes": len(data), **pdf_info(data)}))
    urls = list(a.url)
    if a.urls_file:
        urls += [l.strip() for l in Path(a.urls_file).read_text().splitlines() if l.strip() and not l.startswith("#")]
    if not urls:
        return 0
    from txprecinct.fetch import FetchClient
    c = FetchClient(agent="pdf-probe")
    out_dir = Path(a.out_dir) if a.out_dir else None
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for u in urls:
        s = urlsplit(u)
        query = "&".join(q for q in s.query.split("&") if q and not q.startswith("sfvrsn="))
        key = f"{s.netloc}{s.path}" + (f"?{query}" if query else "")
        cdx = (f"https://web.archive.org/cdx/search/cdx?url={quote(key, safe='')}&matchType=prefix&output=json"
               f"&fl=timestamp,original,statuscode,mimetype,digest,length&filter=statuscode:200&limit=50")
        r = c.get(cdx, purpose="pdf-probe:cdx")
        rows = json.loads(r.text() or "[]")[1:] if r.ok else []
        first: dict = {}
        for row in rows:
            first.setdefault(row[1].split("?sfvrsn=")[0], row)
        rec = {"url": u, "cdx_url": cdx, "cdx_error": r.error, "captures": [x[:2] for x in rows], "replays": []}
        for ts, orig, *_ in list(first.values())[:6]:
            rr = c.get(f"https://web.archive.org/web/{ts}id_/{orig}", purpose="pdf-probe:replay")
            body = rr.body or b""
            rp = {"original": orig, "capture_utc": ts, "replay_error": rr.error, "bytes": len(body),
                  "sha256": hashlib.sha256(body).hexdigest() if body else None,
                  "orig_last_modified": rr.headers.get("x-archive-orig-last-modified"),
                  "orig_date": rr.headers.get("x-archive-orig-date")}
            if rr.ok and body[:5] == b"%PDF-":
                rp.update(pdf_info(body))
                if out_dir and len(body) < SAVE_LIMIT:
                    name = f"{ts}_{hashlib.sha256(orig.encode()).hexdigest()[:12]}.pdf"
                    (out_dir / name).write_bytes(body)
                    rp["saved_file"] = name
            rec["replays"].append(rp)
        results.append(rec)
        print(json.dumps(rec))
    if out_dir:
        (out_dir / "index.json").write_text(json.dumps(results, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
