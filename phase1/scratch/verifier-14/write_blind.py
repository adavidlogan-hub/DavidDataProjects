import json, sys, datetime, re
sys.path.insert(0, '.')
from txprecinct.config import load_config
from txprecinct.store import Store
from txprecinct.fetch import normalize_url
from phase1.schema import compute_tag, compute_confidence

st = Store(load_config().state_dir)
def h(url):
    r = st.latest_ok(normalize_url(url))
    return dict(r)["content_hash"] if r else ""

REASON = "tag changed in targeted pass 3"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
NO_CLARITY = "Not on Clarity: the county's results pages link no results.enr.clarityelections.com election, so check 1 does not apply. "
NO_WB = "Check 3: wayback-data index for this county has no election-night captures in any window. "

C = {}
# ---------------- Cottle
cb = "https://www.cottlecountytx.gov"
C["Cottle"] = dict(
 elections={
  "2024_general": {"result": "LATER", "check": "2",
   "fact": "Elections.Archive page lists 'November 2024 General Election Results' (results.11.5.pdf): scanned Electionware 'Summary Results Report ... UNOFFICIAL RESULTS', county totals only, footer 'Election Summary - 11/05/2024 9:38 PM' (printed run time on election night); server Last-Modified Wed, 06 Nov 2024 16:25:41 GMT (10:25 AM CST Nov 6). The only precinct report, 'Precinct Results' (Precinct results.pdf, footer 'Precinct Summary - 11/05/2024 9:37 PM'), was scanned 2024-11-22 (XMP CreateDate) and has server Last-Modified Fri, 24 Jan 2025 04:28:12 GMT, i.e. known upload after election night. Rule 43 reading: county totals printed on election night, the only precinct report uploaded later: LATER (county_totals_first_seen 2024-11-05 21:38 CT, printed)."},
  "2026_primary": {"result": "UNDETERMINED", "check": "none",
   "fact": "Elections.2026 page has only post-election files for the primary: 'Election Results' (election_results.pdf, 'OFFICIAL RESULTS', footer 'Election Summary - 03/24/2026 11:35 AM', Last-Modified 25 Mar 2026) and 'Official Results' (reconciliation signed 3-16-26, Last-Modified 16 Mar 2026). No election-night file survives; no Wayback captures."},
  "2026_runoff": {"result": "UNDETERMINED", "check": "none",
   "fact": "'Unofficial Results' (Unoffical Results.pdf) is an SOS 'Election Unofficial Results Report' county-totals form with no printed time, scanned 2026-05-27 13:11 CDT and Last-Modified Wed, 27 May 2026 18:46:51 GMT (1:46 PM CDT May 27), after election night. Official files dated June 5. No election-night file; no Wayback captures."}},
 rationale=NO_CLARITY + NO_WB + "Only the 2024 general is determined (LATER by check 2: county totals printed 9:38 PM election night, precinct report uploaded Jan 2025), so the tag is COUNTY_ONLY_PRECINCT_AT_CANVASS with low confidence.",
 sources=[
  (cb + "/page/Elections.Archive", "Links for 2024 general: results.11.5.pdf, Precinct results.pdf, canvass report"),
  (cb + "/page/Elections.2026", "Links for 2026 primary and runoff results files"),
  (cb + "/upload/page/0106/2024/results.11.5.pdf", "Rendered scan: county-totals Summary Results Report, footer 11/05/2024 9:38 PM; Last-Modified 2024-11-06 16:25:41 GMT"),
  (cb + "/upload/page/0106/2024/Precinct results.pdf", "Rendered scan: Precinct Summary 11/05/2024 9:37 PM; XMP CreateDate 2024-11-22; Last-Modified 2025-01-24 04:28:12 GMT"),
  (cb + "/upload/page/0105/2026/election_results.pdf", "Official results 03/24/2026; Last-Modified 2026-03-25"),
  (cb + "/upload/page/0105/2026/Official Total 2026 Primary.pdf", "Official reconciliation signed 3-16-26"),
  (cb + "/upload/page/0105/2026/Unoffical Results.pdf", "SOS unofficial county totals form, no printed time; Last-Modified 2026-05-27 18:46:51 GMT"),
 ])
