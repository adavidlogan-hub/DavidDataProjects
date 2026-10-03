"""targeted5-A: apply archived-file sweep findings to evidence files."""
import json, sys
sys.path.insert(0, '.')
from phase1.schema import validate_v2, compute_tag, compute_confidence

AG = 'targeted5-A'
NOTE = 'Targeted pass 5 2026-10-03 (targeted5-A): '
WB = lambda ts, u: f'https://web.archive.org/web/{ts}id_/{u}'


def load(c):
    return json.load(open(f'phase1/evidence/{c}.json'))


def save(c, r):
    tag, single = compute_tag(r['elections'])
    r['tag'] = tag
    r['confidence'] = compute_confidence(r)
    validate_v2(r)
    with open(f'phase1/evidence/{c}.json', 'w') as f:
        json.dump(r, f, indent=2, ensure_ascii=False)
    print(c, r['tag'], r['confidence'])


# ---------------- Ellis ----------------
c = 'Ellis'; r = load(c)
u5 = 'https://www.livevoterturnout.com/ENR/ellistxenr/5/en/Index_5.html'
url5 = WB('20260304054954', u5)
r['elections']['2026_primary'] = {
    'result': 'LIVE', 'check': '3', 'rule': 'live_precinct_view',
    'county_totals_first_seen': '2026-03-03 23:34 CT (same page; Website Updated time and server upload)',
    'precinct_first_seen': '2026-03-03 23:34 CT',
    'night_updates_with_precinct_numbers': '1 observed (one election-night capture); the page is the live auto-refreshing results publication, so the number of releases cannot be counted',
    'evidence_url': url5,
    'evidence_snapshot_timestamp': '20260304054954',
    'fact': ("Live precinct view rule, as applied to Williamson (DECISIONS 39, 61b). Archived-file sweep replay (wayback-data "
             "phase1/targeted/sweep/Ellis/2026_primary_20260304054954_8115d68933.html, sha256 6d52b316...) of the county's election-night "
             "results site for the March 3, 2026 primary, livevoterturnout.com/ENR/ellistxenr/5/en/Index_5.html ('Ellis County, Texas Election "
             "Department March 3, 2026 - Democratic Primary Election'), captured 2026-03-03 23:49:54 CST. Original server Last-Modified "
             "'Wed, 04 Mar 2026 05:34:47 GMT' (11:34:47 PM CST election night). The page shows '<span id=\"lblLastPublishedDateTime\" "
             "class=\"updated-at\">3/3/2026 11:34:46 PM</span>', reloads itself ('<input type=\"hidden\" name=\"hdnAutoRefresh\" "
             "id=\"hdnAutoRefresh\" value=\"600\" />'; 'Refresh Display' onclick=\"javascript: document.location.reload(true);\"), has "
             "precinct results switched on ('<input type=\"hidden\" name=\"hdnPrecinctLevelResults\" id=\"hdnPrecinctLevelResults\" "
             "value=\"1\" />'; tab onclick \"PrecinctTabClick(); if($('#hdnPrecinctLevelResults').val() === '1') { "
             "SetPrecinctResults('precinct-list');\") and embeds, in the same published page as the county totals ('Unofficial Election "
             "Results Absentee: Complete Early Voting: Complete Election Day: Complete ... Ballots Counted 18,806 Absentee 209 Early Voting "
             "12,477 Election Day 6,120'), per-precinct candidate tables for 60 precincts with votes, e.g. 'Precinct: 1001 - Contest: DEM US "
             "Senator ... Candidate Name Total Votes Percentage James Talarico 73 13.72% Ahmad R. Hassan 3 0.56% Jasmine Crockett 456 85.71%'. "
             "The per-precinct DEM US Senator votes sum to 18,649 of 18,806 ballots counted, so the precinct numbers include the election-day "
             "votes. Unlike Williamson's copy (all zeros), this copy shows precinct numbers with election-day votes on election night (printed "
             "and uploaded 11:34 PM, captured 11:49 PM). Only one election-night copy exists, so two releases cannot be counted from captures; "
             "the result rests on the live precinct view rule (rule 47 alone, with one observed release, would give END)."),
}
r['sources'].append({
    'url': url5, 'via': 'wayback_branch',
    'content_hash': '6d52b3165543b42d86febb00be183bdb8790d6142fe293e07cbf5c1f76807c52',
    'quote': ("Website Updated: 3/3/2026 11:34:46 PM | orig Last-Modified Wed, 04 Mar 2026 05:34:47 GMT | hdnAutoRefresh value=\"600\" | "
              "hdnPrecinctLevelResults value=\"1\" | Election Day: Complete ... Ballots Counted 18,806 ... Election Day 6,120 | Precinct: 1001 - "
              "Contest: DEM US Senator ... James Talarico 73 13.72% Ahmad R. Hassan 3 0.56% Jasmine Crockett 456 85.71%"),
    'supports': ("2026_primary LIVE under the live precinct view rule: election-night copy (captured 11:49 PM CST) of the county's live, "
                 "auto-refreshing ENR page with per-precinct candidate votes including election-day votes in the same publication as the county "
                 "totals; wayback-data phase1/targeted/sweep/Ellis/2026_primary_20260304054954_8115d68933.html"),
})
r['evidence_url'] = url5
r['evidence_snapshot_timestamp'] = '20260304054954'
r['precinct_first_seen_local_time'] = '2026-03-03 23:34 CT'
r['tag_rationale'] = ("Only the 2026 primary is determined (LIVE, check 3 under the live precinct view rule, from the 11:49 PM CST archived copy of "
                      "the county's auto-refreshing ENR page showing per-precinct candidate votes updated 11:34 PM); one determined election gives "
                      "LIVE_PRECINCT with confidence low. The 2024 general and 2026 runoff remain UNDETERMINED.")
