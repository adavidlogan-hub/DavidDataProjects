# Phase 1 run issues log

Issues reported by agents during the full run, kept for the final report.

## Batch 8 (research-8, Tom Green to Zavala; 27 counties, 29.2 min, 342,871 agent tokens)
- Check 3 not possible during the run: wayback-data branch not yet published (harvest still running). All elections not settled by checks 1 or 2 are UNDETERMINED with "check 3 pending".
- Unreadable county sites: Wichita (403 on every page), Van Zandt (fetch module refused: robots.txt disallowed or unreachable), Wood (empty 202; settled by Clarity instead).
- Dead or moved seed URLs: Tom Green, Val Verde, Webb, Wheeler, Victoria, Williamson.
- No upload-time evidence (server returns request time or no Last-Modified): CivicPlus DocumentCenter (Webb, Winkler, Val Verde) and /page/open/ hosts (Tom Green, Upshur, Zavala).
- Wise: www.co.wise.tx.us refused by the fetch module; pages read on the county's ems.co.wise.tx.us host instead. Wise Clarity elections.json returned 403.
- Williamson: election-night results on livevoterturnout.com show only one final update time (no history); its single Clarity listing (May 2026 runoff, EID 127277) has updates dated Aug 27 2026 and later.
- Washington runoff left UNDETERMINED: precinct report printed 9:38 PM election night but uploaded 11:17 AM next day.
- Scanned PDFs read by rendering page 1 to an image (Ward, Webb, Wilson).
- Rule breach: one direct curl to vanzandtcounty.org/robots.txt outside the fetch module (connection reset, nothing used).

## Vendor agent (113 vendor-county rows across 72 counties; Clarity presence for all 254)
- Clarity elections.json is unreliable as a fingerprint: 30 counties return 200 (22 non-empty lists, 8 empty: Bexar, Hunt, Jefferson, Kendall, Lubbock, Montague, Parker, Victoria), 221 return 404, 3 return 403 (Liberty, Potter, Wise). Clay and Robertson have Clarity folders without elections.json. Tarrant lists only May 2025 although its site links 2024 and 2026 Clarity elections.
- The build container's egress proxy refuses plain http:// requests ("Host not in allowlist"). 173 SOS-listed county URLs are http://; 137 loaded over https. Counties whose sites are http-only cannot be read from this container (the Windows laptop is not affected).
- soesoftware.com and scytl.us return empty 202 (bot challenge); businesswire.com 403; Dallas civicweb agenda disallowed by robots.txt (Dallas Scytl renewal remains a search lead only).
- Added source: TX SOS "Voting Systems by County" PDF (revised 09/01/2026): ES&S 141 counties, Hart 113.
- Rule breach: one direct curl to www.co.zavala.tx.us outside the fetch module (403, unused).
