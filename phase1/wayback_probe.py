"""List Wayback Machine captures of a results host during election-night windows.

Windows are 7pm to 3am Central, expressed in UTC because CDX timestamps are UTC:
  Nov 5 2024 general   (CST, UTC-6): 2024-11-06 01:00 to 09:00 UTC
  Mar 3 2026 primary   (CST, UTC-6): 2026-03-04 01:00 to 09:00 UTC
  May 26 2026 runoff   (CDT, UTC-5): 2026-05-27 00:00 to 08:00 UTC

    python -m phase1.wayback_probe --county Harris --agent research-A results.example.gov/path
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from txprecinct.fetch import FetchClient  # noqa: E402

WINDOWS = {
    "2024_general": ("20241106010000", "20241106090000", -6),
    "2026_primary": ("20260304010000", "20260304090000", -6),
    "2026_runoff": ("20260527000000", "20260527080000", -5),
}
OUT_DIR = Path(__file__).resolve().parent / "evidence" / "wayback"


def to_central(ts: str, offset_hours: int) -> str:
    dt = datetime.strptime(ts, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
    return (dt + timedelta(hours=offset_hours)).strftime("%Y-%m-%d %H:%M:%S") + (" CST" if offset_hours == -6 else " CDT")


def probe(client: FetchClient, url_prefix: str) -> dict:
    result = {"url_prefix": url_prefix, "probed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "windows": {}}
    for name, (frm, to, off) in WINDOWS.items():
        cdx = (f"https://web.archive.org/cdx/search/cdx?url={quote(url_prefix, safe='')}&matchType=prefix"
               f"&from={frm}&to={to}&output=json&fl=timestamp,original,statuscode,mimetype,digest&limit=5000")
        r = client.get(cdx, purpose=f"wayback:{name}")
        entry = {"cdx_url": cdx, "ok": r.ok, "error": r.error, "content_hash": r.content_hash, "captures": []}
        if r.ok:
            rows = json.loads(r.text() or "[]")
            if rows:
                assert rows[0][0] == "timestamp", f"unexpected CDX header {rows[0]}"
                for ts, orig, status, mime, digest in rows[1:]:
                    entry["captures"].append({"timestamp_utc": ts, "central": to_central(ts, off), "original": orig,
                                              "status": status, "mimetype": mime, "digest": digest,
                                              "replay_url": f"https://web.archive.org/web/{ts}id_/{orig}"})
        result["windows"][name] = entry
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    ap.add_argument("--agent", required=True)
    ap.add_argument("url_prefix")
    a = ap.parse_args(argv)
    res = probe(FetchClient(agent=a.agent), a.url_prefix)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{a.county.replace(' ', '_')}.json"
    existing = json.loads(out.read_text()) if out.exists() else {"county": a.county, "probes": []}
    existing["probes"].append(res)
    out.write_text(json.dumps(existing, indent=2))
    summary = {k: (len(v["captures"]) if v["ok"] else v["error"]) for k, v in res["windows"].items()}
    print(json.dumps({"county": a.county, "url_prefix": a.url_prefix, "windows": summary}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
