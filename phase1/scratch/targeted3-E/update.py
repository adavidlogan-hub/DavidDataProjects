import json, sys
sys.path.insert(0, '.')
from phase1.schema import compute_tag, compute_confidence, validate_v2

A = "targeted3-E"
def load(c): return json.load(open(f"phase1/evidence/{c}.json"))
def save(c, d):
    tag, single = compute_tag(d["elections"])
    d["tag"] = tag
    d["confidence"] = compute_confidence(d)
    validate_v2(d)
    json.dump(d, open(f"phase1/evidence/{c}.json", "w"), indent=2, ensure_ascii=False)
    open(f"phase1/evidence/{c}.json", "a").write("\n")
    print(c, d["tag"], d["confidence"], {k: (v["result"], v["check"]) for k, v in d["elections"].items()})
def note(d, s): d["notes"] = (d["notes"] + " " if d["notes"] else "") + f"Targeted pass 3 2026-10-02 ({A}): {s}"

# ---------------- Val Verde
c = "Val_Verde"; d = load(c)
PRI = "https://valverdecounty.texas.gov/DocumentCenter/View/10174/2026-JOINT-PRIMARY-ELECTIONS-UNOFFICIAL-RESULTS"
RUN = "https://valverdecounty.texas.gov/DocumentCenter/View/10450/2026-JOINT-PRIMARY-RUN-OFF-UNOFFICIAL-RESULTS"
GEN = "https://valverdecounty.texas.gov/DocumentCenter/View/8410/Unofficial-Results-Val-Verde-County-General-Election-202"
d["elections"]["2026_primary"] = {"result": "LATER", "check": "2",
  "county_totals_first_seen": "2026-03-03 21:35 CT", "precinct_first_seen": "",
  "night_updates_with_precinct_numbers": "0", "evidence_url": PRI,
  "fact": "'Unofficial Joint Primary Results' (scanned, 22 pages, read from page images): 'Summary Results Report Joint Primary Election March 3, 2026 ... UNOFFICIAL RESULTS Val Verde ... Ballots Cast - Total 6,180 195 4,135 1,850' (TOTAL, Absentee, Early Voting, Election Day), county totals per contest only; every page footer 'Election Summary - 03/03/2026 9:35 PM'. Printed run time on election night (rule 43). Scan CreationDate Wed Mar 4 2026 15:18 UTC (9:18 AM CST Mar 4); DocumentCenter sends no Last-Modified. Precinct numbers appear only in 'Final -Official Joint Primary Results - Precinct-by-Precinct' (DocumentCenter ID 10206, listed after the canvass notices); no unofficial precinct report is listed."}
d["elections"]["2026_runoff"] = {"result": "LATER", "check": "2",
  "county_totals_first_seen": "2026-05-26 20:27 CT", "precinct_first_seen": "",
  "night_updates_with_precinct_numbers": "0", "evidence_url": RUN,
  "fact": "'Unofficial Results - Val Verde County' (scanned, 4 pages, read from page images): 'Summary Results Report Joint Primary Run Off May 26, 2026 ... UNOFFICIAL RESULTS Val Verde ... Registered Voters - Total 30,721 Ballots Cast - Total 1,520', then county totals per contest (for example 'REP US Senator ... John Cornyn 347 Ken Paxton 691'); footer 'Election Summary - 05/26/2026 8:27 PM' (pages 1 to 3); page 4 is the 'Preliminary Election Reconciliation - Unofficial Totals' (in person 1,391, mail 129, total 1,520, dated 5-26-26), so the 8:27 PM summary already holds all 1,520 ballots. Printed run time on election night (rule 43). Scan CreationDate Wed May 27 2026 14:42 UTC; no Last-Modified. Precinct numbers only in 'Official Results Precinct by Precinct' (ID 10473, posted later)."}
