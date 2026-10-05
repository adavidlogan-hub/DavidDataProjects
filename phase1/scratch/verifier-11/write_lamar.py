import json, sys, datetime
sys.path.insert(0, '.')
from phase1.schema import compute_tag, compute_confidence
C = "https://results.enr.clarityelections.com/TX/Lamar/"
el = {
 "2024_general": {"result": "END", "check": "1", "county_totals_first_seen": "", "precinct_first_seen": "2024-11-05 20:38 CT",
   "fact": "Clarity EID 122497 ('2024 General Election'; detail.xml Region Lamar, ElectionDate 11/5/2024). Opened myself: v350862 Timestamp '11/5/2024 7:14:07 PM CST', per-precinct votes only in VoteType Early (Election Day sum 0); v351606 Timestamp '11/5/2024 8:38:14 PM CST', all 26 voting precincts (1A3B ... 4G) carry Election Day votes, e.g. President/Vice President, REP Donald J. Trump/JD Vance, Election Day, <Precinct name=\"1A3B\" votes=\"322\">. v351606 is the last published version, so election-day precinct numbers appeared once on election night with the final unofficial count. 8 versions return HTTP 404, all numbered before v350862 (whose election-day sum is 0), so none can be an earlier election-day release."},
 "2026_primary": {"result": "LIVE", "check": "1", "county_totals_first_seen": "", "precinct_first_seen": "2026-03-03 19:49 CT",
   "fact": "Clarity EID 126018 ('2026 Primaries'; Region Lamar, ElectionDate 3/3/2026). Opened myself: v368392 '3/3/2026 7:10:40 PM CST' (Early and Absentee precinct votes only, Election Day 0); v368410 '3/3/2026 7:49:38 PM CST' Election Day votes in 7 of 26 precincts (1A3B, 1A5A, 1C, 1F, 2A1A, 2G, 3G), e.g. REP US Senator, Wesley Hunt, Election Day, <Precinct name=\"1A3B\" votes=\"34\">; v368424 '8:11:21 PM CST' same 7 precincts; v368431 '3/3/2026 8:23:24 PM CST' Election Day votes in all 26 precincts (sum 112830 vs 27895). Two distinct election-night releases of per-precinct election-day votes."},
 "2026_runoff": {"result": "LATER", "check": "1", "county_totals_first_seen": "2026-05-26 19:15 CT", "precinct_first_seen": "",
   "fact": "Clarity EID 126354 ('2026 Primary Runoff'; Region Lamar, ElectionDate 5/26/2026). Opened myself: v372923 '5/26/2026 6:50:34 PM CDT' (Early and Absentee only) and v372935 '5/26/2026 7:15:22 PM CDT', the last published version. Its reporting units are not voting precincts but three ballot groups: <Precinct name=\"Lamar County\" totalVoters=\"16449\" ballotsCast=\"1999\">, \"County and Commissioner Pct 2\" (7151 voters), \"County and Commissioner Pct 4\" (9464 voters), e.g. REP US Senator, Ken Paxton, Election Day: Lamar County 421, County and Commissioner Pct 2 110, County and Commissioner Pct 4 362. These are county-level totals split by ballot style, not the 26 voting precincts used in the primary and general. No voting-precinct numbers on Clarity that night or later, and the county Elections page lists no runoff precinct report (only sample ballots, voters-who-voted lists, hand count audit files). Election-night county-totals update at 7:15 PM CDT gives LATER (precinct numbers never published online as far as found)."},
}
for e in el.values():
    for k in ("night_updates_with_precinct_numbers",):
        pass
rec = {"county": "Lamar", "elections": el}
tag, single = compute_tag(el)
conf = compute_confidence(rec)
out = {"county": "Lamar", "reason_selected": "third opinion on an earlier research/verifier disagreement",
 "verifier_tag": tag, "verifier_confidence": conf, "elections": el,
 "rationale": f"Check 1 decides all three elections differently: Nov 2024 END (one election-night release, 8:38 PM), Mar 2026 LIVE (7:49 PM partial and 8:23 PM full precinct releases), May 2026 runoff LATER (Clarity units are ballot groups, not voting precincts). No two results agree, so the fixed rule gives {tag}, confidence {conf}.",
 "sources": [], "written_blind_at_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
 "agent": "verifier-11"}
src = [
 ("https://www.co.lamar.tx.us/page/Elections", "582497ff43d9d5bc3846a33dfc33bf017b7dbed2216d22661ce8b6e353590f6f", "County Elections page links 'Election Results' to https://results.enr.clarityelections.com/TX/Lamar/; no county results PDFs for the three elections"),
 (C+"122497/350862/reports/detailxml.zip", "5e261b77d3ce55cdc61d85d586499b2f3ba377c0afbb669567a5bc667da477f3", "First election-night update 2024: 7:14:07 PM CST, Election Day precinct votes 0"),
 (C+"122497/351606/reports/detailxml.zip", "9bf8368e962a03887c8ce684461feec47c622bc95a326a09399a300615448872", "8:38:14 PM CST, last version, Election Day votes in all 26 precincts; Region Lamar, ElectionDate 11/5/2024"),
 (C+"126018/368392/reports/detailxml.zip", "7f4a8e06814e378c5294a3ff115f9a24e283b3682408af733f888218abaf9e05", "First election-night update primary: 7:10:40 PM CST, Election Day 0"),
 (C+"126018/368410/reports/detailxml.zip", "956bbbb2a28d0758606a665830c51bc6ec674751abb7d7e83bf7ac7a6a05eb59", "7:49:38 PM CST, Election Day votes in 7 precincts"),
 (C+"126018/368431/reports/detailxml.zip", "de57346b0593888829706038539fc7116def19e6bdd76640785d3549903da942", "8:23:24 PM CST, Election Day votes in 26 precincts"),
 (C+"126354/372923/reports/detailxml.zip", "70deb5b8ae12fa5dddf7426f6c7215933289c945ecc6f96020a791d6772a78b1", "Runoff 6:50:34 PM CDT, Early and Absentee only"),
 (C+"126354/372935/reports/detailxml.zip", "8796df0521af82783f1e735badc023a1dae66225be391d4f6cfa3efc99f78a35", "Runoff 7:15:22 PM CDT, last version; units are ballot groups Lamar County / County and Commissioner Pct 2 / Pct 4"),
 ("phase1/verification/clarity/Lamar.json", "", "Own check 1 script run (--out-dir phase1/verification/clarity), EIDs from elections.json reached via the county's Clarity link"),
]
import hashlib
out["sources"] = [{"url": u, "content_hash": h, "what_i_checked": w} for u, h, w in src]
json.dump(out, open("phase1/verification/Lamar_third.json", "w"), indent=2)
print(tag, conf)
