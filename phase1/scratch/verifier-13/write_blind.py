import json, sys, os
sys.path.insert(0, '.')
from phase1.schema import compute_confidence, compute_tag
NOW = sys.argv[1]
R = "tag changed in targeted pass 3"
W = "Wayback branch index.json for this county: harvest recorded every CDX query as robots_disallowed_or_unreachable, no captures; check 3 unavailable"
recs = {}

recs["Tyler"] = {
 "county": "Tyler", "reason_selected": R,
 "elections": {
  "2024_general": {"result": "UNDETERMINED", "check": "none",
   "fact": "Election Information page (co.tyler.tx.us/page/tyler.ElectionInformation) lists under 2024 NOVEMBER 5 GENERAL ELECTION: 'Unofficial Election Precinct Summary' (file named 'Unofficial Election Results for Nov 7 2023000001.pdf'), 'Official Election Summary Results' (Election Summary.pdf), 'Official Election Precinct Summary Results' (Election Precicnt Summary.pdf). All three return HTTP 404 on www.co.tyler.tx.us and on newtools.cira.state.tx.us. No surviving file, no times. Check 3: wayback harvest for co.tyler.tx.us failed (robots_disallowed_or_unreachable), no captures."},
  "2026_primary": {"result": "LATER", "check": "2", "county_totals_first_seen": "2026-03-03 22:07 CT",
   "fact": "Only results file for the primary: '/upload/page/3316/RESULTS/2026 UNOFFICIAL RESULTS.pdf' (scanned, 22 pages). Header 'Summary Results Report / TX TYLER 260303 Primary 6110' with stamp 'UNOFFICIAL RESULTS PCT BY PCT REPORT' (pages 1-13) and 'ACCUMULATIVE REPORT' (pages 14-22); every page is county totals by contest (Total, Absentee, Early Voting, Election Day; 'Election Day Precincts Reporting 17 of 17'), no per-precinct breakdown. Printed footer 'Election Summary - 03/03/2026 10:07 PM' (REP pages) and '10:13 PM' (DEM pages). Server Last-Modified Wed, 04 Mar 2026 18:40:46 GMT (12:40 PM CST Mar 4, after election night; same on newtools.cira mirror). No other unofficial or precinct report for the primary is linked ('OFFICIAL RESULTS ( tba )'). County totals printed on election night, no precinct report posted: LATER under the rule 43 reading."},
  "2026_runoff": {"result": "UNDETERMINED", "check": "none",
   "fact": "2026 PRIMARY RUNOFF ELECTION NOTICES section shows the text 'UNOFFICIAL RESULTS' with no link; 'OFFICIAL RESULTS' links to the SOS goelect EVR turnout site. No county file and no time. Check 3 unavailable (harvest error)."}},
 "rationale": "Not on Clarity (elections.json 404). Only the 2026 primary is determined: LATER from a county-totals report printed 10:07 PM on election night with no precinct report posted. 2024 files are 404 and the runoff has no file. One determined election gives COUNTY_ONLY_PRECINCT_AT_CANVASS at low confidence.",
 "sources": [
  {"url": "https://www.co.tyler.tx.us/page/tyler.ElectionInformation", "content_hash": "a753072580e96b20483601ec32bad82060a9e9961d719c7f894a123b9dbb3381", "what_i_checked": "List of result links per election"},
  {"url": "https://www.co.tyler.tx.us/upload/page/3316/RESULTS/2026 UNOFFICIAL RESULTS.pdf", "content_hash": "46056854de0ed36806b4586966550f64b97662ea85d39285a90826c683bc2d80", "what_i_checked": "Rendered pages 1, 3 and 4-22: county totals only, printed 03/03/2026 10:07 PM and 10:13 PM; Last-Modified 04 Mar 2026 18:40:46 GMT"},
  {"url": "https://www.co.tyler.tx.us/upload/page/3316/Election Precicnt Summary.pdf", "content_hash": "f67fc72af6821a0fd2461c9336df4c49fbb8ed1b8f5caedf85baf2648594ecdd", "what_i_checked": "HTTP 404 (also the 2024 unofficial and official summary links, and newtools.cira copies)"},
  {"url": "git:origin/wayback-data:phase1/wayback_snapshots/Tyler/index.json", "content_hash": "", "what_i_checked": W},
  {"url": "https://results.enr.clarityelections.com/TX/Tyler/elections.json", "content_hash": "", "what_i_checked": "check 1 script: no Clarity election list (404)"}]}

