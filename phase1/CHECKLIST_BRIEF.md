# Phase 1 checklist brief (v2)

Question for each county: does it publish individual precinct result numbers on election night, and how?
Use only public online sources. Never contact a county. Never guess.

Repo root: /home/user/DavidDataProjects. Write only your county files in phase1/evidence/ and files in your own scratch folder (given in your task). Do not read phase1/evidence_v1/ (earlier method). Do not edit code. The only git commands allowed are `git fetch origin wayback-data` and `git show origin/wayback-data:<path>`.

## Tools (all go through the shared fetch module, which handles rate limits, robots.txt, retries, and the cache)
- Fetch a page or file: `python3 -m txprecinct.get "<url>" --agent <id> --purpose "check<N>:<County>"`
- Read a cached body (decompresses gzip): `python3 -m txprecinct.cat "<url>"` or `--out file`
- Check 1 script: `python3 -m phase1.clarity_timeline --county "<County>" --agent <id>` (writes phase1/checks/clarity/<County>.json)
- Web search is allowed only to locate a county's results page or vendor site. Search text is never evidence. Load it with ToolSearch "select:WebSearch", and record each search through `python3 -m txprecinct.searchlog` (check first, record after).
- Contacts: do not research phone or email. The build fills them from the SOS list (data/seed_counties.csv).

## The three elections
2024_general = Nov 5 2024, 2026_primary = Mar 3 2026, 2026_runoff = May 26 2026.
Election night = 7:00 PM election day to 3:00 AM the next morning, county local time (Hudspeth and El Paso are Mountain time).

## Checks, in order. Stop for an election as soon as one check settles it.
1. **Vendor update log.** Start from the county's website in data/seed_counties.csv and find where it posts results. If results are on Clarity (results.enr.clarityelections.com/TX/<County>), run the check 1 script. It reads every published update and reports its timestamp and how many precincts have nonzero candidate votes. If another vendor site exposes a dated update history, read it the same way and record what you read.
2. **County-posted reports.** On the county's results page, list the reports for each election: title (for example "Unofficial Precinct Results", "Cumulative", "Canvass", "Official"), printed run time or date, and the server upload time (the Last-Modified header, which the fetch module records; view it with `python3 -c "import sys; sys.path.insert(0,'.'); from txprecinct.config import load_config; from txprecinct.store import Store; from txprecinct.fetch import normalize_url; r=Store(load_config().state_dir).latest_ok(normalize_url(sys.argv[1])); print(dict(r))" "<url>"`). A server that stamps every file with the request time gives no upload evidence; say so.
3. **Wayback Machine.** `git fetch origin wayback-data`, then read `git show origin/wayback-data:phase1/wayback_snapshots/<County_with_underscores>/index.json`. It lists archived election-night captures of the county's election pages with their local times and saved files. Open saved files with `git show origin/wayback-data:phase1/wayback_snapshots/<County>/<file>` and look for per-precinct candidate numbers. If the county folder is not there yet, write "check 3 pending" for that election.
   Live precinct view rule: if an archived election-night copy of the county's own live results page or app contains a precinct-by-precinct candidate results view that loads its numbers from the same live, refreshing data feed as the county totals (for example a "Precinct Reporting" tab that requests per-precinct vote files with a cache-busting time), record that election as LIVE from check 3, quote the code or markup that shows it, and cap the county's confidence at med. A per-precinct turnout table (ballots cast by precinct) does not qualify; only per-precinct candidate votes do.

## Common situations (learned in the pilot)
- Clarity's elections.json can be empty or incomplete (Hidalgo stops at 2020; Bexar's is empty). If the script says "not listed", find links to results.enr.clarityelections.com/TX/<County>/<EID>/ and pass the IDs: `--eid 2024_general=<id> --eid 2026_primary=<id> --eid 2026_runoff=<id>`. Prefer links on the county's own pages; a link from any public page (news, Wikipedia) is acceptable ONLY if the downloaded detail.xml itself shows <Region> equal to the county and <ElectionDate> equal to the election date. Record the link's source page and that Region/ElectionDate check in sources. Never probe ranges of IDs.
- For multi-word counties, use the Clarity slug exactly as it appears in the county's own link to Clarity; the script takes `--county` as that slug (spaces become underscores).
- On some Clarity updates the precinct values are marked "protected" on election night (Travis and Tarrant runoffs). The script counts these as zero precincts with votes; that election is then LATER if precinct numbers appear after election night.
- Seed website URLs are sometimes dead (403 over http, 404) or redirect. Try https and the county's current domain; one web search to locate the site is fine.
- Some county sites return an empty HTTP 202 or 403 to every request (bot protection). Do not try to get around it. Use the vendor site the county links to if you can find it; otherwise that check fails for that county.
- If robots.txt disallows a host, the fetch module refuses; accept it and note it.
- PDF creation metadata (CreationDate) counts as a printed run time, not as an upload time.
- Budget about 3 minutes and 8 fetches of effort per county beyond check 1. UNDETERMINED is a normal outcome; check 3 will be run later for undetermined elections.
- If check 3 data is not yet on the wayback-data branch, set check "none" and result UNDETERMINED for elections not settled by checks 1 or 2, and add "check 3 pending" in notes.

