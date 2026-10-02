import json,sys
sys.path.insert(0,'.')
from phase1.schema import compute_tag, compute_confidence, validate_v2
p='phase1/evidence/Angelina.json'
d=json.load(open(p))
B='https://www.angelinacounty.net/files/pdf/elections/pdf/2026/030326/'
d['elections']['2026_primary']={
 "result":"LATER","check":"2",
 "county_totals_first_seen":"2026-03-03 22:05 CT",
 "precinct_first_seen":"",
 "night_updates_with_precinct_numbers":"0",
 "evidence_url":B+"unofficial.results.rep.030326.pdf",
 "fact":"Ruled LATER under DECISIONS 67. The county's Previous Elections page (https://www.angelinacounty.net/previous-elections/), section 'March 3rd Elections', links 'Unofficial Results (DEM)' and 'Unofficial Results (REP)' (unofficial.results.dem/rep.030326.pdf), 'Unofficial Totals (DEM)/(REP)', 'Official Total Reconciliation (DEM)/(REP)', 'Reconciliation of Total Votes Cast at Each Polling Location', hand count audit files and notices; no precinct results report of any kind is listed for this election. The Unofficial Results files are county totals: 'Summary Results Report UNOFFICIAL RESULTS TX Angelina County 260303 Primary 6110 21 of 21 ED March 3, 2026 Angelina County', candidate totals by Absentee, Early Voting and Election Day, footer 'Election Summary - 03/03/2026 10:05 PM' (pages 1 to 12 REP and 14 to 21 DEM 'of 22'), so the county-totals report was printed 10:05 PM CST on election night. The online copies are scans (Adobe Paper Capture) uploaded Mon, 09 Mar 2026 13:15 GMT, after election night. 'Unofficial Totals' are SOS Form 12-1 'Preliminary Election Reconciliation - Unofficial Totals' (ballot counts, no candidate votes; Last-Modified 04 Mar 2026 20:22 GMT and 05 Mar 2026 14:01 GMT); 'Reconciliation of Total Votes Cast at Each Polling Location' is SOS Form 12-3 (turnout by location, Last-Modified 01 Apr 2026). No per-precinct candidate votes for this election appear on the county site (precinct numbers never published online as far as the county pages show). Caveat (DECISIONS 67): Last-Modified dates the current copies only."}