# ---------------- Live Oak
lb = "https://www.co.live-oak.tx.us/upload/page/1218/"
C["Live Oak"] = dict(
 elections={
  "2024_general": {"result": "LIVE", "check": "2",
   "fact": "liveoak.Results page lists per-precinct 'Unofficial Pct. N ... Results' PDFs (Hart-style 'Unofficial Results Pct N' reports with Absentee, Early Voting and Election Day Voting candidate columns). Server Last-Modified times fall across election night: Pct 1 Argenta (Run Time 8:56 PM, Election Day votes e.g. Trump 120) 06 Nov 2024 03:08:51 GMT = 9:08 PM CST; W George West 03:34:11; Simmons 03:36:24; E George West 03:53:44; Ray Point 03:57:56; W Three Rivers 04:03:17; Nell 04:10:59; E Three Rivers 04:12:48; Oakville 04:16:05; Whitsett 04:16:34; Swinney Switch 04:17:55; Pct 2 Lagarto (Run Time 10:37 PM, Election Day votes) 04:37:48 GMT = 10:37 PM CST; Unofficial Cumulative 04:45:31 GMT. Precinct numbers with election-day votes were posted in many separate uploads from 9:08 PM to 10:37 PM: LIVE."},
  "2026_primary": {"result": "LATER", "check": "2",
   "fact": "Election History page, March 3 2026 'ELECTION NIGHT RESULTS': 'Early Voting Results', 'Election Night Results', 'Cumulative Results-Democratic', 'Cumulative Results-Republican', 'Election Reconciliation - Official Totals'; no precinct report listed. 'Election Night Results' (EN Unoffical Results.pdf) is a 19-page 'Cumulative Results Report - Election Night Results' (county totals), Run Time 11:09 PM, Run Date 03/03/2026 (printed on election night); Last-Modified 18 Mar 2026 20:45:18 GMT. No unofficial precinct report was ever posted: LATER (county_totals_first_seen 2026-03-03 23:09 CT, printed)."},
  "2026_runoff": {"result": "LATER", "check": "2",
   "fact": "Election History page, 2026 results: 'Unofficial Election Night Results - Republican' (2026May/unoffical res rep.pdf) is a 'Cumulative Results Report' county totals, Run Time 9:38 PM 05/26/2026, Precincts Reporting 14 of 14, Last-Modified Wed, 27 May 2026 02:48:19 GMT (9:48 PM CDT); Democratic version Last-Modified 02:47:59 GMT. No unofficial precinct report listed for the runoff (only Official Results 5.26.26, reconciliation, hand count audit). LATER (county_totals_first_seen 2026-05-26 21:47 CT upload)."}},
 rationale=NO_CLARITY + "Check 3: wayback-data CDX lookups for co.live-oak.tx.us failed (robots_disallowed_or_unreachable), no captures. Primary and runoff are LATER by check 2 (two deciding elections), 2024 general is LIVE, so the rule gives COUNTY_ONLY_PRECINCT_AT_CANVASS, med (check 2).",
 sources=[
  ("https://www.co.live-oak.tx.us/page/liveoak.Results", "Nov 5 2024 per-precinct unofficial PDFs list"),
  ("https://www.co.live-oak.tx.us/page/liveoak.Election History", "2026 primary and runoff results lists"),
  (lb + "2024/Entered%20By%20Bec/Unofficail%20EV%20ARGENTA%20Results.pdf", "Pct 1 run 8:56 PM with election-day votes; Last-Modified 2024-11-06 03:08:51 GMT"),
  (lb + "2024/Entered%20By%20Bec/LAGARTO.pdf", "Pct 2 run 10:37 PM with election-day votes; Last-Modified 2024-11-06 04:37:48 GMT"),
  (lb + "2024/Entered%20By%20Bec/E%20George%20West.pdf", "Last-Modified 2024-11-06 03:53:44 GMT"),
  (lb + "2024/Entered%20By%20Bec/Unofficial%20Cumulative%20Results.pdf", "Last-Modified 2024-11-06 04:45:31 GMT"),
  (lb + "2026/Results/EN%20Unoffical%20Results.pdf", "Cumulative Election Night Results, run 11:09 PM 03/03/2026, county totals; Last-Modified 2026-03-18"),
  (lb + "2026/Results/Cumulative%20Results-Rep.pdf", "Official cumulative county totals (11 pages), no precinct pages"),
  (lb + "2026May/unoffical%20res%20rep.pdf", "Runoff cumulative county totals run 9:38 PM 05/26/2026; Last-Modified 2026-05-27 02:48:19 GMT"),
  (lb + "2026May/unoffical%20res%20dem.pdf", "Last-Modified 2026-05-27 02:47:59 GMT"),
 ])