## Result per election (pick exactly one)
- `LIVE`: precinct numbers that include election-day votes appear in two or more updates during election night (updates with only early, mail, or absentee precinct numbers do not count). For Clarity, use the script's election_night_updates_with_election_day_precinct_votes.
- `END`: precinct numbers that include election-day votes appear on election night, once, with the final unofficial count.
- `LATER`: on election night the county publishes county totals only (or early-vote-only precinct numbers); precinct numbers with election-day votes come after election night, or are never published online. Say which in the note.
  LATER needs positive election-night evidence: a county-totals file (or update) whose printed run time or upload time falls on election night, and no precinct numbers with election-day votes that night. Put that election-night time in county_totals_first_seen. If no file from election night survives (only files dated after election night, such as official or canvass reports), the election is UNDETERMINED, not LATER: we cannot see what was posted that night.
- `NONE` likewise needs positive evidence (for example the county's own page linking that election's results only to the SOS site); missing files alone are UNDETERMINED.
- `NONE`: the county publishes no results of its own for that election (results only via the SOS).
- `UNDETERMINED`: the checks cannot decide.

## County tag (fixed rule, do not deviate)
Map LIVE to LIVE_PRECINCT, END to PRECINCT_END_OF_NIGHT, LATER to COUNTY_ONLY_PRECINCT_AT_CANVASS, NONE to NO_SITE_OR_SOS_ONLY.
- If two or three elections share the same result (ignoring UNDETERMINED), that is the tag.
- If exactly one election is determined, use it, confidence low.
- Otherwise UNKNOWN.
Confidence: high when the deciding elections were settled by check 1 or by check 3 snapshot content; med when settled by check 2 with both a printed run time and a server upload time on election night; low otherwise.

## Output: phase1/evidence/<County_with_underscores>.json
All of these keys (strings; empty string when not applicable):
county, tag, confidence, elections_office_phone (""), elections_office_email (""), results_url, platform (vendor_hosted | clarity_style | county_pdfs | homegrown | sos_feed_only | unknown), host, evidence_url (the single best evidence link), evidence_snapshot_timestamp (Wayback timestamp if check 3 decided it), precinct_first_seen_local_time (earliest election-night time precinct numbers were seen, "YYYY-MM-DD HH:MM CT" or MT), stated_change_2026 ("y" only if the county's own site says in 2025 or 2026 that it is adding or changing precinct reporting, with the URL in stated_change_source; otherwise "n"), stated_change_source, usage_notice_text (exact text of any distribution or usage notice on the results page, else ""), notes, tag_rationale (one or two sentences applying the rule), agent, method_version ("v2").
Plus:
"elections": {"2024_general": {"result": "...", "check": "1|2|3|none", "county_totals_first_seen": "", "precinct_first_seen": "", "night_updates_with_precinct_numbers": "", "evidence_url": "", "fact": "what the source shows, verbatim where possible"}, "2026_primary": {...}, "2026_runoff": {...}},
"sources": [{"url": "...", "via": "fetch_module|clarity_script|wayback_branch|websearch", "content_hash": "...", "quote": "...", "supports": "..."}]

Validate: `python3 -c "import json,sys; sys.path.insert(0,'.'); from phase1.schema import validate_v2; validate_v2(json.load(open('phase1/evidence/<File>.json')))"`
No em dashes, en dashes, or emojis anywhere (replace any in quoted source text with a hyphen and say so in notes).
Final reply: a table of county, tag, confidence, and per-election results with the check used; plus counts of fetches and searches, and anything that did not work.
