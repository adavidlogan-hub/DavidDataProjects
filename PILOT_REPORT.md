# Pilot report: Phase 1 on 17 counties

Written 2026-10-02. Pilot counties: Harris, Dallas, Bexar, Travis, Tarrant, Hidalgo, Ector, Midland, Brewster, Loving, Lubbock, Wilbarger, Comal, Smith, Hudspeth, Jim Hogg, Sabine.

## Summary

- 17 of 17 counties completed with the three-check method (method v2). 12 carry a tag backed by timestamps or upload times; 5 are UNKNOWN.
- The first pilot pass (method v1, free-form research) was rejected by the owner and discarded. The rerun with a fixed checklist took less than half the time per county and tagged twice as many counties.
- Verifier round 1 confirmed 4 of 5 LIVE_PRECINCT tags (Travis, Hidalgo, Midland, Tarrant). Bexar disagreed because of a gap in the instructions about where Clarity election IDs may come from; it is UNKNOWN until re-verified.
- Projection for all 254 counties was 70 to 80 minutes of research with 8 agents. Actual: the full run finished in about 40 minutes (see the last section).

## Results (method v2, before the Wayback check and the check 1 reconciliation)

| County | Tag | Confidence | Basis |
|---|---|---|---|
| Travis | LIVE_PRECINCT | high | Clarity update log; verified |
| Hidalgo | LIVE_PRECINCT | high | Clarity update log; verified |
| Midland | LIVE_PRECINCT | high | Clarity update log; verified |
| Tarrant | LIVE_PRECINCT | high | Clarity update log (2024, 2026 primary); runoff precinct values hidden until June 2; verified |
| Bexar | UNKNOWN (research: LIVE_PRECINCT) | low | Verifier disagreement; pending re-verification |
| Dallas | LIVE_PRECINCT | low | Only the 2026 runoff is on Clarity; county site blocks automated requests |
| Comal | LIVE_PRECINCT | low | Clarity 2024 only; 2026 on Enhanced Voting, which keeps no update history |
| Hudspeth | COUNTY_ONLY_PRECINCT_AT_CANVASS | med | Precinct results posted the day after each election |
| Ector | COUNTY_ONLY_PRECINCT_AT_CANVASS | low | Election-night report county-wide only |
| Brewster | COUNTY_ONLY_PRECINCT_AT_CANVASS | low | Runoff only; timing from PDF creation dates |
| Wilbarger | COUNTY_ONLY_PRECINCT_AT_CANVASS | low | County totals only; no precinct report ever posted |
| Jim Hogg | COUNTY_ONLY_PRECINCT_AT_CANVASS | low | Precinct reports uploaded next day in 2 of 3 elections |
| Harris | UNKNOWN | low | See below |
| Loving | UNKNOWN | low | Nothing posted online |
| Lubbock | UNKNOWN | low | Site blocks automated requests; Clarity host disallowed by robots.txt |
| Smith | UNKNOWN | low | Election-night reports overwrite each other |
| Sabine | UNKNOWN | low | Only official reports online |

Harris: the Wayback Machine saved Harris's live results app at 8:01 PM on the 2026 primary night and 8:47 PM on runoff night. Both copies contain a "Precinct Reporting" tab that loads per-precinct candidate votes (rep-pv-<contest>.json, dem-pv-<contest>.json) from the same live data folder as the county totals. The precinct files themselves were not archived. See DECISIONS.md for how this is applied.

## Agents used

| Agent | Counties | Wall time | Agent tokens | Tool calls |
|---|---|---|---|---|
| research-A, v1 (discarded) | 9 | 30.0 min | 348,571 | 177 |
| research-B, v1 (discarded) | 8 | 33.1 min | 357,853 | 185 |
| research-A, v2 | 8 | 15.4 min | 205,264 | 109 |
| research-B, v2 | 9 | 23.2 min | 271,069 | 152 |
| verifier, round 1 | 5 | 14.5 min | 184,396 | 71 |

Per county, v2 research used about 28,000 agent tokens and about 2.3 agent-minutes, against about 42,000 tokens and 3.7 agent-minutes in v1.

## Fetches

All network requests went through the shared fetch module (rate limits, robots.txt, cache), except four direct curl calls by agents that are logged as rule breaches in phase1/RUN_ISSUES.md.

| Stage | Requests logged | Succeeded | Web searches |
|---|---|---|---|
| Pilot v1 (13:49 to 14:40 UTC, including setup) | 871 | 552 | 85 |
| Pilot v2 research | 447 | 258 | 8 |
| Verifier round 1 | 171 | 41 | 2 |

Failures are mostly Clarity update versions that the vendor has purged (HTTP 404), sites that block automated requests (empty HTTP 202 or 403), and robots.txt refusals.

## Wall time

