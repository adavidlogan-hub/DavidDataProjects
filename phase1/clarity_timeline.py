"""Check 1: read a Clarity results site's update log for the three target elections.

For each election, every published update version is opened (reports/detailxml.zip)
and two facts are read straight from the file: the update's Timestamp and how many
precincts have a nonzero candidate vote count (<Precinct ... votes="N"> inside a
contest). Nothing is inferred; the output lists every update.

    python -m phase1.clarity_timeline --county Travis --agent research-A
Output: phase1/checks/clarity/<County>.json
"""
from __future__ import annotations

import argparse
import gzip
import io
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from txprecinct.fetch import FetchClient  # noqa: E402

BASE = "https://results.enr.clarityelections.com/TX"
TARGETS = {"2024_general": "11/5/2024", "2026_primary": "3/3/2026", "2026_runoff": "5/26/2026"}
OUT = Path(__file__).resolve().parent / "checks" / "clarity"
# Election-day vote types as Clarity names them across Texas counties ("Election Day", "Election",
# "ELECTION DAY", "ED Provisional", "Election Day In-Person", "Election Day Provisionals").
# Early, mail, absentee, provisional-only, over/undervote, and registration types do not match.
ED_VOTETYPE_RE = re.compile(r"(?i)^(election\b|ed\b)")
TS_RE = re.compile(r"(\d+/\d+/\d{4} \d+:\d{2}:\d{2} [AP]M)\s*([A-Z]{2,4})?")


def body(r) -> bytes:
    assert r.ok, f"fetch failed: {r.url}: {r.error}"
    return gzip.decompress(r.body) if r.body[:2] == b"\x1f\x8b" else r.body


def read_detail(zbytes: bytes) -> dict:
    z = zipfile.ZipFile(io.BytesIO(zbytes))
    names = [n for n in z.namelist() if n.lower().endswith(".xml")]
    assert names, "detailxml.zip has no xml"
    ts, precincts_with_votes, cells = None, set(), 0
    ed_precincts = set()
    in_contest = 0
    votetype = None
    with z.open(names[0]) as fh:
        for ev, el in ET.iterparse(fh, events=("start", "end")):
            tag = el.tag
            if ev == "start" and tag == "Contest":
                in_contest += 1
            elif ev == "start" and tag == "VoteType":
                votetype = el.attrib.get("name", "")
            elif ev == "end":
                if tag == "Timestamp" and ts is None:
                    ts = (el.text or "").strip()
                elif tag == "Precinct" and in_contest and "votes" in el.attrib:
                    v = el.attrib["votes"]
                    if v.isdigit() and int(v) > 0:
                        cells += 1
                        precincts_with_votes.add(el.attrib.get("name"))
                        if votetype and ED_VOTETYPE_RE.match(votetype):
                            ed_precincts.add(el.attrib.get("name"))
                elif tag == "Contest":
                    in_contest -= 1
                el.clear()
    assert ts, "no Timestamp in detail.xml"
    return {"timestamp": ts, "precincts_with_votes": len(precincts_with_votes), "nonzero_precinct_vote_cells": cells,
            "precincts_with_election_day_votes": len(ed_precincts)}


def on_election_night(ts: str, election_date: str) -> bool:
    """True if the local timestamp is between 7:00 PM election day and 3:00 AM the next day."""
    m = TS_RE.search(ts)
    assert m, f"unparseable timestamp {ts!r}"
    t = datetime.strptime(m.group(1), "%m/%d/%Y %I:%M:%S %p")
    d = datetime.strptime(election_date, "%m/%d/%Y")
    return d + timedelta(hours=19) <= t <= d + timedelta(hours=27)


