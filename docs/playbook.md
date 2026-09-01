# The monthly playbook

The human-readable version. Everything here can be done without the skills — the
skills just make it faster.

## The shape of a month

Three jobs, every month: find a venue, find speakers, tell people. The venue is
the only one that blocks. Speakers can be found in a fortnight; a room cannot.

At any moment you're running two cycles — the tail of this month's and the head
of next month's. That's why the pipeline lives in a file.

## Step zero: set the date

There is no rule. Pick the Saturday, then record it:

```bash
python3 scripts/meetup_date.py --confirm 2026-10-24
```

Everything else counts backwards from that. Until it is recorded, the scripts
show a suggested date and label it as such, and nothing that names a date should
go out.

## Start here, every time

```bash
python3 scripts/meetup_date.py --timeline
python3 scripts/pipeline_report.py
```

The first says where you are, and whether the date is real or a guess. The
second says who's waiting on you.

```bash
python3 scripts/pipeline_report.py --pitch
```

That one prints the track-record facts for a venue mail, counted from
`meetups.csv`. Never write those numbers from memory.

## Week by week

### T-45 to T-38 — venue wave one

Open `data/venues.csv`. Take, in order:

1. `warm` rows from last cycle whose `next_action_date` has come up. These said
   "not this month" and meant it. Best leads you have.
2. Past hosts from `data/meetups.csv` who haven't hosted in six months.
3. Fresh leads, if the first two give you fewer than six.

Five to eight first touches. Not thirty. Every one gets a crossover paragraph
written for that org — if you can't be bothered writing it, don't send the mail.

Set `next_action_date` on every row. A row without one is invisible to the
report and will be forgotten.

At T-38, one follow-up on anyone silent. Four lines.

### T-32 to T-30 — close the venue

T-32 is the breakup mail for anyone still silent. It feels like giving up; it
isn't. It converts a dead row into a dated lead for next cycle, and it's the
step that makes month twelve easier than month one.

Anyone warm gets a phone call, not a mail. At this point you're four weeks out
and mail is too slow.

T-30, venue confirmed, confirmation mail with the logistics questions. Answer
them now rather than at 22:00 the night before.

If you're at T-25 with no venue: fall back to a coworking space, or move the
meetup by a week. Moving it is better than announcing a date with no address.

### T-28 to T-21 — speakers

Six to ten invites for three slots. Main session first — the announcement needs
a headline.

Reference past talks by title. Lead with the BoF for anyone hesitant; "no slides
needed" removes the single biggest reason people say no.

T-21: announcement live on LinkedIn and meetup.com, host named. Second speaker
wave for whatever's still open, now with a venue to name.

### T-14 to T-7 — lock it

Agenda locked. Confirm-and-brief every speaker: title, format, time, address,
arrival time, your phone number. Ask about recording; never assume.

T-10, reconfirm logistics with the host — headcount, name list, AV, parking.
T-7, reminder post.

### T-2 to T — the meetup

Final check the Thursday before: AV, food, directions, host's mobile number.

On the day, arrive 45 minutes early. Test AV with the actual laptops. Thank the
host from the front of the room, by name. Group photo before people drift off.
Leave the room as you found it — it's the whole basis of the re-ask.

### T+2 to T+3 — close the loop

The part everyone skips, and the part that compounds:

1. Thank-you to the host and the on-site contact. Specific.
2. Thank-you to each speaker, naming something that actually happened in their talk.
3. Recap post, host tagged.
4. Row appended to `data/meetups.csv`.
5. `last_talk_title` / `last_talk_date` updated for each speaker.
6. **Every `warm` venue row re-queued** with `next_action_date` set to next
   cycle's T-45.

Step 6 takes two minutes and is the highest-leverage thing in this document.

## Rules that don't bend

**Draft, never send.** Every mail gets read by a human before it goes. The moment
this feels automated to the person receiving it, it stops working.

**No real contact data in the repo.** Only `*.sample.csv` is public.

**Volume discipline.** Ten researched mails beat thirty templated ones, and don't
burn a list you'll be working for years.

**Every row has a `next_action_date`.** A row without one doesn't exist.

## When it goes wrong

| | |
|---|---|
| No venue at T-25 | Coworking fallback, or move the date a week |
| One speaker at T-18 | Main session + BoF. A BoF can be arranged in a week. |
| Host cancels at T-5 | Coworking space, or the online fallback. Post immediately. |
| Speaker drops at T-3 | Extend Q&A and run a longer BoF. Nobody minds. |
| Nobody replies at all | The list is stale or the mails are generic. Fix the crossover paragraphs before adding names. |
