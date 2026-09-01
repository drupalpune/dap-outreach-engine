---
name: prospect-research
description: Research Pune organisations as potential meetup venue hosts or people as potential speakers, identify plausible contacts from public sources, and append qualified rows to the pipeline. Use when asked to find venue leads, research an org before contacting them, or work out who to approach inside a company.
---

# Prospect research

A research assistant that saves you twenty minutes per lead. Not a lead-gen
machine — be honest about that with the user.

## What this can and cannot do

**Can:** careers pages, engineering blogs and their named authors, public
community and events pages, past meetup and conference sponsor lists,
Drupal.org organisation and user profiles, company About/Team pages, public
GitHub activity, news about offices and funding.

**Cannot:** scrape LinkedIn, find personal email addresses, or verify that
someone still works somewhere. **Email addresses usually have to be filled in by
hand.** Say so rather than guessing a pattern — a bounced first touch is worse
than no first touch.

Never guess at `firstname@company.com`. Leave `contact_email` blank and flag it.

## Researching an org

1. **Check the pipeline first.** If they're already in `data/venues.csv`, say so
   and show the history instead of researching again. Contacting an org twice
   through two different doors is the worst outcome here.
2. **Search** the org: what they build, size, Pune office, tech stack.
3. **Classify** into an `org_type`: `product | services | agency | coworking | edu | community | other`.
4. **Score against the ICP** in `skills/venue-outreach/references/host-icp.md`.
   Say plainly when something is a weak fit — a short list of good leads beats a
   long list of bad ones.
5. **Find the plausible contact.** By preference: community manager / DevRel →
   engineering head → an EM who's active in the community → HR/L&D. Never
   facilities as a first contact. Name the source for every person you name.
6. **Pick the crossover angle** — a key from `crossover-angles.md`, based on
   `org_type` and what you found.
7. **Write the fit note**, one paragraph, into `notes`. Specific: what they
   build, why they'd say yes, what might block it.
8. **Append the row** to `data/venues.csv` with `stage` = `not_contacted` and
   `next_action_date` = the current cycle's T-45.

## Output format

Report per org, before writing anything:

```
ORG          Example Product Labs
Type         product
Fit          Strong - 200-person product company, Baner, PHP in the stack
Contact      Asha Example, Engineering Manager
  source     named author on their engineering blog, Jan 2026
  email      NOT FOUND - needs manual lookup
Angle        php-oss
Why          Ships a PHP-based product, blog shows an open-source bent, Baner
             office is 15 min from the usual crowd. Weekend access unknown -
             worth asking early.
Watch out    No prior community events found; may be a first for them.
```

Then ask before appending rows.

## Finding speaker leads

Same shape, different sources: conference speaker lists (DrupalCon, PHP
conferences, local meetups), engineering blog authors, Drupal.org contribution
profiles, maintainers of modules the community uses, past DAP attendees who
asked good questions.

For a speaker row, note `expertise_tags` from what they've actually written or
talked about, and put the source of the lead in `notes`. A speaker invite that
references their actual work converts far better than a cold ask.

## Guardrails

- **Never invent a name, role, or email.** Blank and flagged beats plausible and wrong.
- **Public sources only.** No LinkedIn scraping, no email-guessing tools, no data brokers.
- Say where each fact came from, so the opening line of the first touch can be honest.
- If research turns up nothing solid, say the org is unresearchable rather than
  padding it.
- 8–10 good leads a cycle. Not thirty. See `references/sourcing-playbook.md`.

The fit note ends up paraphrased in a mail, so run it through the `unslop`
skill before writing it into `notes`.

## References

- `references/sourcing-playbook.md` — where to look, in order
- `skills/venue-outreach/references/host-icp.md` — the fit criteria
