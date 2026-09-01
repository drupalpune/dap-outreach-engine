---
touch: 2
name: Nudge
send_at: T-21
stage_after: invited
next_action: Close out or move to next month
next_action_offset_days: 7
---

# Touch 2 — nudge

Short. Reply in the same thread.

---

**Subject:** Re: DAP {{month}} meetup — {{meetup_date_short}} — would you like to take a slot?

Hi {{first_name}},

Just bumping this — we're locking the agenda on {{rsvp_by_date}}.

{{status_line}}

A no is completely fine, and I'll ask again next month. If it's the topic
that's the blocker, tell me roughly what you work on and I'll suggest something.

Best,
{{sender_name}}

---

## `{{status_line}}` — pick one

- **Slots left:** "We still have {{open_slots}} open."
- **Agenda shaping up:** "{{confirmed_speaker}} is doing the main session on {{topic}}, so there's a good room for it."
- **Down to one:** "We're down to the {{last_slot}} slot."
- **Full:** don't send this. Send the next-month ask instead.

## Variant 2-b — interested but no topic yet

`stage` is `interested` and no topic has landed. This is the highest-value mail
in the speaker track — most people don't think they have a talk.

> Hi {{first_name}},
>
> You mentioned you'd be up for a slot — shall we pin down a topic? Going on what you work on, any of these would land well:
>
> - {{topic_suggestion_1}}
> - {{topic_suggestion_2}}
> - {{topic_suggestion_3}}
>
> Or something else entirely. A rough title is enough for now; we can shape it later.
>
> Best,
> {{sender_name}}

Draw the suggestions from `references/topic-prompts.md` crossed with the row's
`expertise_tags` and `notes`. Concrete and specific to them, never generic.

## Rules

- One nudge. Chasing a volunteer twice is how you lose a speaker for good.
- No reply after this → `declined` for this month, `next_action_date` = next month's T-28. Not a permanent no.
- If they said "maybe next month", believe them and diarise it.
