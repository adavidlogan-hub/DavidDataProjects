import json, sys, datetime
sys.path.insert(0, ".")
from phase1.schema import compute_confidence, compute_tag
p = "phase1/verification/Ellis.json"
e = json.load(open(p))
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
e["verdict_before_owner_ruling"] = {
 "verifier_tag": e["verifier_tag"],
 "verifier_confidence": e["verifier_confidence"],
 "agree": e["agree"],
 "2026_primary": dict(e["elections"]["2026_primary"]),
 "rationale": e["rationale"],
 "comparison_notes_2026_primary": e["comparison_notes"]["2026_primary"],
}
pr = e["elections"]["2026_primary"]
pr["result"] = "LIVE"
pr["check"] = "3"
pr["rule"] = "live_precinct_view"
pr["fact"] = pr["fact"].split(" The precinct numbers are static markup")[0] + (
 " Live precinct view rule as clarified by the owner (DECISIONS 75): the page reloads itself on a timer "
 "('<input type=\"hidden\" name=\"hdnAutoRefresh\" id=\"hdnAutoRefresh\" value=\"600\" />'; 'Refresh Display' "
 "onclick=\"javascript: document.location.reload(true);\") and carries per-precinct candidate vote tables "
 "('<input type=\"hidden\" name=\"hdnPrecinctLevelResults\" id=\"hdnPrecinctLevelResults\" value=\"1\" />'; "
 "'Precinct: 1001 - Contest: DEM US Senator ... Jasmine Crockett 456 85.71%') in the same published page as the "
 "county totals ('Ballots Counted 18,806 ... Election Day 6,120'), with election-day votes, on election night. "
 "LIVE from check 3 under that rule; confidence capped at med.")
e["verifier_tag"], single = compute_tag(e["elections"])
e["verifier_confidence"] = compute_confidence({"county": "Ellis", "elections": e["elections"]})
e["rationale"] = ("Only the 2026 primary is determined. Under the live precinct view rule as clarified by the owner "
 "(DECISIONS 75, CHECKLIST_BRIEF.md), the 11:49 PM CST archived copy of the county's self-refreshing livevoterturnout "
 "page (auto-refresh 600 s, Website Updated 11:34:46 PM, server Last-Modified 11:34 PM CST) carrying per-precinct "
 "candidate votes with election-day votes in the same published page as the county totals is a live precinct view, "
 "so the primary is LIVE from check 3. 2024 and the runoff have no surviving election-night file. Fixed rule: one "
 "determined election gives LIVE_PRECINCT, computed confidence low. Before the ruling the verifier read the "
 "CHECKLIST_BRIEF.md wording as requiring a separately loaded feed and gave END (kept under verdict_before_owner_ruling).")
e["agree"] = (e["verifier_tag"] == e["research_tag"])
e["comparison_notes"]["2026_primary"] = ("Same after the owner ruling (DECISIONS 75): research and verifier both LIVE, "
 "check 3, rule live_precinct_view, from the same file (sweep replay of ellistxenr/5/en/Index_5.html captured "
 "05:49:54 UTC Mar 4, original Last-Modified 05:34:47 GMT, per-precinct candidate votes with Election Day complete in "
 "the same self-refreshing page as the county totals). The earlier disagreement (verifier END) was over the rule "
 "wording only, not facts; the earlier note is kept under verdict_before_owner_ruling.")
e["owner_ruling_applied_at_utc"] = now
s = json.dumps(e, indent=1, ensure_ascii=False)
assert "—" not in s and "–" not in s
open(p, "w").write(s + "\n")
print(e["verifier_tag"], e["verifier_confidence"], e["agree"], single)
