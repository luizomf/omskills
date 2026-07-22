# AGENTS.md

This is the maintainer's personal skill collection. It started as a fork/adaptation of [mattpocock/skills](https://github.com/mattpocock/skills), first copied on May 24, 2026, and has since pulled in selected changes from later upstream snapshots. This is not the original repo; the original is [mattpocock/skills](https://github.com/mattpocock/skills). This repository is maintained independently: do not synchronize from the original, and implement useful ideas locally under omskills conventions.

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

After completing a task that changes this repository, verify the intended diff,
create a conventional commit, and push the current branch to `origin` unless
the maintainer explicitly asks to keep the changes local. Treat the private remote as
backup; do not leave finished work only in the worktree.

## Repo Purpose

`omskills` is not runtime application code. It is a curated set of agent skills, prompts, setup docs, and small helper scripts for the maintainer's workflow with Codex and other coding agents.

The default workflow these skills should reinforce is:

`idea -> grill -> spec -> tickets -> implement -> review -> PR -> handoff`

When a task touches architecture, shared behavior, Docker/runtime, AI runners, TTS, persistence, or publish flows, do not jump straight to implementation. First check for an existing issue, triage it, use `grill-with-docs` if there is ambiguity, and record durable decisions in `CONTEXT.md` or `docs/adr/`.

If there is a real tradeoff, unresolved dependency, architectural ambiguity, or two plausible options with different costs, stop and talk to the maintainer.

## Agent skills

### Issue tracker

Specs, tickets, and issues are tracked in GitHub Issues. See `docs/agents/issue-tracker.md`.

### Triage labels

The two category roles and five state roles from omskills are used as GitHub labels. See `docs/agents/triage-labels.md`.

### Domain docs

This is a single-context repository with `CONTEXT.md` and root-level ADRs. See `docs/agents/domain.md`.

## Skill Buckets

Skills are organized under `skills/`:

- `engineering/` - daily code work and issue/architecture workflows.
- `productivity/` - non-code workflow tools.

There are two plugin manifests, `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`. They are mirrors: the same skill list, in the same order. Any change to one must be made to the other.

Core skills should appear in the top-level `README.md` and both plugin manifests. Optional skills may be documented in their bucket README without being part of the manifests.

All active skills are agent-discoverable: omit `disable-model-invocation` so their names, descriptions, and locations enter supporting harnesses' system context. New skills remain user-only by default and must set `disable-model-invocation: true` until observed use justifies the permanent context load and the maintainer approves discovery.

Each active skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`. Each bucket README should list the skills in that bucket with one-line descriptions.

When renaming a skill, update all of these together:

- folder name
- frontmatter `name`
- README references
- bucket README references
- `.codex-plugin/plugin.json`
- `.claude-plugin/plugin.json`
- hard-coded mentions in other skills, ADRs, scripts, and docs

## Adaptation Rules

Prefer Codex-oriented language and paths. Keep Claude-specific references only when a skill specifically targets Claude Code.

Do not delete inherited material just because it is not part of the first active set. Move or demote it only when the intent is clear.

Before installing or testing skills locally, verify the manifest and references first.
