import json, os, sys, datetime
sys.path.insert(0,'.'); sys.path.insert(0,'phase1/scratch/verifier-15')
from h import h
from phase1.schema import compute_confidence, compute_tag
NOW=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
REASON="tag changed in targeted pass 3"
def src(u, what, wb=None):
    if wb: return {"url": u, "content_hash": wb, "what_i_checked": what}
    return {"url": u, "content_hash": h(u)[0], "what_i_checked": what}
DC="https://www.bosquecounty.gov/DocumentCenter/View/"
PW="https://parmercounty.texas.gov/wp-content/uploads/"
PM="https://parmercounty.texas.gov/index.php?rest_route=/wp/v2/media&"
HK="https://newtools.cira.state.tx.us/upload/page/7706/"
def q(s):
    import urllib.parse; return urllib.parse.quote(s)
recs={}
recs["Bosque"]={
 "elections":{
  "2024_general":{"result":"END","check":"2","fact":"Check 3 (wayback-data Bosque/2024_general_20241106052529_5ddaaf66ae2e.html, captured 2024-11-05 23:25:29 CST, and _20241106081609 at 02:16 CST) shows the county's old WordPress elections page (bosquecounty.us/elections/) linking \"Unofficial Reconciliation 11.5.24\", \"Unofficial Grand Totals\", one file per precinct (\"Pct 1 Iredell\" through \"Pct 11 Cayote\", wp-content/uploads/2024/11/) and \"Early Voting and Ballot by Mail\"; same 11 precinct links in both captures. The original WordPress files now 404; the same titles are on the CivicPlus page /199 (DocumentCenter 578 to 590, no Last-Modified, so no upload time). Pct 1 Iredell (View/587, scanned, read visually): \"Summary Results Report 2024 General Election ... UNOFFICIAL RESULTS PCT 1 IREDELL\", columns Absentee, Early Voting, Election Day (Trump/Vance 534 total, 219 Election Day), footer \"Precinct Summary - 11/05/2024 8:53 PM\"; PDF CreationDate 2024-11-06 03:13:41 UTC (9:13 PM CST). The 11 precinct scans were created 8:46 to 9:17 PM CST, grand totals 9:49 PM, reconciliation 10:51 PM. Printed run time on election night and no upload time (rule 47), corroborated by the election-night page captures; one set of precinct files, so END."},
  "2026_primary":{"result":"END","check":"2","fact":"Page /286 (CivicPlus, DocumentCenter sends no Last-Modified) tab \"UNOFFICIAL RESULTS\" lists \"Grand Totals Unofficial Results\" (View/2239), \"Early Voting Unofficial Results 03.03.2026\" (2226) and \"Pct. 1 Iredell Unofficial Results\" through \"Pct. 11 Cayote Unofficial Results\" (2227 to 2238). Pct 1 (View/2235, scanned, read visually): \"Precinct Summary Results Report 2026 Primary Election ... UNOFFICIAL RESULTS IREDELL PCT 1\", Election Day column (Ballots Cast 259, 159 Election Day; Paxton 117 total, 67 Election Day), footer \"Precinct Summary - 03/03/2026 9:32 PM\", CreationDate 2026-03-04 03:44:05 UTC (9:44 PM CST). Other precinct scans 8:46 PM (Pct 10) and 9:03 PM (Pct 3); grand totals printed \"Election Summary - 03/03/2026 10:21 PM\" (11 of 11 Election Day precincts reporting). Printed run time on election night, no upload time (rule 47). Wayback: CDX ok, no captures."},
  "2026_runoff":{"result":"END","check":"2","fact":"Page /290 lists \"Unofficial Grand Totals 05.26.26\" (View/2514), \"Early Voting Unofficial Results 05.26.26\" (2513), \"Unofficial Precinct Totals 05.26.26\" (2515), \"Preliminary Election Reconciliation - Unofficial Totals 05.26.26\" (2516). View/2515 (scanned, 8 pages, read visually): \"Precinct Summary Results Report 2026 Primary Runoff Election ... UNOFFICIAL RESULTS PRECINCT 1 - MERIDIAN (3)\", Election Day column (Paxton 282 total, 143 Election Day), footer \"Precinct Summary - 05/26/2026 8:34 PM\"; CreationDate 2026-05-27 02:11:38 UTC (9:11 PM CDT). No upload time (CivicPlus). Printed run time on election night (rule 47). Wayback: CDX ok, no captures."}},
 "rationale":"All three elections show unofficial per-precinct reports with Election Day votes printed on election night (8:53 PM, 9:32 PM, 8:34 PM) on a host with no upload times; for 2024 the county's elections page was also captured at 11:25 PM election night already linking every precinct file. Three END results give PRECINCT_END_OF_NIGHT; all rest on check 2 printed times, so confidence med.",
 "sources":[
  src("https://web.archive.org/web/20241106052529id_/https://www.bosquecounty.us/elections/?os=vbkn4ztqhoorjmxr5bP0w2IDHZ&ref=app","wayback-data branch saved file Bosque/2024_general_20241106052529_5ddaaf66ae2e.html (11:25 PM CST Nov 5 2024): links to Unofficial Grand Totals, Unofficial Reconciliation and 11 per-precinct PDFs","5ddaaf66ae2ebb016b742ac38a9f462c692bf9f1bee0d7c81025a54ba30266d7"),
  src("https://web.archive.org/web/20241106081609id_/https://www.bosquecounty.us/elections/?os=wtmb5utkcxk5refappahtvjlve","wayback-data saved file Bosque/2024_general_20241106081609_f4348cd22bd7.html (2:16 AM CST Nov 6): same 11 precinct links","f4348cd22bd76f22eac9ad21bc090ce82139083797cf4d84d2410c18552896ce"),
  src("https://www.bosquecounty.gov/199/2024-November-5-General-Election","current page: unofficial precinct files (DocumentCenter 578 to 590) and official files"),
  src(DC+"587/Pct-1-Iredell-PDF","rendered page 1: UNOFFICIAL RESULTS PCT 1 IREDELL, Election Day column, printed 11/05/2024 8:53 PM; CreationDate 03:13:41 UTC Nov 6; no Last-Modified"),
  src(DC+"589/Unofficial-Grand-Totals-PDF","CreationDate 2024-11-06 03:49:07 UTC (9:49 PM CST)"),
  src(DC+"577/Early-Voting-and-Ballot-by-Mail-PDF","CreationDate 2024-11-06 01:27:37 UTC (7:27 PM CST)"),
  src(DC+"590/Unofficial-Reconciliation-11524-PDF","CreationDate 2024-11-06 04:51:26 UTC"),
  src("https://www.bosquecounty.gov/286/2026-March-3rd-Primary-Election","UNOFFICIAL RESULTS tab: grand totals, early voting, 11 precinct files"),
  src(DC+"2235","rendered page 1: Pct 1 Iredell unofficial, Election Day column, printed 03/03/2026 9:32 PM; CreationDate 03:44:05 UTC Mar 4"),
  src(DC+"2239","rendered page 1: Election Summary unofficial, printed 03/03/2026 10:21 PM; CreationDate 05:28:37 UTC Mar 4"),
  src(DC+"2227","CreationDate 2026-03-04 02:46:21 UTC (Pct 10)"),
  src("https://www.bosquecounty.gov/290/2026-May-26th-Primary-Runoff","runoff page: Unofficial Precinct Totals 05.26.26 and others"),
  src(DC+"2515","rendered pages 1 and 2: unofficial precinct summary with Election Day column, printed 05/26/2026 8:34 PM; CreationDate 02:11:38 UTC May 27"),
  src(DC+"2514","CreationDate 2026-05-27 02:11:22 UTC (grand totals)"),
  src("https://results.enr.clarityelections.com/TX/Bosque/elections.json","check 1 script: no Clarity election list (404); output phase1/verification/clarity/Bosque.json","")]}
