import json, sys, copy
sys.path.insert(0, '.')
from phase1.schema import compute_confidence, compute_tag
NOW = sys.argv[1]
notes = {
 "Tyler": {
  "research_tag": "COUNTY_ONLY_PRECINCT_AT_CANVASS", "agree": True,
  "comparison_notes": {
   "2024_general": "Same (UNDETERMINED). Both found the 2024 links dead (HTTP 404) and no election-night file; Wayback harvest has no captures (the index records robots_disallowed_or_unreachable for every query, which research words as 'no election-night captures').",
   "2026_primary": "Same (LATER, check 2, county_totals_first_seen 2026-03-03 22:07 CT). Same file, same reading: county contest totals only, footer 10:07 PM, Last-Modified 04 Mar 2026 18:40:46 GMT, no precinct report. Research's DEM-page footer '10:12 PM' is correct; my blind fact said '10:13 PM', and a higher-resolution render of pages 14, 16 and 22 shows 10:12 PM.",
   "2026_runoff": "Same (UNDETERMINED). The runoff 'UNOFFICIAL RESULTS' label has no link; 'OFFICIAL RESULTS' goes to the SOS turnout site.",
   "unsupported_claims": "None that affect results. Research notes still contain the stale sentence that the primary scan 'could not be read without OCR' and 'Check 3 pending (origin/wayback-data branch not found)', both superseded later in the same notes."}},
 "Scurry": {
  "research_tag": "COUNTY_ONLY_PRECINCT_AT_CANVASS", "agree": True,
  "comparison_notes": {
   "2024_general": "Same result (UNDETERMINED), different fact. Research says there are no 2024 general results on the Election Information or Previous Elections pages ('which ends with the March 5, 2024 primary'). The Previous Elections page I fetched (hash 31a964e0...) has a 'NOVEMBER 5, 2024 GENERAL ELECTION' section linking 'Official Election Summary Results' (/upload/page/0166/Scan_20250617.pdf) and 'Official Precinct Summary Results' (/upload/page/0166/widgets/Scan_20250616.pdf). These are official files, so the result is still UNDETERMINED.",
   "2026_primary": "Same (LATER, check 2, county_totals_first_seen 2026-03-03 20:06 CT). Same files and times: county totals footer 03/03/2026 8:06 PM; four precinct reports footer 08/24/2026 12:01 PM, Last-Modified 24 Aug 2026.",
   "2026_runoff": "Same (UNDETERMINED). Both read summary and precinct reports printed 06/02/2026 and uploaded Jun 11 and Aug 24 2026.",
   "unsupported_claims": "Research 2024 fact and notes ('No results for the 2024 general ... are posted'; Previous Elections page 'ends with the March 5, 2024 primary') are not supported: the Previous Elections page lists official Nov 2024 summary and precinct scans. No effect on the result."}},
 "Coleman": {
  "research_tag": "COUNTY_ONLY_PRECINCT_AT_CANVASS", "agree": True,
  "comparison_notes": {
   "2024_general": "Same result (LATER), different check label. I settled it by check 2: the live CIRA copy of 'UNOFFICIAL ALL PRECINCTS coleman county.pdf' (same sha256 9ae01f73... as the Wayback capture) has server Last-Modified 06 Nov 2024 02:41:05 GMT (8:41 PM CST) and footer 11/05/2024 8:00 PM; research used check 3 (the 1:42 AM CST capture of the same file) with county_totals_first_seen 20:00 CT (printed time). Both show county totals only and the only precinct file is the official report printed 11/12/2024, uploaded 15 Nov 2024. Either label gives the same tag and med confidence (the runoff is check 2).",
   "2026_primary": "Same (UNDETERMINED). Unofficial files printed 03/05 and 03/10/2026, uploaded 21 Apr 2026.",
   "2026_runoff": "Same (LATER, check 2). Same file and times (footer 8:02 PM, Last-Modified 00:39:30 GMT = 7:39 PM CDT; both noted the clock inconsistency). Research county_totals_first_seen 20:02 CT (printed), mine 19:39 CT (upload); both on election night.",
   "unsupported_claims": "None found. The research quote of the 2024 file and the runoff file matched what I read."}},
 "Howard": {
  "research_tag": "COUNTY_ONLY_PRECINCT_AT_CANVASS", "agree": True,
  "comparison_notes": {
   "2024_general": "Same (LATER, check 2, county_totals_first_seen 2024-11-05 21:31 CT). Same file ENR w WI.pdf, footer 9:22 PM, Last-Modified 03:31:53 GMT; no precinct file listed for 2024.",
   "2026_primary": "Same (UNDETERMINED). Only canvass files.",
   "2026_runoff": "Same (LATER, check 2, county_totals_first_seen 2026-05-26 20:32 CT). ENR.pdf county totals printed 8:32 PM; uploaded 8:56 AM May 27; no unofficial precinct report, only the June 3 canvass table. I confirmed research's PDF ModDate 2026-05-27 13:50:15 UTC.",
   "unsupported_claims": "None on facts. The research notes are internally stale: the targeted pass 3 sentence says '2026_runoff stays UNDETERMINED', while the election record (updated under DECISIONS 67) is LATER; the record, not the note, matches the evidence."}},
}
for c, n in notes.items():
    p = f"phase1/verification/{c}.json"
    d = json.load(open(p))
    d["research_tag"] = n["research_tag"]; d["agree"] = n["agree"]
    d["comparison_notes"] = n["comparison_notes"]; d["compared_at_utc"] = NOW
    s = json.dumps(d, indent=2, ensure_ascii=False)
    assert "—" not in s and "–" not in s
    open(p, "w").write(s + "\n")

