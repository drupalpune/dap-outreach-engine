---
touch: 2
name: Follow-up
send_at: T-38
stage_after: followed_up
next_action: Breakup mail if still no reply
next_action_offset_days: 6
---

# Touch 2 — follow-up

Four lines. Not forty. The long version already sat in their inbox; sending it
again is the fastest way to get filtered.

Reply in the same thread. New subject lines on a follow-up read as a mail merge.

---

**Subject:** Re: Hosting the {{month}} Drupal Pune meetup — {{meetup_date_short}}?

Hi {{first_name}},

Just floating this back up in case it got buried — we're still looking for a
host for {{meetup_date_long}}.

{{urgency_or_detail_line}}

Happy to send more detail, or to keep it simple: a yes, a no, or a "ask me next
month" all work.

Best,
{{sender_name}}

---

## `{{urgency_or_detail_line}}` — pick one

- **Neutral:** "It's a Saturday morning, 09:30 to 13:30, about thirty people."
- **Something changed:** "We've since confirmed {{speaker_name}} for the main session on {{talk_topic}}."
- **Nearly full:** "We're finalising the venue this week, so I wanted to check before we lock something else in." — only if true.
- **Softening:** "No pressure at all if it's not a fit — just didn't want it to go unanswered."

## Rules

- Only after 5–7 working days of silence. Not three.
- One follow-up. Chasing twice before the breakup mail is where goodwill goes.
- If they replied at all — even "let me check" — this is not the right template.
  Answer their actual message, and set `next_action_date` to whenever they said.
- Never open with "Just following up on my previous email" as the whole message.
