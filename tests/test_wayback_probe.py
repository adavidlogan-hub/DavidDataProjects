from phase1.wayback_probe import WINDOWS, to_central


def test_windows_are_7pm_to_3am_central():
    for name, (frm, to, off) in WINDOWS.items():
        assert to_central(frm, off).split()[1] == "19:00:00", name
        assert to_central(to, off).split()[1] == "03:00:00", name


def test_election_dates():
    assert to_central(WINDOWS["2024_general"][0], -6).startswith("2024-11-05")
    assert to_central(WINDOWS["2026_primary"][0], -6).startswith("2026-03-03")
    assert to_central(WINDOWS["2026_runoff"][0], -5).startswith("2026-05-26")
