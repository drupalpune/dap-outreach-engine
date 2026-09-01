# T-minus timeline

T = meetup day, **as confirmed in `data/cycles.csv`**, not as computed. DAP's
real dates have landed on the first, second, third and fourth Saturday depending
on the month; the nth-weekday rule in `meetup_date.py` is a hint for undecided
months and matches only 3 of the last 10 meetups. Everything below counts back
from the confirmed date.

The machine-readable copy of this table is `TIMELINE` in
`scripts/meetup_date.py`; if you change one, change both.

| When | Action | Skill |
|---|---|---|
| T-45 | Venue wave 1 — 5–8 orgs, first touch | `venue-outreach` |
| T-40 | Research top-up if wave 1 was thin | `prospect-research` |
| T-38 | Venue follow-up on non-responders | `venue-outreach` |
| T-32 | Breakup mail on cold ones; escalate warm ones to a call | `venue-outreach` |
| T-30 | **Venue confirmed.** Confirmation + logistics checklist | `venue-outreach` |
| T-28 | Speaker wave 1 — invite 6–10 people | `speaker-outreach` |
| T-21 | LinkedIn + meetup.com post live; second speaker wave | `speaker-outreach` |
| T-14 | **Agenda locked.** Confirm-and-brief each speaker | `speaker-outreach` |
| T-10 | Logistics reconfirm with host | `venue-outreach` |
| T-7 | Reminder post; nudge registrants | — |
| T-2 | Final check: AV, food, directions, host number | `meetup-cycle` |
| T | Meetup day | — |
| T+2 | Thank-yous; recap post; log to `meetups.csv` | both |
| T+3 | Re-queue warm venue leads for next cycle | `venue-outreach` |

## Why the numbers are what they are

**Setting the date is step zero.** Before T-45 means anything, someone has to
decide which Saturday it is and record it:

```bash
python3 scripts/meetup_date.py --confirm 2026-10-24
```

Until then the cycle has a guessed T-minus, and a guessed date must never reach
an email.

**T-45 for venue wave one.** Fifteen working days before the T-30 deadline
covers one follow-up and a breakup, and still leaves room to source more leads
if wave one is thin. If Pune orgs turn out slower than that, move to T-60 — it
is one number in `TIMELINE`.

**T-30 venue confirmed.** Not arbitrary: the announcement goes out at T-21 and
needs an address, and speakers confirm at T-14 partly on where it is.

**T-28 speakers, after the venue.** Deliberate. "Hosted at X on the 17th" is a
much stronger invite than "somewhere in Pune, probably". If the venue slips,
invite anyway at T-24 and mention the venue is being finalised.

**T-21 announcement.** Three weeks is about the floor for RSVPs. Two weeks
noticeably costs attendance.

**T-14 agenda locked.** Speakers need a fortnight. Locking later means either a
worse talk or a dropout.

**T+3 re-queue.** The compounding step. Every "not this month" from this cycle
becomes a dated lead for the next one. Skip it for three months and the pipeline
is back to being a list of cold orgs.

## Cycles overlap

T-45 for next month lands around T-15 of this one. That is normal and it is why
the pipeline lives in a file rather than in your head: at any moment you are
running the tail of one cycle and the head of the next.

## Slippage tolerance

| Milestone | Can slip? |
|---|---|
| T-45 venue wave 1 | Yes, a few days. Past T-40 you're compressed. |
| T-30 venue confirmed | Barely. Past T-25, consider moving the date. |
| T-21 announcement | No. Post with what you have. |
| T-14 agenda locked | A day or two at most. |
| T-10 logistics | Yes, but not past T-5. |
| T-2 final check | No. |