# ---------------- Hutchinson
hb = "https://www.co.hutchinson.tx.us"
MIG = ("Server Last-Modified on every file of this Umbraco site is an August 2026 bulk re-upload (2024 general files 12 Aug 2026 15:38:27-28 GMT, 2026 primary files 10 Aug 2026 19:06:15 GMT, March 2024 official files 12 Aug 2026 16:37:56 GMT, precinct map 4 Aug 2026), so it carries no information about original posting; treated as no upload time available (verifier judgment, flagged). ")
C["Hutchinson"] = dict(
 elections={
  "2024_general": {"result": "END", "check": "2",
   "fact": "Election Information and Results page, 2024 General: 'Precint By Precinct Unofficial Results' (48 pages, 'Summary Results Report ... 2024 GENERAL UNOFFICIAL RESULTS', 'Precinct 11', per-precinct candidate votes with Election Day column, footer 'Precinct Summary - 11/05/2024 9:55 PM', scan CreationDate 2024-11-05T22:01:17-06:00) and 'General Unofficial Results' (footer 'Election Summary - 11/05/2024 9:53 PM', Election Day Precincts Reporting 8 of 8). " + MIG + "Rule 47: no upload time, printed run time on election night: END (one precinct report)."},
  "2026_primary": {"result": "END", "check": "2",
   "fact": "'Unofficial Results Precinct by Precinct Republican' (80 pages, 'ELECTION DAY UNOFFICIAL RESULTS', Precinct 11 Election Day votes e.g. Cornyn 68, footer 'PRECINCT BY PRECINCT REPULICAN - 03/03/2026 10:08 PM', PDF CreationDate 2026-03-04 04:11:47 UTC = 10:11 PM CST) and Democratic version (10:11 PM); 'Unofficial Summary Republican' footer 10:13 PM with Election Day Precincts Reporting 8 of 8. " + MIG + "END by rule 47 (printed time on election night, one precinct report per party)."},
  "2026_runoff": {"result": "END", "check": "2",
   "fact": "'Precinct by Precinct Results Republican' (scan, 'UNOFFICIAL REPUBLICAN RESULTS', Precinct 11 Election Day votes, footer 'UNOFFICIAL REPUBLICAN RESULTS - 05/26/2026 9:31 PM', scan CreationDate 2026-05-26T20:47:22-06:00 = 9:47 PM CDT); Democratic version scanned 20:46:35-06:00. The posted unofficial summary is a later update (footer 'Election Summary - 06/02/2026 8:34 AM'). " + MIG + "END by rule 47."}},
 rationale=NO_CLARITY + NO_WB + "All three elections have an unofficial precinct-by-precinct report printed on election night; the site's Last-Modified is a site-wide August 2026 re-upload, read as no upload time. Rule gives PRECINCT_END_OF_NIGHT, med (check 2). If the August 2026 Last-Modified were instead read as a known later upload (rule 47 example), all three would fall to LATER under the rule 43 reading (county-totals summaries printed on election night for 2024 and the primary; runoff would be UNDETERMINED since its posted summary is dated 06/02), giving COUNTY_ONLY_PRECINCT_AT_CANVASS.",
 sources=[
  (hb + "/county-information/election-information/election-information-and-results/", "Lists unofficial summary and precinct-by-precinct reports for all three elections"),
  (hb + "/county-information/election-information/previous-election-results/", "Older files; their Last-Modified also Aug 2026 (migration)"),
  (hb + "/media/q2zdxmw0/2024-general-precint-by-precinct-unofficial-results.pdf", "Precinct Summary 11/05/2024 9:55 PM; CreationDate 2024-11-05T22:01:17-06:00; LM 2026-08-12"),
  (hb + "/media/ston3ymd/2024-general-unofficial-results.pdf", "Election Summary 11/05/2024 9:53 PM"),
  (hb + "/media/uk0je5o1/precinct-by-precinct-republican.pdf", "Primary precinct report 03/03/2026 10:08 PM; LM 2026-08-10"),
  (hb + "/media/uvxa0mxp/precinct-by-precinct-democrat.pdf", "Primary precinct report 03/03/2026 10:11 PM"),
  (hb + "/media/twsjt1tb/unofficial-summary-republican.pdf", "Primary summary 10:13 PM"),
  (hb + "/media/1p3coyq3/precinct-by-precinct-republican.pdf", "Runoff precinct report 05/26/2026 9:31 PM; scan 20:47:22-06:00"),
  (hb + "/media/h4eaghqa/unofficial-results-republican.pdf", "Runoff summary dated 06/02/2026 8:34 AM"),
  (hb + "/media/kjwnc4zv/2024-march-republican-official-results.pdf", "March 2024 file with LM 12 Aug 2026 (shows migration)"),
 ])
