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

## Batch 1 (research-1, Anderson to Camp; 30 counties, 33.9 min, 400,758 agent tokens)
- Applied the stricter LIVE reading (election-day precinct votes only); this prompted DECISIONS 36 and the check 1 reconciliation pass.
- Bastrop runoff reporting units are combined polling places ("Poll 1" to "Poll 4"), not regular precincts; recorded as END.
- END from printed run time only (no upload time): Bandera, Burnet, Bowie runoffs.
- Egress proxy refused www.bosquecounty.gov ("Host not in allowlist") even with full network access; Bosque UNKNOWN.
- Bot protection (not circumvented): Aransas (Incapsula), Brazoria (Akamai 403), Bastrop (empty 202), Burleson ENR portal (Cloudflare).
- Bell: robots.txt disallows all agents, so its 2026 Clarity links could not be read from the county site.
- Dead links: Bailey 2024 and primary unofficial files; Briscoe 2024 unofficial file.
- Cameron and Angelina live results apps show only the current state (vote centers, no history).
- Two scanner clocks contradict printed times (Armstrong 2024, Brown 2024); noted in the records.

## Verification findings
- Clarity reporting units are not always voting precincts: Lamar's 2026 runoff units are ballot groups ("Lamar County", "County and Commissioner Pct 2/4"); Bastrop's runoff uses combined polling places ("Poll 1" to "Poll 4"). verifier-1 judged Lamar's runoff LATER on this basis; the disagreement sets Lamar to UNKNOWN. Check 1 counts any <Precinct> element; a future refinement would compare unit names with the county's precinct list.
- Verifier blind misses (verifier found the research-cited file only on comparison): Carson, Hardin, Live Oak (verifier-2); Freestone, Houston, Bexar 2024 (verifier-1). Corrected under DECISIONS 44 with blind verdicts kept.
- Research claims a verifier found unsupported: Crosby (runoff file exists), Zapata (2024 file exists), Floyd 2024 (state unofficial results file exists), Dimmit runoff (canvass PDF loads), Roberts primary (scan creation time is on election night).
- Clarity vote-type labels are not always reliable: Robertson's "Election Day" vote type is already full before polls close and never changes, while the election-day returns arrive under "EV Mail" (verifier-3). The check 1 election-day measure therefore read Robertson as one release (END); the verifier read it as LIVE. Disagreement sets Robertson to UNKNOWN. A future refinement: treat a vote type as election-day only if it grows after 7 PM.
- Research claims a verifier found unsupported (verifier-3): Scurry ("no 2026 primary results"; an unofficial summary printed 8:06 PM exists), Tyler (primary scan footer 10:07 PM not read), Bee (official cumulative report exists), Cooke (page also lists 2024 elections).
- Montague's Clarity detail.xml ElectionDate fields read 10/11/2024 and 5/12/2026 rather than the election dates; IDs came from the county's own links and ElectionName matches.

## Targeted pass (eight largest UNKNOWN counties)
- Williamson: nothing new decided. livevoterturnout pages embed per-precinct tables (hdnPrecinctLevelResults=1, auto-refresh 600 s) but the vendor keeps no older versions; only final stamps after each election survive. Pending lead: targeted extended Wayback captures of livevoterturnout.com/ENR/williamsontxenr (7 PM to 9 AM), which would decide each election from check 3. Community Impact (Mar 4 2026, 7 a.m.) reports precinct-reporting counts, not precinct numbers: lead only.
- Nueces: decided by the bounded Clarity ID search (DECISIONS 51): IDs 122486 (Nov 2024), 125938 (Mar 2026), 126381 (May 2026), confirmed by Region and ElectionDate. Check 1: 8 and 9 distinct election-night precinct releases (LIVE, LIVE); runoff precinct values protected throughout (LATER). Now LIVE_PRECINCT, high. Lead from targeted-Nueces: KRIS 6 link to Clarity EID 121711 (May 2024).
- Collin, Hays, Brazoria: nothing decided. Collin's election-night files were county summaries (names found by search, now 404); Hays's 2026 primary page captured at 8:35 PM shows county totals only, before election-day counting; Brazoria news shows county totals only. All three wait on the targeted archive results.
- Montgomery: 2026 primary LATER from a county cumulative (county totals) report printed 2:08 AM and uploaded 2:15 AM CST on election night, linked from Community Impact (new method: county file links inside news articles). Tag COUNTY_ONLY_PRECINCT_AT_CANVASS, low (one election). Caveat: the county's live results page elections.mctx.org/electioninfo/eResultsMain.aspx (redirects to election.mctx.org) is refused by this environment's proxy (502), so an election-night precinct listing there cannot be ruled out; the Windows laptop should check it directly.
- Bounded Clarity ID search results: Lubbock (all three; owner override), Parker 2024 (122585; Parker now LIVE_PRECINCT high), Jefferson (122828, 126017, 126276; LIVE in all three, LIVE_PRECINCT high). No IDs in range for Williamson, Clay, Guadalupe, Potter, Wise, Liberty.
