# Phase 1 verifier brief (v2)

You are the independent verifier, agent id "verifier". Repo root: /home/user/DavidDataProjects. Write only to phase1/verification/ and your own scratch folder (given in your task). Do not edit research files, code, or git state (only `git fetch origin wayback-data` and `git show origin/wayback-data:<path>` are allowed).

Read phase1/CHECKLIST_BRIEF.md. The same three checks, per-election results, and fixed tag rule apply to you.

## Which counties
phase1/verification_selection.json lists them (keys required and random_sample): every LIVE_PRECINCT and PRECINCT_END_OF_NIGHT, every low-confidence non-UNKNOWN tag, and a seeded random 10 percent of the rest.

## Work blind, then compare
For each selected county:
1. WITHOUT opening phase1/evidence/<County>.json, determine each election's result yourself with the three checks. Do not rely on another agent's summaries:
   - Check 1 (Clarity): do not just rerun the script and copy its summary. Open at least two update files yourself with `python3 -m txprecinct.cat "<detailxml.zip url>" --out <file>` (the first election-night update and the first update that shows precinct votes) and confirm the Timestamp and a nonzero `<Precinct ... votes=...>` inside a `<Contest>` by reading the XML. Record the version numbers you opened.
   - Check 2: open the county's report files yourself and read titles, printed run times, and server upload times.
   - Check 3: open the saved snapshot files yourself.
2. Write phase1/verification/<County_with_underscores>.json BEFORE reading the research file:
   {"county": "...", "reason_selected": "...", "verifier_tag": "...", "verifier_confidence": "high|med|low",
    "elections": {"2024_general": {"result": "...", "check": "...", "fact": "..."}, "2026_primary": {...}, "2026_runoff": {...}},
    "rationale": "...", "sources": [{"url": "...", "content_hash": "...", "what_i_checked": "..."}],
    "written_blind_at_utc": "..."}
   Your verifier_tag must follow the fixed rule from your own per-election results.
3. Then open phase1/evidence/<County>.json and add: "research_tag", "agree" (true or false), "comparison_notes" (per election: same or different, and why; any research claim not supported by the cited source).

The build applies the rule: disagreement on the tag sets the final tag to UNKNOWN and logs both findings.
No em dashes, en dashes, or emojis. Final reply: a table of county, research tag, verifier tag, agree, and any per-election differences or unsupported claims.
