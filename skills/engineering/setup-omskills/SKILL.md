---
name: setup-omskills
description: Configure repository instructions, issue-tracker operations, triage-label mappings, and domain-doc locations. Use when tracker-backed planning or delivery lacks the required repository configuration.
---

# Setup Omskills

Configure:

- the issue tracker and exact repository used for Specs, Tickets, issues, and Wayfinder maps;
- the tracker strings mapped to the two triage category roles and five state roles; and
- the locations and consumer rules for `CONTEXT.md` and ADRs.

Use repository evidence to recommend values, obtain user confirmation, then write the configuration.

## Process

### 1. Inspect the repository safely

Check every listed source that exists before making a recommendation:

- remote names from `git remote`, without URLs;
- root `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, and `CODEX.md` for existing instructions and `## Agent skills` sections;
- root `CONTEXT.md` and `CONTEXT-MAP.md`;
- root `docs/adr/` and, when a context map exists, the context and ADR paths derived from its actual local `CONTEXT.md` links;
- `docs/agents/` for prior setup output, including a previously selected remote;
- `.scratch/` for an existing local-markdown tracker convention;
- the installed skill list for `triage`; and
- monorepo indicators: `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or populated `packages/*` directories with their own `src/`.

Select a remote before inspecting any remote URL:

1. With no remotes, continue without remote evidence.
2. With one remote, select it.
3. With multiple remotes, reuse a remote explicitly recorded by the existing setup only when it is still present. Otherwise the repository target is materially ambiguous: list only the remote names, recommend the likely intended one when repository evidence supports it, and ask which to use.

After selection, run the bundled `scripts/inspect-remote.py` with that one remote name. It calls `git remote get-url` for only the selected remote and emits only the credential-free host, repository path, and normalized repository target. Never run `git remote -v`, print the raw URL, read or copy `.git/config`, or persist userinfo, tokens, or other credential-bearing URL parts.

### 2. Resolve configuration choices

Summarize the observed and missing configuration. Process sections A–C in order, ask one question at a time, and wait for its answer. Start each unresolved section with the evidence-based recommendation. Explain alternatives only when at least two remain consistent with repository evidence. Skip a section when the repository or an earlier user answer already determines it.

#### A. Issue tracker and repository

The configuration tells skills whether to call a tracker CLI, write local Markdown, or follow another recorded workflow. For a hosted tracker, it also records the selected remote and credential-free repository target; every generated CLI operation must target that repository explicitly instead of relying on ambient remote inference. For GitLab, resolve and record the numeric project ID with a read-only API call so later API operations also target the selected project explicitly.

Recommend GitHub when the selected remote points to GitHub. Recommend GitLab when it points to `gitlab.com` or repository evidence identifies its host as a self-hosted GitLab instance. When no supported selected remote determines the tracker, recommend local markdown if `.scratch/` establishes that convention. Otherwise present all alternatives and ask where work is tracked before recommending one:

- **GitHub:** repository GitHub Issues through `gh`.
- **GitLab:** repository GitLab Issues through [`glab`](https://gitlab.com/gitlab-org/cli).
- **Local markdown:** `.scratch/<feature>/` files in this repository.
- **Other, such as Jira or Linear:** ask the user to describe the workflow in one paragraph and record it as freeform prose.

In GitHub and GitLab configurations, set external PRs or MRs as a request surface to off unless the user explicitly enables them.

#### B. Triage label vocabulary

Skip this section when `triage` is not installed.

Before recommending mappings, run the selected tracker's label-inventory operation from its template. Keep each existing label's exact name, color, and description. For local markdown, inventory the role strings already used in tracked files instead of provisioning labels.

Map these canonical roles to labels that already exist or will be created in the configured tracker:

Category roles:

- `bug` — existing behavior is broken
- `enhancement` — new or changed behavior

State roles:

- `needs-triage` — maintainer evaluation pending
- `needs-info` — reporter information pending
- `ready-for-agent` — recorded context is sufficient for agent execution
- `ready-for-human` — human implementation required
- `wontfix` — request will not be actioned

For each role, prefer an exact existing canonical label. When it is absent, identify likely semantic equivalents from existing names and descriptions, such as `type:bug`, and recommend one rather than creating a duplicate. Ask when multiple plausible equivalents remain. Recommend creating the canonical label only when the inventory shows no semantic equivalent. Then ask whether to accept the complete recommended mapping; ask for individual mappings only if the user declines it.

#### C. Domain docs

Engineering skills read domain terms from `CONTEXT.md` and durable architecture decisions from ADRs.

When inspection finds no genuine monorepo signals among the listed indicators, select **single-context** without asking. When inspection confirms a monorepo, ask the user to choose:

- **Single-context:** root `CONTEXT.md` and `docs/adr/` apply repository-wide.
- **Multi-context:** root `CONTEXT-MAP.md` points to per-context `CONTEXT.md` files, typically one per package or subsystem.

For multi-context output, read the actual local Markdown links under `CONTEXT-MAP.md`'s `## Contexts` section. Resolve each path inside the repository, and derive that context's ADR root as `docs/adr/` under the directory containing the linked `CONTEXT.md`. Do not assume `src/*` or infer context roots from workspace layout. If the map has no valid local context entries, report it as incomplete instead of inventing paths.

### 3. Confirm exact output

Show a draft of:

- the `## Agent skills` block for the selected instruction file;
- `docs/agents/issue-tracker.md`, including the selected remote/repository target and complete consumer operations;
- `docs/agents/domain.md`, including every context and ADR root derived from the map when multi-context; and
- `docs/agents/triage-labels.md` when `triage` is installed.

Wait for the user to approve or edit the draft before writing.

### 4. Write configuration

Select the instruction file with these rules, in order:

1. If root `AGENTS.md` exists, update it.
2. Otherwise, if one or more of `GEMINI.md`, `CLAUDE.md`, or `CODEX.md` exists, list those files and ask which is canonical. Recommend creating `AGENTS.md` unless the repository intentionally uses a tool-specific file.
3. If none exists, ask before creating `AGENTS.md` and recommend that name.

If the user identifies a `CLAUDE.md` as inherited or third-party upstream content, create or update `AGENTS.md` instead.

Replace an existing `## Agent skills` block in place. Otherwise append one without changing surrounding user content:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout — "single-context" or "multi-context"]. See `docs/agents/domain.md`.
```

Include the triage-label subsection and file only when `triage` is installed.

Use these seed templates for the docs files:

- [issue-tracker-github.md](./issue-tracker-github.md) for GitHub;
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md) for GitLab;
- [issue-tracker-local.md](./issue-tracker-local.md) for local markdown;
- [triage-labels.md](./triage-labels.md) for label mapping; and
- [domain.md](./domain.md) for domain-doc consumer rules and layout.

Replace every template placeholder with the approved repository-specific value. For another tracker, write `docs/agents/issue-tracker.md` from the user's recorded operations instead of using a seed template.

#### Provision triage labels

After writing `docs/agents/triage-labels.md`:

1. Re-run the complete label inventory to avoid acting on stale setup evidence.
2. Create only mapped label strings that are still absent and have no approved existing semantic equivalent. Preserve all existing labels and never rename or overwrite one by default.
3. Run the inventory a final time and verify that every canonical triage role resolves to an existing configured label.

For local markdown, perform no provisioning. Label setup is complete only when each canonical triage role resolves to an existing configured label.

### 5. Report completion

Setup is complete when the approved instruction block and required `docs/agents/*.md` files exist, hosted operations explicitly target the selected repository, multi-context paths come from the actual context map, and every mapped tracker label exists when applicable. Report the selected credential-free repository target, files written, and final label verification. State that tracker-backed planning, triage, orchestration, and wayfinding workflows will read this configuration. Users may edit `docs/agents/*.md` directly; rerun this setup only to change trackers or replace the configuration from the beginning.
