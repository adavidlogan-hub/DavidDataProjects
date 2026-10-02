import json, sys, datetime
sys.path.insert(0, '.')
from phase1.schema import compute_tag, compute_confidence
B = "https://www.co.pecos.tx.us/wp-content/uploads/"
el = {
 "2024_general": {"result": "UNDETERMINED", "check": "none",
   "fact": "Not on Clarity (elections.json 404). The WordPress media log for 2024-10-28 to 2024-12-01 lists no election-night upload: the only upload on Nov 5 2024 is appointment-fees-2024-10.pdf at 15:20 local; the first results file is Official-Results-20241105.pdf uploaded 2024-11-12 19:51 local (date_gmt 2024-11-13 01:51). A media search for 'unofficial' returns only 2026 files. No Wayback election-night captures (index.json captures empty for all three windows); no targeted sweep folder for Pecos. No election-night county-totals file survives, so rule 43 gives UNDETERMINED, not LATER."},
 "2026_primary": {"result": "LATER", "check": "2", "county_totals_first_seen": "2026-03-03 22:13 CT",
   "fact": "WordPress media log 2026-03-03 12:00 to 2026-03-05 00:00 lists exactly three uploads: 20260303-Unofficial-Results-EV-Totals.pdf (2026-03-03 18:56:49 local), 20260303-Unofficial-Results-to-include-Election-Day.pdf (2026-03-03 22:13:46 local, date_gmt 2026-03-04 04:13:46; server Last-Modified Wed, 04 Mar 2026 04:13:46 GMT), 20260303-Preliminary-Election-Reconciliation-Unofficial-totals.pdf (2026-03-04 08:11:24, after election night). The election-day file is a 27-page scan (no text layer; read from page images): every page headed 'Summary Results Report / 2026 Primary Election / March 3, 2026 / UNOFFICIAL RESULTS to include Election Day / Pecos County, Texas', contest tables with TOTAL and VOTE % columns only (county totals), footer 'Election Summary - 03/03/2026 9:49 PM', pages 2 of 28 to 28 of 28. No per-precinct candidate votes uploaded on election night. Precinct-level files (20260303-Official-Results-Precinct-by-Precinct-Democratic.pdf and -Republican.pdf) sit in the uploads/2026/04/ folder, i.e. uploaded in April 2026."},
 "2026_runoff": {"result": "LATER", "check": "2", "county_totals_first_seen": "2026-05-26 22:59 CT",
   "fact": "WordPress media log 2026-05-26 12:00 to 2026-05-28 00:00 lists four uploads: 20260526-Unofficial-Results.pdf (2026-05-26 18:55:08 local), 20260526-Unofficial-Results-including-Election-Day.pdf (2026-05-26 22:59:17 local, date_gmt 2026-05-27 03:59:17; server Last-Modified Wed, 27 May 2026 03:59:17 GMT), and two files at 2026-05-27 21:16:53 (Preliminary Election Reconciliation, Notice of Post-Election Hand Count Audit). The election-day file is a 5-page scan read from page images: pages 1 to 4 'Summary Results Report / 2026 Primary Runoff Election / May 26, 2026 / UNOFFICIAL RESULTS / Pecos County, Texas', columns TOTAL, Absentee, Early Voting, Election Day (county totals by vote type), statistics 'Election Day Precincts Reporting 9 of 9', footer 'Election Summary - 05/26/2026 10:01 PM'; page 5 is a 'PRECINCT BASED VOTING' office-to-precinct lookup table with no votes. No per-precinct candidate votes on election night. Precinct-level files (Official-Democrat-Precinct-by-Precinct-Results-for-05_26_2026.pdf, Official-Republican-Precinct-by-Precinct-Results-05_26_2026.pdf) are in uploads/2026/06/."},
}
for e in el.values():
    e.setdefault("county_totals_first_seen", "")