d['tag'],single=compute_tag(d['elections'])
d['confidence']=compute_confidence(d)
d['evidence_url']=B+"unofficial.results.rep.030326.pdf"
d['tag_rationale']="Only the 2026 primary is determined (LATER: county-totals report printed 10:05 PM on election night, and the county's Previous Elections page lists no precinct report for that election); one determined election gives COUNTY_ONLY_PRECINCT_AT_CANVASS with low confidence. 2024 general and 2026 runoff stay UNDETERMINED."
d['agent']=d['agent'] if 'targeted4-F' in d['agent'] else d['agent']+'; targeted4-F'
d['notes']+=(" Targeted pass 4 2026-10-02 (targeted4-F): 2026_primary UNDETERMINED -> LATER (check 2, DECISIONS 67); tag UNKNOWN -> COUNTY_ONLY_PRECINCT_AT_CANVASS, confidence low (one determined election). New source: the county's Previous Elections page (https://www.angelinacounty.net/previous-elections/, linked from the Elections page as 'previous-elections'), which earlier passes had not opened. It lists the 2026 primary 'Unofficial Results (DEM)/(REP)' files (county totals printed 10:05 PM election night) and no precinct report for that election, which meets DECISIONS 67 (ii). 2024_general stays UNDETERMINED: the page's November General Election 2024 block lists 'General Election Canvass Report', 'View Election Unofficial Reconciliation' (unofficial 11.05.24 totals DocScan.pdf, a scanned SOS Form 12-1 ballot-count reconciliation dated 11-5-24 with no candidate votes, read from the page image; Last-Modified Fri, 08 Nov 2024 14:05:08 GMT), 'Election Reconciliation - Official Totals', 'Official Results Election Summary' (scan, Last-Modified 25 Nov 2024) and 'Official Results Precinct Summary' (OFFICIAL RESULTS PRECINCT SUMMARY, CreationDate 14 Nov 2024, Last-Modified 25 Nov 2024); no election-night county-totals results file, so rule 43 (i) is not met. 2026_runoff stays UNDETERMINED: the May 26th Election block lists 'Dem Official Totals', 'Rep Official Totals' (official reconciliation), 'Total Votes Cast at Each Polling Location', hand count audit files and notices, and no unofficial results file; per the task no unlisted file names were guessed. Dead ends: /files/pdf/elections/pdf/2026/030326/ and /2026/ directory listings return HTTP 403; the live app's api/elections.php (which the app's JavaScript uses for past elections) returns HTTP 401 (admin login), so it was not pursued. No wayback-data sweep or targeted archive folder exists for Angelina; the main harvest index has no captures.")
d['sources'] += [
 {"url":"https://www.angelinacounty.net/previous-elections/","via":"fetch_module","content_hash":"9f8aa6b918eca7973dc40e0807857566d542ff12f75c8b793e84cb520a677a3e",
  "quote":"March 3rd Elections ... Official Total Reconciliation (DEM) | Official Total Reconciliation (REP) | Cert. of Post-Election Hand Count Audit Results | Unofficial Results (DEM) | Unofficial Results (REP) | Unofficial Totals (DEM) | Unofficial Totals (REP) | Post Audit Hand Count ... Reconciliation of Total Votes Cast at Each Polling Location",
  "supports":"County listing for the 2026 primary: county-totals unofficial results and no precinct report (DECISIONS 67 (ii)); 2024 general and 2026 runoff blocks list no election-night results file"},
 {"url":B+"unofficial.results.rep.030326.pdf","via":"fetch_module","content_hash":"72f537fa6f9086fc3c654195ad5ddc82da29fa6e67cfd7d5170531bd461d0c3c",
  "quote":"Summary Results Report UNOFFICIAL RESULTS TX Angelina County 260303 Primary 6110 21 of 21 ED ... TOTAL VOTE% Absentee Early Voting Election Day ... Election Summary - 03/03/2026 10:05 PM",
  "supports":"County-totals report printed 10:05 PM CST on 2026 primary election night (Last-Modified Mon, 09 Mar 2026 13:15:43 GMT)"},
 {"url":B+"unofficial.results.dem.030326.pdf","via":"fetch_module","content_hash":"8a56dd2587edc79830861498e9cc5d6f56e93781587c16a18593e0563aebe1ad",
  "quote":"Summary Results Report UNOFFICIAL RESULTS TX Angelina County 260303 Primary 6110 ... Election Summary - 03/03/2026 10:05 PM 15 of 22",
  "supports":"Democratic county totals from the same 10:05 PM election-night summary run (Last-Modified Mon, 09 Mar 2026 13:15:59 GMT)"},
 {"url":B+"unofficial.totals.rep.030326.pdf","via":"fetch_module","content_hash":"5121c5f80b244236fedd2c8859812b9956f22bf14b3498a05ed660bd5973e802",
  "quote":"Preliminary Election Reconciliation - Unofficial Totals ... accurately reflects the unofficial votes and voters as known to me on election night",
  "supports":"'Unofficial Totals' are ballot-count reconciliation forms, not precinct candidate results (Last-Modified Thu, 05 Mar 2026 14:01:39 GMT)"},
 {"url":B+"reconciliation_of_total_votes_cast_at_each_polling_location_030326.pdf","via":"fetch_module","content_hash":"2453ec55b991e517a4832ee6b490e3f01056218f2a8e611d6d3f15346c2a7373",
  "quote":"RECONCILIATION OF TOTAL VOTES CAST AT EACH POLLING LOCATION Date and Nature of Election: MARCH 3, 2026 JOINT PRIMARY",
  "supports":"Per-location turnout form only, no candidate votes (Last-Modified Wed, 01 Apr 2026 13:04:23 GMT)"},
 {"url":"https://www.angelinacounty.net/files/pdf/elections/pdf/2024/unofficial%2011.05.24%20totals%20DocScan.pdf","via":"fetch_module","content_hash":"926281a3d346feea2f27d18b4e258fc9226f2a2edcb7d5ca05fae46703390bc7",
  "quote":"Preliminary Election Reconciliation - Unofficial Totals ... County Angelina ... Election Name General ... Election Date 11-5-24 (read from the page image)",
  "supports":"2024 general 'unofficial' item is a ballot-count reconciliation form, not a county-totals results file (Last-Modified Fri, 08 Nov 2024 14:05:08 GMT)"},
 {"url":"https://www.angelinacounty.net/files/pdf/elections/pdf/2024/Offical%20Precinct%20Summary%2011052024.pdf","via":"fetch_module","content_hash":"44bd1df98178fb424de63acb3036afb6ba348cd22e7a51166895cfc0cc14b934",
  "quote":"Summary Results Report OFFICIAL RESULTS TX Angelina County 241105 General 6110 PRECINCT SUMMARY",
  "supports":"2024 general precinct report is official (CreationDate 14 Nov 2024, Last-Modified Mon, 25 Nov 2024 17:32:02 GMT)"},
]
validate_v2(d)
json.dump(d,open(p,'w'),indent=2,ensure_ascii=False); open(p,'a').write('\n')
print(d['tag'],d['confidence'])
