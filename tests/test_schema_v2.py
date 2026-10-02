from phase1.schema import compute_tag


def el(a, b, c):
    return {"2024_general": {"result": a}, "2026_primary": {"result": b}, "2026_runoff": {"result": c}}


def test_majority():
    assert compute_tag(el("LIVE", "LIVE", "LATER")) == ("LIVE_PRECINCT", False)
    assert compute_tag(el("LATER", "UNDETERMINED", "LATER")) == ("COUNTY_ONLY_PRECINCT_AT_CANVASS", False)


def test_single_election():
    assert compute_tag(el("UNDETERMINED", "END", "UNDETERMINED")) == ("PRECINCT_END_OF_NIGHT", True)


def test_no_agreement_is_unknown():
    assert compute_tag(el("LIVE", "LATER", "UNDETERMINED")) == ("UNKNOWN", False)
    assert compute_tag(el("LIVE", "END", "LATER")) == ("UNKNOWN", False)
    assert compute_tag(el("UNDETERMINED", "UNDETERMINED", "UNDETERMINED")) == ("UNKNOWN", False)