recs["Scurry"] = {
 "county": "Scurry", "reason_selected": R,
 "elections": {
  "2024_general": {"result": "UNDETERMINED", "check": "none",
   "fact": "Previous Elections page lists for NOVEMBER 5, 2024 GENERAL ELECTION only 'Official Election Summary Results' (Scan_20250617.pdf) and 'Official Precinct Summary Results' (Scan_20250616.pdf); no unofficial or election-night file. Wayback index for co.scurry.tx.us: CDX queries ok, no captures in any window."},
  "2026_primary": {"result": "LATER", "check": "2", "county_totals_first_seen": "2026-03-03 20:06 CT",
   "fact": "Unofficial Resutls: 'Summary Report with Group Details' (Unofficial Sumamry Report 332026.pdf, scanned, 19 pages) is county totals ('Election Day Precincts Reporting 11 of 11'), printed footer 'Election Summary - 03/03/2026 8:06 PM' on pages 1 and 19, Last-Modified Mon, 24 Aug 2026 23:00:13 GMT. The four 'Precinct Report with Group Details' files (Pcts 5 6 7 / 8 9 10 / 11 12 13 / 14 15 Unofficial Pct Report.pdf) have per-precinct candidate votes ('PRECINCT 5 ... Election Day') but are printed 'Precinct Summary - 08/24/2026 12:01 PM' and Last-Modified Mon, 24 Aug 2026 22:53 GMT (scan CreationDate Aug 24 2026). County totals printed on election night; the only precinct reports are printed and uploaded after election night: LATER under the rule 43 reading."},
  "2026_runoff": {"result": "UNDETERMINED", "check": "none",
   "fact": "Unofficial Results for May 26, 2026: 'Summary Report with Group Details' printed 'Election Summary - 06/02/2026 2:08 PM', Last-Modified Thu, 11 Jun 2026 13:15:20 GMT; 'Precinct Report with Group Details' printed 'Precinct Summary - 06/02/2026 2:10 PM', Last-Modified Mon, 24 Aug 2026 13:06:12 GMT. No file from election night survives. Wayback: no captures."}},
 "rationale": "Not on Clarity (elections.json 404). Only the 2026 primary is determined: county totals printed 8:06 PM on election night, precinct reports printed and uploaded Aug 24 2026. 2024 has only official files and the runoff's unofficial files were printed June 2. One determined election gives COUNTY_ONLY_PRECINCT_AT_CANVASS at low confidence.",
 "sources": [
  {"url": "https://www.co.scurry.tx.us/page/elections.information", "content_hash": "118e0df8357f1d73b48957d6c8cc02a7822fe97ce56c31b11b0cffde701ad225", "what_i_checked": "2026 primary and runoff result links"},
  {"url": "https://www.co.scurry.tx.us/page/elections.previous.elections", "content_hash": "31a964e0685351d38f060871652e7666f6194ac25a81465e54623a562cfe50b3", "what_i_checked": "Nov 2024 result links (official only)"},
  {"url": "https://www.co.scurry.tx.us/upload/page/0163/Unofficial%20Sumamry%20Report%20332026.pdf", "content_hash": "f7944d1bb31436a386368725f03034b470acab290e84f612a989060b808598a2", "what_i_checked": "Rendered page 1 and 19 footers: 03/03/2026 8:06 PM, county totals; Last-Modified 24 Aug 2026 23:00:13 GMT"},
  {"url": "https://www.co.scurry.tx.us/upload/page/0163/Pcts%205%206%207%20Unofficial%20Pct%20Report.pdf", "content_hash": "baeca3f5323f40b1e995712c884a071fc29900e059afb17ec841ae21c1b35492", "what_i_checked": "Per-precinct report, footer 08/24/2026 12:01 PM; Last-Modified 24 Aug 2026 22:53:30 GMT (other three precinct files a89d3c0c, 98766ae4, 7c95f1ab same footer, Last-Modified 22:53:34 to 22:53:42 GMT)"},
  {"url": "https://www.co.scurry.tx.us/upload/page/0163/Unofficial%20Summary%20Results%20Report%205262026.pdf", "content_hash": "d16640745c8d4d2190df165a92ddafcb2b7e2ac9d53e651dbed9abe75a2505be", "what_i_checked": "Runoff summary footer 06/02/2026 2:08 PM; Last-Modified 11 Jun 2026"},
  {"url": "https://www.co.scurry.tx.us/upload/page/0163/2Unofficial%20Summary%20Results%20by%20PCT%205262026.pdf", "content_hash": "ab7b671c90060f4ae8448979b0e3ae2b5395fa37af9c0da70493cf76bd8e4e06", "what_i_checked": "Runoff precinct report footer 06/02/2026 2:10 PM; Last-Modified 24 Aug 2026"},
  {"url": "git:origin/wayback-data:phase1/wayback_snapshots/Scurry/index.json", "content_hash": "", "what_i_checked": "CDX ok, no captures in any election-night window"}]}