r['notes'] += (' ' + NOTE + "2026_primary changed UNDETERMINED -> LIVE (check 3, live precinct view rule). The archived-file sweep "
               "(phase1/targeted/sweep/Ellis/index.json, swept 2026-10-02 22:49 UTC) replayed the 20260304054954 capture of "
               "ellistxenr/5/en/Index_5.html (Democratic primary page of the March 3, 2026 joint primary): 'Website Updated: 3/3/2026 11:34:46 PM', "
               "original Last-Modified Wed, 04 Mar 2026 05:34:47 GMT (11:34 PM CST), hdnPrecinctLevelResults=1, auto-refresh 600 s, per-precinct "
               "candidate tables for 60 precincts with votes in the same page as the county totals ('Election Day: Complete', Election Day 6,120 "
               "ballots). The Republican page capture 20260304054915 (Index_4) could not be replayed (timed out). Other Ellis replays: "
               "Index_8 captured 2026-05-26 4:00 PM CDT is the May 2, 2026 Joint General and Special Elections page ('Website Updated: 5/8/2026 "
               "7:39:57 PM', Official Results for Canvass), not a target election; DocumentCenter/View/22466 is early-voting locations (Jan 2026); "
               "DocumentCenter 22968 'Preliminary Election Reconciliation - Unoffical Totals' and 18758 replays returned HTTP 404. 2024 general: "
               "CDX found no captures (one query timed out). 2026 runoff unchanged (no election-night capture).")
save(c, r)

