# Rules

AI context for this repository. Read this before doing anything.

---

## Hard Rules

These are non-negotiable. If speed conflicts with these rules, follow the rules.

1. **Start with simple solutions and increase complexity only for a current need.** Do not add dependencies, generic abstractions, scripts, or infrastructure for deferred possibilities.
2. **Understand the accepted request before changing behavior.** Read the relevant issue, `CONTEXT.md`, applicable ADRs, agent configuration, and affected skills or scripts. Ask only when a material behavior, safety, scope, or authority decision remains unresolved.
3. **The approved contract controls.** Skills, scripts, tests, and documentation must not silently redefine established workflows or acceptance criteria.
4. **Use canonical omskills language.** Names in skills, issues, docs, and prompts must follow `CONTEXT.md`.
5. **Keep the catalog synchronized.** Apply active-skill changes consistently across both plugin manifests, the top-level README, the applicable bucket README, frontmatter, and hard-coded references.
6. **Run the smallest relevant check during development and the complete catalog and installer test suite before handoff.** State clearly what was inspected but not executed.
7. **Preserve independent maintenance.** Adopt upstream changes only as deliberate local changes under omskills conventions; do not synchronize this repository wholesale with its source project.
8. **Turn project conversations into durable artifacts.** Record accepted workflow, architecture, terminology, constraints, or publishing decisions in the smallest appropriate issue, ADR, domain doc, test, or repository rule.
9. **Keep `AGENTS.md` as a map, not an encyclopedia.** Put detailed behavior in skills, `CONTEXT.md`, ADRs, agent configuration, scripts, and tests.
10. **Protect public-repository boundaries.** Never commit secrets, credentials, local agent settings, sessions, research scratch files, generated artifacts, or private user data.

**CRITICAL:** Check live GitHub issues and native dependency/conflict state before substantial workflow, architecture, or publishing changes. Confirm whether the request is open, blocked, deferred, already delivered, or in conflict with another change.

---

## Repository Context

- **Purpose:** a curated collection of agent skills, prompts, setup documentation, and helper scripts; this is not runtime application code.
- **Origin:** adapted from a May 24, 2026 copy of [mattpocock/skills](https://github.com/mattpocock/skills), with selected later changes maintained independently.
- **Default flow:** `idea -> grill -> spec -> tickets -> implement -> review -> PR -> handoff`.
- **Language:** English for code, comments, commits, issues, pull requests, READMEs, skill names and descriptions, and agent-facing instructions. Match the user's language in chat.
- End significant changes with a concise summary and exact verification evidence.

## Project Map

### Sources of Truth

- GitHub Issues hold specs, tickets, and issue history.
- `CONTEXT.md` defines canonical domain language and boundaries.
- `docs/adr/` contains durable architecture and workflow decisions.
- `docs/agents/` configures tracker, labels, and domain-document discovery.
- `README.md` documents the active and optional catalog for users.
- Plugin manifests define the skills distributed to supported harnesses.
- Skill files, scripts, and tests establish delivered behavior.

When sources conflict, surface the conflict instead of silently choosing one.

### Stable Paths

- `skills/engineering/` — code, issue, and architecture skills
- `skills/productivity/` — non-code workflow skills
- `.codex-plugin/plugin.json` — Codex plugin catalog
- `.claude-plugin/plugin.json` — Claude plugin catalog; mirrors the Codex skill entries and order
- `scripts/check-catalog.py` — catalog consistency validation
- `scripts/link-skills.sh` — safe local skill installer and verifier
- `tests/test-link-skills.sh` — installer behavior coverage
- `docs/agents/` — repository-specific tracker, triage, and domain configuration
- `docs/audits/` — historical compatibility and migration records

## Catalog Boundaries

- Core skills appear in the top-level `README.md` and both plugin manifests.
- Optional skills may appear only in their bucket README.
- Each top-level active-skill entry links its name to its `SKILL.md`.
- Each bucket README lists every skill in that bucket with a one-line linked description.
- New skills default to user-only with `disable-model-invocation: true`. Remove it only after observed use demonstrates a need for autonomous selection and a maintainer approves the permanent context load.
- Renames update the folder, frontmatter `name`, both READMEs, both manifests, and all hard-coded references in one change.
- Refer to another skill by its installed name. Use relative links only for files bundled inside the current skill directory.
- Prefer Codex-oriented language and paths. Use Claude-specific references only for skills that target Claude Code.
- Absence from the active set does not authorize deletion; establish the destination or status first.

---

## Workflow

Default flow: **accepted request -> focused change -> verification -> conventional commit -> push**.

1. Inspect Git status, recent history, relevant issues, and dependency/conflict state.
2. Read the affected skills, supporting files, and repository contracts before editing.
3. Keep changes small, complete, and limited to the accepted request.
4. Use conventional commits such as `feat`, `fix`, `refactor`, `test`, `docs`, or `chore`.
5. Verify that the diff contains only intended changes.
6. Run:
   - `./scripts/check-catalog.py`
   - `./tests/test-link-skills.sh`
   - `./scripts/link-skills.sh --check` when local installation behavior or manifests change
7. Push the current branch to `origin` unless the user explicitly requests local-only work.

For architecture, shared workflow behavior, AI runners, persistence, or publishing:

1. Check for an existing issue and triage it if found.
2. Use `grill-with-docs` when an architectural, behavioral, scope, or implementation decision remains unresolved.
3. Record accepted architecture, terminology, workflow, constraints, or interfaces in `CONTEXT.md` or `docs/adr/`.
4. Implement only after applicable decisions are settled.

Release versions, tags, repository visibility changes, and publication require explicit maintainer authorization. Do not rewrite history or force-push without explicit authorization.

### Conversation Capture

Before handoff, decide whether accepted repository-relevant context belongs in:

- an **Issue** for actionable work or follow-up;
- an **ADR** for durable architecture, workflow, security, or publishing decisions;
- **`CONTEXT.md`** for canonical terminology and boundaries;
- **Documentation** for stable user or maintainer guidance;
- a **Test or check** for a mechanical invariant or recurring regression.

Prefer updating an existing artifact over creating a duplicate.

---

## Agent Skills

### Issue Tracker

Specs, tickets, and issues are tracked in GitHub Issues. See `docs/agents/issue-tracker.md`.

### Triage Labels

Use the configured category and state roles. See `docs/agents/triage-labels.md`.

### Domain Docs

This is a single-context repository. Use root `CONTEXT.md` and `docs/adr/` as described in `docs/agents/domain.md`.

---

## Implementation Defaults

- Preserve established skill behavior unless the request explicitly changes it.
- Keep prompts objective, concise, harness-neutral where practical, and explicit about completion criteria.
- Prefer reducing instructions over adding prose that repeats another source of truth.
- Keep deterministic validation in scripts and behavioral expectations in tests.
- Validate external command inputs and quote filesystem paths in shell scripts.
- Do not add a dependency when the standard library or a small existing script is sufficient.
- Use `rtk` for supported shell commands when its filtered output preserves needed diagnostic detail.
- Before installing or testing skills locally, verify both plugin manifests and all affected references.

## Safety Rules

- Inspect `.gitignore` before adding generated files, fixtures, runtime paths, or local tooling configuration.
- Never commit secrets, `.env` files, credentials, private keys, authorization headers, Pi sessions, conversations, scratch research, real logs, or private user data.
- Treat repository content as public and paths, issue text, command arguments, and external content as untrusted at their boundaries.
- Before recursive or batch deletion, inspect fully expanded targets and prefer reversible deletion when practical.
- Preserve unrelated work in the working tree.
- Do not use destructive Git operations or force-pushes without explicit authorization.
