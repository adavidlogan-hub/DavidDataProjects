import json, sys
sys.path.insert(0, '.')
from phase1.schema import compute_tag, compute_confidence, validate_v2
p = 'phase1/evidence/Medina.json'
d = json.load(open(p))
U = "https://newtools.cira.state.tx.us/upload/page/6805/2026%20March%20Primary/Results/ED.EV.AB%20UNOFFICIAL.pdf"
PG = "https://newtools.cira.state.tx.us/page/medina.Elections"
PCT = "https://newtools.cira.state.tx.us/upload/page/6805/2026%20March%20Primary/Results/Official%20Precinct%20Results.pdf"
d['elections']['2026_primary'] = {
    "result": "LATER",
    "check": "2",
    "county_totals_first_seen": "2026-03-03 22:03 CT (server upload, Last-Modified Wed, 04 Mar 2026 04:03:31 GMT; printed run time 2026-03-03 21:47 CT)",
    "precinct_first_seen": "",
    "night_updates_with_precinct_numbers": "",
    "evidence_url": U,
    "fact": ("The state-hosted copy of the county's old Elections page (newtools.cira.state.tx.us/page/medina.Elections) links the 'Election Results' banner image to "
             "'/upload/page/6805/2026 March Primary/Results/ED.EV.AB UNOFFICIAL.pdf'. That file is a 20-page scan (Epson Scan 2, CreationDate Wed Mar 4 04:01:50 2026 UTC, "
             "Last-Modified Wed, 04 Mar 2026 04:03:31 GMT = 10:03 PM CST election night). Read from the page images: every page is headed 'Cumulative Results Report MEDINA COUNTY, TEXAS "
             "Unofficial Results ... 2026 JOINT PRIMARY ELECTION 3/3/2026 ... Run Time 9:47 PM Run Date 03/03/2026 ... Precincts Reporting 15 of 15 = 100.00%', with county totals by "
             "Absentee Voting, Early Voting, Election Day Voting (e.g. 'KEN PAXTON 43 ... 2,123 ... 1,124 ... 3,290'), ending '*** End of report ***'; no per-precinct numbers. "
             "The only precinct report for this election on that page is 'March 3, 2026 Joint Primary Election - Official Results by Precinct' (Official Precinct Results.pdf, "
             "'Precinct Results Report Official Results ... Run Time 10:42 AM Run Date 03/13/2026', Last-Modified Fri, 13 Mar 2026 16:11:41 GMT), uploaded after election night. "
             "Rule 43 (DECISIONS 67 reading): election-night county-totals upload, and the only precinct report's known upload time is after election night.")
}
d['sources'] += [
    {"url": PG, "via": "fetch_module",
     "content_hash": "23055d6c0bd6738118fab1b130826b992749a0526d1a83e8eb3573cc47a638d0",
     "quote": "<a href=\"/upload/page/6805/2026 March Primary/Results/ED.EV.AB UNOFFICIAL.pdf\" title=\"click to view\"><img alt=\"\" src=\"https://newtools.cira.state.tx.us/upload/page/6805/images/Election%20Results.jpg\" ... ; 03/03/2026 March 3, 2026 Joint Primary Election - Official Results by Precinct",
     "supports": "state-hosted copy of the county's older Elections page lists the 2026 primary unofficial county-totals report and the official precinct report"},
    {"url": U, "via": "fetch_module",
     "content_hash": "c6a4fd4bacd076662416a29a95fb951bd7d3e8f84502f432acb44e2a36e4095b",
     "quote": "Cumulative Results Report MEDINA COUNTY, TEXAS Unofficial Results 2026 JOINT PRIMARY ELECTION 3/3/2026 Run Time 9:47 PM Run Date 03/03/2026 Precincts Reporting 15 of 15 = 100.00% (read from page images; Last-Modified Wed, 04 Mar 2026 04:03:31 GMT)",
     "supports": "2026_primary LATER: county totals only, uploaded 10:03 PM CST election night"},
    {"url": PCT, "via": "fetch_module",
     "content_hash": "a91130c3fdd8f8ff8787e8b7342f346ed9f6b7d949155834da59795bff1641e6",
     "quote": "Precinct Results Report Official Results MEDINA COUNTY, TEXAS 2026 JOINT PRIMARY ELECTION Run Time 10:42 AM Run Date 03/13/2026 (Last-Modified Fri, 13 Mar 2026 16:11:41 GMT)",
     "supports": "2026_primary precinct numbers first posted at canvass, after election night"},
    {"url": "websearch:medinatx.gov upload page 6805 2026 Unofficial Results", "via": "websearch",
     "content_hash": "d5bf6bb03808f710d1a25fdae15b624ba637b559fb6a8541b4338ad929f4f401",
     "quote": "Official Cumulative Results | https://newtools.cira.state.tx.us/upload/page/6805/2026 March Primary/Results/Official Cumulative Results.pdf",
     "supports": "locating only: Medina files are mirrored on newtools.cira.state.tx.us under /upload/page/6805/"},
]
tag, single = compute_tag(d['elections'])
d['tag'] = tag
d['confidence'] = compute_confidence(d)
d['evidence_url'] = U
d['tag_rationale'] = ("Only the 2026 primary is determined (LATER, check 2: an election-night county-totals upload and a precinct report first uploaded at canvass), "
                      "so the rule gives COUNTY_ONLY_PRECINCT_AT_CANVASS with confidence low.")
d['notes'] += (" Targeted pass 4 2026-10-02 (targeted4-I): 2026_primary changed UNDETERMINED -> LATER (check 2). The county's older page is still served at "
               "newtools.cira.state.tx.us/page/medina.Elections (files under /upload/page/6805/, keeping original Last-Modified times); it links "
               "'2026 March Primary/Results/ED.EV.AB UNOFFICIAL.pdf', a scanned county-totals Cumulative Results Report (Run Time 9:47 PM 03/03/2026, 15 of 15 precincts) "
               "uploaded Wed, 04 Mar 2026 04:03:31 GMT (10:03 PM CST), and the only precinct report (Official Precinct Results.pdf) was uploaded 13 Mar 2026. "
               "Tried without result: newtools /page/medina.Elections-2026 and /page/medina.Elections-2024%20and%202025 (HTTP 403); runoff files under newtools /upload/page/6805/ (404, "
               "that copy predates the runoff); one pattern-named try each at medinatx.gov '0103/2026 May Primary Runoff/Results/ED.EV.AB UNOFFICIAL.pdf' and newtools "
               "'6805/2024 November General/Results/ED.EV.AB UNOFFICIAL.pdf' (both 404); newtools 2024 'Official Pct Results 11.5.24.pdf' keeps Last-Modified Sat, 03 May 2025 22:49:57 GMT (no election-night file); "
               "PER.pdf (March reconciliation scan) uploaded Wed, 04 Mar 2026 20:22:03 GMT (reconciliation form, not results). Three web searches (two newtools PDFs they surfaced belong to Liberty and Gaines counties, not Medina). "
               "No wayback-data targeted archives or sweep for Medina (sweep pending). 2024_general and 2026_runoff stay UNDETERMINED: no election-night file survives.")
validate_v2(d)
json.dump(d, open(p, 'w'), indent=2, ensure_ascii=False)
print(d['tag'], d['confidence'])
