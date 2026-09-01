# Running this as a different chapter

Nothing here is Pune-specific by design. Forking for Drupal Bangalore, Delhi,
Hyderabad — or a non-Drupal community entirely — is a handful of edits.

## What to change

### 1. `chapter.yml`

Chapter name, city, sender identity, links, meetup timing. One file, and the
skills read from it.

### 2. The meetup day rule — `scripts/meetup_date.py`

Default is the third Saturday:

```python
WEEKDAY = calendar.SATURDAY
NTH = 3
```

Second Sunday is `calendar.SUNDAY` and `2`. Anything not "the nth weekday of the
month" — last Friday, alternate months, a fixed date — means editing
`nth_weekday()`. Update `tests/test_meetup_date.py` in the same commit; the
tests hardcode the third-Saturday dates on purpose, so they'll fail loudly and
tell you exactly what you changed.

### 3. `skills/venue-outreach/references/meetup-facts.md`

Rewrite completely. Your agenda, your attendance, your timings, your asks. This
is the file that appears in every mail.

### 4. `skills/venue-outreach/references/host-icp.md`

The org types transfer; the neighbourhoods and company names don't. Bangalore's
list is Koramangala and Indiranagar, not Baner and Hinjewadi.

### 5. `skills/venue-outreach/references/crossover-angles.md`

Keep the structure, rewrite the paragraphs in your own voice. These get read by
people who know you.

### 6. `data/*.sample.csv`

Leave the schema alone unless you have a reason. Replace the fake rows if you
want examples that look like your city.

### 7. The timeline — `TIMELINE` in `scripts/meetup_date.py`

If your city responds more slowly, push venue wave one to T-60. If you have a
standing venue, drop the venue track to just the T-10 reconfirm and start at
T-28 with speakers.

## What not to change

- **Draft-never-send.** The whole thing depends on a human reading every mail.
- **The privacy split.** Only `*.sample.csv` is public. Live contact data stays
  out of the repo, in every fork.
- **The T+3 re-queue.** The one step that makes month twelve easier than month one.

## Multiple organisers

The `claimed_by` column exists so two people don't mail the same org in the same
week. If more than one person runs the pipeline:

- Set `claimed_by` on every row before wave one goes out
- Agree where the live CSV lives — a shared private repo or a Google Sheet, not
  two laptops
- Agree the sender identity: a shared `contact@` alias is better for continuity,
  a personal address gets better reply rates. Pick one and write it in `chapter.yml`.

## A non-Drupal community

The machinery is community-agnostic — a venue track, a speaker track, a cadence,
a pipeline. Rewrite `meetup-facts.md`, `crossover-angles.md` and
`session-formats.md`, keep everything else. The three-format model (main /
lightning / no-slides discussion) travels particularly well.
