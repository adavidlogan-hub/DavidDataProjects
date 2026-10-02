import json, sys
sys.path.insert(0, '.')
from phase1.schema import compute_tag, compute_confidence, validate_v2
AG = "targeted3-I"
NT = "https://newtools.cira.state.tx.us"

def load(c):
    return json.load(open(f"phase1/evidence/{c}.json"))

def save(c, d):
    tag, _ = compute_tag(d["elections"])
    d["tag"] = tag
    d["confidence"] = compute_confidence(d)
    validate_v2(d)
    s = json.dumps(d, indent=2, ensure_ascii=False)
    for ch in ("—", "–"):
        assert ch not in s, (c, ch)
    open(f"phase1/evidence/{c}.json", "w").write(s + "\n")
    print(c, d["tag"], d["confidence"])

def note(d, text):
    d["notes"] = (d["notes"] + " " if d["notes"] else "") + f"Targeted pass 3 2026-10-02 ({AG}): " + text

# ---------------- Jasper ----------------
d = load("Jasper")
e = d["elections"]["2024_general"]
e.update({
    "result": "LATER", "check": "2",
    "county_totals_first_seen": "2024-11-06 00:26 CT (printed run time; server upload 2024-11-06 08:07 CT)",
    "precinct_first_seen": "2024-11-07 10:28 CT (server upload of the unofficial precinct report; printed 2024-11-06 00:32)",
    "night_updates_with_precinct_numbers": "0",
    "evidence_url": NT + "/upload/page/1130/UNOFFICIAL%20SUMMARY%20RESULTS.pdf",
    "fact": "Files on the county's CIRA upload folder (page 1130, the folder behind newtools.cira.state.tx.us/page/jasper.Elections; no longer linked from the page, located by web search): 'UNOFFICIAL SUMMARY RESULTS.pdf' = scanned Electionware 'Summary Results Report UNOFFICIAL RESULTS JASPER COUNTY GENERAL ELECTION November 5, 2024 ... Election Day Precincts Reporting 23 of 23 ... Ballots Cast - Total 20,134', county totals only, footer 'Election Summary - 11/06/2024 12:26 AM' (election night), Last-Modified Wed, 06 Nov 2024 14:07:14 GMT (08:07 AM CST Nov 6). '11-5-24 Unofficial Pct by Pct Results.pdf' = 'Summary Results Report UNOFFICIAL RESULTS General Election November 5, 2024 Jasper County Pct # 1 Three Corners ... REP Donald J. Trump/JD Vance 42 3 6 33' (per precinct with Election Day column), footer 'Precinct Summary - 11/06/2024 12:32 AM', Last-Modified Thu, 07 Nov 2024 16:28:15 GMT (10:28 AM CST Nov 7), after election night, so under rule 47 it cannot show election-night publication. Rule 43: county-totals file with an election-night printed run time and no precinct numbers shown published that night gives LATER. Caveat: the summary itself was uploaded the next morning; LATER rests on its printed run time as rule 43 allows.",
})
d["sources"] += [
    {"url": NT + "/page/jasper.Elections", "via": "fetch_module", "content_hash": "e057414290ff83c68e96b982b42db6b15d4724882dd7655336a5d4d574e69124",
     "quote": "Unofficial Totals; Official PCT by PCT Results; Official Summary Results (no 2024 general results linked)", "supports": "The CIRA copy of the Elections page lists the same 2026 files as www.co.jasper.tx.us; 2024 files are no longer linked"},
    {"url": NT + "/upload/page/1130/UNOFFICIAL%20SUMMARY%20RESULTS.pdf", "via": "fetch_module", "content_hash": "73db33256f3c3d1661b910e50824182ccd016646e02911d8088bfde66a3d05dc",
     "quote": "Summary Results Report UNOFFICIAL RESULTS JASPER COUNTY GENERAL ELECTION November 5, 2024 ... Election Day Precincts Reporting 23 of 23 ... Election Summary - 11/06/2024 12:26 AM", "supports": "2024_general county totals printed on election night; Last-Modified Wed, 06 Nov 2024 14:07:14 GMT"},
    {"url": NT + "/upload/page/1130/11-5-24%20Unofficial%20Pct%20by%20Pct%20Results.pdf", "via": "fetch_module", "content_hash": "6479e86404bb7f7348e7e12242c3e46051bf6e394dae3bfc26042648c8a2861b",
     "quote": "Summary Results Report UNOFFICIAL RESULTS General Election November 5, 2024 Jasper County Pct # 1 Three Corners ... Precinct Summary - 11/06/2024 12:32 AM", "supports": "2024_general precinct report uploaded Thu, 07 Nov 2024 16:28:15 GMT, after election night (rule 47)"},
    {"url": NT + "/upload/page/1130/11-5-24%20Preliminary%20Reconciliation.pdf", "via": "fetch_module", "content_hash": "51d7d34ba470bc7f2016405feb401aeed4c143002ec090d0693a310d72e7e748",
     "quote": "(preliminary reconciliation form, not opened for content)", "supports": "Last-Modified Wed, 06 Nov 2024 19:09:06 GMT; also after election night"},
    {"url": NT + "/upload/page/1130/11-5-24%20Official%20Pct%20by%20Pct%20Results.pdf", "via": "fetch_module", "content_hash": "d148c3f0685c4f76d5470daf51e7435122ead787101e1dbe450002c5341df5c1",
     "quote": "Pct By Pct Results Report General Election November 5, 2024 Pct # 1 Three Corners ... OFFICIAL RESULTS Jasper County", "supports": "Official 2024 precinct report, Last-Modified Mon, 18 Nov 2024 17:15:48 GMT"},
    {"url": "websearch:?q=newtools.cira.state.tx.us upload page 1130 unofficial results jasper county 2024 general election", "via": "websearch", "content_hash": "57a5eb3b0f60a8d879db3dfd7ab1349d768bf5321666cfa70fa9bf1e106753fc",
     "quote": "11 5 24 Unofficial Pct by Pct Results; UNOFFICIAL SUMMARY RESULTS (links only)", "supports": "Located the unlinked 2024 files (search used for locating only)"},
]
d["evidence_url"] = NT + "/upload/page/1130/UNOFFICIAL%20SUMMARY%20RESULTS.pdf"
d["tag_rationale"] = "Only the 2024 general is determined (LATER, check 2: county totals printed 12:26 AM on election night, precinct report uploaded Nov 7); the 2026 primary and runoff stay UNDETERMINED. Exactly one election is determined, so the tag is COUNTY_ONLY_PRECINCT_AT_CANVASS with low confidence."
note(d, "2024_general UNDETERMINED to LATER (check 2). The county's CIRA upload folder (page 1130, found by web search; files no longer linked) still holds 'UNOFFICIAL SUMMARY RESULTS.pdf' (county totals, printed 11/06/2024 12:26 AM, uploaded 08:07 AM Nov 6) and '11-5-24 Unofficial Pct by Pct Results.pdf' (printed 12:32 AM, uploaded 10:28 AM Nov 7). 2026 primary and runoff: no new files (summary printed 03/04/2026 8:31 AM; runoff only official files). Wayback harvest for co.jasper.tx.us was robots-blocked or unreachable; no sweep file; KJAS search found nothing for check 4.")
save("Jasper", d)