recs["Coleman"] = {
 "county": "Coleman", "reason_selected": R,
 "elections": {
  "2024_general": {"result": "LATER", "check": "2", "county_totals_first_seen": "2024-11-05 20:41 CT",
   "fact": "Elections page, NOVEMBER 5, 2024: 'Unofficial Results' = UNOFFICIAL ALL PRECINCTS coleman county.pdf, a 7-page 'Summary Results Report / UNOFFICIAL RESULTS / TX Coleman 241105 General' of county totals ('Election Day Precincts Reporting 5 of 5'), printed 'Election Summary - 11/05/2024 8:00 PM', PDF CreationDate 2024-11-06 02:11:21 UTC, server Last-Modified Wed, 06 Nov 2024 02:41:05 GMT (8:41 PM CST, election night). The only precinct file is 'OFFICIAL RESULTS BY PRECINCT GEN ELEC 11.05.24.pdf' printed 'Precinct Summary - 11/12/2024 9:52 AM', Last-Modified 15 Nov 2024. Check 3 agrees: the wayback capture 2024-11-06 01:42:52 CST of the same file (sha256 9ae01f73..., identical to the live copy) shows county totals only."},
  "2026_primary": {"result": "UNDETERMINED", "check": "none",
   "fact": "Unofficial Results (UNOFFICIAL RESULTS.pdf) printed 'Election Summary - 03/05/2026 12:41 PM', Last-Modified 21 Apr 2026; party files printed 03/10/2026; precinct files are official (printed 04/15/2026). No file from election night survives. Wayback: no captures."},
  "2026_runoff": {"result": "LATER", "check": "2", "county_totals_first_seen": "2026-05-26 19:39 CT",
   "fact": "UNOFFICIAL ELECTION NIGHT RESULTS AND REPORTS: 'COLEMAN COUNTY JOINT ELECTION REPORT' = UNOFFICIAL RESULTS 2026 JOINT RUNOFF.pdf, 3-page county-totals 'Summary Results Report ... 260526 Primary Runoff Election' ('Election Day Precincts Reporting 4 of 4'), printed 'Election Summary - 05/26/2026 8:02 PM', server Last-Modified Wed, 27 May 2026 00:39:30 GMT (7:39 PM CDT May 26; the file's ModDate 00:22:32 UTC and the printed 8:02 PM differ, but every time is on election night). No unofficial precinct report is linked; the only runoff precinct file is 'OFFICIAL PRECINCT RESULTS - REPUBLICAN PARTY.pdf' printed 06/10/2026, Last-Modified 10 Jun 2026."}},
 "rationale": "Not on Clarity (elections.json 404). 2024 and the 2026 runoff are LATER from county-totals reports uploaded on election night with no unofficial precinct report; precinct numbers appear only in official reports after canvass. The primary has no election-night file. Two LATER elections from check 2 give COUNTY_ONLY_PRECINCT_AT_CANVASS, med.",
 "sources": [
  {"url": "https://newtools.cira.state.tx.us/page/coleman.Elections", "content_hash": "6ca4e185fd6621a65aceb3e2a29bf5ac3935ac734cbcd3e99b47e21ba7439dc7", "what_i_checked": "Result links per election (www.co.coleman.tx.us served the home page for these paths)"},
  {"url": "https://newtools.cira.state.tx.us/upload/page/6075/docs/ELECTIONS/2024%20GENERAL%20ELECTION/UNOFFICIAL%20ALL%20PRECINCTS%20coleman%20county.pdf", "content_hash": "9ae01f73397af679cefbcfe22bb54d101181be88a8dd8aecb26ffdc4564a76f3", "what_i_checked": "County totals, printed 11/05/2024 8:00 PM, Last-Modified 06 Nov 2024 02:41:05 GMT"},
  {"url": "https://newtools.cira.state.tx.us/upload/page/6075/docs/ELECTIONS/2024%20GENERAL%20ELECTION/OFFICIAL%20RESULTS%20BY%20PRECINCT%20GEN%20ELEC%2011.05.24.pdf", "content_hash": "d26488741d285ee538f224830fcaafe3e292617869e180f887f79f6cda38062f", "what_i_checked": "Official precinct report printed 11/12/2024, Last-Modified 15 Nov 2024"},
  {"url": "https://newtools.cira.state.tx.us/upload/page/6075/docs/ELECTIONS/2026%20MARCH%20PRIMARY/UNOFFICIAL%20RESULTS%202026%20JOINT%20RUNOFF.pdf", "content_hash": "8c9ad1c2f6bb58eacfcf6f88b95c58687db81e75790ff746cd46befceaf26904", "what_i_checked": "Runoff county totals, printed 05/26/2026 8:02 PM, Last-Modified 27 May 2026 00:39:30 GMT"},
  {"url": "https://newtools.cira.state.tx.us/upload/page/6075/docs/ELECTIONS/2026%20MARCH%20PRIMARY/OFFICIAL%20PRECINCT%20RESULTS%20-%20REPUBLICAN%20PARTY.pdf", "content_hash": "5c2a12281b7a30f6cc8bcf13ee6252dedc55b53ef22c1b12e82fcc5584ddae96", "what_i_checked": "Runoff official precinct report printed 06/10/2026"},
  {"url": "https://newtools.cira.state.tx.us/upload/page/6075/docs/ELECTIONS/2026%20MARCH%20PRIMARY/UNOFFICIAL%20RESULTS.pdf", "content_hash": "a67429e22ca7a07e2c4ae8271c38312f3017f95cb424da31c4ffbfbb6989a847", "what_i_checked": "Primary unofficial printed 03/05/2026 12:41 PM, Last-Modified 21 Apr 2026"},
  {"url": "git:origin/wayback-data:phase1/wayback_snapshots/Coleman/2024_general_20241106074252_9ae01f73397a.pdf", "content_hash": "9ae01f73397af679cefbcfe22bb54d101181be88a8dd8aecb26ffdc4564a76f3", "what_i_checked": "Capture 2024-11-06 01:42:52 CST; identical to live county-totals file"}]}

