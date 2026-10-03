import json
p = "phase1/verification/Ellis.json"
e = json.load(open(p))
e["sources"][0]["content_hash"] = "44a5541db084a48a909719407d7d117c4bfcd2ea7f251d743a7a64b4a38d707a"
e["research_tag"] = "LIVE_PRECINCT"
e["agree"] = False
e["comparison_notes"] = {
 "2024_general": "Same (UNDETERMINED): research and verifier both find only official canvass files and no archived election-night file.",
 "2026_primary": "Different: research LIVE (check 3, rule live_precinct_view), verifier END (check 3). Same file and same facts: both read the sweep replay of ellistxenr/5/en/Index_5.html captured 05:49:54 UTC Mar 4 (11:49 PM CST), original Last-Modified 05:34:47 GMT (11:34 PM CST), 'Website Updated: 3/3/2026 11:34:46 PM', Election Day complete, per-precinct candidate tables in the same page as the county totals. The difference is the reading of the live precinct view rule. As worded in CHECKLIST_BRIEF.md the rule needs a precinct view that 'loads its numbers from the same live, refreshing data feed as the county totals' (example: a tab requesting per-precinct vote files with a cache-busting time, the Harris case of DECISIONS 39). The Ellis page loads no precinct data: the precinct numbers are fixed markup in one static publication (the only data request is the map layer ../ellistxenr_5.txt; refresh is a full page reload). One archived copy of such a page shows precinct numbers in exactly one election-night publication, made after Election Day reporting was complete, which is END under rule 47 (upload time on election night). It meets the rule only under the DECISIONS 61b extension (Williamson: same livevoterturnout page type accepted as a judgment call flagged for verifier and owner). Research itself states 'rule 47 alone, with one observed release, would give END'. This is a rule-reading disagreement, not a blind miss (the verifier opened the cited file blind), so DECISIONS 44 does not apply and no blind_verdict correction is made. If the owner confirms 61b for self-contained livevoterturnout pages, the verifier's facts give LIVE and the tags would agree.",
 "2026_runoff": "Same (UNDETERMINED): no election-night runoff file; current vendor pages last modified 3 Jun 2026; the only runoff-window capture (Index_8) is the May 2 election page captured before polls closed. Research fact mentions only Index_9 and the PDFs, the verifier also checked Index_10 (Last-Modified 3 Jun 2026 20:12:04 GMT); no effect.",
 "research_claims_checked": "Supported: 60 precincts with DEM US Senator votes and their sum 18,649 of 18,806 ballots (verifier recount from the saved file: 60 tables, all nonzero, sum 18,649); Last-Modified and Website Updated times; hdnAutoRefresh 600 and hdnPrecinctLevelResults 1 quotes; Index_8 is the May 2 page. Not supported or outdated: notes say every co.ellis.tx.us page returned HTTP 403, but the verifier's fetch of co.ellis.tx.us/1228/November-5-2024-General-Election returned 200 today (time-dependent, no effect on results). The research description of the page as 'the live auto-refreshing results publication' is accurate, but the claim that it meets the live precinct view rule rests on DECISIONS 61b, not on the CHECKLIST_BRIEF.md wording (see 2026_primary)."
}
json.dump(e, open(p, "w"), indent=1, ensure_ascii=False); open(p, "a").write("\n")

p = "phase1/verification/Guadalupe.json"
g = json.load(open(p))
g["research_tag"] = "COUNTY_ONLY_PRECINCT_AT_CANVASS"
g["agree"] = True
g["comparison_notes"] = {
 "2024_general": "Same (UNDETERMINED): only official files (pct by pct Last-Modified 21 Nov 2024) and no archived election-night file.",
 "2026_primary": "Same (LATER, check 2): same deciding file, 'Unofficial  Results Early Voting and Mail Ballots 5 of 36.pdf', county totals only, printed 03/03/2026 8:33 PM, Last-Modified 03:06:04 GMT Mar 4 (9:06 PM CST). The verifier also fetched the county copy live: HTTP 200, identical hash 005be967..., same Last-Modified, so the upload time is confirmed from the county server today as well as from the replay. Both find no precinct report for this election (official primary reports on the history page are summaries).",
 "2026_runoff": "Same (UNDETERMINED): only the official summary (printed 06/08/2026) and unrelated sweep captures.",
 "research_claims_checked": "Supported: printed time, Last-Modified times, page contents of pages 1, 2 and 31, reconciliation form contents and upload time, Clarity listing does not include target elections, sweep replay outcomes. Not supported by a source: research calls the '36 of 36' file a summary ('lists only the 5 of 36 and 36 of 36 summaries'), but its replay timed out and the county copy is HTTP 404 today, so its content is unseen; the title only suggests the same summary series. If it held precinct pages uploaded on election night the primary would not be LATER; this residual uncertainty applies to both research and verifier and does not change the result under the DECISIONS 67 reading. Also unseen: the election-night copy of elections.election3 (replay timed out), so the page's links that night are not known."
}
json.dump(g, open(p, "w"), indent=1, ensure_ascii=False); open(p, "a").write("\n")
for p in ("phase1/verification/Ellis.json", "phase1/verification/Guadalupe.json"):
    s = open(p).read()
    assert "\u2014" not in s and "\u2013" not in s
    json.loads(s)
print("ok")