# ---------------- Colorado ----------------
d = load("Colorado")
e = d["elections"]["2024_general"]
e["fact"] = ("Page lists only 'Official Results (PDF)' (11-05-24/Official Results.pdf: Election Reconciliation - Official Totals and results, CreationDate 2024-11-18, Last-Modified Nov 19 2024). An unlinked file at the same folder, 11-05-24/Unofficial Results.pdf (requested by the site's own naming pattern used for 26-03-03 and 11-4-25), is an 87-page scan with 'Summary Results Report UNOFFICIAL RESULTS ... Election Summary - 11/05/2024 10:09 PM' and per-precinct pages 'Precinct Summary - 11/05/2024 10:10 PM' with Absentee, Early Voting and Election Day columns; XMP CreateDate 2024-11-05T21:32-06:00, but Last-Modified Wed, 06 Nov 2024 13:11:16 GMT (07:11 AM CST Nov 6), after election night. Rule 47: the known upload time is after election night, so END cannot be shown; county totals and precinct pages are in the same file, so LATER does not apply either. UNDETERMINED. Wayback harvest found no election-night captures for 2024.")
d["sources"] += [
    {"url": "https://www.co.colorado.tx.us/upload/page/6210/11-05-24/Unofficial%20Results.pdf", "via": "fetch_module", "content_hash": "042539cad41e235221e1feb6ec3ca5f425e1e8f6ec42a25054b47d7d349b3e34",
     "quote": "Summary Results Report UNOFFICIAL RESULTS TX Colorado County 241105 General 6110 November 5, 2024 ... Precinct Summary - 11/05/2024 10:10 PM", "supports": "2024 unofficial file with precinct pages printed on election night but uploaded Wed, 06 Nov 2024 13:11:16 GMT (rule 47: UNDETERMINED)"},
    {"url": "https://www.co.colorado.tx.us/upload/page/6210/11-05-24/Official%20Results.pdf", "via": "fetch_module", "content_hash": "542c310b8acc1169427cae61f346a438edd54d3754424a1ddb10137dfc33bc68",
     "quote": "Election Reconciliation - Official Totals ... Election Date November 05, 2024", "supports": "Only linked 2024 file is official, created 2024-11-18"},
]
note(d, "2024_general stays UNDETERMINED. Found unlinked 11-05-24/Unofficial Results.pdf (summary printed 10:09 PM and precinct pages printed 10:10 PM on Nov 5, 2024) but its Last-Modified is 07:11 AM CST Nov 6, after election night, and it holds precinct pages, so neither END (rule 47) nor LATER applies. Wayback 2024 window had no captures; 2026 primary CDX timed out in the harvest; runoff capture is only the Notice of Election. Web search for Colorado County Citizen precinct results found nothing. No sweep file.")
save("Colorado", d)

