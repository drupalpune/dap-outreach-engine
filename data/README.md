# data/

| File | Public? | What it is |
|---|---|---|
| `venues.sample.csv` | yes | Schema + three fake rows. Copy to `venues.csv` to start. |
| `speakers.sample.csv` | yes | Same, for speakers. |
| `meetups.csv` | yes | Past meetup history. Already public on social/website. |
| `cycles.csv` | yes | Confirmed meetup date per cycle. Just dates and venues. |
| `venues.csv` | **no** | Live pipeline. Gitignored. 11 rows, all past hosts, placeholder or missing contacts. |
| `speakers.csv` | **no** | Live pipeline. Gitignored. 33 rows, everyone who has spoken since Jun 2024. |

Start a live pipeline:

```
cp data/venues.sample.csv data/venues.csv
cp data/speakers.sample.csv data/speakers.csv
```

Then delete the fake rows and add your own. `.gitignore` already covers the
non-sample filenames, so real contact data cannot be committed by accident.

**cycles.csv** holds the confirmed date for each cycle:

```
cycle, meetup_date, status, venue, notes
```

`cycle` is `YYYY-MM`. Only rows with `status` = `confirmed` and a real date are
used; a `planned` row is a placeholder for a month nobody has decided. Written by
`meetup_date.py --confirm`, and safe to edit by hand.

This file exists because DAP has no fixed meetup-day rule - the real dates have
landed on the first, second, third and fourth Saturday. `meetup_date.py --audit`
shows the rule against the history.

## Field notes

**venues.csv**

- `org_type` - `product | services | agency | coworking | edu | community | other`.
  Drives which crossover angle the venue-outreach skill picks.
- `stage` - `not_contacted | contacted | followed_up | warm | confirmed | declined | not_a_fit`.
- `crossover_angle` - a key from `skills/venue-outreach/references/crossover-angles.md`,
  or blank to let the skill pick from `org_type`.
- `next_action_date` - what makes a row show up in `pipeline_report.py`. Always set it.
- `claimed_by` - who owns the conversation. Stops two organizers mailing the same org.

**speakers.csv**

- `stage` - `not_contacted | invited | interested | topic_proposed | confirmed | declined | spoke`.
- `preferred_format` - `session | lightning | bof | any`.
- `last_talk_title` / `last_talk_date` - drives the "you spoke with us before" line.

**meetups.csv** is append-only. One row per meetup, added at T+2 by running
`python3 scripts/sync_meetups.py --write` once the meetup is marked *Held* on
drupalpune.in (the website is now the source of truth for everything except
`notes`). Columns:

```
date, host_org, venue_area, attendee_count, main_session, lightning_talk,
bof_topic, speakers, linkedin_post_url, photos_url, notes
```

`kind` is `meetup | camp | social | planning`. Only `meetup` rows count towards
the track-record pitch: DrupalCamp Pune 2024's row shows 12 because that is
meetup.com RSVPs rather than real camp attendance, and quoting it would be
wrong. `speakers` and `notes` are also additions to the schema in the original plan. Real
meetups run more than three sessions and often have co-presenters, so a
semicolon-separated `speakers` list and a free-text `notes` field were needed to
hold the history without losing anything. `notes` is also where the second BoF,
the sponsor, or the reason for a low turnout goes.

Backfilled from the meetup.com group's past events on 1 September 2026: ten
without logging in, then ten more from the organiser view. Twenty events,
Jun 2024 to Aug 2026. The group page reports 53 events in total but the past
list stops at twenty even when signed in as an organiser, so anything before
Jun 2024 is still missing.
