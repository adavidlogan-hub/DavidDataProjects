"""Rule 43 audit: every LATER result must carry an election-night county-totals time.

Prints each LATER election whose county_totals_first_seen is missing, unparseable, or
outside 7 PM election day to 3 AM next day (the time as recorded, county local).
Exit code 1 if any are found.

    python -m phase1.check_later_times
"""
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATES = {"2024_general": "2024-11-05", "2026_primary": "2026-03-03", "2026_runoff": "2026-05-26"}
TIME_RE = re.compile(r"(\d{4}-\d{2}-\d{2})[ T](\d{1,2}):(\d{2})")


def in_window(value: str, election: str) -> bool | None:
    """True if any recorded time (printed run time or upload time) falls on election night."""
    found = TIME_RE.findall(value or "")
    if not found:
        return None
    d = datetime.strptime(DATES[election], "%Y-%m-%d")
    for day, hh, mm in found:
        t = datetime.strptime(f"{day} {int(hh):02d}:{mm}", "%Y-%m-%d %H:%M")
        if d + timedelta(hours=19) <= t <= d + timedelta(hours=27):
            return True
    return False


def main() -> int:
    bad = []
    for p in sorted((ROOT / "evidence").glob("*.json")):
        rec = json.loads(p.read_text())
        for e, x in rec["elections"].items():
            if x["result"] != "LATER":
                continue
            ok = in_window(x.get("county_totals_first_seen", ""), e)
            if ok is not True:
                bad.append((rec["county"], e, x.get("county_totals_first_seen", ""),
                            "missing or unparseable" if ok is None else "outside election night"))
    for b in bad:
        print(" | ".join(b))
    print(f"{len(bad)} LATER results fail rule 43")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