# Jasper: DECISIONS 44 correction
p = "phase1/verification/Jasper.json"
d = json.load(open(p))
d["blind_verdict"] = {"verifier_tag": d["verifier_tag"], "verifier_confidence": d["verifier_confidence"],
                      "elections": copy.deepcopy(d["elections"]), "rationale": d["rationale"]}
d["elections"]["2024_general"] = {"result": "LATER", "check": "2", "county_totals_first_seen": "2024-11-06 00:26 CT",
 "fact": "Corrected after the blind pass (DECISIONS 44); my blind pass did not find these files, which are in the county's CIRA upload folder page 1130 and not linked from the current Elections page. 'UNOFFICIAL SUMMARY RESULTS.pdf' (newtools.cira.state.tx.us/upload/page/1130/, sha256 73db3325...): scanned 'Summary Results Report UNOFFICIAL RESULTS JASPER COUNTY GENERAL ELECTION November 5, 2024', county totals ('Election Day Precincts Reporting 23 of 23', 'Ballots Cast - Total 20,134'), footer 'Election Summary - 11/06/2024 12:26 AM' on all 5 pages (election night), Last-Modified Wed, 06 Nov 2024 14:07:14 GMT (8:07 AM CST). '11-5-24 Unofficial Pct by Pct Results.pdf' (sha256 6479e864...): per-precinct candidate votes with an Election Day column ('Pct # 1 Three Corners ... REP Donald J. Trump/JD Vance 42 3 6 33'), footer 'Precinct Summary - 11/06/2024 12:32 AM', Last-Modified Thu, 07 Nov 2024 16:28:15 GMT (10:28 AM CST Nov 7). County totals printed on election night; the only precinct report's known upload time is after election night: LATER under the rule 43 reading (DECISIONS 67)."}
d["sources"] += [
 {"url": "https://newtools.cira.state.tx.us/upload/page/1130/UNOFFICIAL%20SUMMARY%20RESULTS.pdf", "content_hash": "73db33256f3c3d1661b910e50824182ccd016646e02911d8088bfde66a3d05dc", "what_i_checked": "Opened after the blind pass (cited by research): county totals, footer 11/06/2024 12:26 AM, Last-Modified 06 Nov 2024 14:07:14 GMT"},
 {"url": "https://newtools.cira.state.tx.us/upload/page/1130/11-5-24%20Unofficial%20Pct%20by%20Pct%20Results.pdf", "content_hash": "6479e86404bb7f7348e7e12242c3e46051bf6e394dae3bfc26042648c8a2861b", "what_i_checked": "Opened after the blind pass (cited by research): per-precinct report, footer 11/06/2024 12:32 AM, Last-Modified 07 Nov 2024 16:28:15 GMT"}]
tag, single = compute_tag(d["elections"])
d["verifier_tag"] = tag
d["verifier_confidence"] = compute_confidence({"county": "Jasper", "elections": d["elections"]})
d["rationale"] = "After the DECISIONS 44 correction only the 2024 general is determined (LATER, check 2: county totals printed 12:26 AM on election night, the unofficial precinct report printed 12:32 AM but uploaded 10:28 AM Nov 7). The 2026 primary (unofficial totals printed 8:31 AM Mar 4) and runoff (official files only) stay UNDETERMINED. One determined election gives COUNTY_ONLY_PRECINCT_AT_CANVASS, low. Blind verdict (UNKNOWN) kept in blind_verdict."
d["research_tag"] = "COUNTY_ONLY_PRECINCT_AT_CANVASS"; d["agree"] = True
d["comparison_notes"] = {
 "2024_general": "Different in the blind pass (UNDETERMINED: the current Elections page has no 2024 files), same after correction. I opened the two page-1130 files research cites and they match its quotes and times exactly; corrected to LATER per DECISIONS 44.",
 "2026_primary": "Same (UNDETERMINED). Unofficial totals printed 03/04/2026 8:31 AM, uploaded 05 Mar 2026; official precinct report printed 03/10/2026.",
 "2026_runoff": "Same (UNDETERMINED). Only official runoff files (printed 05/28/2026).",
 "unsupported_claims": "None found. Note: research 2024 precinct_first_seen ('2024-11-07 10:28 CT ...') names the next-day upload time, which is after election night, not an election-night precinct time; this does not affect the LATER result."}
d["compared_at_utc"] = NOW
order = ["county","reason_selected","verifier_tag","verifier_confidence","elections","rationale","sources","written_blind_at_utc","blind_verdict","research_tag","agree","comparison_notes","compared_at_utc","previous_verification"]
d = {k: d[k] for k in order if k in d}
s = json.dumps(d, indent=2, ensure_ascii=False)
assert "—" not in s and "–" not in s
open(p, "w").write(s + "\n")
print("Jasper", tag, d["verifier_confidence"])