def run(county: str, agent: str, eid_override: dict | None = None) -> dict:
    c = FetchClient(agent=agent)
    slug = county.replace(" ", "_")
    res = {"county": county, "check": "clarity_update_log", "elections": {}}
    eid_override = eid_override or {}
    lst = c.get(f"{BASE}/{slug}/elections.json", purpose=f"check1:{county}")
    if not lst.ok and not eid_override:
        res["result"] = f"no Clarity election list ({lst.status or lst.error})"
        return res
    elections = json.loads(body(lst)) if lst.ok else []
    for key, date in TARGETS.items():
        if key in eid_override:
            # Election ID taken from a link on the county's own site (the Clarity list can be incomplete).
            match = [{"EID": eid_override[key], "ElectionName": "(EID supplied from county site link)"}]
            res.setdefault("eid_overrides", {})[key] = eid_override[key]
        else:
            match = [e for e in elections if e.get("Date", "").startswith(date + " ")]
        if not match:
            res["elections"][key] = {"found": False, "note": "election not listed on this county's Clarity site"}
            continue
        # Several listings can share a date (e.g. separate party primaries); read them all.
        per = []
        for e in match:
            eid = e["EID"]
            cur = c.get(f"{BASE}/{slug}/{eid}/current_ver.txt", use_cache=False, purpose=f"check1:{county}")
            ver = body(cur).decode().strip()
            st = json.loads(body(c.get(f"{BASE}/{slug}/{eid}/{ver}/json/en/electionsettings.json",
                                       purpose=f"check1:{county}")))
            updates = []
            for v in st.get("versions", []):
                url = f"{BASE}/{slug}/{eid}/{v}/reports/detailxml.zip"
                r = c.get(url, purpose=f"check1:{county}")
                if not r.ok:
                    updates.append({"version": v, "url": url, "error": r.error or f"HTTP {r.status}"})
                    continue
                d = read_detail(body(r))
                d.update(version=v, url=url, content_hash=r.content_hash,
                         election_night=on_election_night(d["timestamp"], date))
                updates.append(d)
            night = [u for u in updates if u.get("election_night")]
            night_with = [u for u in night if u["precincts_with_votes"] > 0]
            night_with_ed = [u for u in night if u.get("precincts_with_election_day_votes", 0) > 0]
            first = next((u for u in updates if u.get("precincts_with_votes", 0) > 0), None)
            first_ed = next((u for u in updates if u.get("precincts_with_election_day_votes", 0) > 0), None)
            per.append({"eid": eid, "name": e.get("ElectionName"), "updates": updates,
                        "election_night_updates": len(night),
                        "election_night_updates_with_precinct_votes": len(night_with),
                        "first_update_with_precinct_votes": first and {k: first[k] for k in ("timestamp", "version", "url")},
                        "election_night_updates_with_election_day_precinct_votes": len(night_with_ed),
                        "first_update_with_election_day_precinct_votes":
                            first_ed and {k: first_ed[k] for k in ("timestamp", "version", "url")},
                        "unreadable_versions": sum(1 for u in updates if "error" in u)})
        res["elections"][key] = {"found": True, "listings": per}
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    ap.add_argument("--agent", required=True)
    ap.add_argument("--out-dir", default=str(OUT), help="where to write <County>.json (verifier uses its own)")
    ap.add_argument("--eid", action="append", default=[],
                    help="election=EID from a county-site link, e.g. 2026_primary=125934 (repeatable)")
    a = ap.parse_args(argv)
    override = {}
    for kv in a.eid:
        k, _, v = kv.partition("=")
        assert k in TARGETS and v.isdigit(), f"bad --eid {kv!r}"
        override[k] = v
    res = run(a.county, a.agent, override)
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{a.county.replace(' ', '_')}.json").write_text(json.dumps(res, indent=2))
    summary = {"county": a.county, "result": res.get("result", "ok")}
    for k, v in res["elections"].items():
        summary[k] = ("not listed" if not v["found"] else
                      [f"{l['election_night_updates_with_election_day_precinct_votes']}/{l['election_night_updates']} night "
                       f"updates with election-day precinct votes; first "
                       f"{(l['first_update_with_election_day_precinct_votes'] or {}).get('timestamp')}"
                       for l in v["listings"]])
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
