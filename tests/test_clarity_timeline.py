import io
import zipfile

from phase1.clarity_timeline import on_election_night, read_detail

XML = b"""<?xml version="1.0" encoding="utf-8"?>
<ElectionResult><Timestamp>3/3/2026 9:01:03 PM CST</Timestamp>
<VoterTurnout><Precincts><Precinct name="100" ballotsCast="316" /></Precincts></VoterTurnout>
<Contest key="1"><Choice key="1"><VoteType name="Election Day">
<Precinct name="100" votes="12" /><Precinct name="101" votes="0" /></VoteType>
<VoteType name="Early"><Precinct name="100" votes="3" /><Precinct name="102" votes="7" /></VoteType></Choice></Contest>
</ElectionResult>"""


def zipped(x):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("detail.xml", x)
    return buf.getvalue()


def test_read_detail_counts_only_contest_precinct_votes():
    d = read_detail(zipped(XML))
    assert d == {"timestamp": "3/3/2026 9:01:03 PM CST", "precincts_with_votes": 2, "nonzero_precinct_vote_cells": 3,
                 "precincts_with_election_day_votes": 1, "election_day_precinct_vote_sum": 12}


def test_election_day_votetype_names():
    from phase1.clarity_timeline import ED_VOTETYPE_RE as R
    for n in ("Election Day", "Election", "ELECTION DAY", "ED Provisional", "Election Day In-Person",
              "Election Day Provisionals"):
        assert R.match(n), n
    for n in ("Early", "Early Voting", "EV In-person", "EV Mail", "Absentee", "Ballot by Mail", "Overvotes",
              "Undervotes", "Provisional", "regVotersCounty", "Limited", "Vote by Mail", "Absentee/Mail"):
        assert not R.match(n), n


def test_election_night_window():
    assert on_election_night("3/3/2026 7:00:00 PM CST", "3/3/2026")
    assert on_election_night("3/4/2026 2:59:00 AM CST", "3/3/2026")
    assert not on_election_night("3/4/2026 3:01:00 AM CST", "3/3/2026")
    assert not on_election_night("3/3/2026 6:59:00 PM CST", "3/3/2026")
    assert not on_election_night("3/16/2026 1:45:49 PM CDT", "3/3/2026")


def test_election_night_converts_time_zone_labels():
    # Kaufman prints Eastern time: 8:00 PM EST is 7:00 PM CST, inside the window.
    assert on_election_night("11/5/2024 8:00:00 PM EST", "11/5/2024", "Kaufman")
    # 3:30 AM EST is 2:30 AM CST: still inside.
    assert on_election_night("11/6/2024 3:30:00 AM EST", "11/5/2024", "Kaufman")
    # 4:30 AM EST is 3:30 AM CST: outside.
    assert not on_election_night("11/6/2024 4:30:00 AM EST", "11/5/2024", "Kaufman")
    # May runoff is daylight time: 7:30 PM CDT inside; 8:30 PM EDT is 7:30 PM CDT inside.
    assert on_election_night("5/26/2026 8:30:00 PM EDT", "5/26/2026", "Kaufman")
    # Mountain counties: 7:30 PM MST is inside for El Paso; 6:30 PM MST is not.
    assert on_election_night("3/3/2026 7:30:00 PM MST", "3/3/2026", "El_Paso")
    assert not on_election_night("3/3/2026 6:30:00 PM MST", "3/3/2026", "El_Paso")
    # A Central label for a Mountain county converts: 8:15 PM CST is 7:15 PM MST, inside.
    assert on_election_night("3/3/2026 8:15:00 PM CST", "3/3/2026", "Hudspeth")
