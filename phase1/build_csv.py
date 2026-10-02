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
from phase1.schema import CSV_COLUMNS, validate  # noqa: E402

ROOT = Path(__file__).resolve().parent


def main(out: str, counties_file: str) -> None:
    counties = [c.strip() for c in Path(counties_file).read_text().splitlines() if c.strip()]
    rows, log = [], ["# Verification log", ""]
    for county in counties:
        ev_path = ROOT / "evidence" / f"{county.replace(' ', '_')}.json"
        assert ev_path.exists(), f"missing evidence file for {county}: {ev_path}"
        rec = json.loads(ev_path.read_text())
        validate(rec, str(ev_path))
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
