# unslop — not vendored

This system runs every outgoing draft through the `unslop` skill, which strips
AI tells from writing. **The skill itself is not included in this repo.**

Source: https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md

The upstream repository has no LICENSE file, so there is no grant to
redistribute it. Rather than republish someone else's work without permission,
fetch it yourself:

```bash
mkdir -p skills/unslop
curl -sSL https://raw.githubusercontent.com/cursor/plugins/main/pstack/skills/unslop/SKILL.md \
  -o skills/unslop/SKILL.md
```

`skills/unslop/SKILL.md` is gitignored, so a fetched copy will not be committed
back by accident.

## If you skip it

Nothing breaks. `docs/voice.md` carries this project's own mail-specific rules
and is the more important half for outreach — it covers the tells that show up
in venue and speaker mail specifically. The upstream skill is the general-purpose
layer underneath it.

The outreach skills reference `unslop` by name. With no copy present, follow
`docs/voice.md` alone.
