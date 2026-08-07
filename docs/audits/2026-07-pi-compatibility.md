# Pi compatibility audit

> **Historical snapshot:** This audit records the catalog and Pi 0.80.10 compatibility state introduced by commit `50cf110` on July 19, 2026. Skill names and active status below may differ from the current catalog.

Pre-publication tracker item 17: Audit active skills for Pi compatibility

## Scope and baseline

This audit compares all 26 active omskills with Pi 0.80.10 and the current Docker Sandbox. It is a compatibility inventory, not authorization to rewrite every skill or expose blocked skills to Pi.

Pi implements the Agent Skills standard and recursively discovers `SKILL.md` files. It natively supports `disable-model-invocation`; `argument-hint` is unknown frontmatter and is ignored with a warning. User commands are `/skill:<name>`, not Codex's `/<name>` form. Arguments after a Pi skill command are appended to the loaded skill as `User: <args>`.

The repository's per-repo setup contract remains valid. Before first use in a repository, invoke `/skill:setup-omskills` so tracker, triage-label, and domain-doc assumptions are explicit. In particular, the hard dependencies recorded in ADR 0001 remain hard dependencies.

The official Pi subagent example is not currently installed. It can run isolated Pi subprocesses in single, parallel, or chain mode, but its tool is not Codex's `spawn_agent`, and it does not provide persistent Codex tasks, cross-task messaging, scheduled heartbeats, or `create_thread`.

`/tmp` actually exists in the current sandbox, but it is not the user's chosen agent scratch area and should not be treated as a durable environmental contract. Disposable agent artifacts belong under `~/scratch/`; `$TMPDIR` is currently unset.

## Dispositions

- **Ready** — usable in Pi without changing its core behavior.
- **Adapt** — the behavior is portable, but wording, invocation, frontmatter, or environment assumptions need a small Pi-aware change.
- **Blocked** — a required behavior depends on subagents or another unavailable capability.
- **Codex-only** — the core contract depends on Codex task infrastructure that the official Pi subagent example does not replace.

## Skill-by-skill inventory

| Skill | Disposition | Pi compatibility notes |
| --- | --- | --- |
| `grill-with-docs` | Adapt | Composition is portable. Replace or abstract Codex-style `/grilling` and `/domain-modeling` references; Pi user commands use `/skill:*`. |
| `triage` | Adapt | Tracker workflow and `disable-model-invocation` work. Preserve the setup gate; its `/setup-omskills` and composed-skill references need harness-neutral or Pi-aware invocation wording. |
| `improve-codebase-architecture` | Blocked | Requires one clean Explore agent via `spawn_agent`. The official Pi extension could provide isolation after installation, but the tool contract must be rewritten. Its temp fallback must prefer `~/scratch/` in this environment instead of relying on `/tmp`. |
| `setup-omskills` | Adapt | The prompt-driven setup process, templates, and hidden user invocation work in Pi. Invoke it as `/skill:setup-omskills`; update generated/help text without weakening ADR 0001. |
| `to-spec` | Adapt | Core workflow works. Preserve the setup gate and replace the Codex command spelling. |
| `to-tickets` | Adapt | Core workflow works. Preserve the setup gate; update `/implement` and setup command spelling. Fresh-context sizing is conceptual and does not itself require subagents. |
| `implement` | Blocked | Implementation and TDD are available, but its mandatory closing `code-review` currently requires an unavailable clean reviewer. It becomes usable after the review dependency is ported, or only if the contract is deliberately weakened to inline review. |
| `wayfinder` | Adapt | Issue-map workflow does not require subagents. Update composed-skill and setup invocations. Tracker-specific support for native child/dependency operations remains a tracker concern, not a Pi incompatibility. |
| `prototype` | Ready | No harness-specific tool dependency. Branch and artifact behavior remain repository operations. |
| `diagnosing-bugs` | Adapt | Diagnosis loop is portable. Only its handoff to `improve-codebase-architecture` needs portable invocation wording; that downstream skill remains blocked. |
| `research` | Blocked | Requires a background agent. Pi's official example can isolate delegated research but is synchronous from the parent tool's perspective, so the current “keep working while it reads” promise is unavailable without a different extension or a deliberate semantic change. |
| `tdd` | Ready | No Pi-specific incompatibility. |
| `domain-modeling` | Ready | No Pi-specific incompatibility. |
| `codebase-design` | Blocked in one branch | The reference skill is usable, but `DESIGN-IT-TWICE.md` requires a clean designer through `spawn_agent`. Keep that branch unavailable until subagents are ported. |
| `code-review` | Blocked | A clean read-only reviewer is a core quality boundary. Port `spawn_agent` to the installed Pi subagent tool before exposing this skill. |
| `orchestrate-issue-queue` | Blocked | Fresh writers/reviewers can plausibly be ported to Pi subagents, but tool names and role contracts need adaptation. The supervised `PING`/`PONG` task channel is separately unavailable and must remain optional or Codex-only. |
| `resolving-merge-conflicts` | Ready | No harness-specific dependency. Its strong “always resolve” policy is a workflow choice, not a Pi compatibility issue. |
| `supervise-async-codex-task` | Codex-only | Depends on `create_thread`, persistent task addresses, task messaging, wakeups, and scheduled heartbeats. The official Pi subagent example provides none of these. Retain as explicitly Codex-only or design a separate Pi extension; do not pretend subagent installation is sufficient. |
| `grill-me` | Adapt | Interview behavior is portable; update the composed `/grilling` invocation. |
| `caveman` | Ready | Session-persistent communication mode is prompt behavior and works in Pi. |
| `grilling` | Ready | No harness-specific dependency. |
| `prompt-comprehension-audits` | Blocked | Two clean identities are essential to the audit. Port both `spawn_agent(... fork_turns: "none")` calls to isolated Pi subagents before use. |
| `handoff` | Adapt | Pi supports hidden user invocation and passes command arguments, but ignores `argument-hint`. Resolve the output directory explicitly to `~/scratch/` in this environment rather than an ambiguous OS temp directory. |
| `teach` | Adapt | Core workspace workflow works. Pi ignores `argument-hint`; opening generated files may depend on host/TUI integration, so failure to open must not invalidate file creation. |
| `write-a-skill` | Ready | Structure and description guidance match Pi's skill model. Pi-specific package/discovery advice can remain external rather than bloating this generic skill. |
| `writing-great-skills` | Ready | Its `disable-model-invocation` model matches Pi: hidden skills are absent from the system prompt and remain user-invoked. Pi command spelling should be documented at the installation/integration layer, not necessarily in this reference. |

