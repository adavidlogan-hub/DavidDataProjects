import json, sys
sys.path.insert(0, '.')
from phase1.schema import compute_tag, compute_confidence, validate_v2

AG = "targeted3-L"
def load(c): return json.load(open(f"phase1/evidence/{c}.json"))
def save(c, d):
    tag, _ = compute_tag(d["elections"]); d["tag"] = tag
    d["confidence"] = compute_confidence(d)
    validate_v2(d)
    json.dump(d, open(f"phase1/evidence/{c}.json", "w"), indent=2, ensure_ascii=False)
    print(c, d["tag"], d["confidence"])
def src(url, via, h, quote, supports):
    return {"url": url, "via": via, "content_hash": h, "quote": quote, "supports": supports}

# ---------- Hutchinson ----------
C = "https://newtools.cira.state.tx.us/upload/page/10714/docs/"
d = load("Hutchinson")
e = d["elections"]
e["2024_general"] = {"result": "END", "check": "2", "county_totals_first_seen": "",
  "precinct_first_seen": "2024-11-05 22:27 CT", "night_updates_with_precinct_numbers": "1",
  "evidence_url": C + "2024/2024%20General%20Precint%20by%20Precinct%20Unofficial%20Results.pdf",
  "fact": "The county's earlier election page (newtools.cira.state.tx.us/page/hutchinson.ElectionInformation, still online) links 'Precinct by Precinct Unofficial Results' to 2024/2024 General Precint by Precinct Unofficial Results.pdf, Last-Modified Wed, 06 Nov 2024 04:27:09 GMT (2024-11-05 22:27 CST). Same content hash (2b0536...) as the August 2026 Umbraco copy. Scanned page 1 read from the page image: 'Summary Results Report TX Hutchinson County November 5, 2024 ... 2024 GENERAL UNOFFICIAL RESULTS ... Precinct 11 ... REP Donald J. Trump/JD Vance 1,047 22 788 237' (Absentee, Early Voting, Election Day); footer 'Precinct Summary - 11/05/2024 9:55 PM'. The companion county summary ('Election Summary - 11/05/2024 9:53 PM', 'Election Day Precincts Reporting 8 of 8') was uploaded as 2024 General Unofficial Results.pdf at Wed, 06 Nov 2024 04:56:08 GMT (10:56 PM CST). One unofficial precinct report, uploaded on election night with the complete count."}
e["2026_primary"] = {"result": "LATER", "check": "2", "county_totals_first_seen": "2026-03-03 22:29 CT",
  "precinct_first_seen": "", "night_updates_with_precinct_numbers": "0",
  "evidence_url": C + "Voter%20Turnout/Unofficial%20Summary%20Republican.pdf",
  "fact": "On the county's earlier election page, 'Unofficial Summary Republican' (Voter Turnout/Unofficial Summary Republican.pdf, same content hash 2a7ed0... as the current copy, county totals printed 10:13 PM with 'Election Day Precincts Reporting 8 of 8') has Last-Modified Wed, 04 Mar 2026 04:29:33 GMT (2026-03-03 22:29 CST), and 'Unofficial Summary Democratic' Wed, 04 Mar 2026 04:29:37 GMT. The precinct reports 'Precinct by Precinct Republican' (content hash 4c6985..., footer 'PRECINCT BY PRECINCT REPULICAN - 03/03/2026 10:08 PM', per-precinct Election Day votes such as 'Ken Paxton 150 3 91 56') and 'Precinct by Precinct Democrat' have Last-Modified Wed, 04 Mar 2026 15:10:14 GMT and 15:10:20 GMT (9:10 AM CST March 4), after election night. County totals on election night; precinct numbers the next morning."}
e["2026_runoff"] = {"result": "END", "check": "2", "county_totals_first_seen": "",
  "precinct_first_seen": "2026-05-26 21:48 CT", "night_updates_with_precinct_numbers": "1",
  "evidence_url": C + "2026%20Runoff/Precinct%20by%20Precinct%20Republican.pdf",
  "fact": "On the county's earlier election page, '2026 Runoff/Precinct by Precinct Republican.pdf' (same content hash 3a7ca8... as the current copy; scan read from the page image: 'Summary Results Report 2026 Primary Runoff Election May 26, 2026 UNOFFICIAL REPUBLICAN RESULTS Hutchinson County Precinct 11 ... Ken Paxton 109 4 55 50', footer 'UNOFFICIAL REPUBLICAN RESULTS - 05/26/2026 9:31 PM') has Last-Modified Wed, 27 May 2026 02:48:23 GMT (9:48 PM CDT), and 'Precinct by Precinct Democratic.pdf' Wed, 27 May 2026 02:48:20 GMT (9:48 PM CDT). One unofficial precinct report per party, uploaded on election night."}
