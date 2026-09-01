# DAP Outreach Engine

A repeatable monthly motion for running a community meetup: find a venue, find
speakers, tell people. Packaged as Claude Skills, a couple of Python scripts and
a CSV pipeline, so it works the same in month twelve as in month one.

Built for [Drupalers Association Pune](https://drupalpune.in) - 859 members, on
[meetup.com](https://www.meetup.com/pune-drupal-group/) and
[LinkedIn](https://www.linkedin.com/company/102374470/). Any chapter can fork it — see [chapter-config.md](skills/meetup-cycle/references/chapter-config.md).

**The system drafts. You send.** Every mail lands in Gmail drafts for review.
Nothing goes out automatically, ever. Community outreach dies the moment it
feels automated, and a bad draft caught at review costs nothing.

## Why

Every month, the same three jobs, living in your head and in copy-pasted email
drafts. This turns it into a pipeline with a cadence, tracked stages and reusable
templates — the shape a GTM team uses, minus the CRM licence.

| GTM concept | Here |
|---|---|
| ICP | Org profile that makes a good venue host |
| Lead list | `data/venues.csv` |
| Sequence | 3-touch email cadence tied to T-minus meetup date |
| Pipeline stages | not_contacted → contacted → followed_up → warm → confirmed / declined |
| Deal desk | Logistics checklist |
| Second motion | Speaker recruitment |

## Quick start

```bash
python3 scripts/meetup_date.py --next 4
```

```bash
python3 scripts/meetup_date.py --audit
```

`--audit` checks the hint rule against the real history in `data/meetups.csv`.
It currently reports 3 matches out of 10, which is why dates are set by hand.

```bash
cp data/venues.sample.csv data/venues.csv && cp data/speakers.sample.csv data/speakers.csv && python3 scripts/pipeline_report.py
```

Full install, including connecting Gmail: [docs/setup.md](docs/setup.md).

## The four skills

| Skill | Ask it | It does |
|---|---|---|
| **meetup-cycle** | "where are we on the October meetup" | Computes the date, reports the cycle against the timeline, says what's due, hands off |
| **venue-outreach** | "draft a venue mail to X" | Picks the right touch, personalises it, drafts it, updates the pipeline |
| **speaker-outreach** | "invite speakers for October" | Same, plus tracks which of the three slots are open |
| **prospect-research** | "find me venue leads in Pune" | Public-source research on an org, plausible contacts, appends a qualified row |
| **unslop** | (runs automatically) | Strips AI tells from every draft before you see it. Not shipped here - [fetch it](skills/unslop/ATTRIBUTION.md). |

`meetup-cycle` is the one you invoke by name. The rest get pulled in.

Every draft passes a voice check before it reaches you: [docs/voice.md](docs/voice.md) — a venue mail that reads
as machine-written gets deleted, and the person deleting it is someone you'll
meet at a conference.

## Cadence

T = meetup day, set by hand per cycle in [data/cycles.csv](data/cycles.csv).
There is no fixed rule: DAP has met on the first, second, third and fourth
Saturday depending on the month. `meetup_date.py` will suggest a third Saturday
for undecided months and label it clearly as a suggestion, but a suggested date
must never reach an email.

```bash
python3 scripts/meetup_date.py --confirm 2026-10-24
```

| When | Action |
|---|---|
| T-45 | Venue wave 1 — 5–8 orgs |
| T-38 | Venue follow-up |
| T-32 | Breakup mails; escalate warm leads to a call |
| T-30 | **Venue confirmed** + logistics |
| T-28 | Speaker wave 1 — 6–10 invites |
| T-21 | Announcement live; second speaker wave |
| T-14 | **Agenda locked**; brief every speaker |
| T-10 | Logistics reconfirm |
| T-2 | Final check |
| T | Meetup |
| T+2 | Thank-yous, recap, log to `meetups.csv` |
| T+3 | Re-queue "not this month" leads for next cycle |

That last row is the compounding part. A soft no is the most valuable output of
a cold sequence and it's the one that always gets lost.

Full detail: [docs/playbook.md](docs/playbook.md).

## Privacy

Real names, emails and numbers **never enter this repo.** Only `*.sample.csv`
with fake rows is public; `venues.csv` and `speakers.csv` are gitignored.
`meetups.csv` is public history — it's already on social and the website.

## Layout

```
skills/          four Claude Skills, plus a pointer to a fifth: SKILL.md + assets (templates) + references (facts)
scripts/         meetup_date.py (the date + timeline), pipeline_report.py (what's due)
data/            sample CSVs, schema notes, public meetup history, confirmed cycle dates
docs/            playbook.md (runbook), setup.md (install), voice.md (how drafts should read)
tests/           pytest, 37 tests over the date, pipeline and CSV integrity
chapter.yml      chapter name, sender identity, slot definitions
```

## Editing

- The meetup description lives once, in
  [meetup-facts.md](skills/venue-outreach/references/meetup-facts.md). Every mail
  references it.
- Dates are never typed. `scripts/meetup_date.py` computes them.
- The crossover paragraph is conditional on `org_type` — see
  [crossover-angles.md](skills/venue-outreach/references/crossover-angles.md).
  It's the paragraph that changes per target; the rest of the mail is stable.

## Two things worth keeping in mind

**Volume vs relationship.** GTM tooling optimises for throughput. This is a small
pool of Pune orgs you'll keep running into for the next decade. The system should
make you *more* personal per mail, not let you send more of them. Thirty
first-touches a month means something has gone wrong.

**The pipeline is the asset, not the skills.** The templates are two hours of
work. The compounding value is sixty Pune orgs with notes on who said what and
when, and forty speakers with topics they care about. Build the CSVs even if you
never use the skills.

## Licence

MIT. See [LICENSE](LICENSE).
