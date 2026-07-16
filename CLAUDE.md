# CLAUDE.md

Canonical project instructions live in `AGENTS.md`. This file is kept only for Claude-compatible tooling.

Skills are organized into bucket folders under `skills/`:

- `engineering/` — daily code work
- `productivity/` — daily non-code workflow tools

Core skills must have a reference in the top-level `README.md` and an entry in both plugin manifests, `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`, which are kept as mirrors of each other. Optional skills may be documented in their bucket README without being part of the manifests.

Each skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`.

Each bucket folder has a `README.md` that lists every skill in the bucket with a one-line description, with the skill name linked to its `SKILL.md`.
