#!/usr/bin/env python3
"""Meetup date arithmetic for a chapter's monthly cadence.

**The date is set by hand, one cycle at a time.** Confirmed dates live in
`data/cycles.csv` and always win. The nth-weekday rule below is only a hint for
months you have not decided yet - DAP's real history runs on the third or fourth
Saturday depending on the month, so no single rule describes it. Run
`--audit` to see that for yourself.

Usage:
    python3 scripts/meetup_date.py                      # next meetup
    python3 scripts/meetup_date.py 2026-10              # that month
    python3 scripts/meetup_date.py --next 4
    python3 scripts/meetup_date.py 2026-10 --timeline
    python3 scripts/meetup_date.py --confirm 2026-10-24 # record a real date
    python3 scripts/meetup_date.py --audit              # rule vs history
"""

from __future__ import annotations

import argparse
import calendar
import csv
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

# The hint rule, used only for months with no confirmed date in cycles.csv.
WEEKDAY = calendar.SATURDAY
NTH = 3

CYCLES_PATH = Path(__file__).resolve().parents[1] / "data" / "cycles.csv"

# T-minus offsets, in days before the meetup. Mirrors docs/playbook.md.
TIMELINE = [
    (45, "Venue wave 1 - 5-8 orgs, first touch", "venue-outreach"),
    (40, "Research top-up if wave 1 list was thin", "prospect-research"),
    (38, "Venue follow-up on non-responders", "venue-outreach"),
    (32, "Breakup mail on cold ones; escalate warm ones to a call", "venue-outreach"),
    (30, "VENUE CONFIRMED. Send confirmation + logistics checklist", "venue-outreach"),
    (28, "Speaker wave 1 - invite 6-10 people", "speaker-outreach"),
    (21, "LinkedIn + meetup.com post live; second speaker wave", "speaker-outreach"),
    (14, "AGENDA LOCKED. Confirm-and-brief mail to each speaker", "speaker-outreach"),
    (10, "Logistics reconfirm with host (headcount, passes, AV)", "venue-outreach"),
    (7, "Reminder post; nudge registrants", "-"),
    (2, "Final check: AV, food, directions, host contact number", "meetup-cycle"),
    (0, "Meetup day", "-"),
    (-2, "Thank-you to host and speakers; recap post; log to meetups.csv", "both"),
    (-3, "Re-queue 'not this month' venue leads for the next cycle", "venue-outreach"),
]


def nth_weekday(year: int, month: int, weekday: int = WEEKDAY, nth: int = NTH) -> date:
    """Return the nth given weekday of a month. Raises if it doesn't exist."""
    if not 1 <= month <= 12:
        raise ValueError(f"month out of range: {month}")
    if nth < 1:
        raise ValueError(f"nth must be >= 1, got {nth}")
    first = date(year, month, 1)
    offset = (weekday - first.weekday()) % 7
    day = 1 + offset + (nth - 1) * 7
    days_in_month = calendar.monthrange(year, month)[1]
    if day > days_in_month:
        raise ValueError(f"no {nth}th weekday {weekday} in {year}-{month:02d}")
    return date(year, month, day)


def meetup_date(year: int, month: int) -> date:
    """The *hint* date for a month, from the nth-weekday rule.

    This is a suggestion, not the meetup date. Use `resolve()`.
    """
    return nth_weekday(year, month)


def load_cycles(path: Path | str | None = None) -> dict[str, date]:
    """Confirmed meetup dates from cycles.csv, keyed 'YYYY-MM'.

    Rows with a blank date, or a status other than 'confirmed', are ignored -
    a planned cycle has no date yet.
    """
    path = Path(path) if path else CYCLES_PATH
    if not path.exists():
        return {}
    out: dict[str, date] = {}
    with path.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            cycle = (row.get("cycle") or "").strip()
            raw = (row.get("meetup_date") or "").strip()
            status = (row.get("status") or "").strip().lower()
            if not cycle or not raw or status != "confirmed":
                continue
            try:
                out[cycle] = date.fromisoformat(raw)
            except ValueError:
                continue
    return out