g = d["elections"]["2024_general"]
g["fact"] = "'2024 General Election Unofficial Results' (scanned, 10 pages, read from page images): 'Summary Results Report General Election November 5, 2024 ... UNOFFICIAL RESULTS Val Verde County, Texas', county totals, footer 'Election Summary - 11/06/2024 2:58 PM' on every page, so it was printed after election night; scan CreationDate Nov 6 2024 21:42 UTC. No Last-Modified. No election-night file survives (rule 43), so UNDETERMINED. Wayback harvest found no captures."
g["evidence_url"] = GEN
d["sources"] += [
 {"url": PRI, "via": "fetch_module", "content_hash": "c0f3be7f3601e74598d1f801a2f9c050a64a8000462e3b4c01fdc0964540ca4b", "quote": "Summary Results Report Joint Primary Election March 3, 2026 ... UNOFFICIAL RESULTS Val Verde ... Election Summary - 03/03/2026 9:35 PM (read from page images 1 and 22)", "supports": "2026_primary LATER: county totals printed on election night"},
 {"url": RUN, "via": "fetch_module", "content_hash": "fa58e4244960f8d2661b3de89d50643925ea67879568babca8d4c535dce32f2d", "quote": "Summary Results Report Joint Primary Run Off May 26, 2026 ... UNOFFICIAL RESULTS Val Verde ... Ballots Cast - Total 1,520 ... Election Summary - 05/26/2026 8:27 PM (read from page images 1, 2, 4)", "supports": "2026_runoff LATER: county totals printed on election night"},
 {"url": GEN, "via": "fetch_module", "content_hash": "8da7666cc1cdca5a190ce6e56e87e6df317305f9f0d8e6725baab53b556d4c3d", "quote": "Summary Results Report General Election November 5, 2024 ... UNOFFICIAL RESULTS ... Election Summary - 11/06/2024 2:58 PM (read from page images 1 and 10)", "supports": "2024_general stays UNDETERMINED: printed after election night"},
]
d["evidence_url"] = PRI
d["platform"] = "county_pdfs"
d["notes"] = d["notes"].replace("Check 3 pending (origin/wayback-data branch not found).", "Wayback harvest (valverdecounty.org) found no election-night captures; no targeted archive or sweep folder.")
note(d, "read the scanned unofficial results PDFs as page images. 2026_primary and 2026_runoff UNDETERMINED to LATER (check 2): both are county-total Election Summary reports printed on election night (9:35 PM Mar 3 and 8:27 PM May 26) under rule 43/47 basis, with precinct numbers only in the later official precinct-by-precinct reports. Note the scans themselves were created the next morning (Mar 4 9:18 AM, May 27 9:42 AM CDT), so the election-night time is the printed run time, not an upload time. 2024_general unofficial report printed Nov 6 2:58 PM, stays UNDETERMINED. Sweep: no folder (not in the 28 largest).")
d["tag_rationale"] = "2026_primary and 2026_runoff are both LATER (county-total reports printed on election night, precinct numbers only in official reports), so COUNTY_ONLY_PRECINCT_AT_CANVASS; both rest on check 2, so med."
save(c, d)

# ---------------- Lamb
c = "Lamb"; d = load(c)
LR = "https://www.co.lamb.tx.us/upload/page/0112/docs/Primary%20Runoff%20Results%205.26.26.pdf"
d["elections"]["2026_runoff"] = {"result": "LATER", "check": "2",
  "county_totals_first_seen": "2026-05-26 21:04 CT", "precinct_first_seen": "",
  "night_updates_with_precinct_numbers": "0", "evidence_url": LR,
  "fact": "'Primary Runoff Election Unofficial Results 5.26.26' (scanned, 2 pages, read from page images): 'Summary Results Report TX Lamb County 260526 Primary Runoff Election ... May 26, 2026 ... ELECTION UNOFFICIAL SUMMARY Lamb County ... Election Day Precincts Reporting 11 of 11 ... Ballots Cast - Total 1,024 84 349 591', county totals per contest (for example 'John Cornyn 419 42 134 243 Ken Paxton 537 25 194 318'); footer 'Election Summary - 05/26/2026 9:04 PM'. Printed run time on election night (rule 43/47 LATER basis). Scan CreationDate Wed May 27 2026 18:53:38 UTC; Last-Modified Wed, 27 May 2026 18:56:34 GMT (1:56 PM CDT May 27). No precinct results file is listed for the runoff (the 'REP/DEM PCT n 5.26.26' links are sample ballots per the verifier); 'Official Results' is also a summary. Agrees with verifier (phase1/verification/Lamb.json)."}
