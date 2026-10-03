import json, datetime
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
WB = "git show origin/wayback-data:phase1/targeted/sweep/"

ellis = {
 "county": "Ellis",
 "reason_selected": "tag changed in targeted pass 5",
 "verifier_tag": "PRECINCT_END_OF_NIGHT",
 "verifier_confidence": "low",
 "elections": {
  "2024_general": {
   "result": "UNDETERMINED",
   "check": "none",
   "fact": "County page co.ellis.tx.us/1228/November-5-2024-General-Election now lists only canvass files: 'Official Cumulative Results Summary', 'Official Precinct by Race Results' (DocumentCenter/View/19538/241105-General-Precinct-by-Race-Report-Whole-Precincts), 'Official Countywide Vote Center Turnout Reporting', 'Official Reconciliation Report', 'Official Results for Canvass and other Documents' (zipped), plus a link to the SOS unofficial results. No unofficial or election-night file is linked. No Clarity site (elections.json 404, check 1 script). Targeted sweep (wayback-data, phase1/targeted/sweep/Ellis/index.json) found 0 archived files for elliscountytx.gov and livevoterturnout.com/ENR/ellistxenr in the 2024 window (one CDX query timed out, the retry returned 0 rows); phase1/wayback_snapshots/Ellis CDX for co.ellis.tx.us timed out. No election-night file survives, so UNDETERMINED."
  },
  "2026_primary": {
   "result": "END",
   "check": "3",
   "fact": "Archived copy (sweep saved file 2026_primary_20260304054954_8115d68933.html, sha256 6d52b316..., 5,065,943 bytes) of https://www.livevoterturnout.com/ENR/ellistxenr/5/en/Index_5.html, the page the county's March 3 2026 page links as its Democratic Party results. Wayback capture 2026-03-04 05:49:54 UTC (11:49 PM CST Mar 3, election night); original server Last-Modified 'Wed, 04 Mar 2026 05:34:47 GMT' (11:34 PM CST, election night). Page text: 'Website Updated: 3/3/2026 11:34:46 PM', 'March 3, 2026 - Democratic Primary Election', 'Unofficial Election Results Absentee: Complete Early Voting: Complete Election Day: Complete', 'Ballots Counted 18,806 Absentee 209 Early Voting 12,477 Election Day 6,120', 'Vote Centers Reporting 100% ... Fully Reporting 30 Total Precincts 30'. The same file carries a 'Precincts Reporting' tab (hdnPrecinctLevelResults value=\"1\") with per-precinct candidate votes for all 39 contests, for example 'Precinct: 1001 - Contest: DEM US Senator ... James Talarico 73 13.72% Ahmad R. Hassan 3 0.56% Jasmine Crockett 456 85.71%' (precincts 1001 to 1061). Election Day is complete, so these precinct totals include election-day votes; it is the final count of the night (current canvass version, Last-Modified 10 Mar 2026, shows 18,894 ballots, consistent with late ballots added). Only one election-night copy exists (the Republican page Index_4 was captured at 05:49:15 UTC but its replay timed out), so precinct numbers are seen once on election night: END. The precinct numbers are static markup inside this one published page (the page's refresh is a full reload, 'document.location.reload(true)', auto-refresh 600 s); no per-precinct data file is requested, so the live precinct view rule is not applied (see rationale)."
  },
  "2026_runoff": {
   "result": "UNDETERMINED",
   "check": "none",
   "fact": "County page elliscountytx.gov/1384/May-26-2026-Republican-and-Democratic-Jo links livevoterturnout Index_9 (Republican) and Index_10 (Democratic) plus official canvass PDFs. Current Index_9 Last-Modified 'Wed, 03 Jun 2026 20:15:50 GMT' ('Website Updated: 6/3/2026 3:15:50 PM'), Index_10 Last-Modified 'Wed, 03 Jun 2026 20:12:04 GMT', both after election night. The only archived runoff-window file (sweep 2026_runoff_20260526210012_48ce061902.html) is Index_8, captured 21:00 UTC May 26 (4:00 PM CDT, before polls closed), Last-Modified 8 May 2026, and it is the 'May 2, 2026- Joint General and Special Elections' page, not the runoff. No election-night runoff file survives: UNDETERMINED."
  }
 },
 "rationale": "Only the 2026 primary is determined (END from an election-night archived copy of the county's vendor results page with per-precinct candidate votes, Election Day complete, server Last-Modified 11:34 PM CST); 2024 and the runoff have no surviving election-night file. Fixed rule: one determined election gives PRECINCT_END_OF_NIGHT, confidence low. Live precinct view rule: not met as worded. The rule requires a precinct view that 'loads its numbers from the same live, refreshing data feed as the county totals' (example: a tab that requests per-precinct vote files with a cache-busting time). Here the precinct numbers are not loaded from any feed: they are fixed markup in a single page published at 11:34:46 PM, the same snapshot that holds the county totals, and the only data request in the page is a map file (../ellistxenr_5.txt). One archived copy therefore shows precinct numbers in exactly one publication, after Election Day reporting was complete, which is END under rule 47 (election-night upload time), not LIVE; it cannot show whether earlier publications that night carried precinct results (hdnPrecinctLevelResults is a per-publication setting).",
 "sources": [
  {"url": "https://www.elliscountytx.gov/403/Prior-Election-Results", "content_hash": "44a5541db084a48a909719407d7d117c4bfcd2ea7f251d743a7a65fea34a99a2"[:0] + "44a5541db084a48a909719407d7d117c4bfcd2ea7f251d743a7a6", "what_i_checked": "Index of election result pages by year"},
  {"url": "https://www.co.ellis.tx.us/1228/November-5-2024-General-Election", "content_hash": "8b2fc12c96f00a5e0015fa9791646fab806037dea4d914dc4c0b2e8cf935bb20", "what_i_checked": "Nov 2024 page: only official canvass files and SOS link"},
  {"url": "https://www.elliscountytx.gov/1363/March-3-2026-Joint-Primary-Elections", "content_hash": "97a9a6334932e91fb1f12bd799d3b6574051a231a85473c4c69581f8861cd308", "what_i_checked": "Primary page: links livevoterturnout Index_4 (Republican) and Index_5 (Democratic) plus official PDFs"},
  {"url": "https://www.elliscountytx.gov/1384/May-26-2026-Republican-and-Democratic-Jo", "content_hash": "734ea582c1a92ba2f08f8ce7801c83ddc118dbc4dcf5d18477f90d3c6a0f25a4", "what_i_checked": "Runoff page: links Index_9 and Index_10 plus official PDFs"},
  {"url": "https://www.livevoterturnout.com/ENR/ellistxenr/5/en/Index_5.html", "content_hash": "e520ecfe600567c9dda2c831df5637086dd4792a178e76b51597f7ad0aab70cd", "what_i_checked": "Current canvass version: Last-Modified 10 Mar 2026 19:11:37 GMT, 18,894 ballots"},
  {"url": "https://www.livevoterturnout.com/ENR/ellistxenr/4/en/Index_4.html", "content_hash": "a10121ed0cc138f6102fa3867fee7cdc68aa58e105c84234c863f28117ffce51", "what_i_checked": "Current Republican primary page: Last-Modified 10 Mar 2026 19:10:57 GMT"},
  {"url": "https://www.livevoterturnout.com/ENR/ellistxenr/9/en/Index_9.html", "content_hash": "f9faf477d3595491243a362d3d9cbe0518b3d7b80faf024440f9bb11eb17281b", "what_i_checked": "Current Republican runoff page: Last-Modified 3 Jun 2026 20:15:50 GMT"},
  {"url": "https://www.livevoterturnout.com/ENR/ellistxenr/10/en/Index_10.html", "content_hash": "41fbf8c5b38f77d7cc9ef62edcc44aef03abe7ade40de27782b032a0b9d882d1", "what_i_checked": "Current Democratic runoff page: Last-Modified 3 Jun 2026 20:12:04 GMT"},
  {"url": WB + "Ellis/2026_primary_20260304054954_8115d68933.html", "content_hash": "6d52b3165543b42d86febb00be183bdb8790d6142fe293e07cbf5c1f76807c52", "what_i_checked": "Archived Index_5 at 05:49:54 UTC Mar 4, original Last-Modified 05:34:47 GMT; per-precinct candidate votes, Election Day complete; refresh mechanism (full page reload)"},
  {"url": WB + "Ellis/2026_runoff_20260526210012_48ce061902.html", "content_hash": "a840c8dfd1845fc40dd09d3fabbcd18f857115053d699ddc5b850e6294eb2d2e", "what_i_checked": "Archived Index_8 (gzip): May 2 2026 election page, Last-Modified 8 May 2026, captured before polls closed"},
  {"url": WB + "Ellis/index.json", "content_hash": "", "what_i_checked": "Sweep CDX results per election and replay Last-Modified values"},
  {"url": "https://results.enr.clarityelections.com/TX/Ellis/elections.json", "content_hash": "", "what_i_checked": "check 1 script: no Clarity election list (404)"}
 ],
 "written_blind_at_utc": now
}
ellis["sources"][0]["content_hash"] = ""