# ---------------- Brooks ----------------
d = load("Brooks")
d["sources"] += [
    {"url": "https://www.co.brooks.tx.us/upload/page/5156/November%20General%20Cumulative%20Results%2011052024.pdf", "via": "fetch_module", "content_hash": "78064e29525d6470c9e4746badd875b87b98f126c7db35001fc5a59412f0ee40",
     "quote": "(8-page RICOH scan; CreationDate Wed Nov 6 15:10:49 2024 UTC)", "supports": "2024 county totals file uploaded Wed, 06 Nov 2024 15:43:14 GMT, after election night; no election-night time"},
    {"url": "https://newtools.cira.state.tx.us/upload/page/5156/Preliminary%20Election%20Reconciliation-%20Unofficial%20Totals%2011052024.pdf", "via": "fetch_module", "content_hash": "4586a0ed528e933cd5d30723144a6e3421bfe84ce9d645e89149b17cbda75f7b",
     "quote": "Preliminary Election Reconciliation- Unofficial Totals 11052024.pdf (link title)", "supports": "Last-Modified Thu, 14 Nov 2024 22:33:36 GMT; not election night"},
]
note(d, "2024_general stays UNDETERMINED: 'November General Cumulative Results 11052024.pdf' is a scan created 09:10 AM CST Nov 6 and uploaded 09:43 AM CST Nov 6; the preliminary reconciliation was uploaded Nov 14. No file for 2024 has an election-night printed or upload time. Wayback harvest had no captures in any window; no sweep file; no check 4 source found.")
save("Brooks", d)

