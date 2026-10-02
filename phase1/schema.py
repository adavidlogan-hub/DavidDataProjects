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
