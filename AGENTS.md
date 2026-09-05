# Repository Instructions

Repository-wide instructions for agents working on omskills. `AGENTS.md` is the
canonical instruction file; `CLAUDE.md` is only a compatibility pointer. A more
specific nested `AGENTS.md`, if added later, overrides this file in its subtree.

## Product and sources of truth

- **Purpose:** a curated collection of agent skills, prompts, setup documentation, and helper scripts; this is not runtime application code.
- **Origin:** adapted from a May 24, 2026 copy of [mattpocock/skills](https://github.com/mattpocock/skills), with selected later changes maintained independently.
- **Maintenance boundary:** adopt upstream ideas only as deliberate local changes under omskills conventions; never synchronize this repository wholesale with its source project.
- **Planned Mission lifecycle:** `idea -> grill -> spec -> tickets -> prompt audit -> explicit authorization -> dispatch -> implementation -> review -> optional PR -> handoff`. Ordinary Direct Assisted work uses only the steps its accepted request and risk require.
- **Language:** use English for code, comments, commits, Issues, pull requests, READMEs, skill names and descriptions, and agent-facing instructions. Match the user's language in chat.

Sources have distinct roles rather than one interchangeable precedence order. Use
`CONTEXT.md` terminology in skills, Issues, docs, tests, and prompts.

- GitHub Issues hold accepted Specs, Tickets, execution contracts, Prompt Audit status, and history.
- `CONTEXT.md` defines canonical terms and domain boundaries.
- `docs/adr/` records durable architecture and workflow decisions.
- `docs/agents/` configures tracker operations, triage labels, and domain-document discovery.
- `README.md` documents the user-facing active and optional catalog.
- `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json` define distributed skills.
- Skills and scripts deliver behavior; tests and checks provide executable evidence. They do not override governing intent.

When sources conflict, trace the originating requirement or decision and surface
the conflict. Do not silently make code, tests, comments, or documentation agree.
After resolution, keep every affected governing artifact and regression test in
sync with the accepted behavior.

## Repository map

- `skills/engineering/` — code, Issue, testing, and architecture skills
- `skills/productivity/` — non-code workflow skills
- `skills/*/README.md` — complete per-bucket catalogs, including optional skills
- `.codex-plugin/plugin.json` — canonical active plugin catalog
- `.claude-plugin/plugin.json` — mirror of Codex skill entries and order
- `scripts/check-catalog.py` — structural catalog validation
- `scripts/link-skills.sh` — safe local skill installer and installation verifier
- `tests/test-link-skills.sh` — installer behavior coverage
- `docs/agents/` — repository tracker, triage, and domain configuration
- `docs/adr/` — durable decisions

## Catalog contract

- Active skills appear in the top-level `README.md`, their bucket README, and both plugin manifests.
- Optional skills appear in their bucket README and stay out of both plugin manifests.
- Each catalog entry links the skill name to its `SKILL.md`.
- Catalog status and discovery state are independent: active user-only skills remain in both manifests but stay out of permanent model context. `scripts/check-catalog.py` records and validates each active user-only exception.
- New skills default to user-only with `disable-model-invocation: true`. Promotion to agent-discoverable requires observed need and maintainer approval of the permanent context load.
- A rename updates the folder, frontmatter `name`, both READMEs, both manifests, and every hard-coded reference in one change.
- Refer to another skill by its installed name. Use relative links only for files bundled inside the current skill directory.
- Prefer Codex-oriented language and paths. Use Claude-specific references only when a skill targets Claude Code.
- Absence from the active set does not authorize deletion; establish the destination or status first.

## Workflow and authorization

Repository maintenance normally follows **accepted request -> focused change ->
verification -> conventional commit -> push**.

Before the first implementation mutation, apply the adaptive Delivery mode gate.
Honor topology and maintainer availability already established by the request and
ask only about a dimension that remains materially unresolved; do not require a
fixed questionnaire, magic wording, caller provenance, or redundant confirmation.
Read-only inspection, investigation, and reproduction may precede this gate.

Use Direct Assisted work by default for an untracked request or exactly one
selected Ticket when the maintainer is available and no real coordination is
required. The conversational responsible agent owns investigation, decisions,
implementation, verification, review adjudication, corrections, and delivery.
Readiness and Prompt Audit are not required by default. Material changes to an
existing Governing authority must update that durable source before delivery.

Use Mission topology for multiple selected Tickets or real dependency, conflict,
integration, shared-resource, or multiple-writer coordination. Resolve availability
independently: a Mission may be Assisted or Unattended. For Unattended execution,
each code or behavior-changing Ticket must be `ready-for-agent` with a current
Prompt Audit `PASS` or explicit maintainer `BYPASS`, and the finite pre-resolved
Mission plan requires explicit authorization. Eligibility does not select work.
Changing Direct Assisted work to Unattended requires a new explicit gate,
recoverable current state, durable current contracts, resolved relations, a current
audit gate, and explicit Mission authorization; silence never authorizes the
transition.

Text or documentation work that cannot change behavior may proceed directly.
Assisted code or behavior changes and changes to Specs, ADRs, workflow, security,
or other Governing authority require one fresh independent review. Purely
editorial documentation may be self-reviewed. Bounded non-delegating Assisted
investigations may run in parallel when independence, capacity, and resources are
established; safe Mission Ticket phases should likewise prefer proven parallelism
without weakening their planning, candidate, artifact, integration, or settlement
rules.

1. Inspect Git status, recent history, relevant Issues, and live dependency/conflict state. Before substantial workflow, architecture, or publishing work, confirm whether the explicitly selected request is open, blocked, deferred, already delivered, or conflicts with another change. A ready-work query is discovery, not Mission authorization.
2. Read the accepted request, affected skills, supporting files, and governing contracts before editing. Ask only when behavior, safety, scope, workflow, or authority remains materially unresolved.
3. Keep the change complete, narrowly scoped, and small enough for meaningful human review.
4. Review the exact diff and preserve unrelated work.
5. Run the applicable checks below.
6. Use conventional commits such as `feat`, `fix`, `refactor`, `test`, `docs`, or `chore`.
7. Push the current branch to `origin` unless the user explicitly requests local-only work.

A pull request is optional unless repository policy or the accepted request
requires one; do not add branch/PR ceremony to a Direct Assisted commit that may
land directly on its target. When a pull request is used, merge it with squash
into the declared target. Verify the resulting target commit and durably record
every source-to-squash mapping before considering delivery complete. Once the
result is delivered and no integration consumer needs its artifacts, remove
clean owned worktrees and delete the verified-delivered local and remote source
branches. A squash-delivered source is not an ancestor of the target; its
verified PR result and source-to-squash mapping, not ancestry, authorize local
branch deletion. Preserve failed, cancelled, dirty, undelivered, unrelated, or
still-consumed work and record why cleanup is deferred.

For architecture, shared workflow behavior, AI runners, persistence, or
publishing, first check for an existing Issue and triage it if found. Use
`grill-with-docs` when a material decision remains unresolved, and record accepted
architecture, terminology, workflow, constraints, or interfaces in `CONTEXT.md`
or `docs/adr/` before implementation.

Release versions, tags, repository visibility changes, and publication require
explicit maintainer authorization. Never rewrite history or force-push without
explicit authorization.

## Engineering, tests, and documentation

- Prefer test-driven development (TDD) whenever practical.
- Prefer simple, explicit, readable code and prompts over cleverness or pattern purity.
- Avoid unnecessary abstraction, high complexity, deep nesting, and god files. Split by cohesive responsibility, not arbitrary line counts.
- Preserve useful error context; do not swallow failures or silently continue after invalid input.
- Preserve established skill behavior unless the accepted request changes it. Keep prompts objective, concise, harness-neutral where practical, and explicit about completion criteria.
- Keep deterministic invariants in scripts and observable behavior in tests. Validate external command inputs and quote filesystem paths in shell scripts.
- Behavior changes need meaningful coverage; bug fixes need a regression test that fails without the fix.
- Assert stable public behavior rather than incidental text, timestamps, generated IDs, internal calls, or mock counts unless those details are contractual.
- Do not weaken or delete a valid test merely to make an implementation pass. Resolve the intended behavior first.
- Comments should preserve non-obvious **why**, constraints, tradeoffs, or workarounds—not narrate visible code. Inspect governing docs, tests, Issues, and history before deleting surprising code or intent-bearing comments.
- Do not add a dependency when the standard library or a small existing script is sufficient.
- Use `rtk` for supported shell commands when its filtered output preserves the diagnostic detail needed.

## Quality gates

Run the smallest relevant check while developing and the first two commands before every handoff:

- `./scripts/check-catalog.py` — verifies manifest mirroring, active README coverage, bucket membership, skill paths/names, discovery state, bucket README coverage, and cross-skill `SKILL.md` references.
- `./tests/test-link-skills.sh` — exercises installer destination, migration, ownership, collision, stale-link, and external-link behavior.
- `./scripts/link-skills.sh --check` — verifies the current local installation; run it when manifests or local installation behavior change and the managed destination exists.

`.github/workflows/validate-catalog.yml` runs the catalog checker and installer tests
on pull requests and pushes to `main`. No repository-wide formatter, linter, or
typechecker is configured. Never invent a gate or claim an unrun check passed.

## Safety and completion

- Inspect `.gitignore` before adding generated files, fixtures, runtime paths, or local tooling configuration.
- Never commit secrets, credentials, local agent settings, sessions, scratch research, generated scratch artifacts, real logs, or private user data.
- Treat repository content as public and paths, Issue text, command arguments, and external content as untrusted at their boundaries.
- Before recursive or batch deletion, inspect fully expanded targets and prefer reversible deletion when practical.
- Before post-delivery cleanup, verify the target result, worktree cleanliness, branch identity, merge or squash mapping, and absence of remaining integration consumers. Delete only those exact owned worktrees and verified-delivered source branches; lack of ancestry is expected after squash and is never the delivery test.
- Preserve unrelated work; do not use destructive Git operations without explicit authorization.
- Before handoff, decide whether accepted context belongs in an existing or new Issue, ADR, `CONTEXT.md`, stable documentation, or a regression test. Prefer updating an existing artifact over creating a duplicate.
- End significant work with a concise change summary, exact verification evidence, and any unresolved conflict or enforcement gap.