# ---------------- Nolan ----------------
d = load("Nolan")
d["sources"] += [
    {"url": "https://www.co.nolan.tx.us/upload/page/0503/Prelim%2005262026.pdf", "via": "fetch_module", "content_hash": "fda542cd41cd7d41afe5b826687193c730c0a10bc5bb27a260cba66aa8ba4acb",
     "quote": "Preliminary Election Reconciliation - Unofficial Totals (link title; one-page scan)", "supports": "Runoff preliminary reconciliation uploaded Wed, 27 May 2026 01:50:49 GMT (8:50 PM CDT election night); a ballot reconciliation form, not candidate county totals, so it does not satisfy rule 43"},
    {"url": "https://www.co.nolan.tx.us/upload/page/0503/NC%20Official%20Precinct%20Summary%20Results%2005262026.pdf", "via": "fetch_module", "content_hash": "847052dd58628bfe8b8775870b8bd1a61bb36f5a76075789c75e548fe190dd8e",
     "quote": "PRECINCT SUMMARY RESULTS (link title; 18-page scan created Jun 5 2026)", "supports": "Runoff precinct file uploaded Fri, 05 Jun 2026 16:08:44 GMT"},
    {"url": "https://www.co.nolan.tx.us/upload/page/0503/NC%20Official%20Summary%20Results%2005262026.pdf", "via": "fetch_module", "content_hash": "9ced6e9531961a1c34a8430f039b4f9d9802b66c6e7de458956fd4590ab478c3",
     "quote": "ELECTION SUMMARY RESULTS (link title; 3-page scan created Jun 5 2026)", "supports": "Runoff summary uploaded Fri, 05 Jun 2026 16:11:50 GMT"},
    {"url": "https://www.co.nolan.tx.us/upload/page/0503/Official%20Precinct%20Summary%20Results%2003032026%20canvassed.pdf", "via": "fetch_module", "content_hash": "8c9d1ef1b7a97389db8a8b7e599169aee3baa1b7640b3dace583f239c00ef122",
     "quote": "PRECINCT SUMMARY RESULTS (link title; 143-page scan created Mar 27 2026)", "supports": "Primary precinct file uploaded Fri, 27 Mar 2026 19:34:45 GMT"},
]
note(d, "No change. Upload times: runoff official summary and precinct files Jun 5 2026, primary canvassed precinct file Mar 27 2026; the runoff preliminary reconciliation form was uploaded 8:50 PM CDT on election night but holds ballot counts, not candidate totals. Three requests for likely unofficial file names (NC Unofficial ... 05262026, Unofficial Precinct Summary Results 03032026) returned 404. Wayback harvest was robots-blocked or unreachable for co.nolan.tx.us; no sweep file; web search for Sweetwater/Nolan precinct results found nothing.")
save("Nolan", d)

# ---------------- Somervell ----------------
d = load("Somervell")
d["sources"] += [
    {"url": "https://www.somervell.co/CivicAlerts.aspx", "via": "fetch_module", "content_hash": "6365c55014f9e8132edc7558734f56e6ad0aaf911ab0a829b65b0e17a7a6619b",
     "quote": "(no election results items)", "supports": "No results posted as News Flash items"},
    {"url": "https://www.somervell.co/Archive.aspx", "via": "fetch_module", "content_hash": "80cb780b316e581ddb9c4eaf3212d7b71fab7ca6b45af91b6393f4d06fd1f307",
     "quote": "(no election results items)", "supports": "No results in the CivicPlus Archive Center"},
]
note(d, "No change. The Elections page (DocumentCenter items 1137 to 1203) holds only Nov 2026 notices; Past Election Results ends with Nov 2022; CivicAlerts and Archive Center have no results. Wayback harvest was robots-blocked or unreachable for somervell.co; no sweep file; web search found no third-party precinct results.")
save("Somervell", d)

# ---------------- Crosby ----------------
d = load("Crosby")
e = d["elections"]["2026_runoff"]
e["fact"] = ("Correction: the Elections page does list runoff results. '2026 RUNOFF CUMULATIVE' (2026/2026Runoffcumulative.pdf) is a scanned Hart 'Cumulative Results Report ... CROSBY COUNTY, TEXAS PRIMARY RUNOFF ELECTION 5/26/2026 ... Official Results ... Run Time 1:55 PM Run Date 06/03/2026' (county totals by vote type, e.g. 'Ken Paxton 16 102 146 264'; read from the page image), CreationDate 2026-06-04, Last-Modified Fri, 05 Jun 2026 15:12:03 GMT. No election-night file and no precinct numbers online, so UNDETERMINED under rule 43.")
d["sources"] += [
    {"url": "https://www.co.crosby.tx.us/upload/page/8077/2026/2026Runoffcumulative.pdf", "via": "fetch_module", "content_hash": "877ea8cbbd26bd5593bebf771355ec6aee8cffebbb4a865b8b3c9078a770f22c",
     "quote": "Cumulative Results Report ... CROSBY COUNTY, TEXAS PRIMARY RUNOFF ELECTION 5/26/2026 ... Official Results ... Run Time 1:55 PM Run Date 06/03/2026 (page image)", "supports": "Only runoff file is official county totals, uploaded Fri, 05 Jun 2026 15:12:03 GMT"},
]
note(d, "No result change. Corrected the 2026_runoff fact per verifier: the page links '2026 RUNOFF CUMULATIVE' (official, run 06/03/2026, uploaded Jun 5). Primary cumulative re-checked: Last-Modified Fri, 29 May 2026 17:39:04 GMT for the 2026PRIMARYCUMULATIVE.pdf copy at the folder root. Wayback harvest: no captures (runoff CDX timed out); no sweep file.")
save("Crosby", d)

