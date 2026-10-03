import json
N = {
"Caldwell": {
 "2024_general": "same (UNDETERMINED): no election-night file survives; the only election-night Wayback capture is the retired 2016 to 2018 page.",
 "2026_primary": "same (LATER, check 2): county totals with election-day votes uploaded 10:44 PM CST Mar 3; the unofficial PCTbyPCT reports were uploaded 9:47 AM CST Mar 4. Quoted counts (REP 3,618 61 2,206 1,351; 7:14 PM summary with Election Day 0) checked and supported.",
 "2026_runoff": "same (LATER, check 2): county totals printed 8:57 PM (DEM 8:56 PM, checked), uploaded 9:10 PM CDT; precinct reports created May 28, uploaded May 29.",
 "unsupported_claims": "None found. Not checked by me: the 2024 'FINAL_PCTbyPCT11052024.pdf' Last-Modified 11 Dec 2024 (official file, does not affect the result). The notes still carry the superseded first-pass sentence that the election-night summary files 'were not opened'."},
"Crockett": {
 "2024_general": "same (UNDETERMINED): no 2024 files on the Elections page; no wayback folder.",
 "2026_primary": "same (LATER, check 2): scanned county-totals summary printed 'Election Summary - 03/03/2026 07:44PM', uploaded Mar 4 10:07 AM CST; no precinct results posted.",
 "2026_runoff": "same (LATER, check 2): scanned county-totals summary printed 'Election Summary - 05/26/2026 07:16PM', uploaded May 27; no precinct results posted.",
 "unsupported_claims": "None found; the quoted Paxton and Cornyn rows match the page images."},
"Lamb": {
 "2024_general": "same (UNDETERMINED): no files listed; the CDX query for this window failed (connection refused), so check 3 is incomplete rather than empty.",
 "2026_primary": "same (UNDETERMINED): no files listed; CDX query failed as above.",
 "2026_runoff": "same (LATER, check 2): scanned 'ELECTION UNOFFICIAL SUMMARY' printed 05/26/2026 9:04 PM, uploaded May 27 1:56 PM CDT; the PCT links are sample ballots; no precinct results posted. Quoted counts checked on page images.",
 "unsupported_claims": "None found. The web search mentioned in the notes is not checkable from sources (search text is not evidence; no effect on results)."},
"Menard": {
 "2024_general": "same (UNDETERMINED): the linked 'Menard County 2024 Nov 5 ENR.pdf' returns 404 (also on the cira mirror); Wayback CDX was robots-blocked.",
 "2026_primary": "same (LATER, check 2): cumulative county-totals report, Run Time 8:48 PM, uploaded 8:56 PM CST Mar 3; no per-precinct sections; the 'SB ... Prt n' links are sample ballots.",
 "2026_runoff": "same (LATER, check 2): scanned cumulative county totals, Run Time 7:38 PM / 7:40 PM, uploaded 8:35 PM CDT May 26; no precinct results posted.",
 "unsupported_claims": "None found."},
"Val Verde": {
 "2024_general": "same (UNDETERMINED): the unofficial summary is printed 11/06/2024 2:58 PM, after election night; no Wayback captures.",
 "2026_primary": "same (LATER, check 2): scanned county-totals summary printed 03/03/2026 9:35 PM (no upload time on CivicPlus); precinct numbers only in the official precinct-by-precinct report. Quoted 'Ballots Cast - Total 6,180 195 4,135 1,850' checked and supported.",
 "2026_runoff": "same (LATER, check 2): scanned county-totals summary printed 05/26/2026 8:27 PM, total 1,520 equal to the reconciliation; precinct numbers only in the official report.",
 "unsupported_claims": "None on results. Minor: the notes say valverdecounty.org returned 403 and www.valverdecounty.texas.gov was refused; on 2026-10-02 both loaded for me (valverdecounty.org serves the same home page as valverdecounty.texas.gov), so those were transient and do not affect the results."},
}
for c, n in N.items():
    fn = f"phase1/verification/{c.replace(' ', '_')}.json"
    v = json.load(open(fn))
    ev = json.load(open(f"phase1/evidence/{c.replace(' ', '_')}.json"))
    v["research_tag"] = ev["tag"]
    v["agree"] = ev["tag"] == v["verifier_tag"]
    v["comparison_notes"] = n
    for e in ("2024_general", "2026_primary", "2026_runoff"):
        assert ev["elections"][e]["result"] == v["elections"][e]["result"], (c, e)
    txt = json.dumps(v, indent=1, ensure_ascii=False)
    assert "—" not in txt and "–" not in txt
    open(fn, "w").write(txt + "\n")
    print(c, v["research_tag"], v["verifier_tag"], v["agree"])