g = {
 "county": "Guadalupe",
 "reason_selected": "tag changed in targeted pass 5",
 "verifier_tag": "COUNTY_ONLY_PRECINCT_AT_CANVASS",
 "verifier_confidence": "low",
 "elections": {
  "2024_general": {
   "result": "UNDETERMINED",
   "check": "none",
   "fact": "Results history page (guadalupetx.gov/page/elections.history) lists for Nov 2024 only official files, including '11-5-24-GC_General-PrctbyPrct.pdf' ('Guadalupe County General Election-pct by pct - Official Results', 456 pages, CreationDate 2024-11-21, Last-Modified Thu, 21 Nov 2024 22:21:08 GMT) and '11.5.24-GC_General-Official_Results.pdf'. Clarity election list exists but does not list this election (check 1 script). Targeted sweep found 0 archived guadalupetx.gov files or pages in the 2024 window; wayback_snapshots harvest was robots-blocked. No election-night file survives: UNDETERMINED."
  },
  "2026_primary": {
   "result": "LATER",
   "check": "2",
   "fact": "County file https://www.guadalupetx.gov/upload/page/0358/Unofficial%20%20Results%20Early%20Voting%20and%20Mail%20Ballots%205%20of%2036.pdf (live fetch 200, same hash as the archived copy 005be967...; server Last-Modified 'Wed, 04 Mar 2026 03:06:04 GMT' = 9:06 PM CST Mar 3, election night). Scanned 31-page PDF (ScandAll PRO, CreationDate 2026-03-04 02:40:01 UTC), read by rendering pages: 'Summary Results Report Guadalupe County / March 3, 2026 Joint Primary Elections / Unofficial Results / Early Voting, Absentee, Election / 5 Vote Centers of 36 Reporting', footer 'Election Summary - 03/03/2026 8:33 PM'; county totals only with Election Day, Early Voting, Absentee columns (for example REP US Senator: John Cornyn 5,000, Ken Paxton 4,574); page 31 'DEM Proposition #13'; no per-precinct pages. Also 'Unofficial Reconciliation Form.pdf' (Preliminary Election Reconciliation - Unofficial Totals, 31,612 ballots counted, signed 3/3/26; Last-Modified Wed, 04 Mar 2026 06:04:22 GMT = 12:04 AM CST). A '36 of 36' file of the same series was archived but its replay timed out and the county copy now returns HTTP 404. The official reports on the history page ('3-3-26_Rep_Primary-Official_Results.pdf', 'Election Summary Report ... Official Results', printed 03/10/2026 2:31 PM, Last-Modified Mon, 30 Mar 2026 20:50:45 GMT; Dem equivalent) are summary reports; no unofficial or official precinct report for this election is linked or archived. DECISIONS 67: (i) met by the 8:33 PM / 9:06 PM county-totals file; (ii) met: no unofficial precinct report found (precinct numbers apparently never published online). Caveat: the election-night copy of the results page (elections.election3, 05:34 UTC Mar 4) could not be replayed, so its link list that night is unseen."
  },
  "2026_runoff": {
   "result": "UNDETERMINED",
   "check": "none",
   "fact": "Results page now shows the June 13 2026 New Braunfels runoff; history page lists for May 26 only 'Official_Result-052626.pdf' ('Election Summary Report Joint Primary Runoff Election ... Official Results', printed 06/08/2026 12:45 PM, Last-Modified Fri, 11 Sep 2026 13:35:34 GMT). Targeted sweep of guadalupetx.gov in the runoff window found only unrelated files (press releases, calendars, a Mar 2026 vote center list); no election-night results file archived. No election-night file survives: UNDETERMINED."
  }
 },
 "rationale": "Only the 2026 primary is determined: an election-night county-totals summary (printed 8:33 PM, uploaded 9:06 PM CST) and no precinct report of any kind for that election, so LATER under DECISIONS 67. 2024 and the runoff have only official post-canvass files. Fixed rule: one determined election gives COUNTY_ONLY_PRECINCT_AT_CANVASS, confidence low.",
 "sources": [
  {"url": "https://www.guadalupetx.gov/page/elections.election3", "content_hash": "5b29ff66c3a16e667cb3284fa881bb8fc50223a7977428cd0c91110406c0fc4d", "what_i_checked": "Current results page (June 13 2026 election only)"},
  {"url": "https://www.guadalupetx.gov/page/elections.history", "content_hash": "29dcfb249b3a05060dc1371b0078e6d100fb530ae3aa52a4e8cce8685fb46c34", "what_i_checked": "History page: official files only for the three elections"},
  {"url": "https://www.guadalupetx.gov/upload/page/0358/Unofficial%20%20Results%20Early%20Voting%20and%20Mail%20Ballots%205%20of%2036.pdf", "content_hash": "005be96704cac7fe35782a96dbda495e30302072eb418f3db526e51018731d4f", "what_i_checked": "Rendered pages 1, 2, 31: county totals summary, 8:33 PM, Last-Modified 03:06:04 GMT Mar 4"},
  {"url": WB + "Guadalupe/2026_primary_20260304101838_5793aa3481.pdf", "content_hash": "f7eec609a7ffa9df86286a37df4ecb25298fd5e1f00e8487efbd2f5183ca16b1", "what_i_checked": "Unofficial Reconciliation Form, original Last-Modified 06:04:22 GMT Mar 4; no candidate votes"},
  {"url": "https://www.guadalupetx.gov/upload/page/0358/docs/030326/Unofficial%20%20Results%20Early%20Voting%20and%20Mail%20Ballots%2036%20of%2036.pdf", "content_hash": "", "what_i_checked": "Live fetch HTTP 404; archived replay timed out"},
  {"url": "https://www.guadalupetx.gov/upload/page/0210/docs/2026/3-3-26_Rep_Primary-Official_Results.pdf", "content_hash": "f7ec9a76a3dcc170e61025e0259476916999d06c72bc39df99707e1e3432ac45", "what_i_checked": "Official summary report, printed 03/10/2026, Last-Modified 30 Mar 2026"},
  {"url": "https://www.guadalupetx.gov/upload/page/0210/docs/2026/5-26/Official_Result-052626.pdf", "content_hash": "f07436e27747b67743f4f94d7d328829363b05aeb7da8d7f3df64f481cc42399", "what_i_checked": "Runoff official summary, printed 06/08/2026, Last-Modified 11 Sep 2026"},
  {"url": "https://www.guadalupetx.gov/upload/page/0210/docs/2024/11-5-24-GC_General-PrctbyPrct.pdf", "content_hash": "8b4eb4c3d8f98988fe3ac1ed38f4b4ae2819667c903af1163e64c505ba81fd58", "what_i_checked": "Nov 2024 official precinct report, Last-Modified 21 Nov 2024"},
  {"url": WB + "Guadalupe/index.json", "content_hash": "", "what_i_checked": "Sweep CDX rows and replays per election"},
  {"url": "https://newtools.cira.state.tx.us/page/guadalupe.elections.election3", "content_hash": "", "what_i_checked": "State mirror: HTTP 403, not used"},
  {"url": "https://results.enr.clarityelections.com/TX/Guadalupe/elections.json", "content_hash": "", "what_i_checked": "check 1 script: none of the three elections listed"}
 ],
 "written_blind_at_utc": now
}
for name, rec in (("Ellis", ellis), ("Guadalupe", g)):
    s = json.dumps(rec, indent=1, ensure_ascii=False)
    assert "\u2014" not in s and "\u2013" not in s
    open(f"phase1/verification/{name}.json", "w").write(s + "\n")
print(now)
