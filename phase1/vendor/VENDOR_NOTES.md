# Vendor agent notes (phase 1, agent id "vendor", 2026-10-02)

Public online sources only. Every fetch went through `txprecinct.get` (robots.txt enforced, cached, hashed). Every web search was checked with `txprecinct.searchlog check` first and recorded afterwards with `searchlog record --agent vendor` (35 queries recorded). Search text was used only as a lead; each row in `vendor_links.csv` quotes a fetched page, and the build script checked that every quote appears in the cached body behind its `content_hash`.

## Files

| File | What it holds |
|---|---|
| `vendor_links.csv` | 113 rows, 72 counties. One row per county, vendor and source. Columns as specified. |
| `clarity_presence.csv` | All 254 counties: status of `results.enr.clarityelections.com/TX/<County>/elections.json`, count of listed elections, flags for 11/5/2024, 3/3/2026 and 5/26/2026 (matched on the listing's `Date` field), and the election names with dates. |
| `clarity_root_probe.csv` | Extra: status of the Clarity county folder root `.../TX/<County>/` for all 254 counties. It catches Clarity sites that have no `elections.json`. |
| `sos_voting_systems_by_county.csv` | Extra: the voting system vendor and software version for each county, taken from the Texas SOS "Voting Systems by County" PDF (revised 09/01/2026, hash b53a0e07...). It covers all 254 counties: ES&S 141, Hart 113. This is a state source, not a vendor client list, so it is kept out of `vendor_links.csv`. It agrees with every Hart and ES&S row in `vendor_links.csv`. |

## What worked

1. **Clarity fingerprint.** `elections.json` returned 200 for 30 counties and 404 for 221. It returned 403 (nginx) for Liberty, Potter and Wise. Of the 30:
   - 22 have a non-empty list: Bastrop, Bell, Comal, Dallas, Denton, El Paso, Fort Bend, Galveston, Gregg, Guadalupe, Hidalgo, Hood, Kaufman, Lamar, Midland, Nueces, Rockwall, Rusk, Tarrant, Travis, Williamson, Wood.
   - 8 return an empty list `[]`: Bexar, Hunt, Jefferson, Kendall, Lubbock, Montague, Parker, Victoria.

   The root probe found 2 more Clarity folders that have no `elections.json`: Clay and Robertson. Both counties' own sites link to Clarity election IDs. Counts of listings that include each target election: 2024 general 15, 2026 primary 13, 2026 runoff 15. 16 of the 254 `elections.json` responses came from the shared cache. Other agents had fetched them earlier the same day, between 14:21 and 15:15 UTC.
2. **County pages that link to vendor-hosted results.** I scanned every cached HTML page in the shared fetch cache, including pages other agents fetched, for links to vendor hosts. I then fetched the SOS-listed county website for each of 239 counties, plus up to 2 election or results subpages per county, and scanned those too. This produced most of the county_site rows:
   - Clarity: 18 counties.
   - ES&S product or how-to-vote links: 16.
   - Hart Verity links: 7. An eighth Hart county_site row, Comal, comes from its orders page, not from a link.
   - LiveVoterTurnout: Cameron, Ellis, Williamson.
   - Enhanced Voting: Comal results, Hays ballot tracker.
   - KnowInk Poll Pad: Austin.
   - ElectionLink turnout widget: Travis.
3. **Vendor press releases.**
   - Hart (hartintercivic.com, PRNewswire, one county-hosted PDF): 21 counties.
   - KnowInk news: Bexar and Dallas.
4. **Agendas and minutes.**
   - Midland: 10/10/2022 minutes approving a "Scytl software contract for election night reporting".
   - Harris: 2024 Hart Verity sole source.
   - Burleson: 2020 minutes covering KnowINK and Hart Poll Pads.
   - Comal: Hart Verity license orders for 2025 and 2026, from the county orders page.
5. **Civera / ElectionStats:** Jim Wells County's own launch notice (2025).
6. **VOTEC:** Votebeat news articles name 8 counties. These are voter registration (VEMACS) customers, not results reporting.

## Per vendor (counties in vendor_links.csv)

| Vendor | Counties |
|---|---|
| Clarity / Scytl / SOE | 30 |
| Hart InterCivic | 30 |
| ES&S | 18 (San Augustine is marked former) |
| VOTEC | 8 (news) |
| KnowInk | 4 |
| LiveVoterTurnout (operator not identified) | 3 |
| Enhanced Voting | 2 (Comal results; Hays is a mail ballot tracker only) |
| Civera | 1 |
| ElectionLink (operator not identified) | 1 |
| Tyler Technologies | 0 |

## Gaps and things that did not work

- **The Clarity list is incomplete.** Comparing `elections.json` with links on the counties' own sites shows several gaps:
  - Tarrant lists only 5/3/2025, but its site links the 2024 general (EID 122489) and the 2026 primary (EID 125924).
  - Bexar, Kendall, Montague and Victoria return an empty list, yet their sites link 2026 Clarity elections.
  - Hidalgo stops at 2020.

  So "not listed" in `clarity_presence.csv` does not mean "not on Clarity". Use the county-site EID links or `clarity_root_probe.csv` together with it.
- **Liberty, Potter and Wise get a 403 from Clarity's nginx**, both on `elections.json` and on the folder root. A nonexistent county gets a 404 page instead. These three may have restricted or retired Clarity folders. This is unresolved.
- **Comal is marked "former" for Clarity.** Its past-results page links Clarity through May 2025 and Enhanced Voting from November 2025. Parker's newest Clarity link on its own site is 2021 and its `elections.json` is empty. It is left as "customer" with year 2021, because no source states a change.
- **Unreadable vendor sites.**
  - soesoftware.com and scytl.us return HTTP 202 with an empty body, which looks like a bot challenge. SOE customer testimonials (search text mentions Wood and Lamar counties) and the Scytl client pages could not be read.
  - businesswire.com returns 403, so the Hart Harris and Montgomery releases were not readable. Harris is covered by its own agenda. Montgomery has no row.
  - The Dallas County civicweb agenda is disallowed by robots.txt. Search text says the 1/5/2021 agenda had a renewal of the "Master SaaS Agreement between SOE Software Corporation d/b/a SCYTL and Dallas County" with ENR fees of $27,000. That is a lead only, not evidence.
- **The Enhanced Voting results page is a JavaScript app.** The county appears only in the URL slug (`comal-county-tx`), so Comal's evidence is the county's own links. No Enhanced Voting client list was found, and the vendor home page names no Texas county.
- **livevoterturnout.com has no visible operator.** The home page is blank, and pages show only county logos. Tenex Software Solutions sells a "Live Results" product, but no fetched page ties it to livevoterturnout.com.
- **Some vendor statements give counts but name no counties.** KnowInk says "over 160 counties across the Lone Star State" and Civera says Ballot Verifier is "adopted by counties in Texas". These were not turned into rows.
- **No Tyler Technologies, VOTEC or KnowInk results-reporting product was found for any Texas county.** Comal Order 556 grants an exemption for "Tyler Technologies Software". It is not election-specific and was not recorded.
- **Most SOS-listed county URLs (173) are plain http.** The session's egress proxy refuses them ("Host not in allowlist"). I retried them over https, and 137 then loaded. Several county hosts still fail on TLS, robots or 403, so coverage of small counties is partial.
- **Process slip:** one plain `curl` request to www.co.zavala.tx.us was made outside the fetch module while diagnosing the 403s. It returned 403 and its result was not used.

Build scripts and intermediate files (sweep logs, link scan) are in this agent's scratch folder, `scratchpad/vendor/`, and are not part of the deliverable.