recs["Parmer"]={
 "elections":{
  "2024_general":{"result":"LATER","check":"2","fact":"Elections page (parmercounty.texas.gov/?page_id=334) links \"Election Night Results\" to results.texas-election.com and the county's \"Nov 5, 2024 General Election\" official results. WordPress media list (index.php?rest_route=/wp/v2/media, after/before around election night) shows \"Unofficial Results General Election Nov. 5, 2024\" uploaded 2024-11-06T03:43:44 GMT (9:43 PM CST, Last-Modified the same) and \"Unofficial Election Reconciliation Nov. 5, 2024\" at 03:48:10 GMT. The results file (scanned, read visually) is county totals only: \"Summary Results Report ... UNOFFICIAL RESULTS Total Ballots 11-5-2024\", \"Precincts Reporting 7 of 7\", footer \"Election Summary - 11/05/2024 9:27 PM\". No other unofficial file in the media list for Nov 5 to 7. Precinct numbers first appear in \"11524-General-Election-Official-Results.pdf\" (35 pages, \"Precinct Summary - 11/13/2024 10:02 AM\"), uploaded 2025-01-29. County totals on election night, precinct numbers only after (rule 43)."},
  "2026_primary":{"result":"LATER","check":"2","fact":"Media list: \"Unoffical 3-3-2026 Primary\" (wp-content/uploads/2026/03/Unoffical-3-3-2026-Primary.pdf) uploaded 2026-03-04T03:58:19 GMT (9:58 PM CST, Last-Modified the same); 21 pages: preliminary reconciliation plus a 20-page \"Summary Results Report ... Primary 2026 UNOFFICIAL RESULTS\", county totals with Absentee, Early Voting, Election Day columns, footer \"Election Summary - 03/03/2026 9:13 PM\" on every page, no precinct pages. Next morning an SOS-format Democratic unofficial report (county totals) at 15:52 GMT Mar 4. No precinct report in the media list for Mar 3 to Mar 31; precinct numbers only with the official results uploaded 2026-03-19. County totals on election night, no election-night precinct report (rule 43)."},
  "2026_runoff":{"result":"END","check":"2","fact":"Media list: \"Unoffical Results Runoff 5-26-26\" uploaded 2026-05-27T02:08:35 GMT (9:08 PM CDT, Last-Modified the same), then identical copies (-1, -2, -3, same content hash 4b1771b9...) at 02:18, 02:51 GMT and 12:26 GMT next morning. The 25-page file (scanned, read visually) contains the reconciliation, two Election Summary reports (printed 7:47 PM and 7:57 PM, 7 of 7 Election Day precincts) and a 16-page \"UNOFFICIAL PRECINCT RESULTS 2026 RUNOFF\" Precinct Summary, precinct 101: Ballots Cast 133, 108 Election Day; Paxton 73 (59 Election Day), footer \"Precinct Summary - 05/26/2026 7:53 PM\". Upload time on election night (rule 47); same content in every copy, so one set of precinct numbers: END."}},
 "rationale":"2024 general and 2026 primary: county-totals unofficial files uploaded on election night (9:43 PM, 9:58 PM per WordPress upload dates and Last-Modified), no precinct report that night, precinct numbers only in official results weeks later: LATER. 2026 runoff: precinct summary uploaded 9:08 PM election night: END. Two LATER give COUNTY_ONLY_PRECINCT_AT_CANVASS; both deciding elections are check 2, so med.",
 "sources":[
  src("https://parmercounty.texas.gov/?page_id=334","elections page: Election Night Results link to SOS; official results links per election"),
  src(PM+"after=2024-11-05T12:00:00&before=2024-11-07T12:00:00&per_page=100","media upload dates around Nov 5 2024 election night"),
  src(PW+"2024/11/Unofficial-Results-General-Election-Nov.-5-2024.pdf","county totals only, printed 11/05/2024 9:27 PM, Last-Modified 06 Nov 2024 03:43:44 GMT"),
  src(PW+"2024/11/Unofficial-Election-Reconciliation-Nov.-5-2024.pdf","reconciliation, uploaded 03:48 GMT Nov 6"),
  src("https://parmercounty.texas.gov/index.php?rest_route=/wp/v2/media&after=2024-11-07T12:00:00&before=2025-01-31T00:00:00&per_page=100","only result file after election night is the official results on 2025-01-29"),
  src(PW+"2025/01/11524-General-Election-Official-Results.pdf","35 pages, Precinct Summary printed 11/13/2024 10:02 AM"),
  src(PM+"after=2026-03-03T12:00:00&before=2026-03-05T12:00:00&per_page=100","media upload dates around Mar 3 2026 election night"),
  src(PW+"2026/03/Unoffical-3-3-2026-Primary.pdf","21 pages, county totals Election Summary printed 03/03/2026 9:13 PM, Last-Modified 04 Mar 2026 03:58:19 GMT"),
  src(PW+"2026/03/ELECTION-UNOFFICIAL-RESULT-REPORT_Democrat-2.pdf","SOS-format Democratic county totals, uploaded 15:52 GMT Mar 4"),
  src("https://parmercounty.texas.gov/index.php?rest_route=/wp/v2/media&after=2026-03-05T12:00:00&before=2026-04-01T00:00:00&per_page=100","no unofficial precinct report; official results 2026-03-19"),
  src(PM+"after=2026-05-26T12:00:00&before=2026-05-28T12:00:00&per_page=100","media upload dates around May 26 2026 election night"),
  src(PW+"2026/05/Unoffical-Results-Runoff-5-26-26.pdf","25 pages incl. 16-page unofficial precinct summary printed 05/26/2026 7:53 PM with Election Day column; Last-Modified 27 May 2026 02:08:35 GMT"),
  src("https://results.enr.clarityelections.com/TX/Parmer/elections.json","check 1 script: no Clarity election list (404)","")]}
