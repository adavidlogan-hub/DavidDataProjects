from phase1.archive_lookup import parse_linkformat


def test_parse_linkformat_and_windows():
    text = ('<http://archive.ph/abc>; rel="memento"; datetime="Wed, 06 Nov 2024 03:10:00 GMT",\n'
            '<http://web.archive.org/web/2024/x>; rel="first memento"; datetime="Tue, 05 Nov 2024 12:00:00 GMT",\n'
            '<http://archive.ph/def>; rel="last memento"; datetime="Wed, 27 May 2026 05:00:00 GMT"')
    ms = parse_linkformat(text)
    assert [m["window"] for m in ms] == ["2024_general", None, "2026_runoff"]