d["sources"].append({"url": LR, "via": "fetch_module", "content_hash": "ed7ce8ff688728964354e66d4519580fdcd823b99f46c7f56a1b3933c8f46dde", "quote": "Summary Results Report TX Lamb County 260526 Primary Runoff Election ... ELECTION UNOFFICIAL SUMMARY ... Election Summary - 05/26/2026 9:04 PM (read from page images)", "supports": "2026_runoff LATER: county totals printed on election night"})
d["evidence_url"] = LR
d["notes"] = d["notes"].replace("2024 general and 2026 primary: check 3 pending.", "2024 general and 2026 primary: Wayback harvest found no election-night captures (some CDX queries failed with connection refused).")
note(d, "read the scanned runoff unofficial results as page images (the research had called it unreadable): county-total Election Summary printed 05/26/2026 9:04 PM, so 2026_runoff UNDETERMINED to LATER (check 2), matching the verifier. One web search for primary results found nothing for Lamb. 2024_general and 2026_primary stay UNDETERMINED (no files on the current page). Sweep: no folder.")
d["tag_rationale"] = "Only 2026_runoff is determined (LATER: a county-totals summary printed on election night, no precinct results posted), so COUNTY_ONLY_PRECINCT_AT_CANVASS with confidence low."
d["sources"].append({"url": "websearch:?q=Lamb%20County%20Texas%20March%203%202026%20primary%20unofficial%20results%20Littlefield", "via": "websearch", "content_hash": "f652b45cdf07e1d665765d3abd75fb165dd415861775e02d93c818fee89a52c2", "quote": "no Lamb County results page found", "supports": "locating only"})
save(c, d)

# ---------------- Menard
c = "Menard"; d = load(c)
MP = "https://www.co.menard.tx.us/upload/page/0215/Elections/2026/Primary/Cumulative%20Results-3-3-2026%2008-49-21%20PM.pdf"
MR = "https://www.co.menard.tx.us/upload/page/0215/Elections/2026/Runoff/20260526201711scan.pdf"
MG = "https://www.co.menard.tx.us/upload/page/0215/Menard%20County%202024%20Nov%205%20ENR.pdf"
MPG = "https://www.co.menard.tx.us/page/menard.Elections"
d["elections"]["2026_primary"] = {"result": "LATER", "check": "2",
  "county_totals_first_seen": "2026-03-03 20:48 CT", "precinct_first_seen": "",
  "night_updates_with_precinct_numbers": "0", "evidence_url": MP,
  "fact": "Elections page links 'ELECTION NIGHT RESULTS' to 'Cumulative Results-3-3-2026 08-49-21 PM.pdf' (18 pages, text layer): 'Cumulative Results Report MENARD COUNTY, TEXAS Unofficial Results ... PRIMARY ELECTION ... Run Time 8:48 PM ... Run Date 03/03/2026', county totals by 'Absentee Voting / Early Voting / Election Day Voting / Total' (for example 'James Talarico 0 0.00% 23 69.70% 13 72.22% 36 69.23%'); no per-precinct numbers. CreationDate Wed Mar 4 2026 02:49:35 UTC; Last-Modified Wed, 04 Mar 2026 02:56:15 GMT (8:56 PM CST Mar 3, election night). No other primary results file is listed (only sample ballots, notices, and hand count audit certifications)."}