recs["Howard"] = {
 "county": "Howard", "reason_selected": R,
 "elections": {
  "2024_general": {"result": "LATER", "check": "2", "county_totals_first_seen": "2024-11-05 21:31 CT",
   "fact": "Election Information page, November 5, 2024: 'Election Night UNOFFICIAL Results - ENR w WI.pdf', a 7-page 'Summary Results Report / UNOFFICIAL RESULTS / ELECTION NIGHT' of county totals ('Election Day Precincts Reporting 12 of 12'), printed 'Election Night Results - 11/05/2024 9:22 PM', server Last-Modified Wed, 06 Nov 2024 03:31:53 GMT (9:31 PM CST). Also 'EV Results w WI.pdf' (early/mail county totals, printed 8:09 PM, Last-Modified 02:14:36 GMT). No precinct report of any kind is linked for 2024."},
  "2026_primary": {"result": "UNDETERMINED", "check": "none",
   "fact": "2026 Primary Election lists only canvass files (2026 Rep Canvass Table.pdf printed 03/10/2026 12:35 PM, Last-Modified 18 Mar 2026) and audit notices. No election-night file survives. Check 3 unavailable (harvest error)."},
  "2026_runoff": {"result": "LATER", "check": "2", "county_totals_first_seen": "2026-05-26 20:32 CT",
   "fact": "Election Results: ENR.pdf, 4-page county totals 'Election Night Voting Results / Unofficial Results' ('Election Day Precincts Reporting 7 of 7'), printed 'Election Summary - 05/26/2026 8:32 PM' (CreationDate 2026-05-27 01:32:29 UTC), Last-Modified Wed, 27 May 2026 13:56:10 GMT. The only precinct-level file is 'Canvass Table_poll_5_26_2026.pdf' (scan, CreationDate and Last-Modified 03 Jun 2026). County totals printed on election night; no unofficial precinct report posted."}},
 "rationale": "Not on Clarity (elections.json 404). 2024 and the 2026 runoff are LATER: election-night county-totals reports (2024 uploaded 9:31 PM; runoff printed 8:32 PM) and no unofficial precinct report; precinct numbers only in canvass tables. Primary undetermined. Two LATER elections from check 2 give COUNTY_ONLY_PRECINCT_AT_CANVASS, med.",
 "sources": [
  {"url": "https://newtools.cira.state.tx.us/page/howard.Election.Information", "content_hash": "96bf39d8bd3b85b26b438eae7fab803eee6d418a64ba146b851e524a62e89d66", "what_i_checked": "Election Results and Past Election Results links (seed URL www.co.howard.tx.us default.aspx returns 404)"},
  {"url": "https://newtools.cira.state.tx.us/upload/page/0454/2024%20November/ENR%20w%20WI.pdf", "content_hash": "39b1cd47cb19437b6365209896c7e022f9a78b46718f9f4cfea0545e9faf1e4a", "what_i_checked": "County totals printed 11/05/2024 9:22 PM; Last-Modified 06 Nov 2024 03:31:53 GMT"},
  {"url": "https://newtools.cira.state.tx.us/upload/page/0454/2026%20Primary/Runoff/ENR.pdf", "content_hash": "cc575ae58a3b3738cd9fb63f0f24354bc7683f7536cafba1b3c526ebeadb1d5c", "what_i_checked": "County totals printed 05/26/2026 8:32 PM; Last-Modified 27 May 2026 13:56:10 GMT"},
  {"url": "https://newtools.cira.state.tx.us/upload/page/0454/2026%20Primary/Runoff/Canvass%20Table_poll_5_26_2026.pdf", "content_hash": "c57ec3dc64b91e785c6f5b52e495b5b947299c2ec9aabb0152cc9e2013071f73", "what_i_checked": "Precinct canvass table scanned and uploaded 03 Jun 2026"},
  {"url": "https://newtools.cira.state.tx.us/upload/page/0454/2026%20Primary/Canvass/2026%20Rep%20Canvass%20Table.pdf", "content_hash": "0a2f45be034b18317824bc19489cdaf8e9d0fec5c78075f756fd4a94c42a16a6", "what_i_checked": "Primary canvass printed 03/10/2026; only primary results file"},
  {"url": "git:origin/wayback-data:phase1/wayback_snapshots/Howard/index.json", "content_hash": "", "what_i_checked": W}]}

