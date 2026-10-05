import json, sys, os, datetime
sys.path.insert(0, '.')
sys.path.insert(0, '/tmp/claude-0/-home-user-DavidDataProjects/b9d39f46-6729-513d-bc75-aa4d5d82b4b6/scratchpad')
from h import h
from phase1.schema import compute_tag, compute_confidence
NOW = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
WB = '792164786fb683af797a84c69470c803a5ebe55f'
REASON = "tag changed in targeted pass 3"
U = lambda r: {"result": "UNDETERMINED", "check": "none", "fact": r}
L2 = lambda f: {"result": "LATER", "check": "2", "fact": f}

def src(url, what):
    return {"url": url, "content_hash": h(url) or "", "what_i_checked": what}

C = {}
# Caldwell
cb = "https://www.co.caldwell.tx.us/upload/page/0213/docs/"
C["Caldwell"] = dict(
 elections={
  "2024_general": U("Elections.Results Page lists for Nov 5 2024 only files from after election night: \"Unofficial Early Voting and Election Day Results\" (FinalUnofficialResults110524.pdf, header \"FINAL UNOFFICIAL RESULTS\", printed \"Election Summary - 11/13/2024 5:45 PM\", Last-Modified Thu 14 Nov 2024 02:42:17 GMT), \"Unofficial Early Voting and Election Day Pct by Pct\" (FinalPCTbyPCT11052024.pdf, printed \"Precinct Summary - 11/13/2024 8:00 PM\", Last-Modified 14 Nov 2024 02:42:32 GMT), and a scanned preliminary reconciliation (Last-Modified 06 Nov 2024 15:28:53 GMT = 9:28 AM CST Nov 6). No election-night file survives. Check 3: the only election-night capture (2024-11-06 01:43 CST) is of the old /page/ElectionResults page, which still lists 2016 to 2018 files only; no 2024 content."),
  "2026_primary": L2("County totals on election night: \"FULL Summary Results_REP Primary_030326.pdf\" and \"FULL Summary Results_DEM_Primary 030326.pdf\" (\"Summary Results Report ... UNOFFICIAL RESULTS\", county totals with an Election Day column, e.g. DEM ballots cast Election Day 1,226), printed \"03/03/2026 10:19 PM\" / \"10:18 PM\", Last-Modified Wed 04 Mar 2026 04:44:53 GMT (10:44 PM CST Mar 3); an earlier summary printed 7:14 PM was uploaded 02:20 GMT (8:20 PM CST). The only unofficial precinct reports (\"FULL PCTbyPCT_Rep/Dem Primary Unofficial_030326.pdf\", per-precinct candidate votes with Election Day column) print \"03/03/2026 10:50\" but have Last-Modified Wed 04 Mar 2026 15:47:28 and 15:47:40 GMT (9:47 AM CST Mar 4), after election night (rule 43 reading / rule 47). No other upload time found (newtools.cira mirror path 404)."),
  "2026_runoff": L2("County totals on election night: \"Unofficial_REP Primary Runoff_05262026.pdf\" and \"Unofficial_DEM ...\" (\"Summary Results Report ... UNOFFICIAL RESULTS\", Ballots Cast - Total 2,810 with Election Day 1,207), printed \"Republican Primary Runoff Results - 05/26/2026 8:57 PM\", Last-Modified Wed 27 May 2026 02:10:10 GMT (9:10 PM CDT May 26). The unofficial precinct reports (\"Unofficial_DEM/REP Primary Runoff_PCTbyPCT Report.pdf\") print \"05/28/2026 3:49 PM\" / \"3:51 PM\", Last-Modified Fri 29 May 2026 13:24 GMT; the FinalUnofficial precinct reports are from Jun 2. No precinct numbers posted on election night."),
 },
 sources=[
  src("https://www.co.caldwell.tx.us/page/Elections.Results Page", "results page: list of reports for all three elections"),
  src(cb+"2024/FinalUnofficialResults110524.pdf", "2024 unofficial summary, printed Nov 13, Last-Modified Nov 14"),
  src(cb+"2024/FinalPCTbyPCT11052024.pdf", "2024 unofficial precinct report, printed Nov 13, Last-Modified Nov 14"),
  src(cb+"2024/PRELIMINARYRECONCILLIATION_110524.pdf", "scanned reconciliation, Last-Modified Nov 6 9:28 AM CST"),
  src(cb+"2026/Primaries/FULL Summary Results_REP Primary_030326.pdf", "primary county totals printed 10:19 PM, Last-Modified 10:44 PM CST Mar 3"),
  src(cb+"2026/Primaries/FULL Summary Results_DEM_Primary 030326.pdf", "primary county totals printed 10:18 PM, Last-Modified 10:44 PM CST Mar 3"),
  src(cb+"2026/Primaries/Summary Results_REP Primary_030326.pdf", "earlier summary printed 7:14 PM, Last-Modified 8:20 PM CST"),
  src(cb+"2026/Primaries/FULL PCTbyPCT_Rep Primary Unofficial_030326.pdf", "precinct report printed 10:50, Last-Modified Mar 4 9:47 AM CST"),
  src(cb+"2026/Primaries/FULL PCTbyPCT_Dem Primary Unofficial_030326.pdf", "precinct report printed 10:50, Last-Modified Mar 4 9:47 AM CST"),
  src(cb+"2026/Primary Runoff/Unofficial_REP Primary Runoff_05262026.pdf", "runoff county totals printed 8:57 PM, Last-Modified 9:10 PM CDT"),
  src(cb+"2026/Primary Runoff/Unofficial_DEM Primary Runoff_05262026.pdf", "runoff county totals, Last-Modified 9:10 PM CDT"),
  src(cb+"2026/Primary Runoff/Unofficial_REP Primary Runoff_PCTbyPCT Report.pdf", "runoff precinct report printed May 28, Last-Modified May 29"),
  src(cb+"2026/Primary Runoff/Unofficial_DEM Primary Runoff_PCTbyPCT Report.pdf", "runoff precinct report printed May 28, Last-Modified May 29"),
  {"url": "git show origin/wayback-data:phase1/wayback_snapshots/Caldwell/2024_general_20241106074317_8210af7296bb.html", "content_hash": "8210af7296bbf7e53de4442c3c328abe99b188cea0ae4fdc72c5d2398d7e7876", "what_i_checked": "election-night capture of old ElectionResults page: only 2016 to 2018 files (wayback-data "+WB[:12]+")"},
 ])
