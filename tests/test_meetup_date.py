"""Tests for scripts/meetup_date.py. Run: python3 -m pytest tests/ -q"""

import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from meetup_date import (  # noqa: E402
    due_now,
    meetup_date,
    next_meetup,
    nth_weekday,
    timeline_for,
    upcoming,
)


@pytest.mark.parametrize(
    "year,month,expected",
    [
        (2026, 9, date(2026, 9, 19)),
        (2026, 10, date(2026, 10, 17)),
        (2026, 11, date(2026, 11, 21)),
        (2026, 12, date(2026, 12, 19)),
        (2027, 1, date(2027, 1, 16)),
        (2026, 2, date(2026, 2, 21)),   # short month
        (2028, 2, date(2028, 2, 19)),   # leap year
    ],
)
def test_third_saturday(year, month, expected):
    assert meetup_date(year, month) == expected
    assert expected.weekday() == 5


def test_month_starting_on_saturday():
    # Aug 2026 starts on a Saturday: 1, 8, 15 -> third is the 15th.
    assert date(2026, 8, 1).weekday() == 5
    assert meetup_date(2026, 8) == date(2026, 8, 15)


def test_every_month_for_five_years_is_a_saturday_in_range():
    for year in range(2026, 2031):
        for month in range(1, 13):
            d = meetup_date(year, month)
            assert d.weekday() == 5
            assert 15 <= d.day <= 21  # the third Saturday always lands here


def test_nth_weekday_rejects_bad_input():
    with pytest.raises(ValueError):
        nth_weekday(2026, 13)
    with pytest.raises(ValueError):
        nth_weekday(2026, 1, nth=0)
    with pytest.raises(ValueError):
        nth_weekday(2026, 2, nth=5)  # no fifth Saturday in Feb 2026


def test_next_meetup_before_during_after():
    assert next_meetup(date(2026, 9, 1), cycles={}) == date(2026, 9, 19)
    assert next_meetup(date(2026, 9, 19), cycles={}) == date(2026, 9, 19)
    assert next_meetup(date(2026, 9, 20), cycles={}) == date(2026, 10, 17)


def test_next_meetup_rolls_the_year():
    assert next_meetup(date(2026, 12, 20), cycles={}) == date(2027, 1, 16)


def test_upcoming_is_strictly_increasing():
    ds = [d for d, _ in upcoming(6, date(2026, 9, 1), cycles={})]
    assert ds[0] == date(2026, 9, 19)
    assert ds == sorted(ds)
    assert len(set(ds)) == 6


def test_timeline_offsets_land_correctly():
    steps = {s.offset: s.when for s in timeline_for(date(2026, 10, 17), date(2026, 9, 1))}
    assert steps[45] == date(2026, 9, 2)
    assert steps[30] == date(2026, 9, 17)
    assert steps[0] == date(2026, 10, 17)
    assert steps[-2] == date(2026, 10, 19)   # T+2


def test_timeline_status_marks_past_present_future():
    steps = {s.offset: s.status for s in timeline_for(date(2026, 10, 17), date(2026, 9, 17))}
    assert steps[45] == "done"
    assert steps[30] == "today"
    assert steps[0] == "upcoming"


def test_due_now_catches_today_and_recent_overdue():
    offsets = {s.offset for s in due_now(date(2026, 10, 17), date(2026, 9, 17))}
    assert 30 in offsets   # today
    assert 32 in offsets   # two days overdue
    assert 38 not in offsets   # outside the 3-day window


def test_which_nth():
    from meetup_date import which_nth
    assert which_nth(date(2026, 8, 22)) == 4
    assert which_nth(date(2026, 6, 20)) == 3
    assert which_nth(date(2026, 1, 10)) == 2
    assert which_nth(date(2025, 8, 2)) == 1


def test_audit_history_flags_mismatches(tmp_path):
    from meetup_date import audit_history
    csv_path = tmp_path / "meetups.csv"
    csv_path.write_text(
        "date,host_org\n"
        "2026-06-20,A\n"   # third Saturday - matches
        "2026-07-25,B\n"   # fourth Saturday - differs
        ",C\n"             # blank date - skipped
        "not-a-date,D\n"   # unparseable - skipped
    )
    rows = audit_history(csv_path)
    assert len(rows) == 2
    assert rows[0] == (date(2026, 6, 20), 3, True)
    assert rows[1] == (date(2026, 7, 25), 4, False)


def test_real_history_does_not_match_the_configured_rule():
    """Guard: the shipped default is third Saturday, the real history is not.

    If someone changes WEEKDAY/NTH to fit the history, this test should be
    updated in the same commit - that is the point of it.
    """
    from pathlib import Path
    from meetup_date import audit_history
    path = Path(__file__).resolve().parents[1] / "data" / "meetups.csv"
    if not path.exists():
        pytest.skip("no history file")
    rows = audit_history(path)
    if not rows:
        pytest.skip("history file is empty")
    matches = sum(1 for _, _, ok in rows if ok)
    assert matches < len(rows), (
        "every historical meetup now matches the configured rule - "
        "if that is intentional, delete this test"
    )



def test_confirmed_date_beats_the_hint_rule():
    from meetup_date import resolve
    cycles = {"2026-10": date(2026, 10, 24)}
    assert resolve(2026, 10, cycles) == (date(2026, 10, 24), "confirmed")
    assert resolve(2026, 11, cycles) == (date(2026, 11, 21), "suggested")


def test_next_meetup_prefers_a_confirmed_date():
    cycles = {"2026-10": date(2026, 10, 24)}
    from meetup_date import next_meetup_with_source
    assert next_meetup_with_source(date(2026, 10, 1), cycles) == (
        date(2026, 10, 24), "confirmed")
    # a confirmed date already past is skipped, next month falls back to the hint
    assert next_meetup_with_source(date(2026, 10, 25), cycles) == (
        date(2026, 11, 21), "suggested")


def test_load_cycles_ignores_planned_and_malformed_rows(tmp_path):
    from meetup_date import load_cycles
    p = tmp_path / "cycles.csv"
    p.write_text(
        "cycle,meetup_date,status,venue,notes\n"
        "2026-09,2026-09-19,confirmed,QED42,\n"
        "2026-10,,planned,,no date yet\n"
        "2026-11,2026-11-28,planned,,pencilled but not settled\n"
        "2026-12,not-a-date,confirmed,,\n"
    )
    assert load_cycles(p) == {"2026-09": date(2026, 9, 19)}


def test_confirm_writes_and_updates(tmp_path):
    from meetup_date import confirm, load_cycles
    p = tmp_path / "cycles.csv"
    confirm(date(2026, 10, 24), p, venue="Somewhere")
    assert load_cycles(p) == {"2026-10": date(2026, 10, 24)}
    confirm(date(2026, 10, 17), p)                      # corrected later
    assert load_cycles(p) == {"2026-10": date(2026, 10, 17)}
    confirm(date(2026, 11, 28), p)
    assert len(load_cycles(p)) == 2
    assert "Somewhere" in p.read_text()                 # existing fields survive


def test_real_cycles_file_parses():
    from meetup_date import load_cycles, CYCLES_PATH
    if not CYCLES_PATH.exists():
        pytest.skip("no cycles.csv")
    cycles = load_cycles()
    assert cycles.get("2026-09") == date(2026, 9, 19)
