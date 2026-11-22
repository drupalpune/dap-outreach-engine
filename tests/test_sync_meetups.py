"""Tests for scripts/sync_meetups.py."""

import csv
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import sync_meetups as sm  # noqa: E402

DATA = Path(__file__).resolve().parents[1] / "data"
HEADER = ["date", "kind", "host_org", "venue_area", "attendee_count", "main_session",
          "lightning_talk", "bof_topic", "speakers", "linkedin_post_url", "photos_url", "notes"]
SITE_HEADER = [c for c in HEADER if c != "notes"]


def row(**kw):
    return {c: kw.get(c, "") for c in HEADER}


def test_new_site_row_is_added_with_empty_notes():
    local = [row(date="2026-08-22", kind="meetup", notes="keep me")]
    site = [{c: "" for c in SITE_HEADER} | {"date": "2026-09-19", "kind": "meetup", "host_org": "QED42"}]
    merged, report = sm.merge(HEADER, local, SITE_HEADER, site)
    assert [r["date"] for r in merged] == ["2026-08-22", "2026-09-19"]
    assert merged[1]["host_org"] == "QED42" and merged[1]["notes"] == ""
    assert report["added"] == ["2026-09-19"]


def test_site_value_wins_but_blank_never_wipes_and_notes_untouched():
    local = [row(date="2026-08-22", attendee_count="20", linkedin_post_url="https://x.invalid/p", notes="internal")]
    site = [{c: "" for c in SITE_HEADER} | {"date": "2026-08-22", "attendee_count": "22"}]
    merged, report = sm.merge(HEADER, local, SITE_HEADER, site)
    r = merged[0]
    assert r["attendee_count"] == "22"
    assert r["linkedin_post_url"] == "https://x.invalid/p"
    assert r["notes"] == "internal"
    assert report["updated"] == [("2026-08-22", [("attendee_count", "20", "22")])]


def test_local_only_rows_are_kept_and_reported():
    local = [row(date="2024-10-19", kind="camp"), row(date="2026-08-22")]
    site = [{c: "" for c in SITE_HEADER} | {"date": "2026-08-22"}]
    merged, report = sm.merge(HEADER, local, SITE_HEADER, site)
    assert len(merged) == 2
    assert report["local_only"] == ["2024-10-19"]


def test_unknown_site_column_is_rejected():
    with pytest.raises(ValueError):
        sm.merge(HEADER, [], SITE_HEADER + ["surprise"], [])


def test_identical_export_is_a_no_op(tmp_path):
    """The real history, exported the way the site does (no notes), changes nothing."""
    local_path = DATA / "meetups.csv"
    header, local = sm.read_csv(local_path.read_text(encoding="utf-8"))
    export = tmp_path / "export.csv"
    with export.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=[c for c in header if c != "notes"], extrasaction="ignore")
        w.writeheader()
        w.writerows(local)
    site_header, site = sm.read_csv(export.read_text(encoding="utf-8"))
    _, report = sm.merge(header, local, site_header, site)
    assert report["added"] == [] and report["updated"] == [] and report["local_only"] == []


def test_write_round_trip(tmp_path):
    local = tmp_path / "meetups.csv"
    sm.write_csv(local, HEADER, [row(date="2026-08-22", main_session='Talk, with "quotes"')])
    header, rows = sm.read_csv(local.read_text(encoding="utf-8"))
    assert header == HEADER and rows[0]["main_session"] == 'Talk, with "quotes"'