# Crockett
crb = "https://www.co.crockett.tx.us/upload/page/9753/"
C["Crockett"] = dict(
 elections={
  "2024_general": U("The county Elections page (co.crockett.tx.us/page/crockett.Elections; seed website blank) lists only 2026 files; nothing for Nov 2024. No Wayback folder for Crockett on wayback-data: check 3 pending. Not on Clarity (elections.json 404)."),
  "2026_primary": L2("\"Unofficial Primary Elections Results 03-03-26\" (2026/unofficialprimaryelectionresults030426.pdf, scanned, 20 pages, read visually): \"Summary Results Report ... UNOFFICIAL RESULTS ... Crockett County\", county totals with Election Day column, \"Election Day Precincts Reporting 4 of 4\", printed footer \"Election Summary - 03/03/2026 07:44PM\" (election night). Last-Modified Wed 04 Mar 2026 16:07:32 GMT (10:07 AM CST Mar 4). No precinct-level results report is posted for the primary (the \"Sample Ballot Pct n\" links are sample ballots)."),
  "2026_runoff": L2("\"Election Results for Republican and Democratic 5/26/2026\" (preliminaryelectionreconciliationunofficialtotals052726.pdf, scanned, 5 pages, read visually): two preliminary reconciliation forms plus a \"Summary Results Report ... TX Crockett County 260526 Primary Runoff ... UNOFFICIAL RESULTS\", county totals with Election Day column, \"Election Day Precincts Reporting 4 of 4\", printed \"Election Summary - 05/26/2026 07:16PM\". Last-Modified Wed 27 May 2026 16:26:46 GMT. No precinct results report posted (only official reconciliations and PEHCA worksheets)."),
 },
 sources=[
  src("https://www.co.crockett.tx.us/page/crockett.Elections", "elections page: list of 2026 reports, nothing for 2024"),
  src(crb+"2026/unofficialprimaryelectionresults030426.pdf", "primary county totals, printed 03/03/2026 07:44PM, Last-Modified Mar 4"),
  src(crb+"preliminaryelectionreconciliationunofficialtotals052726.pdf", "runoff county totals, printed 05/26/2026 07:16PM, Last-Modified May 27"),
  src(crb+"2026/preliminaryelectionreconciliationunofficialtotals2026republicanprimary030426.pdf", "primary reconciliation form, Last-Modified Mar 4"),
 ])
