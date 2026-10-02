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
    assert d == {"timestamp": "3/3/2026 9:01:03 PM CST", "precincts_with_votes": 2, "nonzero_precinct_vote_cells": 3}


def test_election_night_window():
    assert on_election_night("3/3/2026 7:00:00 PM CST", "3/3/2026")
    assert on_election_night("3/4/2026 2:59:00 AM CST", "3/3/2026")
    assert not on_election_night("3/4/2026 3:01:00 AM CST", "3/3/2026")
    assert not on_election_night("3/3/2026 6:59:00 PM CST", "3/3/2026")
    assert not on_election_night("3/16/2026 1:45:49 PM CDT", "3/3/2026")
