"""Tests for scripts/pipeline_report.py."""

import csv
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import pipeline_report as pr  # noqa: E402

DATA = Path(__file__).resolve().parents[1] / "data"


def test_resolve_falls_back_to_sample():
    path = pr.resolve(DATA, "venues")
    assert path is not None and path.name in ("venues.csv", "venues.sample.csv")
    assert pr.resolve(DATA, "nope") is None


def test_sample_rows_use_valid_stages():
    for name, stages in [("venues", pr.VENUE_STAGES), ("speakers", pr.SPEAKER_STAGES)]:
        rows = pr.load(DATA / f"{name}.sample.csv")
        assert rows
        for row in rows:
            assert row["stage"] in stages, f"{name}: bad stage {row['stage']!r}"


def test_sample_dates_parse():
    for row in pr.load(DATA / "venues.sample.csv"):
        for field in ("first_contacted", "last_contacted", "next_action_date"):
            value = row[field]
            assert value == "" or pr.parse_date(value), f"{field}={value!r}"


def test_overdue_skips_closed_stages():
    rows = [
        {"stage": "contacted", "next_action_date": "2026-08-01"},
        {"stage": "declined", "next_action_date": "2026-08-01"},
        {"stage": "contacted", "next_action_date": "2026-12-01"},
        {"stage": "contacted", "next_action_date": ""},
    ]
    late = pr.overdue(rows, date(2026, 9, 1), pr.CLOSED_VENUE)
    assert len(late) == 1
    assert late[0]["next_action_date"] == "2026-08-01"


def test_stage_counts_lists_every_stage_even_at_zero():
    counts = dict(pr.stage_counts([{"stage": "warm"}], pr.VENUE_STAGES))
    assert counts["warm"] == 1
    assert counts["confirmed"] == 0
    assert set(pr.VENUE_STAGES) <= set(counts)


def test_report_runs_end_to_end(capsys):
    assert pr.report(DATA, date(2026, 9, 1)) == 0
    out = capsys.readouterr().out
    assert "19 Sep 2026" in out
    assert "VENUES" in out and "SPEAKERS" in out


@pytest.mark.parametrize("name", [
    "venues.csv", "speakers.csv", "meetups.csv", "cycles.csv",
    "venues.sample.csv", "speakers.sample.csv",
])
def test_csv_files_are_not_ragged(name):
    """Every row has exactly the header's columns.

    An unquoted comma in a free-text field silently shifts every column after
    it, which is how a note ends up in next_action_date. Catch it here.
    """
    path = DATA / name
    if not path.exists():
        pytest.skip(f"{name} not present")
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for lineno, row in enumerate(reader, start=2):
            assert None not in row, f"{name}:{lineno} has more fields than the header"
            assert all(v is not None for v in row.values()), \
                f"{name}:{lineno} has fewer fields than the header"


def test_no_real_contact_data_in_sample_files():
    """Sample files ship publicly. Every address must be unroutable."""
    for name in ("venues.sample.csv", "speakers.sample.csv"):
        for row in pr.load(DATA / name):
            email = row.get("contact_email") or row.get("email") or ""
            if email:
                assert email.endswith(".invalid"), f"{name}: real-looking address {email}"