d["evidence_url"] = e["2026_runoff"]["evidence_url"]
d["precinct_first_seen_local_time"] = "2024-11-05 22:27 CT"
d["sources"] += [
  src("websearch:?q=newtools.cira.state.tx.us upload page 10714 Hutchinson County unofficial results", "websearch", "5ed4bdc2d52ab89a216059ef701d8b69063ab782a68290bd602c2d18157590ee", "* * * Hutchinson County Elections * * * YOUR VOTE MATTERS | https://newtools.cira.state.tx.us/page/hutchinson.ElectionInformation", "located the county's earlier election page and file folder (locating only)"),
  src("https://newtools.cira.state.tx.us/page/hutchinson.ElectionInformation", "fetch_module", "a5832531fd906980a50dca609b1fa7ddb7d6c9ee3159f468507ffd0a5ae65157", "Precinct by Precinct Unofficial Results | .../docs/2024/2024 General Precint by Precinct Unofficial Results.pdf; Republican | .../docs/Voter Turnout/Unofficial Summary Republican.pdf; Republican | .../docs/2026 Runoff/Precinct by Precinct Republican.pdf", "earlier county election page still online, with original upload times on its files"),
  src(C + "2024/2024%20General%20Precint%20by%20Precinct%20Unofficial%20Results.pdf", "fetch_module", "2b0536772704d26b0a996b9e4737b868df43ebedd73da4e35fbbff64a50d0205", "Last-Modified: Wed, 06 Nov 2024 04:27:09 GMT; 'Precinct Summary - 11/05/2024 9:55 PM' (page image)", "2024 general END: precinct report uploaded 10:27 PM CST election night"),
  src(C + "2024/2024%20General%20Unofficial%20Results.pdf", "fetch_module", "cec198ca0a3a81f3fc15bb58144f3a30376c6354f5cf8f32e51a06018cfa9a7f", "Last-Modified: Wed, 06 Nov 2024 04:56:08 GMT; 'Election Day Precincts Reporting 8 of 8 ... Election Summary - 11/05/2024 9:53 PM' (page image)", "2024 count complete at 9:53 PM"),
  src(C + "Voter%20Turnout/Unofficial%20Summary%20Republican.pdf", "fetch_module", "2a7ed0b4cf139671de9005e0cfd3d317cf55ce90a97a44a31a732804cf5cd375", "Last-Modified: Wed, 04 Mar 2026 04:29:33 GMT", "2026 primary county totals uploaded 10:29 PM CST election night"),
  src(C + "Voter%20Turnout/Unofficial%20Summary%20Democratic.pdf", "fetch_module", "121a5f9ca2633ada7e40747bb166ed8fa3281b5eb30719e4ab63da338460115e", "Last-Modified: Wed, 04 Mar 2026 04:29:37 GMT", "2026 primary Democratic county totals uploaded on election night"),
  src(C + "Voter%20Turnout/Precinct%20by%20Precinct%20Republican.pdf", "fetch_module", "4c698052d8bfc53968e195c0d59cef4f10d369a1b520c4dec20f6e61755f3992", "Last-Modified: Wed, 04 Mar 2026 15:10:14 GMT; 'ELECTION DAY UNOFFICIAL RESULTS 2026 Primary Election March 3, 2026 Hutchinson County Precinct 11 ... Ken Paxton 150 3 91 56'", "2026 primary precinct report uploaded 9:10 AM CST March 4, after election night"),
  src(C + "Voter%20Turnout/Precinct%20by%20Precinct%20Democrat.pdf", "fetch_module", "b41a85342c056d71ae4a1c6999d301ccd77d3bea89fdf58ba9a9f79b38a26986", "Last-Modified: Wed, 04 Mar 2026 15:10:20 GMT", "2026 primary Democratic precinct report uploaded after election night"),
  src(C + "2026%20Runoff/Precinct%20by%20Precinct%20Republican.pdf", "fetch_module", "3a7ca88674949afbce40818486f3468eedf913d5e4351090231ba28b2c279612", "Last-Modified: Wed, 27 May 2026 02:48:23 GMT; 'UNOFFICIAL REPUBLICAN RESULTS - 05/26/2026 9:31 PM' (page image)", "2026 runoff END: precinct report uploaded 9:48 PM CDT election night"),
  src(C + "2026%20Runoff/Precinct%20by%20Precinct%20Democratic.pdf", "fetch_module", "ad652963c87413d033e7e73b1f0c32a8f2eb5eb1dd1faba9373efbd429b88f18", "Last-Modified: Wed, 27 May 2026 02:48:20 GMT", "2026 runoff Democratic precinct report uploaded on election night"),
]
d["tag_rationale"] = "2024_general END and 2026_runoff END (check 2, election-night upload times on the county's earlier site); 2026_primary LATER. Two elections share END, so the rule gives PRECINCT_END_OF_NIGHT; confidence med because check 2 decides."
d["notes"] += " Targeted pass 3 2026-10-02 (targeted3-L): Settled the verifier disagreement (verifier END x3 on printed times; research UNDETERMINED x3 under rule 47 because the Umbraco copies were re-uploaded in August 2026). A web search located the county's earlier election page, still online at newtools.cira.state.tx.us/page/hutchinson.ElectionInformation, whose files are byte-identical (same content hashes) to the current copies but keep their original Last-Modified times: 2024 precinct report uploaded 2024-11-05 22:27 CST (END); 2026 primary county summaries uploaded 2026-03-03 22:29 CST but precinct reports 2026-03-04 09:10 CST (LATER); 2026 runoff precinct reports uploaded 2026-05-26 21:48 CDT (END). Tag UNKNOWN to PRECINCT_END_OF_NIGHT. Wayback (web.archive.org) was unreachable from the fetch module during this pass (robots.txt fetch reset), so no archive check; sweep not expected for this county."
save("Hutchinson", d)