# ---------------- Guadalupe ----------------
c = 'Guadalupe'; r = load(c)
ug = 'https://www.guadalupetx.gov/upload/page/0358/Unofficial%20%20Results%20Early%20Voting%20and%20Mail%20Ballots%205%20of%2036.pdf'
urlg = WB('20260306015913', ug)
ur = 'https://www.guadalupetx.gov/upload/page/0358/docs/030326/Unofficial%20Reconciliation%20Form.pdf'
urlr = WB('20260304101838', ur)
r['elections']['2026_primary'] = {
    'result': 'LATER', 'check': '2',
    'county_totals_first_seen': '2026-03-03 21:06 CT (server upload; printed 2026-03-03 20:33 CT)',
    'precinct_first_seen': '',
    'night_updates_with_precinct_numbers': '0',
    'evidence_url': urlg,
    'fact': ("Archived-file sweep replay (wayback-data phase1/targeted/sweep/Guadalupe/2026_primary_20260306015913_65eec88a8b.pdf, sha256 "
             "005be967...) of the county file 'Unofficial  Results Early Voting and Mail Ballots 5 of 36.pdf' (guadalupetx.gov/upload/page/0358/), "
             "a 31-page scanned report read from page images: 'Summary Results Report Guadalupe County March 3, 2026 Joint Primary Elections', "
             "'Unofficial Results Early Voting, Absentee, Election 5 Vote Centers of 36 Reporting', footer 'Election Summary - 03/03/2026 8:33 PM'; "
             "county totals per contest with Election Day, Early Voting and Absentee columns (e.g. 'REP REP US Senator ... Ken Paxton 4,574 ... "
             "Election Day 469 ... John Cornyn 5,000'); no per-precinct numbers on the pages read (1, 2, 31 of 31; every page is a contest summary "
             "and the last is 'DEM Proposition #13'). Original server Last-Modified 'Wed, 04 Mar 2026 03:06:04 GMT' (9:06 PM CST election "
             "night); PDF CreationDate 2026-03-03 20:40:01 -06:00. The 'Unofficial Reconciliation Form.pdf' (Preliminary Election Reconciliation "
             "- Unofficial Totals, county ballot counts only) was uploaded 'Wed, 04 Mar 2026 06:04:22 GMT' (12:04 AM CST). No precinct report "
             "for this election was found: the Elections Results History page lists only the official primary results, and the Wayback CDX for "
             "guadalupetx.gov from Mar 3 to Mar 24 (keyword filter includes precinct and pct) lists only the 5 of 36 and 36 of 36 summaries, the "
             "reconciliation form, a returned-ballots log and vote-center locations. LATER under the DECISIONS 67 reading of rule 43."),
}
r['sources'] += [
    {'url': urlg, 'via': 'wayback_branch',
     'content_hash': '005be96704cac7fe35782a96dbda495e30302072eb418f3db526e51018731d4f',
     'quote': ("Summary Results Report Guadalupe County March 3, 2026 Joint Primary Elections | Unofficial Results Early Voting, Absentee, "
               "Election 5 Vote Centers of 36 Reporting | Election Summary - 03/03/2026 8:33 PM | orig Last-Modified Wed, 04 Mar 2026 03:06:04 GMT "
               "(read from page images)"),
     'supports': ("2026_primary LATER: county-totals report printed 8:33 PM and uploaded 9:06 PM CST on election night; wayback-data "
                  "phase1/targeted/sweep/Guadalupe/2026_primary_20260306015913_65eec88a8b.pdf")},
    {'url': urlr, 'via': 'wayback_branch',
     'content_hash': 'f7eec609a7ffa9df86286a37df4ecb25298fd5e1f00e8487efbd2f5183ca16b1',
     'quote': ("Preliminary Election Reconciliation - Unofficial Totals | County Guadalupe | Election Name Primary Election | Election Date "
               "03/03/2026 | Total voters (A+B) 32241 | orig Last-Modified Wed, 04 Mar 2026 06:04:22 GMT (read from page image)"),
     'supports': "2026_primary: county-level unofficial reconciliation uploaded 12:04 AM CST election night (no precinct numbers)"},
]
r['evidence_url'] = urlg
r['tag_rationale'] = ("Only the 2026 primary is determined (LATER, check 2: county-totals report printed 8:33 PM and uploaded 9:06 PM on election "
                      "night, no precinct report found), so the single-election rule gives COUNTY_ONLY_PRECINCT_AT_CANVASS with confidence low.")
r['notes'] += (' ' + NOTE + "2026_primary changed UNDETERMINED -> LATER (check 2, deciding fact the archived original Last-Modified 9:06 PM CST and "
               "printed time 8:33 PM of the 'Unofficial  Results Early Voting and Mail Ballots 5 of 36.pdf' county-totals report, read from page "
               "images of the sweep replay). Other Guadalupe replays: 'Unofficial Reconciliation Form.pdf' (county ballot counts, uploaded 12:04 AM); "
               "returned-ballots log (uploaded 8:18 AM Mar 3); ED vote-center locations (Jan 28); the 36 of 36 summary (captured 4:17 AM Mar 4) and "
               "the elections.election3 page capture (11:34 PM CST) could not be replayed (timed out). 2024 general: CDX found no captures. 2026 "
               "runoff: 31 captures, all unrelated (press releases, calendars, fee schedules); unchanged.")
