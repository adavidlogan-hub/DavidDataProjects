"""Write check 1 results into a county's evidence file (used after the bounded ID search).

Each election's result is derived exactly as in phase1/reconcile_check1.py (distinct
election-night releases of election-day precinct votes: 2+ LIVE, 1 END, 0 with night
updates LATER). Elections the check 1 file cannot decide are left as they are.

    python -m phase1.apply_check1 --county Parker --check1 phase1/checks/clarity_orchestrator/Parker.json --agent orchestrator
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from phase1.reconcile_check1 import derive  # noqa: E402
from phase1.schema import ELECTIONS, compute_confidence, compute_tag, validate_v2  # noqa: E402

ROOT = Path(__file__).resolve().parent


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    ap.add_argument("--check1", required=True)
    ap.add_argument("--agent", required=True)
    a = ap.parse_args(argv)
    slug = a.county.replace(" ", "_")
    p = ROOT / "evidence" / f"{slug}.json"
    rec = json.loads(p.read_text())
    ck = json.loads(Path(a.check1).read_text())
    changed = []
    for e in ELECTIONS:
        listings = ck["elections"].get(e, {}).get("listings", [])
        res, fact = derive(listings)
        if res is None:
            continue
        night = [u for l in listings for u in l["updates"] if u.get("election_night") and "timestamp" in u]
        first = next((l["first_update_with_election_day_precinct_votes"] for l in listings
                      if l["first_update_with_election_day_precinct_votes"]), None)
        eids = ", ".join(f"{l['eid']}" for l in listings)
        old = rec["elections"][e]["result"]
        rec["elections"][e] = {
            "result": res, "check": "1",
            "county_totals_first_seen": min((u["timestamp"] for u in night), default="") if res == "LATER" else "",
            "precinct_first_seen": first["timestamp"] if first and res in ("LIVE", "END") else "",
            "night_updates_with_precinct_numbers": str(max(l["election_night_distinct_election_day_precinct_releases"]
                                                       for l in listings)),
            "evidence_url": (first or {}).get("url") or (night[0]["url"] if night else listings[0]["updates"][0]["url"]),
            "fact": f"Clarity election ID(s) {eids}, found by the bounded ID search and confirmed by Region and "
                    f"ElectionDate in detail.xml (DECISIONS 51). {fact}",
        }
        changed.append(f"{e}: {old} -> {res}")
    dest = ROOT / "checks" / "clarity" / f"{slug}.json"
    shutil.copyfile(a.check1, dest)
    rec["sources"].append({"url": f"https://results.enr.clarityelections.com/TX/{slug}/", "via": "clarity_script",
                           "content_hash": "", "supports": "check 1",
                           "quote": f"phase1/checks/clarity/{slug}.json; IDs from phase1/checks/clarity_eid_probe/{slug}.json"})
    if not rec.get("owner_override"):
        rec["tag"], _ = compute_tag(rec["elections"])
        rec["confidence"] = compute_confidence(rec)
    deciding = [rec["elections"][e] for e in ELECTIONS if rec["elections"][e]["check"] == "1"
                and rec["elections"][e]["result"] in ("LIVE", "END")]
    if deciding and not rec["evidence_url"]:
        rec["evidence_url"] = deciding[0]["evidence_url"]
    if deciding and not rec["precinct_first_seen_local_time"]:
        rec["precinct_first_seen_local_time"] = min(x["precinct_first_seen"] for x in deciding)
    if not rec["results_url"]:
        rec["results_url"] = f"https://results.enr.clarityelections.com/TX/{slug}/"
    rec["platform"] = "clarity_style"
    rec["host"] = "results.enr.clarityelections.com"
    rec["tag_rationale"] = f"Check 1 (Clarity update logs): {'; '.join(changed)}. Tag by the fixed rule."
    rec["notes"] = (rec["notes"] + f" Targeted pass 2026-10-02 ({a.agent}): check 1 applied after bounded Clarity ID "
                    f"search: {'; '.join(changed)}.").strip()
    validate_v2(rec, str(p))
    p.write_text(json.dumps(rec, indent=2, ensure_ascii=False))
    print(json.dumps({"county": a.county, "changes": changed, "tag": rec["tag"], "confidence": rec["confidence"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