d["elections"]["2026_runoff"] = {"result": "LATER", "check": "2",
  "county_totals_first_seen": "2026-05-26 19:38 CT", "precinct_first_seen": "",
  "night_updates_with_precinct_numbers": "0", "evidence_url": MR,
  "fact": "Elections page links 'Election Night Results' to '20260526201711scan.pdf' (scanned, 2 pages, read from page images): 'Cumulative Results Report MENARD COUNTY, TEXAS ... 2026 May 26 Official Joint Primary Runoff ... Run Time 7:38 PM Run Date 05/26/2026 ... Unofficial Results ... Precincts Reporting 6 of 6 = 100.00%', county totals by 'Early Voting / Election Day Voting / Total' (for example 'John Cornyn 61 43.57% 31 32.98% 92 39.32%'); page 2 Democratic, Run Time 7:40 PM. Last-Modified Wed, 27 May 2026 01:35:21 GMT (8:35 PM CDT May 26, election night). (CreationDate reads Wed May 27 02:17:34 2026 UTC, which is after the upload time; the file name stamp 20260526201711 suggests the scanner wrote local 8:17 PM with a wrong offset.) No other runoff results file is listed."}
g = d["elections"]["2024_general"]
g["fact"] = "Elections page lists 'Election Night Results / Resultados de la noche de las elecciones' linking to 'Menard County 2024 Nov 5 ENR.pdf', but that file returned HTTP 404 to the fetch module on 2026-10-02, so its content and times cannot be read. Wayback harvest could not query (robots_disallowed_or_unreachable at the time)."
g["evidence_url"] = MG
d["results_url"] = MPG
d["platform"] = "county_pdfs"
d["host"] = "www.co.menard.tx.us"
d["evidence_url"] = MR
d["sources"] += [
 {"url": MPG, "via": "fetch_module", "content_hash": "cd38d3915f443376d35ccf79bae8dbbab32c8d1a15371b48f6e2c98de6b20c25", "quote": "/upload/page/0215/Elections/2026/Runoff/20260526201711scan.pdf | Election Night Results ; /upload/page/0215/Elections/2026/Primary/Cumulative Results-3-3-2026 08-49-21 PM.pdf | ELECTION NIGHT RESULTS ; /upload/page/0215/Menard County 2024 Nov 5 ENR.pdf | Election Night Results / Resultados de la noche de las elecciones", "supports": "the county posts one election-night results file per election"},
 {"url": MP, "via": "fetch_module", "content_hash": "9d2df242e9d7b84b969026f6fed48bbcc1a9147978ac61ae9955360a1c8fe77d", "quote": "Cumulative Results Report MENARD COUNTY, TEXAS Unofficial Results ... Run Time 8:48 PM ... Run Date 03/03/2026 (Last-Modified Wed, 04 Mar 2026 02:56:15 GMT)", "supports": "2026_primary LATER: county totals uploaded on election night"},
 {"url": MR, "via": "fetch_module", "content_hash": "4ab7bb8784ecbc8166a8581fd9f52bd2ed3aee236f29d606c45551cea1c54510", "quote": "Cumulative Results Report MENARD COUNTY, TEXAS ... Run Time 7:38 PM Run Date 05/26/2026 ... Precincts Reporting 6 of 6 = 100.00% (read from page image; Last-Modified Wed, 27 May 2026 01:35:21 GMT)", "supports": "2026_runoff LATER: county totals uploaded on election night"},
 {"url": MG, "via": "fetch_module", "content_hash": "f67fc72af6821a0fd2461c9336df4c49fbb8ed1b8f5caedf85baf2648594ecdd", "quote": "HTTP 404", "supports": "2024_general file linked but not retrievable"},
]
note(d, "the fetch module now reaches www.co.menard.tx.us (earlier robots.txt reset was transient). The Elections page links an 'Election Night Results' file for each election. 2026_primary UNDETERMINED to LATER (check 2): cumulative county-totals report, run 8:48 PM, uploaded 8:56 PM CST Mar 3. 2026_runoff UNDETERMINED to LATER (check 2): cumulative county-totals scan, run 7:38 PM, uploaded 8:35 PM CDT May 26. No precinct results files listed for either. 2024_general ENR file 404, stays UNDETERMINED. Sweep: no folder.")
d["tag_rationale"] = "2026_primary and 2026_runoff are LATER (election-night county-totals reports uploaded that night, no precinct results posted), so COUNTY_ONLY_PRECINCT_AT_CANVASS; both from check 2, so med."
save(c, d)