save(c, r)

# ---------------- Tom Green ----------------
c = 'Tom_Green'; r = load(c)
ut = 'https://www.tomgreencountytx.gov/upload/page/0091/docs/2024/20241105/report4.pdf'
urlt = WB('20241106070232', ut)
r['elections']['2024_general'] = {
    'result': 'LATER', 'check': '2',
    'county_totals_first_seen': '2024-11-05 23:10 CT (server upload; printed run time 2024-11-05 22:46 CT)',
    'precinct_first_seen': '',
    'night_updates_with_precinct_numbers': '0',
    'evidence_url': urlt,
    'fact': ("Archived-file sweep replay (wayback-data phase1/targeted/sweep/Tom_Green/2024_general_20241106070232_b9b3ee2143.pdf, sha256 "
             "0a733df4...) of the county file /upload/page/0091/docs/2024/20241105/report4.pdf, captured 2024-11-06 01:02 CST: a 9-page scanned "
             "'Cumulative Results Report / Tom Green County / Unofficial Results / 110524 General/Special Election', handwritten 'Batch 6', "
             "'Run Time 10:46 PM', 'Run Date 11/05/2024', 'Precincts Reporting 0 of 49 = 0.00%', county totals per contest with Absentee, Early "
             "Voting and Election Day Voting columns (e.g. 'DONALD J. TRUMP/JD VANCE ... Election Day 6,631 ... Total 33,100'), ending '*** End of "
             "report ***'; no per-precinct numbers (read from page images 1, 5, 7, 9). Original server Last-Modified 'Wed, 06 Nov 2024 05:10:40 GMT' "
             "(11:10 PM CST election night); scan CreationDate 2024-11-06 05:02 UTC. The only precinct report for this election online is the "
             "'Official Precinct Results' ('Official Results', Run Date 11/27/2024), and the Wayback CDX for tomgreencountytx.gov from Nov 5 to "
             "Nov 26, 2024 (53 files, keyword filter includes precinct and pct) has no 2024 general precinct report. LATER under the DECISIONS 67 "
             "reading of rule 43."),
}
r['sources'].append({
    'url': urlt, 'via': 'wayback_branch',
    'content_hash': '0a733df41514cccc02f40da5c784a03421a2f992617c1daf96aae6b1291c7f24',
    'quote': ("Cumulative Results Report | Tom Green County | Unofficial Results | 110524 General/Special Election | Run Time 10:46 PM Run Date "
              "11/05/2024 | Precincts Reporting 0 of 49 = 0.00% | orig Last-Modified Wed, 06 Nov 2024 05:10:40 GMT (read from page images)"),
    'supports': ("2024_general LATER: county-totals report printed 10:46 PM and uploaded 11:10 PM CST on election night; wayback-data "
                 "phase1/targeted/sweep/Tom_Green/2024_general_20241106070232_b9b3ee2143.pdf"),
})
r['tag_rationale'] = ("All three elections are LATER (election-night county-totals uploads with no election-night precinct report; precinct numbers "
                      "only in the official canvass reports), so the rule gives COUNTY_ONLY_PRECINCT_AT_CANVASS; confidence med because the deciding "
                      "elections rest on check 2.")
r['notes'] += (' ' + NOTE + "2024_general changed UNDETERMINED -> LATER (check 2, deciding fact the archived original Last-Modified 11:10 PM CST "
               "and printed run time 10:46 PM of report4.pdf, a county-totals Cumulative Results Report marked 'Batch 6', read from page images of "
               "the sweep replay). 'Batch 6' implies earlier releases (report1 to report3 or similar) that the archive did not capture. Other Tom "
               "Green replays (2023 COSA/ISD reports, auditor reports, 2020 sample ballots, campaign finance reports) are not target-election "
               "results. 2026 runoff: CDX empty. Tag unchanged.")
save(c, r)

