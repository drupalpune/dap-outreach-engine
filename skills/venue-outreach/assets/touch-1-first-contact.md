---
touch: 1
name: First contact
send_at: T-45
stage_after: contacted
next_action: Follow up if no reply
next_action_offset_days: 7
---

# Touch 1 — first contact

Aim: one screen on a phone. Every sentence either establishes credibility or
makes the ask smaller. If the crossover paragraph could have been sent to any
other org, rewrite it.

---

**Subject:** Hosting the {{month}} Drupal Pune meetup — {{meetup_date_short}}?

Hi {{first_name}},

{{opening_line}}

I help run Drupalers Association Pune — a free monthly meetup for developers in
the city. We meet on the third Saturday of every month, and we're looking for a
host for {{meetup_date_long}}. I wanted to ask whether {{org_name}} would be up
for it.

{{crossover_paragraph}}

What it involves on your side:

- A room seating 20–30, roughly 09:30 to 13:30
- A projector or screen with HDMI, and Wi-Fi for the speakers
- Weekend entry access for a named list

We handle everything else — speakers, agenda, promotion, RSVPs, photos. {{track_record_line}}

{{host_benefit_line}}

If this is worth a look, I'm happy to send the full run of show, or drop by and
see the space. And if the timing is wrong, I'll check back for a later month —
no problem either way.

Best,
{{sender_name}}
{{sender_title}}
{{sender_phone}}

---

## Tokens

| Token | Source |
|---|---|
| `{{month}}` | computed from `meetup_date.py` |
| `{{meetup_date_short}}` | e.g. `17 Oct` |
| `{{meetup_date_long}}` | e.g. `Saturday 17 October` |
| `{{first_name}}` | `contact_name` |
| `{{org_name}}` | `org_name` |
| `{{opening_line}}` | from `source` — see below |
| `{{crossover_paragraph}}` | `crossover-angles.md`, keyed on `crossover_angle` or `org_type` |
| `{{track_record_line}}` | counted from `data/meetups.csv` |
| `{{host_benefit_line}}` | one line from the "What a host gets" list in `meetup-facts.md` |
| `{{sender_*}}` | `chapter.yml` |

## Writing `{{opening_line}}`

Derived from the `source` column. It answers "why is this person in my inbox".

| `source` looks like | Opening line |
|---|---|
| Met at an event | "We met at {{event}} back in {{month}} — good to talk about {{topic}} then." |
| Intro from someone | "{{referrer}} suggested I get in touch." |
| Their blog / talk | "I've been reading {{org_name}}'s engineering blog — the post on {{topic}} in particular." |
| Careers page / cold | "Hope you're doing well." — then get straight to it. Don't fake a connection. |
| Hosted before | Use touch 1-b below instead. |

## Variant 1-b — they have hosted before

If `hosted_before` is `yes`, drop the credentials entirely:

> Hi {{first_name}},
>
> Hope you're well. We're planning the {{month}} meetup for {{meetup_date_long}}
> and I wanted to ask first whether {{org_name}} would be up for hosting again —
> {{last_hosted_reference}} worked really well, and a few people still bring it up.
>
> Same shape as last time: 09:30 to 13:30, 25–40 people, we handle the rest.
> Would that work?
>
> Best,
> {{sender_name}}

## Rules

- Never send this without a filled `{{crossover_paragraph}}`.
- No attachments on a first touch.
- Don't say "sponsorship", "partnership opportunity", or "synergy". This is one room, one morning.
- Give them an easy no in the last paragraph. It is what makes the re-ask in three months possible.
