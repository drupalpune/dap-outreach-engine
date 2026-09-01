---
touch: 3
name: Breakup / close-out
send_at: T-32
stage_after: declined
next_action: Re-queue for next cycle
next_action_offset_days: 45
---

# Touch 3 — breakup

The most valuable mail in the sequence, and the one people skip. It converts
silence into a dated re-entry point instead of a dead row.

Genuinely close the loop. Do not make it a third ask wearing a hat.

---

**Subject:** Re: Hosting the {{month}} Drupal Pune meetup — {{meetup_date_short}}?

Hi {{first_name}},

I'm assuming the timing isn't right for {{month}}, so I'll stop filling your
inbox — and we'll get the {{month}} meetup sorted elsewhere.

We run one of these every month, so I'll check back around {{re_ask_month}} in
case things look different then. If something changes before that, or if there's
someone else at {{org_name}} I should be talking to instead, do let me know.

Either way, you're very welcome at the meetup as an attendee — {{meetup_link}}.

Best,
{{sender_name}}

---

## Variant 3-b — they said "not this month"

An explicit soft no is the best outcome short of a yes. Set `stage` to `warm`,
not `declined`, and set `next_action_date` to T+45 of the *next* cycle.

> Hi {{first_name}},
>
> Completely understood — thanks for coming back to me.
>
> I'll check in again around {{re_ask_month}} for the {{re_ask_month}} meetup.
> If there's a month that suits you better, tell me and I'll plan the calendar
> around it instead.
>
> Best,
> {{sender_name}}

## Rules

- Sets `stage` = `declined` (silence) or `warm` (soft no). Never leave it at `followed_up`.
- **Always** sets `next_action_date` to the next cycle. A breakup with no re-entry date is a lost lead.
- Log the reason in `notes` if they gave one. Six months on, "no weekend access" and "not interested" are very different rows.
- No guilt, no "I'll take that as a no then". You will see this person at a conference.