def resolve(year: int, month: int, cycles: dict[str, date] | None = None) -> tuple[date, str]:
    """The meetup date for a month, and where it came from.

    Returns (date, "confirmed") when cycles.csv has one, else
    (hint, "suggested"). Callers should show the difference - acting on a
    suggested date as though it were settled is how the wrong date reaches
    an email.
    """
    cycles = load_cycles() if cycles is None else cycles
    key = f"{year:04d}-{month:02d}"
    if key in cycles:
        return cycles[key], "confirmed"
    return nth_weekday(year, month), "suggested"


def next_meetup(today: date | None = None, cycles: dict[str, date] | None = None) -> date:
    """The next meetup on or after `today`, confirmed date winning."""
    return next_meetup_with_source(today, cycles)[0]


def next_meetup_with_source(
    today: date | None = None, cycles: dict[str, date] | None = None
) -> tuple[date, str]:
    today = today or date.today()
    cycles = load_cycles() if cycles is None else cycles
    year, month = today.year, today.month
    for _ in range(24):
        when, source = resolve(year, month, cycles)
        if when >= today:
            return when, source
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)
    raise RuntimeError("no meetup date found in the next 24 months")


def upcoming(
    count: int, today: date | None = None, cycles: dict[str, date] | None = None
) -> list[tuple[date, str]]:
    """The next `count` meetups as (date, source) pairs."""
    today = today or date.today()
    cycles = load_cycles() if cycles is None else cycles
    out: list[tuple[date, str]] = []
    cursor = today
    for _ in range(count):
        when, source = next_meetup_with_source(cursor, cycles)
        out.append((when, source))
        cursor = when + timedelta(days=1)
    return out


def confirm(when: date, path: Path | str | None = None, **fields: str) -> None:
    """Record a confirmed meetup date in cycles.csv, updating any existing row."""
    path = Path(path) if path else CYCLES_PATH
    cycle = f"{when.year:04d}-{when.month:02d}"
    cols = ["cycle", "meetup_date", "status", "venue", "notes"]
    rows: list[dict[str, str]] = []
    if path.exists():
        with path.open(newline="", encoding="utf-8") as fh:
            rows = [dict(r) for r in csv.DictReader(fh)]
    row = next((r for r in rows if (r.get("cycle") or "").strip() == cycle), None)
    if row is None:
        row = {c: "" for c in cols}
        row["cycle"] = cycle
        rows.append(row)
    row["meetup_date"] = when.isoformat()
    row["status"] = "confirmed"
    for k, v in fields.items():
        if v:
            row[k] = v
    rows.sort(key=lambda r: r.get("cycle", ""))
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


@dataclass
class TimelineStep:
    offset: int
    when: date
    action: str
    skill: str
    status: str  # "done" | "today" | "upcoming"


def timeline_for(target: date, today: date | None = None) -> list[TimelineStep]:
    """The full T-minus calendar for a meetup, marked against today."""
    today = today or date.today()
    steps = []
    for offset, action, skill in TIMELINE:
        when = target - timedelta(days=offset)
        if when < today:
            status = "done"
        elif when == today:
            status = "today"
        else:
            status = "upcoming"
        steps.append(TimelineStep(offset, when, action, skill, status))
    return steps


def due_now(target: date, today: date | None = None, window: int = 3) -> list[TimelineStep]:
    """Steps due today or within the last `window` days (i.e. overdue)."""
    today = today or date.today()
    out = []
    for step in timeline_for(target, today):
        age = (today - step.when).days
        if 0 <= age <= window:
            out.append(step)
    return out



def which_nth(d: date) -> int:
    """Which occurrence of its own weekday `d` is within its month (1-based)."""
    return (d.day - 1) // 7 + 1


def audit_history(csv_path, weekday: int = WEEKDAY, nth: int = NTH) -> list[tuple]:
    """Compare real meetup dates against the configured rule.

    Returns (date, actual_nth, matches_rule) per row in the history file.
    """
    import csv as _csv

    out = []
    with open(csv_path, newline="", encoding="utf-8") as fh:
        for row in _csv.DictReader(fh):
            raw = (row.get("date") or "").strip()
            if not raw:
                continue
            try:
                d = date.fromisoformat(raw)
            except ValueError:
                continue
            actual = which_nth(d)
            out.append((d, actual, d.weekday() == weekday and actual == nth))
    return sorted(out)