rec = {"county": "Pecos", "elections": el}
tag, single = compute_tag(el)
conf = compute_confidence(rec)
out = {"county": "Pecos", "reason_selected": "tag changed in targeted pass 3",
 "verifier_tag": tag, "verifier_confidence": conf, "elections": el,
 "rationale": f"Two elections (2026 primary, 2026 runoff) are LATER from check 2: the complete WordPress upload log for each election night shows only a county-totals Summary Results Report uploaded that night (10:13 PM CST and 10:59 PM CDT) and no precinct report until April and June. Nov 2024 has no surviving election-night file and no archive capture, so it is UNDETERMINED. Fixed rule gives {tag}; confidence {conf} (check 2 results).",
 "sources": [], "written_blind_at_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
 "agent": "verifier-11"}
src = [
 ("https://www.co.pecos.tx.us/wp-json/wp/v2/media?after=2024-10-28T00:00:00&before=2024-12-01T00:00:00&per_page=100", "ff3647ebcff24cd59248a286847878fc3e1f17fd5b02b0cdffe4998b31da7e33", "WordPress upload log Nov 2024: no election-night upload; first results file Nov 12"),
 ("https://www.co.pecos.tx.us/wp-json/wp/v2/media?after=2026-03-03T12:00:00&before=2026-03-05T00:00:00&per_page=100", "fa16823def08b0b9e7d4ebd13813f60e0bc323bddc595b19605beddec04ac8d2", "WordPress upload log March 2026 election night: three uploads, times"),
 ("https://www.co.pecos.tx.us/wp-json/wp/v2/media?after=2026-05-26T12:00:00&before=2026-05-28T00:00:00&per_page=100", "65c5bfaaaae6baea4196154d6b4d8c6b22af0210483b7c83b1433ed46f7abca7", "WordPress upload log May 2026 election night: four uploads, times"),
 ("https://www.co.pecos.tx.us/wp-json/wp/v2/media?search=unofficial&per_page=100", "881b8e81212de6a767ee6bd5198ddef03fb075c8aed8d5f0bb6b3348deb409ea", "All media titled unofficial: only 2026 files, none for Nov 2024"),
 (B+"2026/03/20260303-Unofficial-Results-to-include-Election-Day.pdf", "8be59354ac08295beb31df7afaeaf9d30218844fccb4363945cd0becb6d3c34d", "Scanned county-totals Summary Results Report, printed 03/03/2026 9:49 PM, Last-Modified 04 Mar 2026 04:13:46 GMT; read from rendered page images"),
 (B+"2026/03/20260303-Unofficial-Results-EV-Totals.pdf", "0930cc27c0fa52e88a1173fbed9c695dde5ffd0e61ff6ced2b6b68c8c586882f", "Early-vote totals upload 6:56 PM, before election night window"),
 (B+"2026/05/20260526-Unofficial-Results-including-Election-Day.pdf", "9f499a93afb69275091a00c0937ae8f92dc311929fedf433173a351027e58f23", "Scanned county-totals Summary Results Report, printed 05/26/2026 10:01 PM, Last-Modified 27 May 2026 03:59:17 GMT; read from rendered page images"),
 (B+"2026/05/20260526-Unofficial-Results.pdf", "b257074b300e97c8f809f9aec8b3b5b080451cb8afe8c396964d62704f17442e", "Early-vote totals upload 6:55 PM"),
 ("https://www.co.pecos.tx.us/election-information-past-elections/", "3074739cd2b8398bc560bf52c9f47e425d08b581e1b9453a767b11c29cf39866", "Past elections page lists official and precinct-by-precinct files in uploads/2026/04 and 2026/06 folders"),
 ("git:origin/wayback-data:phase1/wayback_snapshots/Pecos/index.json", "", "No election-night captures for any election"),
 ("https://results.enr.clarityelections.com/TX/Pecos/elections.json", "", "Clarity check 1 script: no Clarity election list (404)"),
]
out["sources"] = [{"url": u, "content_hash": h, "what_i_checked": w} for u, h, w in src]
json.dump(out, open("phase1/verification/Pecos.json", "w"), indent=2)
print(tag, conf)