# ---------------- Zapata
zb = "https://www.co.zapata.tx.us/upload/page/6434/docs/"
C["Zapata"] = dict(
 elections={
  "2024_general": {"result": "LATER", "check": "2",
   "fact": "zapata.Elections 'Elections Results Archive' lists only 'November 5, 2024 General & ZCISD Election (unofficial)' for Nov 2024 (newtools.cira.state.tx.us copy): a 7-page 'Cumulative Results Report' county totals, Run Time 10:55 PM, Run Date 11/05/2024, with Election Day Voting column; Last-Modified Wed, 06 Nov 2024 05:25:18 GMT (11:25 PM CST, election night). No precinct report for Nov 2024 is listed. LATER (county_totals_first_seen 2024-11-05 22:55 CT)."},
  "2026_primary": {"result": "LATER", "check": "2",
   "fact": "Home page 'UNOFFICIAL' links 'ZAPATA COUNTY UNOFFICIAL - MARCH 2026 - DEM/REP': 'Cumulative Results Report MARCH 3,2026 PRIMARY ELECTION', county totals, Run Time 10:15 PM, Run Date 03/03/2026 (both parties); Last-Modified Wed, 04 Mar 2026 20:42:37-38 GMT (2:42 PM CST Mar 4). No unofficial precinct report listed. LATER on the printed run time (county_totals_first_seen 2026-03-03 22:15 CT)."},
  "2026_runoff": {"result": "LATER", "check": "2",
   "fact": "Home page 'UNOFFICIAL' '2026 Primary Runoff Election - unofficial': 'Cumulative Results Report MAY 26, 2026 PRIMARY RUNOFF', county totals, Run Time 11:10:25 PM, Run Date 05/26/2026, Precincts Reporting 7 of 7; Last-Modified Thu, 28 May 2026 17:38:38 GMT. No unofficial precinct report listed (official cumulative and canvass report posted June 3). LATER on the printed run time (county_totals_first_seen 2026-05-26 23:10 CT)."}},
 rationale=NO_CLARITY + "Check 3: wayback-data CDX lookups for co.zapata.tx.us failed (robots_disallowed_or_unreachable), no captures. All three elections show county totals printed (2024 also uploaded) on election night and no unofficial precinct report: COUNTY_ONLY_PRECINCT_AT_CANVASS, med (check 2).",
 sources=[
  ("http://www.co.zapata.tx.us/", "Home page links unofficial and official 2026 primary and runoff results"),
  ("https://www.co.zapata.tx.us/page/zapata.Elections", "Elections Results Archive lists Nov 2024 unofficial results only"),
  ("https://newtools.cira.state.tx.us/upload/page/6427/docs/Results/November%205%202024%20General%20and%20ZCISD%20-%20unofficial%20results.pdf", "Cumulative county totals run 10:55 PM 11/05/2024; LM 2024-11-06 05:25:18 GMT"),
  (zb + "ZAPATA COUNTY UNOFFICIAL - MARCH 2026 - DEM.pdf", "Cumulative county totals run 10:15 PM 03/03/2026; LM 2026-03-04 20:42:38 GMT"),
  (zb + "ZAPATA COUNTY UNOFFICIAL - MARCH 2026 - REP.pdf", "Cumulative county totals run 10:15 PM 03/03/2026"),
  (zb + "2026 Primary Runoff Election - unofficial.pdf", "Cumulative county totals run 11:10:25 PM 05/26/2026; LM 2026-05-28 17:38:38 GMT"),
 ])