- Infrastructure build and network unblocking: 13:49 to 14:07 UTC.
- Pilot v1 (discarded): 14:00 to 14:30.
- Pilot v2 research: 14:40 to 15:03 (23 minutes, two agents in parallel).
- Verifier round 1: 15:05 to 15:20.
- Wayback harvest for the 17 pilot counties: 59.6 minutes on GitHub Actions (14:49 to 15:49), mostly waiting on the Wayback search service.

## Issues found

1. Network: the build container initially blocked every target site; resolved when the owner enabled full network access. web.archive.org still refuses this cloud provider, so Wayback harvesting runs on GitHub Actions. Plain http:// requests and a few hosts (www.bosquecounty.gov) are still refused by the proxy.
2. Method v1 let agents improvise; one used Clarity's update log and the other did not. Fixed by a written checklist, one shared script for check 1, and a validator that rejects any tag that does not follow the fixed rule.
3. Clarity's own election lists are incomplete or empty for many counties (Hidalgo, Bexar, Tarrant, Fort Bend, Montague, Parker, Kendall, Victoria). The script takes election IDs found on county pages, and provenance is checked in the downloaded data (Region and ElectionDate).
4. Clarity hides precinct values ("protected") in some elections (Travis, Tarrant, Galveston runoffs).
5. Check 1 needed three corrections found during the run: count only precinct numbers that include election-day votes; convert time zone labels (Kaufman's are Eastern); require distinct releases (Gregg repeated identical numbers). A reconciliation pass re-applies these to every Clarity county.
6. Many county web servers report the request time instead of the upload time (CivicPlus DocumentCenter and others), so check 2 often cannot prove election-night posting.
7. Some county sites block automated requests or disallow crawlers in robots.txt; these are not circumvented.
8. Wayback coverage of election nights is thin: only Harris, Tarrant, Dallas, and Hidalgo had any election-night captures among the 17 pilot counties.
9. The first harvest run lost its downloads when the final git push failed; the workflow now saves its cache and an artifact even on failure.

## Projection for all 254 counties, and actual

| Item | Projected after pilot | Actual full run |
|---|---|---|
| Research wall time, 8 agents | 70 to 80 min | about 40 min (15:15 to 15:55 UTC) |
| Agent tokens, research | about 7 million | about 3.3 million for 237 counties (about 14,000 per county) |
| Wayback harvest | 15 to 20 hours | in progress: 6 sequential batches, about 14 hours expected |

Phases 2 and 3 have not started; they wait for the owner's review of the Phase 1 county results.

## Addendum: full Phase 1 run (all 254 counties), final as of 2026-10-02 17:01 UTC

Final tags (counties.csv):

| Tag | Counties |
|---|---|
| LIVE_PRECINCT | 21 (18 high, 1 med, 2 low) |
| PRECINCT_END_OF_NIGHT | 21 (2 high, 9 med, 10 low) |
| COUNTY_ONLY_PRECINCT_AT_CANVASS | 105 (1 high, 57 med, 47 low) |
| NO_SITE_OR_SOS_ONLY | 1 |
| UNKNOWN | 106 |

LIVE_PRECINCT: Bell, Bexar, Comal, Dallas, Denton, El Paso, Fort Bend, Galveston, Harris, Hidalgo, Hunt, Kaufman, Kendall, Midland, Montague, Rockwall, Rusk, Tarrant, Travis, Victoria, Wood.

Verification: 119 counties re-checked blind by six verifier instances; 109 agree (92 percent). The 10 disagreements are UNKNOWN by rule: Cherokee, Haskell, Hutchinson, Lamar, Lamb, Robertson, Scurry, Throckmorton, Tyler, Zapata. In five of them (Haskell, Lamb, Scurry, Tyler, Zapata) the verifier found election-night files the research missed; a targeted follow-up could resolve them.

Rules tightened during the run (DECISIONS 36 to 47) were applied to every county by dedicated passes: election-day precinct votes only; distinct releases; time zone conversion; LATER needs election-night evidence (rule 43, 177 elections re-checked); END needs an election-night upload when one is known (rule 47, 40 elections re-checked).

Effort for the full run (15:14 to 17:01 UTC, about 1 hour 47 minutes):

| Work | Agent tokens |
|---|---|
| 8 research agents (237 counties) | 3,264,218 |
| Vendor agent | 255,822 |
| 6 verifier instances (119 counties) | 1,987,554 |
| 5 normalization passes (rules 43 and 47) | 842,883 |
| Check 3 pilot pass (Harris, Dallas) | 98,452 |
| Total | 6,448,929 |

Session usage reading (API list price equivalent, includes all agents): 48.59 USD before the full run, 269.21 USD after, so about 221 USD for the full run. On the owner's subscription plan this counts toward usage limits rather than being billed.

Still open: the Wayback harvest for 200 of 240 counties was re-run after a robots.txt fix (DECISIONS 46); check 3 for undetermined elections follows when it lands.
