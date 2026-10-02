"""Assemble counties.csv from per-county evidence plus verifier results.

Verifier rule: if the verifier disagrees with the research tag, the final tag is
UNKNOWN and both findings are logged in notes and in phase1/verification_log.md.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import csv as _csv  # noqa: E402
from phase1.schema import CSV_COLUMNS, compute_confidence, validate_v2  # noqa: E402

ROOT = Path(__file__).resolve().parent


SEED = Path(__file__).resolve().parent.parent / "data" / "seed_counties.csv"


def main(out: str, counties_file: str) -> None:
    seed = {r["county"]: r for r in _csv.DictReader(open(SEED, encoding="utf-8"))}
    assert len(seed) == 254, "seed must have 254 counties"
    counties = [c.strip() for c in Path(counties_file).read_text().splitlines() if c.strip()]
    rows, log = [], ["# Verification log", ""]
    for county in counties:
        ev_path = ROOT / "evidence" / f"{county.replace(' ', '_')}.json"
        assert ev_path.exists(), f"missing evidence file for {county}: {ev_path}"
        rec = json.loads(ev_path.read_text())
        validate_v2(rec, str(ev_path))
        rec["confidence"] = compute_confidence(rec)  # one rule for every county (DECISIONS 40)
        clarity_urls = [rec["results_url"], rec["host"]] + [x.get("evidence_url", "") for x in rec["elections"].values()]
        if rec["platform"] != "clarity_style" and any("clarityelections.com" in u for u in clarity_urls):
            log.append(f"- {county}: platform {rec['platform']} normalized to clarity_style (Clarity results URL in record).")
            rec["platform"] = "clarity_style"  # DECISIONS 41
        sd = seed[county]
        if not rec["elections_office_phone"] and not rec["elections_office_email"]:
            rec["elections_office_phone"], rec["elections_office_email"] = sd["phone"], sd["email"]
            rec["notes"] = (rec["notes"] + " Contact from TX SOS county election officials list "
                            f"(page sha256 {sd['sos_officials_hash'][:12]}).").strip()
        assert rec["county"] == county, f"{ev_path}: county field {rec['county']!r} != {county!r}"
        ver_path = ROOT / "verification" / f"{county.replace(' ', '_')}.json"
        if ver_path.exists():
            ver = json.loads(ver_path.read_text())
            assert ver["county"] == county
            if ver["verifier_tag"] != rec["tag"]:
                log.append(f"- {county}: DISAGREE. research={rec['tag']} ({rec['confidence']}); "
                           f"verifier={ver['verifier_tag']}. Final tag set to UNKNOWN.")
                log.append(f"  - research rationale: {rec.get('tag_rationale', '')}")
                log.append(f"  - verifier rationale: {ver.get('rationale', '')}")
                rec["notes"] = (f"Verifier disagreement: research tag {rec['tag']}, verifier tag "
                                f"{ver['verifier_tag']}; set to UNKNOWN per rule. " + rec["notes"]).strip()
                rec["tag"], rec["confidence"] = "UNKNOWN", "low"
            else:
                log.append(f"- {county}: AGREE on {rec['tag']} (reason checked: {ver.get('reason_selected', '')}).")
        rows.append({c: rec[c] for c in CSV_COLUMNS})
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CSV_COLUMNS)
        w.writeheader()
        w.writerows(rows)
    (ROOT / "verification_log.md").write_text("\n".join(log) + "\n", encoding="utf-8")
    print(f"wrote {out} with {len(rows)} rows")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