# ---------------- Dawson
db = "https://www.co.dawson.tx.us/upload/page/1590/"
C["Dawson"] = dict(
 elections={
  "2024_general": {"result": "LATER", "check": "2",
   "fact": "dawson.Election.Information, NOVEMBER 5, 2024: unlabeled 20241105202939.pdf = 'Cumulative Results Report' county totals, Run Time 7:09 PM 11/05/2024 (early and absentee only), Last-Modified Wed, 06 Nov 2024 01:25:56 GMT (7:25 PM CST, election night); 'UNOFFICIAL TOTALS' 20241105220214.pdf = cumulative county totals Run Time 8:32 PM with Election Day votes, Last-Modified 06 Nov 2024 19:38:25 GMT. The only precinct file is 'PRECINCT OFFICIAL TOTALS' (official); no unofficial precinct report posted. LATER (county_totals_first_seen 2024-11-05 19:25 CT upload)."},
  "2026_primary": {"result": "END", "check": "2",
   "fact": "MARCH 3, 2026: 'DEMOCRATIC UNOFFICIAL PRECINCT RESULTS' (PRECINCT RESULTS, Unofficial Results, Run Time 9:33 PM 03/03/2026, per-precinct candidate votes with Election Day Voting column) Last-Modified Wed, 04 Mar 2026 05:59:37 GMT (11:59 PM CST); 'REPUBLICAN UNOFFICIAL PRECINCT RESULTS' (Run Time 10:56 PM) Last-Modified 06:02:36 GMT (12:02 AM CST Mar 4). Matching cumulative reports run 9:38 PM and 10:57 PM, uploaded 11:58 PM and 12:00 AM. Final precinct numbers posted once per party in one posting session at midnight: END."},
  "2026_runoff": {"result": "END", "check": "2",
   "fact": "MAY 26, 2026: 'REPUBLICAN UNOFFICIAL PRECINCT RESULTS' (20260526215018.pdf, scan of 'PRECINCT RESULTS REPORT', Unofficial Results, Run Time 9:35 PM 05/26/2026, precinct 1 Election Day votes e.g. Paxton 25) Last-Modified Wed, 27 May 2026 02:54:14 GMT (9:54 PM CDT); 'DEMOCRATIC UNOFFICIAL PRECINCT RESULTS' (20260526214924.pdf) Last-Modified 02:51:37 GMT (9:51 PM CDT). Cumulative county totals run 9:39 PM uploaded 9:49 PM. END."}},
 rationale=NO_CLARITY + NO_WB + "Primary and runoff are END by check 2 (unofficial precinct reports uploaded on election night); 2024 general is LATER. Rule gives PRECINCT_END_OF_NIGHT, med.",
 sources=[
  ("https://www.co.dawson.tx.us/page/dawson.Election.Information", "Results lists for all three elections"),
  (db + "2024/20241105202939.pdf", "Cumulative county totals run 7:09 PM; LM 2024-11-06 01:25:56 GMT"),
  (db + "2024/20241105220214.pdf", "Unofficial totals run 8:32 PM; LM 2024-11-06 19:38:25 GMT"),
  (db + "2026/DEMOCRATIC PRECINCT UNOFFICIAL.pdf", "Precinct report run 9:33 PM; LM 2026-03-04 05:59:37 GMT"),
  (db + "2026/REPUBLICAN PRECINCT UNOFFICIAL.pdf", "Precinct report run 10:56 PM; LM 2026-03-04 06:02:36 GMT"),
  (db + "2026/DEMOCRATIC CUMULATIVE UNOFFICIAL.pdf", "Cumulative run 9:38 PM; LM 2026-03-04 05:58:37 GMT"),
  (db + "2026/20260526215018.pdf", "Runoff Rep precinct report run 9:35 PM; LM 2026-05-27 02:54:14 GMT"),
  (db + "2026/20260526214924.pdf", "Runoff Dem precinct report; LM 2026-05-27 02:51:37 GMT"),
  (db + "2026/20260526215149.pdf", "Runoff cumulative run 9:39 PM; LM 2026-05-27 02:49:45 GMT"),
 ])

for county, d in C.items():
    rec = {"county": county, "elections": d["elections"]}
    tag, single = compute_tag(d["elections"])
    conf = compute_confidence(rec)
    fn = county.replace(" ", "_")
    out = {"county": county, "reason_selected": REASON, "verifier_tag": tag, "verifier_confidence": conf,
           "elections": d["elections"], "rationale": d["rationale"],
           "sources": [{"url": u, "content_hash": h(u), "what_i_checked": w} for u, w in d["sources"]],
           "written_blind_at_utc": NOW}
    try:
        prev = json.load(open(f"phase1/scratch/verifier-14/prev_{fn}.json"))
        out["previous_verification"] = prev
    except FileNotFoundError:
        pass
    s = json.dumps(out, indent=2, ensure_ascii=False)
    assert not re.search("[–—]", s), county
    open(f"phase1/verification/{fn}.json", "w").write(s + "\n")
    print(county, tag, conf, [ (e, d["elections"][e]["result"]) for e in d["elections"]], [x["content_hash"][:8] for x in out["sources"]])