# Lamb
lb = "https://www.co.lamb.tx.us/upload/page/0112/docs/"
C["Lamb"] = dict(
 elections={
  "2024_general": U("co.lamb.tx.us/page/ElectionsHome (and its newtools.cira mirror lamb.ElectionsHome, page 9262) lists only May 26 2026 runoff results; nothing for Nov 2024; County Clerk page has no results. Check 3: the Wayback CDX request for this window failed (\"Connection refused\") on wayback-data, no captures; check 3 incomplete."),
  "2026_primary": U("No primary results listed on ElectionsHome or its mirror. Check 3: CDX request failed (\"Connection refused\"), no captures; check 3 incomplete."),
  "2026_runoff": L2("\"Primary Runoff Election Unofficial Results 5.26.26\" (Primary Runoff Results 5.26.26.pdf, scanned, read visually): \"Summary Results Report ... TX Lamb County 260526 Primary Runoff Election ... ELECTION UNOFFICIAL SUMMARY\", county totals with Election Day column (Election Day Precincts Reporting 11 of 11), printed \"Election Summary - 05/26/2026 9:04 PM\"; Last-Modified Wed 27 May 2026 18:56:34 GMT (same on the cira mirror). \"OFFICIAL RESULTS 5.26.26\" is an official summary (Last-Modified 04 Jun 2026). The \"REP/DEM PCT n 5.26.26\" links are sample ballots (\"Official Ballot (Boleta Oficial)\"), Last-Modified Apr 30. No precinct results posted. Wayback CDX for this window ok, no captures."),
 },
 sources=[
  src("https://www.co.lamb.tx.us/page/ElectionsHome", "elections page: only runoff results"),
  src("https://newtools.cira.state.tx.us/page/lamb.ElectionsHome", "cira mirror: same list"),
  src(lb+"Primary Runoff Results 5.26.26.pdf", "runoff unofficial summary printed 9:04 PM May 26, Last-Modified May 27"),
  src(lb+"OFFICIAL RESULTS 5.26.26.pdf", "official summary"),
  src(lb+"REP PCT 1 5.26.26.pdf", "sample ballot, not results"),
  src(lb+"DEM PCT 12 5.26.26.pdf", "sample ballot, not results"),
 ])
# Menard
mb = "https://www.co.menard.tx.us/upload/page/0215/"
C["Menard"] = dict(
 elections={
  "2024_general": U("The Elections page (www.co.menard.tx.us/page/menard.Elections; co.menard.tx.us without www is robots-blocked) links \"Election Night Results / Resultados de la noche de las elecciones\" to /upload/page/0215/Menard County 2024 Nov 5 ENR.pdf, which returns HTTP 404 (also 404 on newtools.cira mirror). No surviving file. Check 3: Wayback CDX for co.menard.tx.us was robots_disallowed_or_unreachable, no captures."),
  "2026_primary": L2("\"ELECTION NIGHT RESULTS\" = Elections/2026/Primary/Cumulative Results-3-3-2026 08-49-21 PM.pdf: \"Cumulative Results Report MENARD COUNTY, TEXAS Unofficial Results\", county totals by Absentee/Early/Election Day Voting, \"Run Time 8:48 PM Run Date 03/03/2026\", no per-precinct sections; Last-Modified Wed 04 Mar 2026 02:56:15 GMT (8:56 PM CST Mar 3). No precinct results report posted (the \"SB Rep/Dem Prt n\" links are sample ballots, Last-Modified Jan 15 2026)."),
  "2026_runoff": L2("\"Election Night Results\" = Elections/2026/Runoff/20260526201711scan.pdf (scanned, read visually): \"Cumulative Results Report MENARD COUNTY, TEXAS ... PRIMARY RUNOFF ELECTION ... Unofficial Results\", county totals with Election Day Voting column, \"Precincts Reporting 6 of 6\", \"Run Time 7:38 PM\" (REP) and \"7:40 PM\" (DEM), \"Run Date 05/26/2026\"; Last-Modified Wed 27 May 2026 01:35:21 GMT (8:35 PM CDT May 26). No precinct results posted."),
 },
 sources=[
  src("https://www.co.menard.tx.us/page/menard.Elections", "elections page: report list"),
  src("https://newtools.cira.state.tx.us/page/menard.Elections", "cira mirror: same list"),
  {"url": mb+"Menard County 2024 Nov 5 ENR.pdf", "content_hash": "", "what_i_checked": "HTTP 404"},
  src(mb+"Elections/2026/Primary/Cumulative Results-3-3-2026 08-49-21 PM.pdf", "primary county totals, run 8:48 PM, Last-Modified 8:56 PM CST"),
  src(mb+"Elections/2026/Runoff/20260526201711scan.pdf", "runoff county totals, run 7:38/7:40 PM, Last-Modified 8:35 PM CDT"),
  src(mb+"Elections/2026/Primary/SB Rep Prt 1.pdf", "sample ballot, not results"),
 ])