def _parse_month(text: str) -> tuple[int, int]:
    parts = text.split("-")
    if len(parts) < 2:
        raise ValueError(f"expected YYYY-MM, got {text!r}")
    return int(parts[0]), int(parts[1])


def main() -> None:
    p = argparse.ArgumentParser(description="Meetup date arithmetic")
    p.add_argument("month", nargs="?", help="YYYY-MM (default: next upcoming meetup)")
    p.add_argument("--next", type=int, default=0, metavar="N", help="list the next N meetups")
    p.add_argument("--timeline", action="store_true", help="print the T-minus calendar")
    p.add_argument("--today", help="override today's date (YYYY-MM-DD) for testing")
    p.add_argument("--audit", action="store_true",
                   help="check the hint rule against data/meetups.csv")
    p.add_argument("--confirm", metavar="YYYY-MM-DD",
                   help="record a confirmed meetup date in data/cycles.csv")
    p.add_argument("--venue", help="venue to record alongside --confirm")
    args = p.parse_args()

    today = date.fromisoformat(args.today) if args.today else date.today()

    if args.confirm:
        when = date.fromisoformat(args.confirm)
        confirm(when, venue=args.venue or "")
        print(f"Recorded {when.isoformat()} ({when.strftime('%A')}) for "
              f"{when.strftime('%B %Y')} in {CYCLES_PATH}")
        hint = nth_weekday(when.year, when.month)
        if hint != when:
            print(f"  note: the hint rule would have said {hint.isoformat()} "
                  f"({which_nth(hint)} x {when.strftime('%A')}); "
                  f"you set the {which_nth(when)} one.")
        return

    if args.audit:
        path = Path(__file__).resolve().parents[1] / "data" / "meetups.csv"
        if not path.exists():
            print(f"no history file at {path}")
            return
        rows = audit_history(path)
        if not rows:
            print("history file has no dated rows")
            return
        names = {5: "Saturday", 6: "Sunday"}
        print(f"Configured rule: {NTH} x {names.get(WEEKDAY, WEEKDAY)} of the month")
        print(f"History: {path}\n")
        for d, actual, ok in rows:
            mark = "match " if ok else "DIFFER"
            print(f"  [{mark}] {d.isoformat()}  {d.strftime('%a')}  #{actual} of its month")
        hits = sum(1 for _, _, ok in rows if ok)
        print(f"\n{hits}/{len(rows)} match the configured rule.")
        if hits != len(rows):
            counts = {}
            for _, actual, _ in rows:
                counts[actual] = counts.get(actual, 0) + 1
            spread = ", ".join(f"#{k}: {v}" for k, v in sorted(counts.items()))
            print(f"Actual spread: {spread}")
            print("The rule in scripts/meetup_date.py does not describe this history.")
            print("Either fix WEEKDAY/NTH, or accept that the date is set by hand each month")
            print("and treat the computed date as a default to override.")
        return

    if args.next:
        for d, source in upcoming(args.next, today):
            tag = "confirmed" if source == "confirmed" else "suggested"
            print(f"{d.isoformat()}  {d.strftime('%a %d %b %Y')}  [{tag}]")
        return

    if args.month:
        target, source = resolve(*_parse_month(args.month))
    else:
        target, source = next_meetup_with_source(today)
    tag = "CONFIRMED" if source == "confirmed" else "SUGGESTED - not set yet"
    print(f"{target.isoformat()}  {target.strftime('%A %d %B %Y')}  "
          f"(T-{(target - today).days})  [{tag}]")
    if source != "confirmed":
        print(f"  From the {NTH} x {target.strftime('%A')} hint rule, which matches "
              f"3 of the last 10 meetups.")
        print(f"  Set the real date:  python3 {Path(__file__).name} "
              f"--confirm {target.isoformat()}")

    if args.timeline:
        print()
        mark = {"done": "x", "today": ">", "upcoming": " "}
        for s in timeline_for(target, today):
            label = f"T-{s.offset}" if s.offset > 0 else ("T" if s.offset == 0 else f"T+{-s.offset}")
            print(f" [{mark[s.status]}] {label:<5} {s.when.isoformat()}  {s.action}  [{s.skill}]")


if __name__ == "__main__":
    main()
