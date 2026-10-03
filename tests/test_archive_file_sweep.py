import zlib

from phase1.archive_file_sweep import UPDATED_RE, local_from_http, night_bounds, parse_printed, score
from phase1.pdf_probe import pdf_info


def test_upload_time_converts_to_local_and_falls_on_night():
    n0, n1, off = night_bounds("2024_general")
    lm = local_from_http("Wed, 06 Nov 2024 07:18:16 GMT", off)
    assert str(lm) == "2024-11-06 01:18:16"
    assert n0 <= lm <= n1


def test_runoff_uses_daylight_offset():
    n0, n1, off = night_bounds("2026_runoff")
    assert off == -5
    assert not (n0 <= local_from_http("Wed, 27 May 2026 09:00:00 GMT", off) <= n1)  # 4 AM CDT


def test_printed_and_updated_strings():
    assert str(parse_printed("11/06/2024     12:37 AM")) == "2024-11-06 00:37:00"
    assert UPDATED_RE.findall("Website Updated: 3/3/2026 7:29:36 PM")[0][1] == "3/3/2026 7:29:36 PM"


def test_precinct_files_rank_first():
    assert score("x/Precinct-Results-Unofficial.pdf") > score("x/Agenda.pdf")


def test_pdf_info_reads_text_and_dates():
    s = zlib.compress(b"BT (PCT 001) Tj (11/06/2024 12:37 AM) Tj ET")
    info = pdf_info(b"%PDF-1.4 << /CreationDate (D:20241106003918-06'00') >> stream\n" + s + b"\nendstream")
    assert info["CreationDate"].startswith("D:2024")
    assert info["printed_datetimes_first_streams"] == ["11/06/2024 12:37 AM"]


def test_cdx_chunk_windows_cover_the_election_window():
    from phase1.archive_file_sweep import FILE_MIME, cdx_url
    u0 = cdx_url("example.gov", "2024_general", FILE_MIME, 0, 3)
    u1 = cdx_url("example.gov", "2024_general", FILE_MIME, 3, 3)
    assert "from=20241105060000" in u0 and "to=20241108060000" in u0
    assert "from=20241108060000" in u1 and "to=20241111060000" in u1
