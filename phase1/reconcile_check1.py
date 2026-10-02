"""Re-derive every check-1 (Clarity) election result from one measure.

For each evidence file, every election whose check is "1" is re-read with the
check 1 script (served from cache), using the Clarity slug and election ID in
that election's own evidence_url. The result is then:
  LIVE   two or more distinct election-night releases of election-day precinct votes
  END    exactly one
  LATER  none on election night, but the county published updates that night
  (unchanged) otherwise, with a note
The county tag is recomputed by the fixed rule. Every change is logged to
phase1/reconcile_log.md and noted in the record. Files are rewritten only when
something changed, and every rewritten file must pass validate_v2.

    python -m phase1.reconcile_check1 [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from phase1.clarity_timeline import run as clarity_run  # noqa: E402
from phase1.schema import ELECTIONS, compute_tag, validate_v2  # noqa: E402

ROOT = Path(__file__).resolve().parent
URL_RE = re.compile(r"results\.enr\.clarityelections\.com/TX/([^/]+)/(\d+)")


def derive(listings: list[dict]) -> tuple[str | None, str]:
    if not listings:
        return None, "no Clarity listing read"
    n = max(l["election_night_distinct_election_day_precinct_releases"] for l in listings)
    night = max(l["election_night_updates"] for l in listings)
    first = next((l["first_update_with_election_day_precinct_votes"] for l in listings
                  if l["first_update_with_election_day_precinct_votes"]), None)
    fact = (f"Clarity update log: {n} distinct election-day precinct releases across {night} election-night updates "
            f"(county local time, 7 PM to 3 AM); first update with election-day precinct votes "
            f"{first['timestamp'] if first else 'none'}.")
    if n >= 2:
        return "LIVE", fact
    if n == 1:
        return "END", fact
    if night > 0:
        return "LATER", fact
    return None, fact + " No election-night updates, so check 1 cannot decide."


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    log = ["# Check 1 reconciliation log", ""]
    changed_files = 0
    for p in sorted((ROOT / "evidence").glob("*.json")):
        rec = json.loads(p.read_text())
        targets = {}
        for e in ELECTIONS:
            x = rec["elections"][e]
            if x["check"] != "1":
                continue
            m = URL_RE.search(x.get("evidence_url", ""))
            if not m:
                log.append(f"- {rec['county']} {e}: check 1 but evidence_url has no Clarity election ID; left as is.")
                continue
            targets[e] = m.groups()
        if not targets:
            continue
        slugs = {s for s, _ in targets.values()}
        assert len(slugs) == 1, f"{p.name}: several Clarity slugs {slugs}"
        res = clarity_run(slugs.pop(), "reconcile", {e: eid for e, (_, eid) in targets.items()})
        (ROOT / "checks" / "clarity" / p.name).write_text(json.dumps(res, indent=2))
        changes = []
        for e in targets:
            new, fact = derive(res["elections"][e].get("listings", []))
            old = rec["elections"][e]["result"]
            if new is None or new == old:
                continue
            changes.append(f"{e}: {old} -> {new}")
            rec["elections"][e]["result"] = new
            rec["elections"][e]["fact"] = f"Reconciled ({old} to {new}). {fact} Previous: {rec['elections'][e]['fact']}"
        if not changes:
            continue
        old_tag = rec["tag"]
        tag, single = compute_tag(rec["elections"])
        rec["tag"] = tag
        if tag != old_tag:
            deciding = [e for e in ELECTIONS if rec["elections"][e]["result"] != "UNDETERMINED"
                        and tag != "UNKNOWN" and {"LIVE": "LIVE_PRECINCT", "END": "PRECINCT_END_OF_NIGHT",
                        "LATER": "COUNTY_ONLY_PRECINCT_AT_CANVASS", "NONE": "NO_SITE_OR_SOS_ONLY"}.get(
                        rec["elections"][e]["result"]) == tag]
            all_strong = deciding and all(rec["elections"][e]["check"] in ("1", "3") for e in deciding)
            rec["confidence"] = "low" if single or tag == "UNKNOWN" or not all_strong else "high"
        rec["notes"] = (rec["notes"] + f" Check 1 reconciled to the election-day precinct measure: "
                        f"{'; '.join(changes)}; tag {old_tag} -> {rec['tag']}.").strip()
        validate_v2(rec, str(p))
        log.append(f"- {rec['county']}: {'; '.join(changes)}. Tag {old_tag} -> {rec['tag']} ({rec['confidence']}).")
        changed_files += 1
        if not a.dry_run:
            p.write_text(json.dumps(rec, indent=2, ensure_ascii=False))
    log.append("")
    log.append(f"Files changed: {changed_files}{' (dry run, nothing written)' if a.dry_run else ''}")
    if not a.dry_run:
        (ROOT / "reconcile_log.md").write_text("\n".join(log) + "\n")
    print("\n".join(log))
    return 0


if __name__ == "__main__":
    sys.exit(main())