# ---------------- Van Zandt ----------------
c = 'Van_Zandt'; r = load(c)
uv1 = 'https://www.vanzandtcounty.org/upload/page/2685/2026/Primary%2003032026/early%20voting%20cumulative.pdf'
uv2 = 'https://www.vanzandtcounty.org/upload/page/2685/2026/Primary%2003032026/Cumulative%20Results-3-3-2026%2010-55-19%20PM.pdf'
uv3 = 'https://www.vanzandtcounty.org/upload/page/2685/2026/finalprecinct_results3112026_125350_pm.pdf'
e = r['elections']['2026_primary']
e['county_totals_first_seen'] = '2026-03-03 20:25 CT (printed run time; server upload 2026-03-03 21:29 CT)'
e['fact'] += (" Targeted pass 5 (sweep replays): two earlier election-night county-totals releases from the same folder: 'early voting "
              "cumulative.pdf' ('Cumulative Results Report ... Unofficial Results ... Precincts Reporting 0 of 18 = 0.00% Run Time 8:25 PM Run Date "
              "03/03/2026', original Last-Modified Wed, 04 Mar 2026 03:29:12 GMT = 9:29 PM CST) and 'Cumulative Results-3-3-2026 10-55-19 PM.pdf' "
              "('Precincts Reporting 15 of 18 = 83.33% Run Time 10:55 PM', Absentee, Early Voting and Election Day Voting county totals, original "
              "Last-Modified Wed, 04 Mar 2026 05:02:44 GMT = 11:02 PM CST); both are 27 pages of county totals with no per-precinct pages. The first "
              "precinct report, 'finalprecinct_results3112026_125350_pm.pdf' ('Precinct Results Report ... Official Results ... Run Date "
              "03/11/2026'), has original Last-Modified Thu, 12 Mar 2026 15:29:16 GMT, after election night.")
r['sources'] += [
    {'url': WB('20260305050235', uv1), 'via': 'wayback_branch',
     'content_hash': 'c0125f94b982e823464c9426486a6c7cb864a3fa28fe7b60da09794002f8b611',
     'quote': "Cumulative Results Report ... Unofficial Results ... Precincts Reporting 0 of 18 = 0.00% Run Time 8:25 PM Run Date 03/03/2026 | orig Last-Modified Wed, 04 Mar 2026 03:29:12 GMT",
     'supports': "2026_primary LATER: first election-night county-totals release (printed 8:25 PM, uploaded 9:29 PM CST); wayback-data phase1/targeted/sweep/Van_Zandt/2026_primary_20260305050235_ea62b1d94e.pdf"},
    {'url': WB('20260305050930', uv2), 'via': 'wayback_branch',
     'content_hash': '6fe33f14ecc83bbd2ed47fab866d5e80c99632c65c9c0f1492b94f341b96c1fb',
     'quote': "Cumulative Results Report ... Unofficial Results ... Precincts Reporting 15 of 18 = 83.33% Run Time 10:55 PM Run Date 03/03/2026 | orig Last-Modified Wed, 04 Mar 2026 05:02:44 GMT",
     'supports': "2026_primary LATER: second election-night county-totals release (printed 10:55 PM, uploaded 11:02 PM CST); wayback-data phase1/targeted/sweep/Van_Zandt/2026_primary_20260305050930_3d361a7a9e.pdf"},
    {'url': WB('20260316123504', uv3), 'via': 'wayback_branch',
     'content_hash': 'e26ececbf8d4f1c3c86bb8ad0af5f9cfc9bd1a968152121ddeefed1deec8c674',
     'quote': "Precinct Results Report March 2026 Primary Election ... Official Results ... Run Date 03/11/2026 | orig Last-Modified Thu, 12 Mar 2026 15:29:16 GMT",
     'supports': "2026_primary: first precinct report uploaded Mar 12, after election night (sweep replay wayback-data phase1/targeted/sweep/Van_Zandt/2026_primary_20260316123504_81a678eb70.pdf)"},
]
r['notes'] += (' ' + NOTE + "2026_primary unchanged (LATER, check 2), strengthened: the sweep replays show two more election-night county-totals "
               "releases (8:25 PM printed / 9:29 PM uploaded and 10:55 PM / 11:02 PM) and the first precinct report uploaded Mar 12; "
               "county_totals_first_seen moved to 8:25 PM. 2024 general: sweep replays are canvass-time or unrelated (official cumulative "
               "uploaded Nov 15, preliminary reconciliation uploaded Nov 6 8:19 AM, 2024 primary runoff canvass); unchanged. 2026 runoff: the "
               "sweep CDX lists files under /upload/page/2685/2026/Runoff 05262026/ ('Early Count.pdf', 'Final.pdf', '05262026 runoff Republican "
               "1and3.pdf', '05262026 runoff Republican 2.pdf', '05262026 runoff Republican 4.pdf', captured Jun 13) but only 'Final.pdf' was "
               "replayed and it timed out; a fetch of these files from the county server was not run (the session's permission check refused the "
               "request). Runoff unchanged (UNDETERMINED).")