## Cross-cutting incompatibilities

### 1. Invocation syntax

The bodies and repository docs use Codex-style commands such as `/setup-omskills`, `/grilling`, and `/code-review`. Pi registers `/skill:setup-omskills`, `/skill:grilling`, and `/skill:code-review`.

Blindly replacing every command would violate the repository's current Codex-oriented convention and make the collection less portable. Decide first whether omskills remains Codex-first with a Pi integration layer, becomes harness-neutral in skill bodies, or carries harness-specific variants. This is a real repository-level tradeoff and should be recorded before broad edits.

### 2. Frontmatter

`disable-model-invocation` needs no compatibility shim. `argument-hint` has no Pi semantic; Pi still passes command arguments, so behavior is preserved while UI discoverability is not. Do not invent a Pi meaning for the field.

### 3. Scratch paths

Two active skills need attention:

- `handoff` asks for the OS temporary directory without resolving one.
- `improve-codebase-architecture` falls back to `/tmp`.

For this sandbox, use `~/scratch/` for disposable agent artifacts. Local-markdown issue storage under a repository's `.scratch/` is durable project workflow and is unrelated; it must not be rewritten to `~/scratch/`.

### 4. Subagents

Hard dependencies:

- `improve-codebase-architecture`
- `code-review`
- `prompt-comprehension-audits`
- substantive delegated paths in `orchestrate-issue-queue`
- `codebase-design`'s Design It Twice branch

Semantic mismatch requiring a decision:

- `research` requires background concurrency, while the official Pi example delegates synchronously.

Not solved by the official example:

- `supervise-async-codex-task`
- supervised task messaging and heartbeat behavior in `orchestrate-issue-queue`

### 5. Installation and discovery

Do not run the Codex linker against Pi. Pi can load this local repository through its `skills` setting or as a local Pi package, and package filters can expose a vetted subset. Loading the repository's conventional `skills/` directory today would discover all 26 skills, including blocked and Codex-only entries. Install only after the exposed subset is decided.

## Recommended migration order

1. Adapt and validate `handoff` as the smallest end-to-end Pi skill.
2. Adapt `setup-omskills`, then validate its first-use flow in a disposable repository under `~/scratch/`.
3. Make a repository-level decision on Codex-first versus harness-neutral invocation wording.
4. Install the official Pi subagent example and test its actual tool contract.
5. Port `code-review` first as the clean-context proof; it unlocks the full `implement` contract.
6. Port `prompt-comprehension-audits`, `improve-codebase-architecture`, and the Design It Twice branch.
7. Decide whether synchronous delegated `research` is acceptable.
8. Treat orchestration separately; retain `supervise-async-codex-task` as Codex-only unless a real Pi task/messaging extension is built.
