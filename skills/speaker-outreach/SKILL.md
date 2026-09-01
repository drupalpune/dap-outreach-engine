---
name: speaker-outreach
description: Draft speaker invitations and briefs for a monthly Drupal meetup, and track which session slots are still open. Use when asked to invite speakers, nudge people who haven't replied, help someone find a topic, confirm and brief a speaker, or thank speakers after the meetup. Produces Gmail drafts only, never sends.
---

# Speaker outreach

Filling three slots a month — main session, lightning talk, BoF — and building a
bench so next month starts from a list rather than from nothing.

**Draft, never send.** Everything goes to Gmail drafts for review.

## Slot model

Every meetup has three slots. Track them and never send a generic ask when you
could send a specific one.

| Slot | Length | Notes |
|---|---|---|
| Main session | 45 min + 15 Q&A | Fill first — the announcement needs a headline |
| Lightning talk | 25 min + 5 Q&A | Best slot for a first-time speaker |
| BoF | 45 min discussion | No slides. Lead with this for anyone hesitant. |

Compute open slots by counting `confirmed` rows in `data/speakers.csv` against
these three. "We still have the lightning slot open" converts; "would you like to
speak" doesn't.

## Workflow

### 1. Date and slot state

```bash
python3 scripts/meetup_date.py
python3 scripts/pipeline_report.py
```

Get the meetup date, which slots are filled, and who is overdue a reply.

### 2. Find the row

`data/speakers.csv` (gitignored). Read `name`, `email`, `expertise_tags`,
`preferred_format`, `city`, `last_talk_title`, `last_talk_date`, `stage`,
`last_contacted`, `notes`.

If they aren't in the file, add a row first. Never invent an email address or a
past talk.

### 3. Pick the touch

| `stage` | Touch | File |
|---|---|---|
| `not_contacted` | 1 — invite | `assets/touch-1-invite.md` |
| `invited`, silent 5+ days | 2 — nudge | `assets/touch-2-nudge.md` |
| `interested`, no topic | 2-b — topic suggestions | in `touch-2-nudge.md` |
| `topic_proposed` + agenda locked | 3 — confirm and brief | `assets/touch-3-confirm-and-brief.md` |
| `confirmed`, meetup done | 4 — thank you | `assets/touch-4-thankyou.md` |
| `declined` this month | none until next cycle | — |

### 4. Personalise

- **If they've spoken before, say so, by title.** `last_talk_title` and
  `last_talk_date` exist for this. It is the difference between an invitation
  and a broadcast.
- Match the format to the person, not to what's convenient — see the table in
  `references/session-formats.md`.
- If they're interested but topicless, offer two or three concrete topics from
  `references/topic-prompts.md` crossed with their `expertise_tags`. Most people
  have five talks in them and haven't labelled any of them.
- Lead with the BoF for anyone hesitant. "No slides needed" removes the single
  biggest reason people say no.
- Out-of-town speakers (`city` != Pune) need three weeks' notice and a mention of
  travel. Check `notes`.

Resolve every `{{#if}}` before drafting. Conditional syntax must never appear in
a draft.

### 5. Draft, show, update

Gmail create-draft tool → show the user the full body → update the row:
`stage`, `last_contacted`, `next_action`, `next_action_date`, `notes`.

If Gmail isn't connected, write to `out/` and say so.

## Cadence

| When | Do |
|---|---|
| T-28 | Wave 1 — 6–10 invites. Main session first. |
| T-21 | Announcement live; wave 2 for whatever's still open |
| T-14 | **Agenda locked.** Confirm-and-brief every speaker. |
| T-1 | One-line reminder with time and address |
| T+2 | Thank-you, log the talk, set the 90-day re-invite |

## Volume

6–10 invites in wave one for three slots. Enough for a decent hit rate, not so
many that you're turning people away — which is worse for a community than an
empty slot.

## Handling replies

| They said | Do |
|---|---|
| Yes, with a topic | `topic_proposed`. Confirm at T-14. |
| Yes, no topic | `interested`. Touch 2-b with concrete suggestions. |
| Not this month | `declined`, `next_action_date` = next month's T-28. Ask again. |
| Too nervous / no time | Offer the BoF explicitly. Half the time this converts. |
| Silence, twice | `declined` for this cycle. Try again in two months, not next month. |

## Voice check

Before showing any draft to the user, check it against `docs/voice.md` for the
mail-specific tells. If the `unslop` skill is installed (see
`skills/unslop/ATTRIBUTION.md` - it is fetched, not shipped), run the draft
through that first. A draft that reads as machine-written gets deleted by someone you will
meet at a conference.

Do this to the finished draft, not to the template. Do not strip the voice out
along with the tells.

## References

- `references/session-formats.md` — the three formats and who to offer which
- `references/topic-prompts.md` — turning "I don't have a talk" into a title