save(c, r)

# ---------------- Grayson ----------------
c = 'Grayson'; r = load(c)
ugr = 'https://www.co.grayson.tx.us/upload/page/0060/docs/General%20November%205%202024%20Election.pdf'
e = r['elections']['2024_general']
e['county_totals_first_seen'] = '2024-11-05 19:44 CT (printed run time; server upload 2024-11-05 19:54 CT)'
e['fact'] += (" Targeted pass 5 (sweep replay): an earlier election-night county-totals release in the same folder, 'General November 5 2024 "
              "Election.pdf' (24 pages, 'Summary Results Report UNOFFICIAL RESULTS', 'Election Day Precincts Reporting 0 of 41', 'Absentee/ Early "
              "Precincts Reporting 41 of 41', footer 'Election Summary - 11/05/2024 07:44PM', no per-precinct pages), original Last-Modified Wed, 06 "
              "Nov 2024 01:54:27 GMT (7:54 PM CST). The Wayback CDX for co.grayson.tx.us from Nov 5 to Nov 26, 2024 (53 files) lists no unofficial "
              "precinct report for this election (it does list the September 14, 2024 Sherman special election's unofficial precinct report, "
              "showing the archive would have caught such a file in these folders).")
r['sources'].append({
    'url': WB('20241106074851', ugr), 'via': 'wayback_branch',
    'content_hash': '3ddef87059d3be18b05d087dd0f61ed03067da3b7eaaed8029617b26cdc0b76e',
    'quote': "Summary Results Report UNOFFICIAL RESULTS | November 5, 2024 General Election Grayson County | Election Day Precincts Reporting 0 of 41 | Election Summary - 11/05/2024 07:44PM | orig Last-Modified Wed, 06 Nov 2024 01:54:27 GMT",
    'supports': "2024_general LATER: first election-night county-totals release (printed 7:44 PM, uploaded 7:54 PM CST); wayback-data phase1/targeted/sweep/Grayson/2024_general_20241106074851_c0897b1595.pdf",
})
r['notes'] += (' ' + NOTE + "2024_general unchanged (LATER, check 2), strengthened by a second election-night county-totals file from the sweep "
               "(printed 7:44 PM, uploaded 7:54 PM CST); county_totals_first_seen moved to 7:44 PM. Other Grayson replays are the Sept 14, 2024 "
               "Sherman special election (its unofficial precinct-by-precinct report, printed 09/14/2024 08:32PM, has original Last-Modified Sun, 15 Sep 2024 02:03:01 GMT, 9:03 PM CDT that election night, so Grayson has "
               "posted unofficial precinct reports on an election night before; no such file for Nov 5, 2024 is in the archive), road plans and "
               "notices. 2026 primary and runoff: sweep CDX queries timed out; unchanged.")
save(c, r)

# ---------------- Williamson ----------------
c = 'Williamson'; r = load(c)
r['notes'] += (' ' + NOTE + "No election changed. The sweep (phase1/targeted/sweep/Williamson/index.json) adds no second election: the only "
               "election-night replay is the already-used Index_11 capture (8:25 PM CST); a second Index_11 capture (20260304160436) shows 'updated "
               "3/4/2026 4:03:37 AM' (Last-Modified 4:03:40 AM CST), after the election-night window. 2024 general replays are early-voting "
               "summaries and polling-place PDFs whose DocumentCenter Last-Modified equals the capture time (request-time stamping, no upload "
               "evidence); 2026 runoff replays are an early-voting summary (timed out), a turnout spreadsheet (9:49 AM May 26) and a notice. The "
               "sweep found no livevoterturnout williamsontxenr captures for 2024 or the runoff (CDX queries timed out).")
save(c, r)
