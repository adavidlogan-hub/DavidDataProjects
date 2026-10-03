# Targeted pass 6 brief (largest UNKNOWN counties: third-party election-night copies)

Applies on top of phase1/CHECKLIST_BRIEF.md, phase1/TARGETED_BRIEF.md (check 4), phase1/TARGETED4_BRIEF.md, and phase1/scratch/verify_round12_rules.md. All rules still apply: public online sources only; never contact anyone; never guess; never construct file URLs from naming patterns; never get around bot protection, robots.txt, paywalls, or logins; every request through the fetch module with your agent id; no em dashes, en dashes, or emojis; do not save raw .html in your scratch folder.

Read each county's evidence file and all pass notes first. Earlier passes exhausted the county's own sites, the Wayback Machine, and mainstream news text. This pass looks for third parties that republished the county's election-night precinct numbers with a timestamp.

## Where to look
1. **County party websites.** County Republican and Democratic party sites often repost the county's precinct-by-precinct report on primary and runoff night. If a party site is WordPress, its media upload log (/wp-json/wp/v2/media or /index.php?rest_route=/wp/v2/media, with after= and before=) dates each uploaded file; posts carry published and modified times.
2. **Newsroom and civic data repositories.** News organizations and civic projects scrape county results on election night into public GitHub repositories; each commit has a timestamp and the files show what the county published. Use web search to locate them; read files and commit history through the fetch module (raw.githubusercontent.com, api.github.com public endpoints for commits on a path). OpenElections (openelections-data-tx) precinct files list their source; commit dates are usually later and then decide nothing.
3. **Local media precinct maps or tables** published on election night with a published or updated time (Community Impact, local TV, newspapers). The fetched page or data file is the evidence, never a search snippet.
4. **City, school district, or other entity sites** that reposted the county's precinct report on election night for the same election (with an upload log or timestamp).

## What counts
Check 4 rules (TARGETED_BRIEF item 2): per-precinct candidate votes for one of the county's races, a time on election night (published, updated, uploaded, or committed), and a statement or evident source that the numbers are the county's election-night results. Two or more distinct timestamped election-night releases give LIVE; one gives END; set "rule": "check4" and the county confidence is capped at med. A third-party copy of a county-totals report does not decide LATER (DECISIONS 62).

## Output
As in TARGETED4_BRIEF; note "Targeted pass 6 2026-10-03 (<agent>): ...". Final reply: table of county, old tag, new tag, confidence, per-election changes with deciding source; fetch and search counts; dead ends and leads.
