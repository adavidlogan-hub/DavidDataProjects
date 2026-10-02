import json, sys
sys.path.insert(0, '.')
from phase1.schema import compute_tag, compute_confidence, validate_v2
A = "targeted3-E"
N = {
 "Uvalde": "no change. Tried: Wix sitemap of www.uvaldecounty.gov (pages-sitemap.xml lists only the 'elections' page, no results page); uvaldecounty.com home (Wix, links only to the .gov Elections page); one web search (found an old uvaldecounty.com/images/elections_admin/.../Results/Cumulative_Results-11-7-2023 PDF, which now returns HTTP 404, so the old results folder is gone). Wayback harvest of uvaldecounty.com found no election-night captures. Sweep: no folder. All three elections stay UNDETERMINED.",
 "Leon": "no change. Re-listed the Elections page: for the 2026 runoff only '05/26/26 Official Precinct Report-Group Detail' (prefix 062226), '05/26/26 Canvass Totals', a 'PRELIMINARY ELECTION RECONCILIATION UNOFFICIAL TOTALS' form (ballot counts, not candidate totals, so not a county-totals results file under rule 43), voter lists and notices; no unofficial runoff results file. Wayback harvest of co.leon.tx.us found no election-night captures. Sweep: no folder. 2026_runoff stays UNDETERMINED; tag stays UNKNOWN (2024_general END, 2026_primary LATER).",
 "Dimmit": "no change. Re-fetched the Elections page (same content hash b53aa717...): only the canvassed runoff results (upload stamp 2026-08-25), primary hand-count audit and notices; no 2024 general items. Wayback harvest found no election-night captures (runoff CDX query failed: connection refused). Sweep: no folder. All three stay UNDETERMINED.",
 "Delta": "no change. www.deltacountytx.com Election Results page still returns HTTP 403 (bot protection, not worked around). One web search for third-party precinct results found only Delta County, Colorado and old KETR stories. Wayback harvest of deltacountytx.com found no election-night captures. Sweep: no folder. All three stay UNDETERMINED.",
 "Hansford": "no change. Re-fetched the Elections page (same content hash 96ef9d58...): still no results files for any of the three elections. Wayback harvest of co.hansford.tx.us found no election-night captures (runoff CDX query failed: connection refused). Sweep: no folder. All three stay UNDETERMINED.",
 "Kent": "no change. Re-fetched the Elections page (new content hash 1b28f449..., adds November 3 2026 general election notices only): results still limited to the certified March 2026 primary results; nothing for the 2024 general or the runoff. No Wayback harvest folder for Kent on the wayback-data branch. Sweep: no folder. All three stay UNDETERMINED.",
}
for c, s in N.items():
    p = f"phase1/evidence/{c}.json"
    d = json.load(open(p))
    d["notes"] = d["notes"] + f" Targeted pass 3 2026-10-02 ({A}): {s}"
    assert d["tag"] == compute_tag(d["elections"])[0] and d["confidence"] == compute_confidence(d)
    validate_v2(d)
    json.dump(d, open(p, "w"), indent=2, ensure_ascii=False); open(p, "a").write("\n")
    print(c, d["tag"], d["confidence"])
