---
name: venue-outreach
description: Draft venue-host outreach mails for a monthly Drupal meetup and keep the venue pipeline current. Use when asked to find or contact a host, draft or follow up a venue mail, close out cold venue leads, confirm a venue, or reconfirm logistics with a host. Produces Gmail drafts only, never sends.
---

# Venue outreach

A four-touch sequence for getting a room for the monthly meetup, plus the
bookkeeping that makes the next cycle easier than this one.

**The hard rule: draft, never send.** Everything lands in Gmail drafts for
review. No exceptions, no "this one is obviously fine". Community outreach dies
the moment it reads as automated, and a bad draft caught at review costs nothing.

## Workflow

### 1. Work out the date

```bash
python3 scripts/meetup_date.py --next 2
```

Never type a meetup date by hand. Hardcoded dates are the thing that breaks in
month four.

### 2. Find the row

Live pipeline is `data/venues.csv` (gitignored). If it doesn't exist, say so and
offer to copy `data/venues.sample.csv`. If the org isn't in the file, add a row
rather than drafting off the cuff — an untracked mail is a mail you will send
twice.

Read from the row: `org_name`, `contact_name`, `contact_role`, `contact_email`,
`org_type`, `crossover_angle`, `source`, `stage`, `last_contacted`,
`hosted_before`, `notes`.

Ask the user for anything missing rather than inventing it. **Never invent a
contact name, email, or a prior interaction.**

### 3. Pick the touch

| Current `stage` | Touch | File |
|---|---|---|
| `not_contacted` | 1 — first contact | `assets/touch-1-first-contact.md` |
| `contacted`, 5+ working days silent | 2 — follow-up | `assets/touch-2-followup.md` |
| `followed_up`, still silent | 3 — breakup | `assets/touch-3-breakup.md` |
| said yes | 4 — confirmation | `assets/touch-4-confirmation.md` |
| `warm` (soft no earlier) | 1 again, next cycle | touch 1 with the re-ask opening |
| `declined`, `not_a_fit` | none | Do not mail. Say why. |

If they replied with anything substantive, **none of these templates apply**.
Answer what they actually asked, and use the templates only for structure.

Sanity-check against `last_contacted` before drafting. If it's under five
working days, say so and ask before drafting a chase.

### 4. Fill it in

- Standing facts (agenda, what the host provides, what they get) come from
  `references/meetup-facts.md`. Reference it; don't fork the text into the draft.
- The crossover paragraph comes from `references/crossover-angles.md`, keyed on
  `crossover_angle`, falling back to `org_type`. **Rewrite it in the org's own
  terms** — their stack, their product. A paragraph that would suit any of sixty
  orgs is a paragraph that reads as a merge.
- The track-record line is counted from `data/meetups.csv` at draft time.
- Leave a token as a visible `{{token}}` if you genuinely can't fill it, and flag
  it above the draft. Never guess and never quietly drop it.

### 5. Create the draft

Use the Gmail connector's **create draft** tool. To `contact_email`, subject and
body from the template.

- Plain text. No HTML, no tracking pixels, no images.
- Sender identity comes from `chapter.yml`.
- If Gmail isn't connected, write the draft to `out/` as a markdown file and say
  that's what you did.

Then show the user the full body in the conversation. They review before it goes.

### 6. Update the pipeline

Every draft updates the row — otherwise the pipeline rots and the whole thing is
just templates in a folder:

- `stage` → per the touch's frontmatter
- `last_contacted` → today (and `first_contacted` if blank)
- `next_action` and `next_action_date` → per the touch's frontmatter
- `notes` → anything learned

Tell the user the row changed, and what to.

## Reading a reply

| They said | Do |
|---|---|
| Yes | Touch 4 today. Then close out every other org in this cycle with touch 3. |
| Yes, but a different month | `stage` = `warm`, `next_action_date` = that month's T-45. This is a good outcome. |
| Not this month | Touch 3-b. `stage` = `warm`, re-ask next cycle. |
| Talk to someone else | New row for that person, `source` = "referred by {{name}}". Original row → `not_a_fit`, with the reason. |
| What's the sponsorship cost | Not a fit for this sequence. Say plainly there's no money involved either way. |
| Nothing, twice | Touch 3. Always with a re-entry date. |

## Volume discipline

Eight to ten researched first-touches per cycle. If you're being asked to draft
thirty, say so — ten well-researched mails convert better and don't burn a list
you'll be working for the next decade.

## Voice check

Before showing any draft to the user, check it against `docs/voice.md` for the
mail-specific tells. If the `unslop` skill is installed (see
`skills/unslop/ATTRIBUTION.md` - it is fetched, not shipped), run the draft
through that first. A draft that reads as machine-written gets deleted by someone you will
meet at a conference.

Do this to the finished draft, not to the template. Do not strip the voice out
along with the tells.

## References

- `references/meetup-facts.md` — the stable meetup description. Edit here, once.
- `references/host-icp.md` — who to target, who inside the org, what to skip.
- `references/crossover-angles.md` — one framing per `org_type`.
- `references/logistics-checklist.md` — for touch 4 and the T-10 reconfirm.
