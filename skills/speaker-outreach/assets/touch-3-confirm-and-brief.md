---
touch: 3
name: Confirm and brief
send_at: T-14
stage_after: confirmed
next_action: Day-before reminder
next_action_offset_days: 13
---

# Touch 3 — confirm and brief

Agenda is locked. This mail is the speaker's single source of truth: when,
where, how long, what to bring. Everything they'd otherwise message you about at
21:00 the night before.

---

**Subject:** Confirmed — you're on at DAP {{month}}, {{meetup_date_short}}

Hi {{first_name}},

You're locked in. Here are the details:

- **Talk:** {{talk_title}}
- **Format:** {{format}} — {{duration}} including Q&A
- **When:** {{meetup_date_long}}, you're on at about {{slot_time}}
- **Where:** {{host_org}}, {{venue_address}}
- **Arrive:** by {{arrival_time}} for the AV check

The room takes 25–40 people — working developers, tech leads, a few students.
Assume they know Drupal but not your particular corner of it.

Practical bits:

- Bring your own laptop. We'll have HDMI and a USB-C adapter.
- {{recording_line}}
- If you can send slides as a PDF afterwards we'll share them with attendees.
- My number for the day: {{sender_phone}}

{{#if bio_needed}}Could you send a one-line bio and a photo for the announcement post? Two sentences is plenty.{{/if}}

Shout if anything changes — better to know now than on the morning.

Best,
{{sender_name}}

---

## Tokens

| Token | Source |
|---|---|
| `{{talk_title}}` | agreed title. If you don't have one, get it before sending. |
| `{{format}}` / `{{duration}}` | `session-formats.md` |
| `{{slot_time}}` | 10:15 main, 11:30 lightning, 12:00 BoF |
| `{{arrival_time}}` | 20 min before their slot, or 09:30 for the main session |
| `{{venue_address}}` | confirmed row in `venues.csv` |
| `{{recording_line}}` | "We'd like to record it — fine by you?" or "We're not recording this one." |

## For BoF proposers

Swap the practical bits for:

> No slides needed — just open with a couple of minutes on why the topic
> interests you, then let the room take it. I'll be there to keep it moving if
> it stalls.

## Rules

- Never send this without a real `{{talk_title}}` and a real venue.
- Ask about recording. Never assume consent.
- Sets `stage` = `confirmed`, `next_action_date` = T-1 for the reminder.