# ---------- Dawson ----------
D = "https://www.co.dawson.tx.us/upload/page/1590/2026/"
d = load("Dawson")
d["elections"]["2026_primary"] = {"result": "END", "check": "2", "county_totals_first_seen": "",
  "precinct_first_seen": "2026-03-03 23:59 CT", "night_updates_with_precinct_numbers": "1",
  "evidence_url": D + "REPUBLICAN%20PRECINCT%20UNOFFICIAL.pdf",
  "fact": "The Election Information page now lists March 3, 2026 primary files, including 'REPUBLICAN UNOFFICIAL PRECINCT RESULTS' (REPUBLICAN PRECINCT UNOFFICIAL.pdf: 'PRECINCT RESULTS ... Unofficial Results DAWSON COUNTY, TEXAS ... PRIMARY ELECTION ... Run Time 10:56 PM Run Date 03/03/2026', precinct 1 'Ken Paxton 6 ... 34 ... 25 ... 65' with an Election Day Voting column; Last-Modified Wed, 04 Mar 2026 06:02:36 GMT = 2026-03-04 00:02 CST) and 'DEMOCRATIC UNOFFICIAL PRECINCT RESULTS' (Run Time 9:33 PM; precinct 1 'James Talarico 2 ... 9 ... 10 ... 21'; Last-Modified Wed, 04 Mar 2026 05:59:37 GMT = 2026-03-03 23:59 CST). Republican cumulative uploaded Wed, 04 Mar 2026 06:00:25 GMT. One unofficial precinct report per party, uploaded on election night; official reports followed 3-12-2026."}
d["sources"] += [
  src("https://www.co.dawson.tx.us/page/dawson.Election.Information", "fetch_module", "67062e4586b6f21b6091894af15d4390c58a4cbf114b4a890d3c642ff06c9a2b", "DEMOCRATIC UNOFFICIAL PRECINCT RESULTS | /upload/page/1590/2026/DEMOCRATIC PRECINCT UNOFFICIAL.pdf; REPUBLICAN UNOFFICIAL PRECINCT RESULTS | /upload/page/1590/2026/REPUBLICAN PRECINCT UNOFFICIAL.pdf", "2026 primary files are now listed"),
  src(D + "REPUBLICAN%20PRECINCT%20UNOFFICIAL.pdf", "fetch_module", "d7a93ddf3c15a4378b74c55dbe4e2daf7e52fa7211d7261a819c351e507a4a3e", "PRECINCT RESULTS ... PRIMARY ELECTION ... Run Time 10:56 PM Run Date 03/03/2026; Last-Modified: Wed, 04 Mar 2026 06:02:36 GMT", "2026 primary END: Republican precinct report uploaded 00:02 CST"),
  src(D + "DEMOCRATIC%20PRECINCT%20UNOFFICIAL.pdf", "fetch_module", "cd6a9f30d28cef7b26cd9c210ece7468162745666b99e2d514e9b00067fa219b", "PRECINCT RESULTS ... Run Time 9:33 PM Run Date 03/03/2026; Last-Modified: Wed, 04 Mar 2026 05:59:37 GMT", "2026 primary END: Democratic precinct report uploaded 23:59 CST"),
  src(D + "REPUBLICAN%20CUMULATIVE%20UNOFFICIAL.pdf", "fetch_module", "d0dbeeb39dcb84eb6444d384b5f83168bd1550cb9718c6aa94aafe961b79a599", "Last-Modified: Wed, 04 Mar 2026 06:00:25 GMT", "cumulative uploaded with the precinct reports"),
]
d["tag_rationale"] = "2026_primary END and 2026_runoff END (check 2, election-night upload times); 2024_general LATER. Two elections share END, so the rule gives PRECINCT_END_OF_NIGHT; confidence med because check 2 decides."
d["notes"] += " Targeted pass 3 2026-10-02 (targeted3-L): The Election Information page now lists the March 3, 2026 primary files (earlier passes saw none). Republican and Democratic unofficial precinct reports (Run Time 10:56 PM and 9:33 PM, Election Day columns) have Last-Modified 2026-03-04 00:02 CST and 2026-03-03 23:59 CST, so 2026_primary UNDETERMINED to END (check 2). Tag UNKNOWN to PRECINCT_END_OF_NIGHT. Wayback check 3 shows no election-night captures; Wayback unreachable during this pass."
save("Dawson", d)

