---
touch: 1
name: Invite
send_at: T-28
stage_after: invited
next_action: Nudge if no reply
next_action_offset_days: 7
---

# Touch 1 — speaker invite

The base version is section 6 of the build plan, cleaned up. Conditional blocks
are marked; resolve them before drafting, never leave the `{{#if}}` syntax in a
draft.

---

**Subject:** DAP {{month}} meetup — {{meetup_date_short}} — would you like to take a slot?

Hi {{first_name}},

Hope you're doing well.

We've locked in {{meetup_date_long}} for the {{month}} Drupal meetup{{#if venue_confirmed}}, hosted at {{host_org}}{{/if}}, and I wanted to check with you personally before we open the agenda up more widely.

{{#if spoke_before}}You did "{{last_talk_title}}" with us in {{last_talk_month}} and it went down really well — would you be up for another one?{{else}}Would you be interested in taking a slot?{{/if}}

We have three formats:

- **Main session** — 45 min + 15 min Q&A
- **Lightning talk** — 25 min + 5 min Q&A
- **BoF** — propose a topic and lead an open discussion, no slides needed

{{#if open_slots}}Currently open: {{open_slots}}.{{/if}}

Anything around Drupal, AI tooling, DevOps, or your own war stories from production works. If you have a topic in mind but aren't sure it fits, send it over anyway and we'll figure it out.

{{#if announcement_live}}Details and the wider announcement: {{linkedin_post_url}}{{/if}}

If you could let me know by {{rsvp_by_date}}, that'd help us lock the agenda.

Best,
{{sender_name}}

---

## Tokens

| Token | Source |
|---|---|
| `{{meetup_date_long}}` | `meetup_date.py` |
| `{{first_name}}` | `name`, first word |
| `{{venue_confirmed}}` / `{{host_org}}` | a `confirmed` row in `venues.csv` |
| `{{spoke_before}}` | `last_talk_title` is non-empty |
| `{{last_talk_month}}` | from `last_talk_date`, e.g. "March" |
| `{{open_slots}}` | slots without a `confirmed` speaker |
| `{{rsvp_by_date}}` | T-14, the agenda lock |
| `{{announcement_live}}` | true from T-21 |

## `{{open_slots}}` phrasing

- All three: omit the line entirely — an empty agenda reads as an empty room.
- Two left: "Currently open: the lightning slot and the BoF."
- One left: "Currently open: just the lightning slot." — real scarcity, works well.
- None: don't send this. Ask for the *next* month instead.

## Variant 1-b — hesitant or first-time speaker

For anyone whose `notes` say nervous, first-time, or "no time to prepare", lead
with the BoF and cut the format list:

> Hi {{first_name}},
>
> We're running the {{month}} meetup on {{meetup_date_long}}, and I thought of you for the open discussion slot — you propose a topic ({{topic_suggestion}} would be perfect) and just steer the conversation for 45 minutes. No slides, no prep beyond turning up with the question.
>
> It's the easiest slot we have and usually the one people enjoy most. Interested?
>
> Best,
> {{sender_name}}

## Rules

- Personal note in the first two lines. A speaker invite that could go to anyone gets treated as a broadcast.
- Never claim someone spoke before unless `last_talk_title` says so.
- 6–10 invites in wave one. More than that and you're overbooking three slots.
- Only state `{{open_slots}}` when it's accurate.
