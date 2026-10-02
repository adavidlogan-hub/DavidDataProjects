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


def rec(*elections):
    names = ("2024_general", "2026_primary", "2026_runoff")
    return {"county": "X", "elections": {n: e for n, e in zip(names, elections)}}


def test_compute_confidence():
    from phase1.schema import compute_confidence
    U = {"result": "UNDETERMINED", "check": "none"}
    assert compute_confidence(rec({"result": "LIVE", "check": "1"}, {"result": "LIVE", "check": "1"}, U)) == "high"
    assert compute_confidence(rec({"result": "LIVE", "check": "1"}, {"result": "LIVE", "check": "3"},
                                  {"result": "LATER", "check": "2"})) == "high"
    assert compute_confidence(rec({"result": "LATER", "check": "2"}, {"result": "LATER", "check": "1"}, U)) == "med"
    assert compute_confidence(rec({"result": "LIVE", "check": "3", "rule": "live_precinct_view"},
                                  {"result": "LIVE", "check": "1"}, U)) == "med"
    assert compute_confidence(rec({"result": "END", "check": "2"}, U, U)) == "low"
    assert compute_confidence(rec(U, U, U)) == "low"
    assert compute_confidence(rec({"result": "LIVE", "check": "1"}, {"result": "LATER", "check": "2"}, U)) == "low"


def test_check4_caps_confidence_at_med():
    from phase1.schema import compute_confidence
    U = {"result": "UNDETERMINED", "check": "none"}
    assert compute_confidence(rec({"result": "LIVE", "check": "4"}, {"result": "LIVE", "check": "1"}, U)) == "med"