recs["Haskell"]={
 "elections":{
  "2024_general":{"result":"UNDETERMINED","check":"none","fact":"Elections page (haskellcountytx.gov/page/haskell.Elections, also newtools.cira.state.tx.us, original Last-Modified kept) lists for Nov 2024 only \"NOVEMBER 5TH 2024 PRECINCT BY PRECINCT ELECTION RESULTS\" (precinct by precinct for nov 2024 election.pdf, scanned 2025-07-08, Last-Modified 05 Feb 2026). No unofficial or election-night file for 2024 survives; County Clerk page has none. Wayback: CDX ok, no captures. Not on Clarity (404)."},
  "2026_primary":{"result":"LATER","check":"2","fact":"\"MARCH 3, 2026 DEMOCRATIC UNOFFICIAL RESULTS\" (ELECTION-UNOFFICIAL-RESULT-REPORT DEMOCRATIC 3.3.26.pdf): \"Texas Secretary of State Election Unofficial Results Report 2026 DEMOCRATIC PRIMARY ELECTION ... HASKELL County\", county totals with Election Day Count column; CreationDate 2026-03-04 05:00:07 UTC, Last-Modified Wed, 04 Mar 2026 05:16:53 GMT (11:16 PM CST, election night). Republican unofficial report (county totals, created 06:06 UTC = 12:06 AM CST) Last-Modified 13:54:56 GMT Mar 4 (7:54 AM, after election night). Precinct reports \"REPBUBLICAN PRECINCT BY PRECINCT 3.3.26\" and \"DEOMOCRATIC PRECINCT BY PRECINCT 3.3.26\" Last-Modified 01 Apr 2026 (scanned Apr 1). County totals on election night, precinct numbers only after (rule 43)."},
  "2026_runoff":{"result":"LATER","check":"2","fact":"\"MAY 26, 2026 REPUBLICAN UNOFFICIAL RESULTS\" (SOS Election Unofficial Results Report, county totals with Election Day Count, scanned) Last-Modified Wed, 27 May 2026 01:33:23 GMT (8:33 PM CDT); \"MAY 26, 2026 DEMOCRATIC UNOFFICIAL RESULTS\" Last-Modified 00:58:27 GMT (7:58 PM CDT). \"PRIMARY RUNOFF RESULTS FOR PRECINCT BY PRECINCT/ REP AND DEM\" (PCT 1 to PCT 10 by EV, ED, BBM) Last-Modified 29 Jun 2026 15:04:45 GMT, scanned Jun 29. Canvass report Last-Modified 10 Jun 2026. County totals on election night, precinct numbers only after (rule 43). Scanner CreationDates run about 48 minutes after the uploads (scanner clock offset), so Last-Modified is used."}},
 "rationale":"Primary and runoff: SOS-format county-totals unofficial reports uploaded on election night (11:16 PM Mar 3; 7:58 and 8:33 PM May 26) on the CIRA host that keeps original Last-Modified times; precinct-by-precinct reports uploaded Apr 1 and Jun 29. 2024 has no surviving election-night file (UNDETERMINED). Two LATER give COUNTY_ONLY_PRECINCT_AT_CANVASS, med (check 2).",
 "sources":[
  src("https://newtools.cira.state.tx.us/page/haskell.Elections","elections page (same content hash as haskellcountytx.gov): result file list"),
  src(HK+q("precinct by precinct for nov 2024 election.pdf"),"Nov 2024 precinct by precinct, Last-Modified 05 Feb 2026, CreationDate 2025-07-08"),
  src(HK+q("ELECTION-UNOFFICIAL-RESULT-REPORT DEMOCRATIC 3.3.26.pdf"),"SOS county totals, Last-Modified 04 Mar 2026 05:16:53 GMT"),
  src(HK+q("ELECTION-UNOFFICIAL-RESULT-REPORT_52585_1772604388995.pdf"),"SOS Republican county totals, created 06:06 UTC, Last-Modified 04 Mar 2026 13:54:56 GMT"),
  src(HK+q("REPUBLICAN PRECINCT BY PRECINCT 3.3.26.pdf"),"Last-Modified 01 Apr 2026 20:44:30 GMT"),
  src(HK+q("DEMOCRATIC PRECINCT BY PRECINCT 3.3.26.pdf"),"Last-Modified 01 Apr 2026 20:43:36 GMT"),
  src(HK+q("REPUBLICAN UNOFFICIAL RESULTS 5.26.26.pdf"),"rendered: SOS county totals; Last-Modified 27 May 2026 01:33:23 GMT"),
  src(HK+q("UNOFFICIAL DEMOCRATIC RUNOFF RESULTS 5.26.26.pdf"),"rendered: SOS county totals; Last-Modified 27 May 2026 00:58:27 GMT"),
  src(HK+q("PRIMARY RUNOFF PCT BY PCT.pdf"),"rendered page 1: PCT 1 to PCT 10 by EV, ED, BBM; Last-Modified 29 Jun 2026 15:04:45 GMT"),
  src(HK+q("CANVASS REPORT FOR 5.26.2026 PRIMARY RUNOFF ELECTION.pdf"),"Last-Modified 10 Jun 2026"),
  src("https://newtools.cira.state.tx.us/page/haskell.County.Clerk","no election results"),
  src("https://results.enr.clarityelections.com/TX/Haskell/elections.json","check 1 script: no Clarity election list (404)","")]}
for c,r in recs.items():
    tag,single=compute_tag(r["elections"])
    rec={"county":c,"reason_selected":REASON,"verifier_tag":tag,"verifier_confidence":None,"elections":r["elections"],"rationale":r["rationale"],"sources":r["sources"],"written_blind_at_utc":NOW,"verifier_agent":"verifier-15"}
    rec["verifier_confidence"]=compute_confidence({"county":c,"elections":r["elections"]})
    p=f"phase1/verification/{c}.json"
    if os.path.exists(p):
        old=json.load(open(p))
        rec["previous_verification"]=old
    for s in rec["sources"]:
        if s["content_hash"] is None: print("MISSING HASH",s["url"])
    txt=json.dumps(rec,indent=1,ensure_ascii=False)
    assert not any(ch in txt for ch in "–—"), c
    open(p,"w").write(txt+"\n")
    print(c,tag,rec["verifier_confidence"],"prev" if "previous_verification" in rec else "")
