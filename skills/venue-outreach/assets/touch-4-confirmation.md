---
touch: 4
name: Confirmation and logistics
send_at: T-30
stage_after: confirmed
next_action: Logistics reconfirm
next_action_offset_days: 20
---

# Touch 4 — confirmation

They said yes. This mail makes the yes concrete and gets the logistics answered
while goodwill is high, four weeks out rather than two days out.

Every question here is one you would otherwise be asking by WhatsApp at 22:00
the night before.

---

**Subject:** Confirmed — Drupal Pune meetup at {{org_name}}, {{meetup_date_long}}

Hi {{first_name}},

Brilliant, thank you — {{meetup_date_long}} at {{org_name}} it is.

Here's the shape of the day so there are no surprises:

- **09:30** — we arrive and set up, tea if you're providing it
- **10:00** — welcome and community updates
- **10:15** — main session, 45 min + Q&A
- **11:30** — lightning talk, 25 min
- **12:00** — open discussion (BoF), no slides
- **12:45** — wrap and group photo
- **13:30** — room clear

Expect 25–40 people. I'll send a confirmed headcount about ten days out.

A few things I need from your side, whenever suits:

1. Room and floor, plus a landmark I can put in the directions post
2. Whether a name list is needed for weekend entry, and by when
3. Projector cable — HDMI, or should we bring an adapter?
4. Guest Wi-Fi, and how people get on it
5. Parking, including two-wheelers
6. A mobile number for whoever's on site that morning
7. Your logo for the announcement post

{{food_line}}

We'll announce it on LinkedIn and meetup.com around {{announcement_date}} with
{{org_name}} named as host — shout if you'd like to see the copy first, or if
anyone from your team wants a couple of minutes at the start to introduce
yourselves.

Thanks again for this.

Best,
{{sender_name}}
{{sender_phone}}

---

## `{{food_line}}`

- **Host offered:** "You mentioned tea and snacks — that's genuinely appreciated. Roughly 30 people."
- **Not discussed:** "On refreshments: if tea/coffee is easy on your side that's lovely, and if not we'll arrange it ourselves. Not a condition."
- **DAP covering:** "We'll bring tea and snacks — just point us at a table."

## After sending

- `stage` → `confirmed`
- `next_action` → "Logistics reconfirm", `next_action_date` → T-10
- Add the venue to the announcement draft
- Every other org in `contacted` or `followed_up` for this cycle now needs
  touch 3, not silence. Close them out this week.
