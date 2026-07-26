---
name: setup-omskills
description: Configure repository instructions, issue-tracker operations, triage-label mappings, and domain-doc locations. Run before first use of `to-spec`, `to-tickets`, `triage`, `code-review`, `orchestrate`, `wayfinder`, `diagnosing-bugs`, `tdd`, `improve-codebase-architecture`, or `grill-with-docs`, or when their required repository configuration is missing.
---

# Setup Omskills

Configure:

- the issue tracker used for specs, tickets, issues, and wayfinder maps;
- the tracker strings mapped to the two triage category roles and five state roles; and
- the locations and consumer rules for `CONTEXT.md` and ADRs.

Use repository evidence to recommend values, obtain user confirmation, then write the configuration.

## Process

### 1. Inspect the repository

Check every listed source that exists before making a recommendation:

- `git remote -v` and `.git/config` for tracker host and repository identity;
- root `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, and `CODEX.md` for existing instructions and `## Agent skills` sections;
- root `CONTEXT.md` and `CONTEXT-MAP.md`;
- `docs/adr/` and `src/*/docs/adr/`;
- `docs/agents/` for prior setup output;
- `.scratch/` for an existing local-markdown tracker convention;
- the installed skill list for `triage`; and
- monorepo indicators: `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or populated `packages/*` directories with their own `src/`.

### 2. Resolve configuration choices

Summarize the observed and missing configuration. Process sections A–C in order, ask one question at a time, and wait for its answer. Start each unresolved section with the evidence-based recommendation. Explain the alternatives only when at least two remain consistent with repository evidence. Skip a section when the repository or an earlier user answer already determines it.

#### A. Issue tracker

The configuration tells skills whether to call a tracker CLI, write local Markdown, or follow another recorded workflow.

Recommend GitHub when a remote points to GitHub. Recommend GitLab when a remote points to `gitlab.com` or a self-hosted GitLab instance. When no supported remote determines the tracker, recommend local markdown if `.scratch/` establishes that convention. Otherwise present all alternatives and ask where work is tracked before recommending one:

- **GitHub:** repository GitHub Issues through `gh`.
- **GitLab:** repository GitLab Issues through [`glab`](https://gitlab.com/gitlab-org/cli).
- **Local markdown:** `.scratch/<feature>/` files in this repository.
- **Other, such as Jira or Linear:** ask the user to describe the workflow in one paragraph and record it as freeform prose.

In GitHub and GitLab configurations, set external PRs or MRs as a request surface to off unless the user explicitly enables them.

#### B. Triage label vocabulary

Skip this section when `triage` is not installed.

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

Ask: “Do you want to keep the default triage labels?” Recommend **yes**. By default, each label string equals its canonical role. Ask for individual mappings only if the user answers no. This prevents creation of duplicate labels such as `bug` when the repository uses `type:bug`.

#### C. Domain docs

Engineering skills read domain terms from `CONTEXT.md` and durable architecture decisions from ADRs.

When inspection finds no genuine monorepo signals among the listed indicators, select **single-context** without asking. When inspection confirms a monorepo, ask the user to choose:

- **Single-context:** root `CONTEXT.md` and `docs/adr/` apply repository-wide.
- **Multi-context:** root `CONTEXT-MAP.md` points to per-context `CONTEXT.md` files, typically one per package or subsystem.

### 3. Confirm exact output

Show a draft of:

- the `## Agent skills` block for the selected instruction file;
- `docs/agents/issue-tracker.md`;
- `docs/agents/domain.md`; and
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

For another tracker, write `docs/agents/issue-tracker.md` from the user's recorded operations instead of using a seed template.

#### Provision triage labels

After writing `docs/agents/triage-labels.md`, verify that every mapped label exists:

- for GitHub or GitLab, list repository labels and create only missing mapped labels;
- preserve every existing label's string, color, description, and all unrelated labels; and
- for local markdown, perform no provisioning.

Label setup is complete only when each canonical triage role resolves to an existing configured label.

### 5. Report completion

Setup is complete when the approved instruction block and required `docs/agents/*.md` files exist and, when applicable, every mapped tracker label exists. Report the files written and state that `to-spec`, `to-tickets`, `triage`, `code-review`, `orchestrate`, `wayfinder`, `diagnosing-bugs`, `tdd`, `improve-codebase-architecture`, and `grill-with-docs` will read this configuration. State that users may edit `docs/agents/*.md` directly; rerun this setup only to change trackers or replace the configuration from the beginning.
