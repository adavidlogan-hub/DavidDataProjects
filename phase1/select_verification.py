"""Choose which counties the verifier re-checks (see DECISIONS.md item 11).

    python -m phase1.select_verification data/pilot_counties.txt --seed 20261002
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from phase1.schema import validate  # noqa: E402

ROOT = Path(__file__).resolve().parent


def select(counties: list[str], seed: int) -> dict:
    required, rest = [], []
    for c in counties:
        rec = json.loads((ROOT / "evidence" / f"{c.replace(' ', '_')}.json").read_text())
        validate(rec)
        if rec["tag"] in ("LIVE_PRECINCT", "PRECINCT_END_OF_NIGHT"):
            required.append({"county": c, "reason": f"tag {rec['tag']}"})
        elif rec["tag"] != "UNKNOWN" and rec["confidence"] == "low":
            required.append({"county": c, "reason": "low confidence"})
        else:
            rest.append(c)
    k = min(len(rest), max(1, math.ceil(0.10 * len(rest)))) if rest else 0
    sample = sorted(random.Random(seed).sample(sorted(rest), k))
    return {"seed": seed, "required": required,
            "random_sample": [{"county": c, "reason": "random 10 percent sample"} for c in sample],
            "not_selected": sorted(set(rest) - set(sample))}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("counties_file")
    ap.add_argument("--seed", type=int, required=True)
    a = ap.parse_args()
    cs = [c.strip() for c in Path(a.counties_file).read_text().splitlines() if c.strip()]
    sel = select(cs, a.seed)
    (ROOT / "verification_selection.json").write_text(json.dumps(sel, indent=2))
    print(json.dumps(sel, indent=2))
