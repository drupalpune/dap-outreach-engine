# Contributing

Two kinds of contribution: improving this for everyone, and adapting it for your
own chapter.

## Adapting it for your chapter

Fork it. Read
[chapter-config.md](skills/meetup-cycle/references/chapter-config.md) — it lists
the seven files to change and the three things not to.

If you build something that would help other chapters — a new `org_type` and its
crossover angle, a different meetup-day rule, a template that works better than
the one here — send it back.

## Improving the shared parts

Most valuable, in order:

1. **Templates that worked.** If a rewritten touch got a better reply rate, that's
   the highest-value contribution here. Say what changed and roughly what happened.
2. **New `org_type` segments** with a crossover angle. If you keep falling back
   to the generic paragraph, that's a missing segment.
3. **Pipeline tooling.** Sheets sync, a nicer report, deduplication.
4. **Docs.** Anything that confused you on first read is a bug.

## Ground rules

**Never commit real contact data.** Sample rows only, obviously fake, with
`.invalid` email domains. Check `git diff` before every commit. This is the one
rule with no exceptions — if real data lands in a public repo's history, it's a
rewrite to remove.

**Keep draft-never-send.** No PR that adds a send path will be merged. The whole
system rests on a human reading every mail.

**Templates read like a person wrote them.** No corporate voice, no "I hope this
email finds you well", no "synergy". These get read by people the organiser will
meet at conferences.

**Tests pass.**

```bash
python3 -m venv .venv && ./.venv/bin/pip install pytest
./.venv/bin/python -m pytest tests/ -q
```

If you change the meetup-day rule, update the tests in the same commit. They
hardcode the third-Saturday dates deliberately.

## Sending a change

1. Fork, branch
2. Make the change; add a test if it's script behaviour
3. Run the tests
4. Check the diff for real contact data
5. Open a PR saying what changed and why, and — if it's a template — what
   happened when you sent it

## Style

- Markdown, one sentence per line where it helps the diff
- Templates: `{{token}}` placeholders, tokens documented in a table underneath
- Skills: frontmatter `name` and `description`; description says when to use it
- Python: standard library only for the scripts, type hints, docstrings
