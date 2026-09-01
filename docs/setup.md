# Setup

## 1. Clone and check it runs

```bash
git clone <repo-url> dap-outreach-engine
cd dap-outreach-engine
python3 scripts/meetup_date.py --next 4
```

Python 3.10 or newer. No dependencies for the scripts themselves.

## 2. Run the tests

```bash
python3 -m venv .venv
./.venv/bin/pip install pytest
./.venv/bin/python -m pytest tests/ -q
```

Worth doing after any change to the meetup-day rule — the tests hardcode the
expected dates, so they'll tell you exactly what your change did.

## 3. Create your live pipeline

```bash
cp data/venues.sample.csv data/venues.csv
cp data/speakers.sample.csv data/speakers.csv
```

Delete the fake rows, add your own. Both filenames are in `.gitignore`, so real
contact data can't be committed by accident.

```bash
python3 scripts/pipeline_report.py
```

## 4. Fill in `chapter.yml`

Sender name, email, phone, and your chapter's links. The skills read sender
identity from here so it appears the same way in every draft.

For anything you'd rather not commit, put it in `chapter.local.yml` — also
gitignored, and it overrides `chapter.yml`.

## 5. Install the skills

**Claude Code / Cowork.** Copy or symlink the skill directories into your skills
folder:

```bash
ln -s "$PWD/skills/venue-outreach" ~/.claude/skills/venue-outreach
ln -s "$PWD/skills/speaker-outreach" ~/.claude/skills/speaker-outreach
ln -s "$PWD/skills/meetup-cycle" ~/.claude/skills/meetup-cycle
ln -s "$PWD/skills/prospect-research" ~/.claude/skills/prospect-research
ln -s "$PWD/skills/unslop" ~/.claude/skills/unslop   # only after fetching it
```

Symlinks mean edits to the repo take effect immediately. Restart your session
afterwards so the skills are picked up.

To use them project-locally instead, run from inside this repo with the skills
in `.claude/skills/`.

## 6. Connect Gmail

The outreach skills create Gmail **drafts**. They never send.

Connect the Gmail connector in your Claude settings. The draft-creation scope is
all that's needed; nothing in this repo calls a send API.

If Gmail isn't connected, the skills write drafts to `out/` as markdown files
instead — also gitignored. Perfectly usable, just a copy-paste at the end.

## 7. Test it before it matters

Ask for a first-touch venue mail for a real org and read it end to end. Check:

- Is the date right, and computed rather than typed?
- Does the crossover paragraph actually fit this org, or could it have gone to anyone?
- Is every `{{token}}` resolved?
- Would you send this as-is?

If the answer to the last one is no, fix the template, not the draft.

## Where live data lives

Default is a local gitignored CSV — simple, no accounts, works offline.

Alternatives, if more than one person runs the pipeline:

| Option | Good | Bad |
|---|---|---|
| Local CSV (default) | Simple, private, offline, git-diffable | One machine only |
| Private repo | Versioned, shared, `claimed_by` works | Merge conflicts on a CSV are unpleasant |
| Google Sheet | Genuinely shared, editable on a phone | Needs a connector; export to CSV for the scripts |

Whichever you pick, the rule is unchanged: **real contact data never enters the
public repo.**

## Privacy summary

| Public | Private |
|---|---|
| `*.sample.csv` (fake rows) | `venues.csv`, `speakers.csv` |
| `meetups.csv` (already public on social) | `chapter.local.yml` |
| Skills, scripts, docs | `out/` drafts |
