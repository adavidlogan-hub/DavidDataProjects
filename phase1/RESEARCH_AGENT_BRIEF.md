# Phase 1 research agent brief

You research Texas counties' election-night results reporting. Repo root: /home/user/DavidDataProjects. Work only inside phase1/evidence/ (write one JSON file per county) and your own scratchpad. Do not edit any other file and do not run git.

## Environment facts (read first)
- Direct HTTP from this container to county sites, sos.state.tx.us, and archive.org is BLOCKED by network policy. The hosted page-fetch tool is blocked for those hosts too. You still must make the standard fetch attempts below through the shared module so the attempts and failures are logged; they fail fast.
- The one working evidence channel is the WebSearch tool. Load it first with ToolSearch query "select:WebSearch". You may also try WebFetch (load with "select:WebFetch") on non-county hosts that search results point to (news sites, ballotpedia, county agenda hosts). Record every WebFetch attempt in your evidence "sources" or "notes" whether it worked or not.

## Mandatory cache discipline (shared infrastructure)
Before every WebSearch, check the shared cache:
    cd /home/user/DavidDataProjects && python3 -m txprecinct.searchlog check "<exact query>"
If it prints CACHED, use that text and do not search again. Otherwise run the search, write the COMPLETE tool result (all titles, URLs, and summary text) to a file in your scratchpad, then record it:
    python3 -m txprecinct.searchlog record --agent <your agent id> --county "<County>" "<exact query>" < /path/to/result.txt
For any direct URL attempt use:
    python3 -m txprecinct.get "<url>" --agent <your agent id> --purpose "phase1:<County>:<what>"

## Per county steps
1. Find the official election results URL and the elections office phone and email (the TX SOS county election officials list is the intended seed; it is blocked, so search for it and for the county elections page).
2. Fingerprint the platform. platform must be one of: vendor_hosted, clarity_style, county_pdfs, homegrown, sos_feed_only, unknown. host is the results hostname. Use only what URLs and quoted text show (for example a results.enr.clarityelections.com URL is clarity_style; links ending in .pdf on the county domain are county_pdfs).
3. Historical timing. Run the Wayback probe once per county for the results host or path prefix you found (it will log a blocked failure in this environment; that is expected):
    python3 -m phase1.wayback_probe --county "<County>" --agent <your agent id> "<host/or/path/prefix>"
   Then search for any citable evidence of WHEN precinct-level results appeared on election night for the Nov 5 2024 general, Mar 3 2026 primary, and May 26 2026 runoff (for example news saying "precinct-by-precinct results were posted at 10:40 p.m.", a county release saying precinct results update with each batch, a results PDF title like "Election Night Precinct Report" with a printed time).
4. Stated changes: search the county elections site, commissioners court agendas/minutes, and local news for 2025 and 2026 statements about adding or changing precinct-level reporting. stated_change_2026 is y only with a citable source; then fill stated_change_source with its URL.
5. Usage notice: record the EXACT text of any distribution/usage notice on the results site only if a source shows it verbatim. Never paraphrase into this field. Otherwise leave it empty and say why in notes.

## Tags (exactly one)
- LIVE_PRECINCT: precinct results updated through the night.
- PRECINCT_END_OF_NIGHT: precinct results posted only with the final unofficial count.
- COUNTY_ONLY_PRECINCT_AT_CANVASS: county totals on election night, precinct detail later (at or after canvass).
- NO_SITE_OR_SOS_ONLY: no county results site; results only through the SOS.
- UNKNOWN: evidence insufficient. NEVER GUESS. "Big counties usually do X" is a guess. A results page that merely has precinct reports today does not tell you WHEN they appeared on election night.

## Evidence rules
- A tag other than UNKNOWN needs at least one source that explicitly supports the timing claim. Put its URL in evidence_url and quote the supporting text in sources[].quote.
- Text that appears ONLY in the search tool's generated summary (not in a result title, URL, or text attributed to a specific page) is a lead, not evidence. It cannot alone support a tag, a phone number, or an email. If you use a lead, say so in notes and lower confidence.
- Confidence: high only with a primary source (county or official document) that directly states or timestamps precinct posting. med for a credible secondary source (news) stating it explicitly. low otherwise. Because Wayback is blocked, prefer med or low unless a primary source is explicit.
- Leave evidence_snapshot_timestamp and precinct_first_seen_local_time empty unless a source gives the time. Format local time as "YYYY-MM-DD HH:MM CT" (or MT for Hudspeth/El Paso local times, stating so).
- Phone and email: record only if they appear in a source attributed to the county or the SOS (title/URL/quoted text). Otherwise leave empty and explain in notes.
- No em dashes, en dashes, or emojis anywhere in your output. Use plain hyphens or commas.

## Output: phase1/evidence/<County with spaces replaced by _>.json
{
  "county": "Jim Hogg",
  "tag": "UNKNOWN",
  "confidence": "low",
  "elections_office_phone": "",
  "elections_office_email": "",
  "results_url": "",
  "platform": "unknown",
  "host": "",
  "evidence_url": "",
  "evidence_snapshot_timestamp": "",
  "precinct_first_seen_local_time": "",
  "stated_change_2026": "n",
  "stated_change_source": "",
  "usage_notice_text": "",
  "notes": "",
  "tag_rationale": "one or two sentences",
  "sources": [{"url": "...", "via": "websearch|webfetch|fetch_module", "query": "...", "quote": "verbatim supporting text", "supports": "tag|contact|results_url|platform|stated_change|usage_notice"}],
  "agent": "<your agent id>",
  "searches_run": 0,
  "cached_search_hits": 0,
  "fetch_module_attempts": 0,
  "webfetch_attempts": 0,
  "started_at_utc": "...",
  "finished_at_utc": "..."
}
Validate each file after writing:
    python3 -c "import json,sys; sys.path.insert(0,'.'); from phase1.schema import validate; validate(json.load(open('phase1/evidence/<File>.json')))"

Budget: aim for about 6 to 12 searches per county; stop early when the evidence is clearly insufficient and tag UNKNOWN. When done, reply with a short table: county, tag, confidence, platform, searches run, and one line on the strongest evidence.
