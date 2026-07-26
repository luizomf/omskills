# AGENTS.md

This repository is the maintainer's independently maintained skill collection. It originated from a May 24, 2026 copy of [mattpocock/skills](https://github.com/mattpocock/skills) and includes selected later changes. Adopt upstream changes only as individual local changes under omskills conventions; do not synchronize this repository with upstream.

## Communication and Language

- Match the user's language in chat.
- Use English for code, git and GitHub content, documentation, issues, pull requests, READMEs, skill names and descriptions, and agent-facing instructions.

Ask for clarification when the requested action is not fully determined by the request and applicable artifacts.

Check local instruction files in this order:

1. `./AGENTS.md`
2. `./GEMINI.md`
3. `./CLAUDE.md`
4. `./CODEX.md`

Use `rtk` for supported shell commands.

After a task changes this repository:

1. Verify that the diff contains only the intended changes.
2. Create a conventional commit.
3. Push the current branch to `origin`.

Always verify and commit completed repository changes. Skip only the push when the maintainer explicitly requests local-only changes.

## Repository Purpose

`omskills` contains agent skills, prompts, setup documentation, and helper scripts; it is not runtime application code.

Skills should support this default sequence:

`idea -> grill -> spec -> tickets -> implement -> review -> PR -> handoff`

For changes to architecture, shared behavior, Docker or runtime behavior, AI runners, TTS, persistence, or publishing:

1. Check for an existing issue and triage it if found.
2. If any architectural, behavioral, scope, or implementation decision remains unresolved, use `grill-with-docs`.
3. Record decisions that establish or change architecture, shared terminology, workflows, constraints, or interfaces in `CONTEXT.md` or `docs/adr/`.
4. Begin implementation only after the issue check and each applicable conditional step are complete.

Stop and consult the maintainer when a dependency is unresolved, an architectural decision remains ambiguous, or plausible options would produce materially different behavior or costs.

## Agent Skills

### Issue tracker

Track specs, tickets, and issues in GitHub Issues. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the two category roles and five state roles from omskills as GitHub labels. See `docs/agents/triage-labels.md`.

### Domain docs

This is a single-context repository. Use `CONTEXT.md` and root-level ADRs as described in `docs/agents/domain.md`.

## Skill Buckets

Store skills under:

- `skills/engineering/` for code, issue, and architecture work;
- `skills/productivity/` for non-code workflow tools.

Keep `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json` identical in skill entries and entry order. Apply every manifest change to both files.

Core skills should appear in the top-level `README.md` and both plugin manifests. Optional skills may be documented in their bucket README without appearing in the plugin manifests.

Omit `disable-model-invocation` from active skills so supporting harnesses receive their names, descriptions, and locations. Set `disable-model-invocation: true` on every new skill until observed use demonstrates a need for autonomous selection and the maintainer approves the permanent context load.

In the top-level `README.md`, each active skill entry must link its name to its `SKILL.md`. Each bucket README should list every skill in that bucket with a one-line description.

When renaming a skill, update all of these in the same change:

- folder name;
- frontmatter `name`;
- top-level and bucket README references;
- `.codex-plugin/plugin.json`;
- `.claude-plugin/plugin.json`;
- hard-coded mentions in skills, ADRs, scripts, and documentation.

## Adaptation Rules

Prefer Codex-oriented language and paths. Use Claude-specific references only in skills that target Claude Code.

An item's absence from the first active set does not authorize its deletion. Move or demote inherited material only when its destination or status is established by the user or repository artifacts.

Before installing or testing skills locally, verify both plugin manifests and all references to the affected skills.

Refer to another skill by its installed name, not by a relative filesystem link. Relative links are only for files bundled inside the current skill directory; some harness tools normalize paths lexically before following installed skill symlinks.