# ---------------- Hardeman ----------------
d = load("Hardeman")
note(d, "No change. Refreshed the Elections page: same files (2026 primary SOS unofficial reports uploaded Mar 5, runoff canvass report Jun 3; nothing for 2024). Wayback harvest: no captures (primary and runoff CDX refused connection); no sweep file; no third-party precinct results found.")
save("Hardeman", d)

# ---------------- Cottle ----------------
d = load("Cottle")
P = NT + "/upload/page/0611/"
d["results_url"] = NT + "/page/cottle.Elections"
d["platform"] = "county_pdfs"
d["host"] = "newtools.cira.state.tx.us"
d["elections"]["2024_general"].update({
    "result": "LATER", "check": "2",
    "county_totals_first_seen": "2024-11-05 21:38 CT (printed run time; server upload 2024-11-06 10:25 CT)",
    "precinct_first_seen": "2025-01-23 22:28 CT (server upload of the unofficial precinct report; printed 2024-11-05 21:37)",
    "night_updates_with_precinct_numbers": "0",
    "evidence_url": P + "2024/results.11.5.pdf",
    "fact": "The CIRA copy of the Elections page (newtools.cira.state.tx.us/page/cottle.Elections; the www.co.cottle.tx.us pages return the Home page) links 'November 2024 General Election Results' (2024/results.11.5.pdf) = scanned Electionware 'Summary Results Report TX Cottle 241105 General 6110 November 5, 2024 UNOFFICIAL RESULTS', county totals (e.g. 'REP Donald J. Trump/JD Vance 565 29 456 80'), footer 'Election Summary - 11/05/2024 9:38 PM' (election night; read from the page image), Last-Modified Wed, 06 Nov 2024 16:25:41 GMT (10:25 AM CST Nov 6). 'Precinct Results' (2024/Precinct results.pdf) = 'Summary Results Report ... UNOFFICIAL RESULTS ... PRECINCT 101' with Election Day column, footer 'Precinct Summary - 11/05/2024 9:37 PM', Last-Modified Fri, 24 Jan 2025 04:28:12 GMT, so under rule 47 it cannot show election-night publication. Rule 43: county-totals file with an election-night printed run time and no precinct numbers shown published that night gives LATER (precinct numbers posted Jan 2025). Caveat: the totals file itself was uploaded the next morning.",
})
d["elections"]["2026_primary"].update({
    "result": "UNDETERMINED", "check": "none",
    "fact": "Only official files: 'Election Results' (2026/election_results.pdf) = 'Summary Results Report TX Cottle County 260303 Primary Election 6110 March 3, 2026 OFFICIAL RESULTS', footer 'Election Summary - 03/24/2026 11:35 AM', Last-Modified Wed, 25 Mar 2026 15:11:32 GMT; 'Official Results' (2026/Official Total 2026 Primary.pdf), Last-Modified Mon, 16 Mar 2026 17:15:36 GMT. No election-night file survives (rule 43).",
})
d["elections"]["2026_runoff"].update({
    "result": "UNDETERMINED", "check": "none",
    "fact": "'Unofficial Results' (2026/Unoffical Results.pdf) = scanned 'Texas Secretary of State Election Unofficial Results Report 2026 REPUBLICAN PRIMARY RUNOFF ELECTION May 26, 2026 COTTLE County' (county totals, no printed time seen), Last-Modified Wed, 27 May 2026 18:46:51 GMT (1:46 PM CDT May 27), after election night; '2026 Primary Runoff Official Results' and '... OffIcial Totals' uploaded Jun 5 2026. No election-night time, so UNDETERMINED (rule 43).",
})
d["sources"] += [
    {"url": NT + "/page/cottle.Elections", "via": "fetch_module", "content_hash": "5099df1a3242ec6200a9e21e9e527d49e91ea5ab4cf7351a9a1e10d95bdafe39",
     "quote": "November 2024 General Election Results; Precinct Results; Unofficial Results; Election Results; Official Results; 2026 Primary Runoff Official Results", "supports": "Cottle's Elections page as served by the CIRA host, listing the results files"},
    {"url": P + "2024/results.11.5.pdf", "via": "fetch_module", "content_hash": "131d71f9f9d8aad82a535b0cc4d36b2c04deebfc4a66b7e844caeb8d54e0a7b7",
     "quote": "Summary Results Report TX Cottle 241105 General 6110 November 5, 2024 UNOFFICIAL RESULTS ... Election Summary - 11/05/2024 9:38 PM (page image)", "supports": "2024_general county totals printed on election night; Last-Modified Wed, 06 Nov 2024 16:25:41 GMT"},
    {"url": P + "2024/Precinct%20results.pdf", "via": "fetch_module", "content_hash": "b96ce36454aad26cab499fe96c79d334b03e221d57d091704b4dd715657f9840",
     "quote": "Summary Results Report TX Cottle 241105 General 6110 November 5, 2024 UNOFFICIAL RESULTS PRECINCT 101 ... Precinct Summary - 11/05/2024 9:37 PM (page image)", "supports": "2024 precinct report uploaded Fri, 24 Jan 2025 04:28:12 GMT (rule 47: not election-night publication)"},
    {"url": P + "2026/election_results.pdf", "via": "fetch_module", "content_hash": "04d6ede3e0e445a7ec6e678022f5d6d4174999ad28cf3392905aea7bf24a4305",
     "quote": "Summary Results Report TX Cottle County 260303 Primary Election 6110 March 3, 2026 OFFICIAL RESULTS ... Election Summary - 03/24/2026 11:35 AM (page image)", "supports": "Primary results file is official, uploaded Mar 25 2026"},
    {"url": P + "2026/Official%20Total%202026%20Primary.pdf", "via": "fetch_module", "content_hash": "eb06278fd7d9053f40b46ac3faee50511c03361069d706d275176847dea2f9da",
     "quote": "Official Results (link title)", "supports": "Uploaded Mon, 16 Mar 2026 17:15:36 GMT"},
    {"url": P + "2026/Unoffical%20Results.pdf", "via": "fetch_module", "content_hash": "796f9407a5211e9b0df2cf64067424331a92a1376628ca8fefc9f118910cff75",
     "quote": "Texas Secretary of State Election Unofficial Results Report 2026 REPUBLICAN PRIMARY RUNOFF ELECTION May 26, 2026 COTTLE County (page image)", "supports": "Runoff unofficial county totals uploaded Wed, 27 May 2026 18:46:51 GMT, after election night"},
    {"url": P + "2026/2026%20Primary%20Runoff%20Official%20Results.pdf", "via": "fetch_module", "content_hash": "a863c861c7995a6e36a7ec85c7436593419a4a6f994fbf0d16944035fa71df2d",
     "quote": "2026 Primary Runoff Official Results (link title)", "supports": "Uploaded Fri, 05 Jun 2026 15:18:28 GMT"},
    {"url": "websearch:?q=cottle county texas election results 2026 primary paducah", "via": "websearch", "content_hash": "b92a4129954cb6390e0e17d0876fb95aaaaa3247bee71a451880b5f6cf222e83",
     "quote": "1Notice of RD Primary https://newtools.cira.state.tx.us/upload/page/0611/2024/1Notice of RD Primary.pdf", "supports": "Identified Cottle's CIRA upload folder 0611 (locating only)"},
]
d["evidence_url"] = P + "2024/results.11.5.pdf"
d["tag_rationale"] = "Only the 2024 general is determined (LATER, check 2: county totals printed 9:38 PM on election night, precinct report uploaded Jan 2025); the 2026 primary and runoff have no election-night file. Exactly one election is determined, so the tag is COUNTY_ONLY_PRECINCT_AT_CANVASS with low confidence."
note(d, "The www.co.cottle.tx.us election pages still return the Home page, but the same CIRA platform serves Cottle's Elections page at newtools.cira.state.tx.us/page/cottle.Elections (found via a web search hit in upload folder 0611; cottle.Elections.2026 and .Archive return 403 there). Listed files and upload times read. 2024_general UNDETERMINED to LATER (check 2); primary and runoff stay UNDETERMINED with facts updated. Platform set to county_pdfs. Wayback harvest had no captures; no sweep file.")
save("Cottle", d)