recs["Jasper"] = {
 "county": "Jasper", "reason_selected": R,
 "elections": {
  "2024_general": {"result": "UNDETERMINED", "check": "none",
   "fact": "The Elections page (co.jasper.tx.us/page/Elections) has no Nov 2024 results section; its 'Election Results/Voting History' link points to the SOS historical page, which is a general link and not specific to an election. No county file or time. Check 3 unavailable (harvest error)."},
  "2026_primary": {"result": "UNDETERMINED", "check": "none",
   "fact": "'Unofficial Totals (PDF)' = 3326 Unofficial Summary Totals.pdf, scanned county totals printed 'Election Summary - 03/04/2026 8:31 AM' (after the 3 AM cutoff), Last-Modified Thu, 05 Mar 2026 21:41:18 GMT. Official precinct report printed 03/10/2026, Last-Modified 20 Mar 2026. No file from election night."},
  "2026_runoff": {"result": "UNDETERMINED", "check": "none",
   "fact": "Only official files: 'Official Summary Results' printed 05/28/2026 11:58 AM and 'Official Pct by Pct Results' printed 05/28/2026 12:02 PM, both Last-Modified 29 May 2026. No election-night file."}},
 "rationale": "Not on Clarity (elections.json 404). No election-night file survives for any election (primary unofficial totals printed 8:31 AM the next morning; runoff official only; no 2024 files), and check 3 has no captures. No election is determined: UNKNOWN.",
 "sources": [
  {"url": "https://www.co.jasper.tx.us/page/Elections", "content_hash": "e9bb0d215d7a870aae91ca63654ab6af9ac300fe5ffe880a54577087aa9606e0", "what_i_checked": "Result links for 2026 elections; no 2024 section"},
  {"url": "https://www.co.jasper.tx.us/upload/page/0095/3326%20Unofficial%20Summary%20Totals.pdf", "content_hash": "ff7b5424d40b1fa7af8fc0f85981155f9a23f9d37b56decec4e81286d120a9ca", "what_i_checked": "Printed 03/04/2026 8:31 AM; Last-Modified 05 Mar 2026"},
  {"url": "https://www.co.jasper.tx.us/upload/page/0095/2026%20elections/3326%20Official%20Pct%20by%20Pct%20Results.pdf", "content_hash": "ded276b4a371cacfb123535e633966c2c23db00653b65ce7735cd5089e890b5d", "what_i_checked": "Official precinct report printed 03/10/2026"},
  {"url": "https://www.co.jasper.tx.us/upload/page/0095/2026%20elections/May%2026th%202026/5-26-2026%20Official%20Pct%20by%20Pct%20Results%20a.pdf", "content_hash": "1e417b188e0c15b9e5c3e51abfc9c5f7a89fbb33f7474cf191d88f570531216d", "what_i_checked": "Official runoff precinct report printed 05/28/2026"},
  {"url": "git:origin/wayback-data:phase1/wayback_snapshots/Jasper/index.json", "content_hash": "", "what_i_checked": W}]}

for c, r in recs.items():
    for e in r["elections"].values():
        e.setdefault("county_totals_first_seen", "")
    tag, single = compute_tag(r["elections"])
    r["verifier_tag"] = tag
    r["verifier_confidence"] = compute_confidence({"county": c, "elections": r["elections"]})
    r["written_blind_at_utc"] = NOW
    path = f"phase1/verification/{c}.json"
    prev = f"phase1/scratch/verifier-13/prev_{c}.json"
    if os.path.exists(prev):
        r["previous_verification"] = json.load(open(prev))
    order = ["county","reason_selected","verifier_tag","verifier_confidence","elections","rationale","sources","written_blind_at_utc","previous_verification"]
    out = {k: r[k] for k in order if k in r}
    s = json.dumps(out, indent=2, ensure_ascii=False)
    for ch in ["—", "–"]:
        assert ch not in s, (c, ch)
    open(path, "w").write(s + "\n")
    print(c, tag, out["verifier_confidence"])
