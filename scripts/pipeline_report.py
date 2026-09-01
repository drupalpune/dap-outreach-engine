#!/usr/bin/env python3
"""Read the venue/speaker CSVs and say what needs doing today.

Falls back to the .sample.csv files when the live ones aren't present, so
a fresh clone still produces output.

Usage:
    python3 scripts/pipeline_report.py
    python3 scripts/pipeline_report.py --data-dir data --today 2026-09-01
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from meetup_date import next_meetup_with_source, due_now  # noqa: E402

VENUE_STAGES = [
    "not_contacted", "contacted", "followed_up", "warm",
    "confirmed", "declined", "not_a_fit",
]
SPEAKER_STAGES = [
    "not_contacted", "invited", "interested", "topic_proposed",
    "confirmed", "declined", "spoke",
]
CLOSED_VENUE = {"confirmed", "declined", "not_a_fit"}
CLOSED_SPEAKER = {"confirmed", "declined", "spoke"}


def resolve(data_dir: Path, name: str) -> Path | None:
    live = data_dir / f"{name}.csv"
    sample = data_dir / f"{name}.sample.csv"
    if live.exists():
        return live
    if sample.exists():
        return sample
    return None


def load(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return [{k: (v or "").strip() for k, v in row.items() if k} for row in csv.DictReader(fh)]


def parse_date(text: str) -> date | None:
    try:
        return date.fromisoformat(text)
    except (ValueError, TypeError):
        return None


def stage_counts(rows: list[dict[str, str]], order: list[str]) -> list[tuple[str, int]]:
    counts = Counter(r.get("stage", "") for r in rows)
    known = [(s, counts.pop(s, 0)) for s in order]
    return known + sorted(counts.items())


def overdue(rows: list[dict[str, str]], today: date, closed: set[str]) -> list[dict[str, str]]:
    out = []
    for r in rows:
        if r.get("stage") in closed:
            continue
        when = parse_date(r.get("next_action_date", ""))
        if when and when <= today:
            out.append(r)
    return sorted(out, key=lambda r: r.get("next_action_date", ""))


def bar(n: int, total: int, width: int = 24) -> str:
    if total == 0:
        return ""
    return "#" * max(1, round(n / total * width)) if n else ""


def report(data_dir: Path, today: date) -> int:
    target, source = next_meetup_with_source(today)
    print(f"DAP pipeline - {today.isoformat()}")
    tag = "confirmed" if source == "confirmed" else "SUGGESTED - date not set"
    print(f"Next meetup: {target.strftime('%a %d %b %Y')}  "
          f"(T-{(target - today).days})  [{tag}]")
    if source != "confirmed":
        print("  Set the real date in data/cycles.csv before drafting anything "
              "that names it.")

    steps = due_now(target, today)
    print("\nDUE NOW")
    if steps:
        for s in steps:
            flag = "TODAY" if s.status == "today" else "OVERDUE"
            print(f"  [{flag:<7}] T-{s.offset:<3} {s.when.isoformat()}  {s.action}  -> {s.skill}")
    else:
        print("  nothing scheduled in the last 3 days")

    for name, order, closed, label in [
        ("venues", VENUE_STAGES, CLOSED_VENUE, "VENUES"),
        ("speakers", SPEAKER_STAGES, CLOSED_SPEAKER, "SPEAKERS"),
    ]:
        path = resolve(data_dir, name)
        print(f"\n{label}")
        if path is None:
            print(f"  no {name}.csv or {name}.sample.csv in {data_dir}")
            continue
        rows = load(path)
        note = "  (sample data)" if path.name.endswith(".sample.csv") else ""
        print(f"  source: {path}{note}   rows: {len(rows)}")
        total = len(rows)
        for stage, n in stage_counts(rows, order):
            if n or stage in order:
                print(f"    {stage:<15} {n:>3}  {bar(n, total)}")
        late = overdue(rows, today, closed)
        if late:
            print(f"  follow-ups due ({len(late)}):")
            key = "org_name" if name == "venues" else "name"
            for r in late:
                who = r.get(key, "?")
                print(f"    - {r['next_action_date']}  {who:<28} {r.get('next_action', '')}")
        else:
            print("  follow-ups due: none")

    path = resolve(data_dir, "meetups")
    if path:
        rows = load(path)
        print(f"\nTRACK RECORD: {len(rows)} meetups logged", end="")
        if rows:
            last = rows[-1]
            print(f", most recent {last.get('date', '?')} at {last.get('host_org', '?')}")
        else:
            print()
    return 0


def pitch(data_dir: Path) -> int:
    """Print the track-record facts for use in a venue mail. Never invent these."""
    path = resolve(data_dir, "meetups")
    if path is None:
        print("no meetups.csv - nothing to claim")
        return 1
    everything = [r for r in load(path) if r.get("date")]
    rows = [r for r in everything if (r.get("kind") or "meetup") == "meetup"]
    other = [r for r in everything if (r.get("kind") or "meetup") != "meetup"]
    if not rows:
        print("meetups.csv is empty - nothing to claim")
        return 1
    rows.sort(key=lambda r: r["date"])
    counts = Counter(r["host_org"] for r in rows if r.get("host_org"))
    nums = [int(r["attendee_count"]) for r in rows if r.get("attendee_count", "").isdigit()]
    recent = [r for r in rows[-6:]][::-1]

    print(f"Meetups logged:   {len(rows)}  ({rows[0]['date']} to {rows[-1]['date']})")
    if nums:
        print(f"Attendance:       {min(nums)}-{max(nums)}, median {sorted(nums)[len(nums)//2]}")
    print(f"Distinct hosts:   {len(counts)}")
    if other:
        kinds = Counter((r.get("kind") or "?") for r in other)
        extra = ", ".join(f"{v} {k}" for k, v in sorted(kinds.items()))
        print(f"Also on record:   {extra} (not counted above)")
    by_year: dict[str, list[int]] = {}
    for r in rows:
        if r.get("attendee_count", "").isdigit():
            by_year.setdefault(r["date"][:4], []).append(int(r["attendee_count"]))
    if len(by_year) > 1:
        trend = "  ".join(
            f"{y}: {sum(v)//len(v)} avg over {len(v)}" for y, v in sorted(by_year.items()))
        print(f"By year:          {trend}")
    print("Recent hosts:     " + ", ".join(f"{r['host_org']} ({r['date'][:7]})" for r in recent))
    print("\nDrop-in line for a first touch:\n")
    seen, names = set(), []
    for r in reversed(rows):                       # most recent distinct hosts
        h = r.get("host_org")
        if h and h not in seen:
            seen.add(h)
            names.append(h)
        if len(names) == 4:
            break
    tail = ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]
    print(f"  We've run {len(rows)} of these, most recently at {rows[-1]['host_org']} in")
    print(f"  {rows[-1]['date'][:7]}. Past hosts include {tail}.")
    print("\nCheck it reads true before sending. These are counted, not estimated.")
    return 0


def main() -> None:
    p = argparse.ArgumentParser(description="Pipeline status report")
    p.add_argument("--pitch", action="store_true",
                   help="print track-record facts for use in a venue mail")
    p.add_argument("--data-dir", default=str(Path(__file__).resolve().parents[1] / "data"))
    p.add_argument("--today", help="override today's date (YYYY-MM-DD)")
    args = p.parse_args()
    today = date.fromisoformat(args.today) if args.today else date.today()
    if args.pitch:
        raise SystemExit(pitch(Path(args.data_dir)))
    raise SystemExit(report(Path(args.data_dir), today))


if __name__ == "__main__":
    main()
