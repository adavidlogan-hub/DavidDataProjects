"""Find a county's Clarity election IDs inside a bounded range (DECISIONS 51).

Clarity election IDs are assigned statewide in sequence, so the IDs other counties
used for the same election bound where a county's ID can be. For each ID in the
range this requests results.enr.clarityelections.com/TX/<County>/<ID>/current_ver.txt
(404 when the ID is not that county's). Every hit is accepted only after the
election's own detail.xml shows Region equal to the county and ElectionDate equal
to the target date.

    python -m phase1.clarity_eid_probe --county Nueces --agent orchestrator
"""
from __future__ import annotations

import argparse
import gzip
import io
import json
import re
import sys
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from txprecinct.fetch import FetchClient  # noqa: E402

BASE = "https://results.enr.clarityelections.com/TX"
# Bounds from election IDs already confirmed for other Texas counties (phase1/checks/clarity).
RANGES = {"2024_general": (122450, 122900, "11/5/2024"),
          "2026_primary": (125900, 126070, "3/3/2026"),
          "2026_runoff": (126070, 126400, "5/26/2026")}


def body(r) -> bytes:
    return gzip.decompress(r.body) if r.body[:2] == b"\x1f\x8b" else r.body


def detail_header(client, slug, eid, ver) -> dict:
    r = client.get(f"{BASE}/{slug}/{eid}/{ver}/reports/detailxml.zip", purpose="eid-probe:verify")
    if not r.ok:
        return {"error": r.error or f"HTTP {r.status}"}
    z = zipfile.ZipFile(io.BytesIO(body(r)))
    head = z.read(z.namelist()[0])[:4000].decode("utf-8", "replace")
    return {k: (re.search(f"<{k}>([^<]*)</{k}>", head) or [None, ""])[1] for k in ("Region", "ElectionName", "ElectionDate")}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    ap.add_argument("--agent", required=True)
    a = ap.parse_args(argv)
    slug = a.county.replace(" ", "_")
    client = FetchClient(agent=a.agent)
    out = {"county": a.county, "ranges": RANGES, "hits": []}
    for election, (lo, hi, date) in RANGES.items():
        def probe(eid):
            r = client.get(f"{BASE}/{slug}/{eid}/current_ver.txt", purpose=f"eid-probe:{election}")
            return eid, (body(r).decode().strip() if r.ok else None)
        with ThreadPoolExecutor(max_workers=4) as ex:
            found = [(e, v) for e, v in ex.map(probe, range(lo, hi + 1)) if v]
        for eid, ver in found:
            h = detail_header(client, slug, eid, ver)
            ok = h.get("Region", "").lower() == a.county.lower() and h.get("ElectionDate") == date
            out["hits"].append({"election": election, "eid": eid, "current_version": ver, **h, "accepted": ok})
    dest = Path(__file__).resolve().parent / "checks" / "clarity_eid_probe"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{slug}.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out["hits"], indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
