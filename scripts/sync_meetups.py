#!/usr/bin/env python3
"""Pull meetup history from the website into data/meetups.csv.

Since drupalpune/campsite#234 the website is where meetups are recorded:
an organiser marks a meetup "Held" and fills in talks, speakers and
attendance, and https://www.drupalpune.in/meetups.csv exports every held
meetup with the same columns as data/meetups.csv, minus `notes`.

This script merges that export into data/meetups.csv, matching rows on
`date`:

- A row on the site but not here is added (with empty notes).
- For a row in both, a non-empty site value replaces the local one. An empty
  site value never wipes a local value.
- `notes` is local-only and is never touched.
- A row here but not on the site is kept and reported, never deleted.

Dry run by default: it prints what would change. Pass --write to save.

Usage:
    python3 scripts/sync_meetups.py
    python3 scripts/sync_meetups.py --write
    python3 scripts/sync_meetups.py --source export.csv   # offline / tests
"""

from __future__ import annotations

import argparse
import csv
import io
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_URL = "https://www.drupalpune.in/meetups.csv"
LOCAL_ONLY = {"notes"}


def read_csv(text: str) -> tuple[list[str], list[dict[str, str]]]:
    reader = csv.DictReader(io.StringIO(text))
    return list(reader.fieldnames or []), list(reader)


def fetch(source: str) -> str:
    if source.startswith(("http://", "https://")):
        req = urllib.request.Request(source, headers={"User-Agent": "dap-outreach-engine sync_meetups"})
        with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 (fixed https URL or user-supplied)
            return resp.read().decode("utf-8-sig")
    return Path(source).read_text(encoding="utf-8-sig")


def merge(local_header: list[str], local: list[dict[str, str]],
          site_header: list[str], site: list[dict[str, str]]):
    """Return (merged rows, report). Rows are sorted by date."""
    unknown = [c for c in site_header if c not in local_header]
    if "date" not in site_header:
        raise ValueError("site export has no 'date' column")
    if unknown:
        raise ValueError(f"site export has columns data/meetups.csv doesn't: {unknown}")

    by_date = {row["date"]: dict(row) for row in local}
    report = {"added": [], "updated": [], "local_only": []}
    site_dates = set()
    for srow in site:
        d = srow["date"]
        site_dates.add(d)
        if d not in by_date:
            by_date[d] = {c: (srow.get(c) or "") for c in local_header}
            report["added"].append(d)
            continue
        row = by_date[d]
        changes = []
        for c in site_header:
            if c in LOCAL_ONLY:
                continue
            new = (srow.get(c) or "").strip()
            if new and new != (row.get(c) or "").strip():
                changes.append((c, row.get(c) or "", new))
                row[c] = new
        if changes:
            report["updated"].append((d, changes))
    report["local_only"] = sorted(d for d in by_date if d not in site_dates)
    merged = [by_date[d] for d in sorted(by_date)]
    return merged, report


def write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({c: row.get(c, "") for c in header})


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--source", default=DEFAULT_URL, help="URL or file of the site export")
    ap.add_argument("--local", default=str(ROOT / "data" / "meetups.csv"))
    ap.add_argument("--write", action="store_true", help="save the merge (default: dry run)")
    args = ap.parse_args(argv)

    local_path = Path(args.local)
    local_header, local = read_csv(local_path.read_text(encoding="utf-8"))
    site_header, site = read_csv(fetch(args.source))
    merged, report = merge(local_header, local, site_header, site)

    for d in report["added"]:
        print(f"+ {d}  new from site")
    for d, changes in report["updated"]:
        for col, old, new in changes:
            print(f"~ {d}  {col}: {old!r} -> {new!r}")
    for d in report["local_only"]:
        print(f"= {d}  only in {local_path.name} (kept; not held on the site, or not entered yet)")
    if not report["added"] and not report["updated"]:
        print("No changes from the site.")
        return 0
    if args.write:
        write_csv(local_path, local_header, merged)
        print(f"Wrote {local_path}")
    else:
        print("Dry run. Re-run with --write to save.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