# ---------- Zapata ----------
Z = "https://newtools.cira.state.tx.us/upload/page/6427/docs/Results/November%205%202024%20General%20and%20ZCISD%20-%20unofficial%20results.pdf"
d = load("Zapata")
d["elections"]["2024_general"] = {"result": "LATER", "check": "2", "county_totals_first_seen": "2024-11-05 23:25 CT",
  "precinct_first_seen": "", "night_updates_with_precinct_numbers": "0", "evidence_url": Z,
  "fact": "The Elections page (page/zapata.Elections) lists 'November 5, 2024 General & ZCISD Election (unofficial)', a 7-page scanned Hart report read from the page images: 'Cumulative Results Report ... ZAPATA COUNTY, TEXAS GENERAL ELECTION 11/5/2024 ... Unofficial Results ... Run Time 10:55 PM Run Date 11/05/2024', county totals only ('Donald J. Trump JD Vance REP 31 ... 2,064 ... 870 ... 2,965', with an Election Day Voting column), ending '*** End of report ***'. Last-Modified Wed, 06 Nov 2024 05:25:18 GMT (2024-11-05 23:25 CST); PDF CreationDate Tue Nov 5 23:06:25 2024. No 2024 general precinct-level file is listed on the page. County totals on election night, no precinct numbers."}
d["evidence_url"] = Z
d["sources"] += [
  src("https://www.co.zapata.tx.us/page/zapata.Elections", "fetch_module", "8ffedcabcaca330a5916071a2cf6e320640b4d1789ee1bf683ecf12af585d3ab", "November 5, 2024 General & ZCISD Election (unofficial) | https://newtools.cira.state.tx.us/upload/page/6427/docs/Results/November%205%202024%20General%20and%20ZCISD%20-%20unofficial%20results.pdf", "the only 2024 general results file listed"),
  src(Z, "fetch_module", "19a05c0b7276b6895edd1f9e28834248cc2f275a7516574d2185b1afa7216bd5", "Cumulative Results Report ... GENERAL ELECTION 11/5/2024 ... Unofficial Results ... Run Time 10:55 PM (page image); Last-Modified: Wed, 06 Nov 2024 05:25:18 GMT", "2024 general LATER: election-night county totals upload"),
]
d["tag_rationale"] = "Only 2024_general is determined (LATER, check 2), so the rule gives COUNTY_ONLY_PRECINCT_AT_CANVASS with confidence low."
d["notes"] += " Targeted pass 3 2026-10-02 (targeted3-L): Settled the verifier disagreement on 2024_general. The research missed the Elections page link the verifier found; opened it myself: county-totals cumulative report (Run Time 10:55 PM) uploaded 2024-11-05 23:25 CST, and no 2024 precinct file listed, so 2024_general UNDETERMINED to LATER (check 2, rule 43). 2026_primary and 2026_runoff stay UNDETERMINED (only files uploaded after election night; agrees with the verifier after its rule 43 re-application). Wayback harvest for co.zapata.tx.us could not run and Wayback was unreachable during this pass. Tag UNKNOWN to COUNTY_ONLY_PRECINCT_AT_CANVASS (low)."
save("Zapata", d)
