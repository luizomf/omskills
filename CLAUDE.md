# CLAUDE.md

Canonical project instructions live in `AGENTS.md`. This file is kept only for Claude-compatible tooling.

Skills are organized into bucket folders under `skills/`:

- `engineering/` — daily code work
- `productivity/` — daily non-code workflow tools
- `misc/` — kept around but rarely used
- `personal/` — tied to my own setup, not promoted
- `in-progress/` — drafts not yet ready to ship
- `deprecated/` — no longer used

Core skills must have a reference in the top-level `README.md` and an entry in `.codex-plugin/plugin.json`. Optional skills may be documented in their bucket README without being part of the Codex plugin manifest. Skills in `personal/`, `in-progress/`, and `deprecated/` must not appear in `.codex-plugin/plugin.json`.

Each skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`.

Each bucket folder has a `README.md` that lists every skill in the bucket with a one-line description, with the skill name linked to its `SKILL.md`.
