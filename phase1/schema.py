"""Phase 1 evidence schema and validation. One JSON file per county in phase1/evidence/."""
from __future__ import annotations

import re

TAGS = ("LIVE_PRECINCT", "PRECINCT_END_OF_NIGHT", "COUNTY_ONLY_PRECINCT_AT_CANVASS",
        "NO_SITE_OR_SOS_ONLY", "UNKNOWN")
CONFIDENCE = ("high", "med", "low")
CSV_COLUMNS = ("county", "tag", "confidence", "elections_office_phone", "elections_office_email",
               "results_url", "platform", "host", "evidence_url", "evidence_snapshot_timestamp",
               "precinct_first_seen_local_time", "stated_change_2026", "stated_change_source",
               "usage_notice_text", "notes")
PLATFORMS = ("vendor_hosted", "clarity_style", "county_pdfs", "homegrown", "sos_feed_only", "unknown")
# Characters banned from every deliverable: em dash, en dash, and emoji ranges.
BANNED_RE = re.compile("[" + "\\u2013\\u2014" + "\\U0001F300-\\U0001FAFF\\u2600-\\u27BF\\U0001F000-\\U0001F2FF" + "]")


def validate(rec: dict, path: str = "") -> None:
    """Assert-not-if: any malformed record stops the build loudly."""
    where = path or rec.get("county", "?")
    missing = [c for c in CSV_COLUMNS if c not in rec]
    assert not missing, f"{where}: missing fields {missing}"
    assert rec["tag"] in TAGS, f"{where}: bad tag {rec['tag']!r}"
    assert rec["confidence"] in CONFIDENCE, f"{where}: bad confidence {rec['confidence']!r}"
    assert rec["stated_change_2026"] in ("y", "n"), f"{where}: stated_change_2026 must be y or n"
    assert rec["platform"] in PLATFORMS, f"{where}: bad platform {rec['platform']!r}"
    if rec["tag"] != "UNKNOWN":
        assert rec["evidence_url"], f"{where}: a non-UNKNOWN tag requires evidence_url"
        assert rec.get("sources"), f"{where}: a non-UNKNOWN tag requires sources"
    if rec["stated_change_2026"] == "y":
        assert rec["stated_change_source"], f"{where}: stated change requires a source"
    for s in rec.get("sources", []):
        assert s.get("url") and s.get("via"), f"{where}: each source needs url and via"
    for k, v in rec.items():
        if isinstance(v, str):
            assert not BANNED_RE.search(v), f"{where}: field {k} contains a banned dash or emoji character"


# ---- v2 (three-check method, see phase1/CHECKLIST_BRIEF.md) ----
ELECTIONS = ("2024_general", "2026_primary", "2026_runoff")
ELECTION_RESULTS = ("LIVE", "END", "LATER", "NONE", "UNDETERMINED")
RESULT_TO_TAG = {"LIVE": "LIVE_PRECINCT", "END": "PRECINCT_END_OF_NIGHT",
                 "LATER": "COUNTY_ONLY_PRECINCT_AT_CANVASS", "NONE": "NO_SITE_OR_SOS_ONLY"}


def compute_tag(elections: dict) -> tuple[str, bool]:
    """Apply the fixed county rule. Returns (tag, single_election) where single_election
    means only one election was determined, which forces confidence low."""
    determined = [elections[e]["result"] for e in ELECTIONS if elections[e]["result"] != "UNDETERMINED"]
    for r in RESULT_TO_TAG:
        if determined.count(r) >= 2:
            return RESULT_TO_TAG[r], False
    if len(determined) == 1:
        return RESULT_TO_TAG[determined[0]], True
    return "UNKNOWN", False


def validate_v2(rec: dict, path: str = "") -> None:
    where = path or rec.get("county", "?")
    assert rec.get("method_version") == "v2", f"{where}: method_version must be v2"
    validate(rec, path)
    el = rec.get("elections")
    assert isinstance(el, dict) and set(el) == set(ELECTIONS), f"{where}: elections must have exactly {ELECTIONS}"
    for e in ELECTIONS:
        x = el[e]
        assert x.get("result") in ELECTION_RESULTS, f"{where}: {e} result {x.get('result')!r}"
        assert x.get("check") in ("1", "2", "3", "none"), f"{where}: {e} check {x.get('check')!r}"
        if x["result"] != "UNDETERMINED":
            assert x["check"] != "none" and x.get("evidence_url") and x.get("fact"), \
                f"{where}: {e} is determined, so it needs check, evidence_url, and fact"
    tag, single = compute_tag(el)
    assert rec["tag"] == tag, f"{where}: tag {rec['tag']} does not follow the rule; rule gives {tag}"
    if single:
        assert rec["confidence"] == "low", f"{where}: only one election determined, confidence must be low"
    for k, v in el.items():
        for kk, vv in v.items():
            if isinstance(vv, str):
                assert not BANNED_RE.search(vv), f"{where}: elections.{k}.{kk} has a banned character"


def compute_confidence(rec: dict) -> str:
    """Deterministic confidence from the per-election records (DECISIONS 40).

    low  : tag UNKNOWN, or only one election decides the tag
    high : two or more deciding elections, all settled by check 1 or check 3 content
    med  : two or more deciding elections, at least one settled by check 2,
           or any deciding election settled under the live precinct view rule
    """
    tag, single = compute_tag(rec["elections"])
    if tag == "UNKNOWN" or single:
        return "low"
    deciding = [rec["elections"][e] for e in ELECTIONS
                if rec["elections"][e]["result"] != "UNDETERMINED"
                and RESULT_TO_TAG.get(rec["elections"][e]["result"]) == tag]
    assert len(deciding) >= 2, f"{rec['county']}: rule gave {tag} without two deciding elections"
    if any(e.get("rule") == "live_precinct_view" for e in deciding):
        return "med"
    if all(e["check"] in ("1", "3") for e in deciding):
        return "high"
    return "med"
