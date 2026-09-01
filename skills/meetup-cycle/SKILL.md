---
name: meetup-cycle
description: Orchestrate a monthly Drupal meetup cycle - work out the meetup date, report where the cycle stands against the T-minus timeline, and say what is due today. Use when asked to start a cycle, check where a meetup stands, ask what is overdue, or run the monthly outreach motion. Hands off to venue-outreach and speaker-outreach for actual drafting.
---

# Meetup cycle

The one skill you invoke by name. It works out where you are, tells you what's
due, and hands off to the outreach skills for the drafting.

## Workflow

### 1. Situate

```bash
python3 scripts/meetup_date.py --timeline
python3 scripts/pipeline_report.py
```

**Check whether the date is confirmed or suggested.** The output says which.
Confirmed dates come from `data/cycles.csv` and are the real thing. A suggested
date is the nth-weekday hint and matches the real history only 3 times in 10 -
never put a suggested date in an email. If the cycle you are working on has no
confirmed date, that is the first thing to raise with the user, and once they
decide:

```bash
python3 scripts/meetup_date.py --confirm 2026-10-24
```

That gives the next meetup date, the full T-minus calendar with today marked,
stage counts for both pipelines, and every row whose `next_action_date` has
passed.

For a specific month: `python3 scripts/meetup_date.py 2026-11 --timeline`.

### 2. Report

Lead with the state of the cycle, in this order:

1. **Date and T-minus.** "Next meetup: Sat 19 Sep, T-18, confirmed." Say
   "date not set yet" when it is only the hint - it changes what is safe to draft.
2. **Venue.** Confirmed? Then name the host. Not confirmed? How many are live,
   how many are warm, and how many days until the T-30 deadline. **This is the
   only genuinely blocking item in the cycle** — say so plainly when it's late.
3. **Speakers.** Slots filled and slots open, by name.
4. **Due today.** From the timeline plus every overdue `next_action_date`.
5. **Overdue.** Anything past its date, oldest first.

Keep it short enough to read on a phone. The user is deciding what to do in the
next twenty minutes.

### 3. Hand off

| Due | Skill |
|---|---|
| Venue first touch, follow-up, breakup, confirmation, logistics | `venue-outreach` |
| Speaker invite, nudge, brief, thank-you | `speaker-outreach` |
| Not enough venue leads to work with | `prospect-research` |
| Announcement or recap copy | not built — draft it by hand |

Don't draft mails inside this skill. Say what's due, invoke the right skill.

## The timeline

Owned by `TIMELINE` in `scripts/meetup_date.py`; the human-readable version is
`references/timeline.md`. Change it in the script — the report reads from there.

Three dates are non-negotiable:

- **T-30 venue confirmed.** Everything downstream needs an address. Late venue
  means a late announcement means a smaller room.
- **T-21 announcement live.** Three weeks is the minimum for RSVPs.
- **T-14 agenda locked.** Speakers need two weeks to prepare.

The rest can slip a few days without much cost.

## Behind schedule

Don't just report lateness — say what to cut.

| Situation | Say |
|---|---|
| T-35, no venue | Escalate: call the warm ones today rather than mailing. Add 3–4 leads via `prospect-research`. |
| T-25, no venue | Decision point. Fall back to a known coworking space, or move the meetup a week. Moving it is better than announcing a venue-less date. |
| T-18, one speaker | Cut to a main session plus a BoF. A BoF needs no preparation and can be organised in a week. |
| T-10, no announcement | Post today with whatever is confirmed. An announcement with two of three slots is fine; silence is not. |

## Starting a cycle (around T-45)

1. `python3 scripts/meetup_date.py --next 2` — confirm the date
2. Check `data/venues.csv` for `warm` rows with a `next_action_date` this cycle —
   these are last month's soft nos, and they are the best leads you have
3. If fewer than 6 workable leads, run `prospect-research`
4. Hand to `venue-outreach` for wave one, 5–8 orgs
5. Set `next_action_date` on every row you touch

## Closing a cycle (T+2 to T+3)

1. Append a row to `data/meetups.csv` — date, host, area, headcount, sessions, links
2. `speaker-outreach` touch 4 for every speaker; update `last_talk_title` / `last_talk_date`
3. `venue-outreach` thank-you to the host; ask once about hosting again in six months
4. **Re-queue every `warm` venue row** for next cycle's T-45. A "no, but maybe
   later" is the most valuable output of a cold sequence and the one that always
   gets lost.

## References

- `references/timeline.md` — the T-minus calendar, annotated
- `references/chapter-config.md` — pointing this at a different chapter