# Val Verde
vb = "https://www.valverdecounty.texas.gov/DocumentCenter/View/"
C["Val Verde"] = dict(
 elections={
  "2024_general": U("valverdecounty.texas.gov/519/_2024 (CivicPlus; DocumentCenter sends no Last-Modified, so no upload times) lists \"2024 General Election Unofficial Results\" (View/8410, scanned, read visually): \"Summary Results Report General Election ... UNOFFICIAL RESULTS\", county totals, printed \"Election Summary - 11/06/2024 2:58 PM\" (after election night), PDF CreationDate Nov 6 21:42 UTC. Precinct-by-precinct only in \"Official Results\" (View/8425). No election-night file. Check 3: CDX ok, no captures. Not on Clarity (elections.json 404)."),
  "2026_primary": L2("\"Unofficial Joint Primary Results\" (/528/_2026, View/10174, scanned, 22 pages, read visually): \"Summary Results Report Joint Primary Election ... UNOFFICIAL RESULTS Val Verde\", county totals with Election Day column on every page, printed \"Election Summary - 03/03/2026 9:35 PM\" (election night; no upload time available, CivicPlus). Precinct-by-precinct only in \"Final -Official Joint Primary Results - Precinct-by-Precinct\" (View/10206). No unofficial precinct report posted."),
  "2026_runoff": L2("\"Unofficial Results - Val Verde County\" (View/10450, scanned, 4 pages, read visually): \"Summary Results Report Joint Primary Run Off ... UNOFFICIAL RESULTS\", county totals (Ballots Cast - Total 1,520, equal to the attached preliminary reconciliation's in-person plus mail total), printed \"Election Summary - 05/26/2026 8:27 PM\"; page 4 is the Preliminary Election Reconciliation dated 5-26-26. Precinct-by-precinct only in \"Official Results Precinct by Precinct\" (View/10473). No unofficial precinct report posted."),
 },
 sources=[
  src("https://www.valverdecounty.texas.gov/270/Elections", "elections hub"),
  src("https://www.valverdecounty.texas.gov/519/_2024", "2024 report list"),
  src("https://www.valverdecounty.texas.gov/528/_2026", "2026 report list"),
  src(vb+"8410/Unofficial-Results-Val-Verde-County-General-Election-202", "2024 unofficial summary printed 11/06/2024 2:58 PM"),
  src(vb+"10174/2026-JOINT-PRIMARY-ELECTIONS-UNOFFICIAL-RESULTS", "primary unofficial summary printed 03/03/2026 9:35 PM"),
  src(vb+"10450/2026-JOINT-PRIMARY-RUN-OFF-UNOFFICIAL-RESULTS", "runoff unofficial summary printed 05/26/2026 8:27 PM"),
 ])

RAT = {
 "Caldwell": "Primary and runoff are LATER (election-night county-totals PDFs with upload times on election night; the only unofficial precinct reports were uploaded the next morning or days later); 2024 has no election-night file. Two LATER results give COUNTY_ONLY_PRECINCT_AT_CANVASS, med (check 2).",
 "Crockett": "Primary and runoff are LATER (scanned county-totals summaries printed 7:44 PM Mar 3 and 7:16 PM May 26; no precinct results posted); 2024 has no files and check 3 is pending. Two LATER results give COUNTY_ONLY_PRECINCT_AT_CANVASS, med (check 2).",
 "Lamb": "Only the runoff is determined (LATER: unofficial county summary printed 9:04 PM May 26, no precinct results posted); 2024 and primary have no files and failed CDX. One determined election gives COUNTY_ONLY_PRECINCT_AT_CANVASS, low.",
 "Menard": "Primary and runoff are LATER (election-night cumulative county-totals reports uploaded 8:56 PM Mar 3 and 8:35 PM May 26; no precinct results posted); the 2024 file is 404. Two LATER results give COUNTY_ONLY_PRECINCT_AT_CANVASS, med (check 2).",
 "Val Verde": "Primary and runoff are LATER (unofficial county-totals summaries printed 9:35 PM Mar 3 and 8:27 PM May 26; precinct-by-precinct posted only as official results); 2024's unofficial summary was printed Nov 6 2:58 PM. Two LATER results give COUNTY_ONLY_PRECINCT_AT_CANVASS, med (check 2).",
}
for county, d in C.items():
    fn = f"phase1/verification/{county.replace(' ', '_')}.json"
    rec = {"county": county, "elections": d["elections"]}
    tag, single = compute_tag(d["elections"])
    conf = compute_confidence(rec)
    out = {"county": county, "reason_selected": REASON, "verifier_tag": tag, "verifier_confidence": conf,
           "elections": d["elections"], "rationale": RAT[county], "sources": d["sources"],
           "written_blind_at_utc": NOW, "verifier_agent": "verifier-12"}
    if os.path.exists(fn):
        old = json.load(open(fn))
        if "previous_verification" not in old:
            out["previous_verification"] = old
        else:
            out["previous_verification"] = old
    txt = json.dumps(out, indent=1, ensure_ascii=False)
    for bad in ("—", "–"):
        assert bad not in txt, (county, bad)
    open(fn, "w").write(txt + "\n")
    print(county, tag, conf, [e["result"] for e in d["elections"].values()])
