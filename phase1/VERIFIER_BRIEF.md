# Phase 1 verifier brief

You are the independent verifier, agent id "verifier". Repo root: /home/user/DavidDataProjects. Write only to phase1/verification/. Do not run git.

Read phase1/RESEARCH_AGENT_BRIEF.md for the environment facts, cache discipline, tag definitions, and evidence rules; they apply to you too. Use agent id "verifier" in every searchlog and fetch command. Cached searches from research agents are allowed (that is what the cache is for) but you must also run at least two queries of your own wording per county so the check is not just a replay.

## Work blind, then compare
For each county assigned to you (list and reason given in phase1/verification_selection.json, keys required and random_sample):
1. WITHOUT opening phase1/evidence/<County>.json, research the county and decide your own tag and confidence using the same rules. Write phase1/verification/<County>.json with your verdict BEFORE reading the research file:
   {"county": "...", "reason_selected": "...", "verifier_tag": "...", "verifier_confidence": "high|med|low",
    "rationale": "...", "sources": [{"url": "...", "via": "...", "query": "...", "quote": "..."}],
    "contact_check": "", "results_url_check": "", "searches_run": 0, "cached_search_hits": 0,
    "written_blind_at_utc": "..."}
2. Then open phase1/evidence/<County>.json and add to your file: "research_tag", "agree" (true/false), "comparison_notes" (what each side relied on; any problems with the research file such as a tag resting on a search-summary lead, a phone or email not supported by a cited source, a wrong results URL). Also fill contact_check and results_url_check with "confirmed", "not confirmed", or "contradicted" plus a short reason.
Do not edit research files. The build script applies the rule: disagreement means the final tag is UNKNOWN.
No em dashes, en dashes, or emojis. Final reply: a table of county, research tag, verifier tag, agree, and any data-quality problems you found in research files.
