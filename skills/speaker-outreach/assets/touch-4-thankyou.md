---
touch: 4
name: Thank you
send_at: T+2
stage_after: spoke
next_action: Invite again
next_action_offset_days: 90
---

# Touch 4 — thank you

Sent within two days, while it's still fresh. Cheapest retention in the whole
system: this is what makes the next invite a formality.

Specific, or don't bother. "Thanks for speaking" is worse than nothing.

---

**Subject:** Thank you for {{meetup_date_short}}

Hi {{first_name}},

Thanks for taking the {{format}} slot on Saturday — {{specific_praise}}.

{{#if audience_reaction}}{{audience_reaction}}{{/if}}

Recap post is up here: {{linkedin_post_url}} — do share it if you'd like.
{{#if photos_url}}Photos: {{photos_url}}{{/if}}

{{#if slides_pending}}If you can send the slides as a PDF I'll pass them on to everyone who came.{{/if}}

Would love to have you back — I'll shout when we've got a month that suits.

Thanks again,
{{sender_name}}

---

## `{{specific_praise}}`

Name something that actually happened. Take a note during the talk if you have to.

- "the bit on the D7 migration rollback got a lot of nodding in the room"
- "three separate people came up afterwards about the caching setup"
- "the Q&A ran over by ten minutes, which is always a good sign"

## After sending

- `stage` → `spoke`
- `last_talk_title` and `last_talk_date` → this talk. This drives the "you spoke with us in {{month}}" line next time.
- `next_action_date` → +90 days, "invite again"
- Append the talk to `data/meetups.csv`
- Note anything about how they present, in `notes` — useful when slotting them next time

## Also

If someone was *going* to speak and dropped out, or was invited and never got a
slot, send them something too. A one-liner — "sorry we couldn't fit you in this
month, you're first on the list for {{next_month}}" — keeps a bench of speakers
instead of a list of people who were once asked.
