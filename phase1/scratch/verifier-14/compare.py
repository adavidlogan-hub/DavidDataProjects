import json, sys, re, copy, datetime
sys.path.insert(0, '.')
from phase1.schema import compute_tag, compute_confidence
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
N = {
"Cottle": {
 "2024_general": "Same: LATER by check 2. Same files (content hashes 131d71f9 and b96ce364 match research's CIRA copies), same 9:38 PM printed county-totals time, same 2025-01-24 04:28:12 GMT upload of the precinct report.",
 "2026_primary": "Same: UNDETERMINED (only official files dated Mar 16 and Mar 24-25).",
 "2026_runoff": "Same: UNDETERMINED (SOS-form unofficial county totals with no printed time, uploaded May 27 1:46 PM CDT).",
 "unsupported_claims": "None on results. Minor: research says the www.co.cottle.tx.us election pages return the Home page; on my fetch http://www.co.cottle.tx.us/page/Elections redirected to https://www.cottlecountytx.gov/page/Elections and the Elections.2026 and Elections.Archive pages there returned the real lists (the site may have changed, or research used a different URL form). Research fills precinct_first_seen for 2024 with the Jan 2025 upload time (2025-01-23 22:28 CT), which is not an election-night time; harmless but the field is meant for election-night sightings."},
"Live Oak": {
 "2024_general": "Same: LIVE by check 2 (per-precinct unofficial PDFs uploaded one by one on election night). Research's precinct_first_seen 21:36 CT (Simmons) is later than the earliest upload I found: Pct 1 Argenta and Pct 14 SW George West at 03:08:51 and 03:09:24 GMT (9:08-9:09 PM CST). Research's Lagarto run time 10:32 PM is correct; my blind fact said 10:37 PM (that is its upload time), a misread on my side.",
 "2026_primary": "Same: LATER by check 2 under the DECISIONS 67 reading. Printed run time on 'Election Night Results' reads 11:09 PM on my zoomed render (research says 11:03 PM); both on election night, result unaffected. Research's fact sentence 'no file posted on election night survives' sits beside the LATER ruling and reflects the earlier rule 43/47 analysis, not a contradiction of the result.",
 "2026_runoff": "Same: LATER by check 2 (county cumulative run 9:38 PM, uploaded 9:48 PM CDT; no precinct report).",
 "unsupported_claims": "None material. Research notes say 'Precincts Reporting 14 of 14' for the primary election-night report; not checked closely (header text blurred) and not result-relevant."},
"Hutchinson": {
 "2024_general": "Same: END by check 2. Blind I used the printed time (no usable upload time on the Umbraco site); research's CIRA copy (byte-identical, hash 2b053677) has original Last-Modified 06 Nov 2024 04:27:09 GMT (10:27 PM CST), which I confirmed, so END now rests on an election-night upload time.",
 "2026_primary": "Different blind, corrected after checking (DECISIONS 44). Blind I had END from the printed 10:08 PM precinct report, treating the August 2026 Umbraco Last-Modified as no upload time. Research cites the county's earlier CIRA page (newtools.cira.state.tx.us/page/hutchinson.ElectionInformation), which I opened: 'Voter Turnout/Precinct by Precinct Republican.pdf' (same hash 4c698052) has Last-Modified Wed, 04 Mar 2026 15:10:14 GMT (re-confirmed with a conditional request, HTTP 304) and the Democratic one 15:10:20 GMT, i.e. 9:10 AM CST Mar 4, while 'Unofficial Summary Republican' (hash 2a7ed0b4, printed 10:13 PM) has 04:29:33 GMT (10:29 PM CST Mar 3). Under the DECISIONS 67 reading this is LATER. Corrected to LATER; blind result kept in blind_verdict.",
 "2026_runoff": "Same: END by check 2. CIRA copy 2026 Runoff/Precinct by Precinct Republican.pdf (hash 3a7ca886) Last-Modified 27 May 2026 02:48:23 GMT (9:48 PM CDT), consistent with my blind scan time 9:47 PM CDT.",
 "unsupported_claims": "None. All CIRA Last-Modified values research quotes match the fetch records I read."},
"Zapata": {
 "2024_general": "Same: LATER by check 2 (cumulative county totals run 10:55 PM, uploaded 11:25 PM CST; no 2024 precinct file).",
 "2026_primary": "Different: research UNDETERMINED, verifier LATER. The 'ZAPATA COUNTY UNOFFICIAL - MARCH 2026 - DEM/REP' files are county-totals 'Cumulative Results Report' scans with printed 'Run Time 10:15 PM Run Date 03/03/2026' (zoomed render), and no unofficial precinct report was ever posted. DECISIONS 67 (i) accepts a printed run time on election night on a county-totals file, so LATER even though the upload was Mar 4 2:42 PM CST. Research's fact mentions only the upload time.",
 "2026_runoff": "Different: research UNDETERMINED, verifier LATER. '2026 Primary Runoff Election - unofficial' is a county-totals 'Cumulative Results Report' with printed 'Run Time 11:10:25 PM Run Date 05/26/2026', 7 of 7 precincts; no unofficial precinct report posted. LATER on the printed run time under DECISIONS 67, despite the May 28 upload.",
 "unsupported_claims": "None false. Research's primary and runoff facts omit the printed election-night run times that decide these elections under DECISIONS 67. The page label 'March 26, 2026 - Primary Runoff Election' quoted by research is confirmed on the home page. Tag agrees (COUNTY_ONLY_PRECINCT_AT_CANVASS) but with three LATER elections confidence computes to med, not research's low."},
"Dawson": {
 "2024_general": "Same: LATER by check 2 (7:09 PM county totals uploaded 7:25 PM CST; no unofficial precinct report).",
 "2026_primary": "Same: END by check 2 (Dem precinct report uploaded 11:59 PM CST, Rep 12:02 AM CST, each once with the final count).",
 "2026_runoff": "Same: END by check 2 (Rep precinct report run 9:35 PM uploaded 9:54 PM CDT; Dem uploaded 9:51 PM CDT).",
 "unsupported_claims": "None. All quoted times and Last-Modified values match my reads."},
}
for county, notes in N.items():
    fn = county.replace(" ", "_")
    v = json.load(open(f"phase1/verification/{fn}.json"))
    r = json.load(open(f"phase1/evidence/{fn}.json"))
    if county == "Hutchinson":
        v["blind_verdict"] = {"verifier_tag": v["verifier_tag"], "verifier_confidence": v["verifier_confidence"],
                              "elections": copy.deepcopy(v["elections"]), "rationale": v["rationale"]}
        v["elections"]["2026_primary"] = {"result": "LATER", "check": "2",
            "fact": "Corrected after the blind pass (DECISIONS 44) from the file research cites: county's earlier CIRA election page newtools.cira.state.tx.us/page/hutchinson.ElectionInformation; 'Voter Turnout/Precinct by Precinct Republican.pdf' (byte-identical to the current copy, hash 4c698052, printed 10:08 PM) has Last-Modified Wed, 04 Mar 2026 15:10:14 GMT (9:10 AM CST Mar 4) and the Democratic one 15:10:20 GMT; 'Unofficial Summary Republican' (hash 2a7ed0b4, county totals printed 10:13 PM) has Last-Modified Wed, 04 Mar 2026 04:29:33 GMT (10:29 PM CST Mar 3). County totals on election night, the only precinct reports uploaded the next morning: LATER (DECISIONS 67)."}
        v["rationale"] = ("Corrected per DECISIONS 44 after opening the CIRA copies research cites (original upload times): 2024 general END (precinct report uploaded 10:27 PM CST), 2026 runoff END (uploaded 9:48 PM CDT), 2026 primary LATER (summary uploaded 10:29 PM CST, precinct reports 9:10 AM next day). Two END elections: PRECINCT_END_OF_NIGHT, med. Blind verdict (END x3 on printed times) kept in blind_verdict.")
        v["corrected_after_blind_at_utc"] = NOW
        v["correction_files"] = ["https://newtools.cira.state.tx.us/page/hutchinson.ElectionInformation",
            "https://newtools.cira.state.tx.us/upload/page/10714/docs/Voter%20Turnout/Precinct%20by%20Precinct%20Republican.pdf",
            "https://newtools.cira.state.tx.us/upload/page/10714/docs/Voter%20Turnout/Precinct%20by%20Precinct%20Democrat.pdf",
            "https://newtools.cira.state.tx.us/upload/page/10714/docs/Voter%20Turnout/Unofficial%20Summary%20Republican.pdf",
            "https://newtools.cira.state.tx.us/upload/page/10714/docs/2024/2024%20General%20Precint%20by%20Precinct%20Unofficial%20Results.pdf",
            "https://newtools.cira.state.tx.us/upload/page/10714/docs/2026%20Runoff/Precinct%20by%20Precinct%20Republican.pdf"]
        tag, _ = compute_tag(v["elections"])
        v["verifier_tag"] = tag
        v["verifier_confidence"] = compute_confidence({"county": county, "elections": v["elections"]})
    v["research_tag"] = r["tag"]
    v["agree"] = (r["tag"] == v["verifier_tag"])
    v["comparison_notes"] = notes
    s = json.dumps(v, indent=2, ensure_ascii=False)
    assert not re.search("[–—]", s)
    open(f"phase1/verification/{fn}.json", "w").write(s + "\n")
    print(county, "research", r["tag"], r["confidence"], "| verifier", v["verifier_tag"], v["verifier_confidence"], "| agree", v["agree"])
