# AGENTS.md

This is the maintainer's personal skill collection. It started as a fork/adaptation of [mattpocock/skills](https://github.com/mattpocock/skills), copied as it existed on May 24, 2026, and is being adapted to the maintainer's use cases. This is not the original repo; the original is [mattpocock/skills](https://github.com/mattpocock/skills). Treat the original repo as upstream inspiration, not as the maintainer's personal instruction set.

## Communication / Language

- Chat language: match the user's language.
- Project language: English for code, git, GitHub, docs, issues, PRs, README,
  skill names, skill descriptions, and agent-facing instructions.

If you are not 100% sure what to do, ask for clarification.

Always look for local instruction files in this order:

1. `./AGENTS.md`
2. `./GEMINI.md`
3. `./CLAUDE.md`
4. `./CODEX.md`

Use `rtk` for shell commands to keep context cleaner.

## Repo Purpose

`omskills` is not runtime application code. It is a curated set of agent skills, prompts, setup docs, and small helper scripts for the maintainer's workflow with Codex and other coding agents.

The default workflow these skills should reinforce is:

`idea -> grill -> docs -> issue -> branch -> PR -> handoff`

When a task touches architecture, shared behavior, Docker/runtime, AI runners, TTS, persistence, or publish flows, do not jump straight to implementation. First check for an existing issue, triage it, use `grill-with-docs` if there is ambiguity, and record durable decisions in `CONTEXT.md` or `docs/adr/`.

If there is a real tradeoff, unresolved dependency, architectural ambiguity, or two plausible options with different costs, stop and talk to the maintainer.

## Skill Buckets

Skills are organized under `skills/`:

- `engineering/` - daily code work and issue/architecture workflows.
- `productivity/` - non-code workflow tools.
- `misc/` - kept around but not part of the core Codex setup by default.
- `personal/` - tied to someone else's setup or private workflow; not promoted.
- `in-progress/` - drafts not ready to ship.
- `deprecated/` - no longer used.

Core skills should appear in the top-level `README.md` and `.codex-plugin/plugin.json`. Optional skills may be documented in their bucket README without being part of the Codex plugin manifest.

Skills in `personal/`, `in-progress/`, and `deprecated/` must not appear in `.codex-plugin/plugin.json`.

Each active skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`. Each bucket README should list the skills in that bucket with one-line descriptions.

When renaming a skill, update all of these together:

- folder name
- frontmatter `name`
- README references
- bucket README references
- `.codex-plugin/plugin.json`
- hard-coded mentions in other skills, ADRs, scripts, and docs

## Adaptation Rules

Prefer Codex-oriented language and paths. Keep Claude-specific references only when a skill specifically targets Claude Code.

Do not delete inherited material just because it is not part of the first active set. Move or demote it only when the intent is clear.

Before installing or testing skills locally, verify the manifest and references first.
