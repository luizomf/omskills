---
name: setup-omskills
description: Sets up an `## Agent skills` block in AGENTS.md/CODEX.md/CLAUDE.md and `docs/agents/` so the omskills engineering skills know this repo's issue tracker, triage label vocabulary, and domain doc layout. Run before first use of `to-spec`, `to-tickets`, `triage`, `code-review`, `wayfinder`, `diagnosing-bugs`, `tdd`, `improve-codebase-architecture`, or `grill-with-docs` - or if those skills appear to be missing context about the issue tracker, triage labels, or domain docs.
disable-model-invocation: true
---

# Setup Omskills

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker** — where issues live (GitHub by default; local markdown is also supported out of the box)
- **Triage labels** — the strings used for the five canonical triage roles
- **Domain docs** — where `CONTEXT.md` and ADRs live, and the consumer rules for reading them

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config` — is this a GitHub repo? Which one?
- `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, and `CODEX.md` at the repo root - which instruction files exist? Is there already an `## Agent skills` section in any of them?
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root
- `docs/adr/` and any `src/*/docs/adr/` directories
- `docs/agents/` — does this skill's prior output already exist?
- `.scratch/` — sign that a local-markdown issue tracker convention is already in use
- Is the `triage` skill installed? This decides whether the label section runs at all.
- Monorepo signals — `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or populated `packages/*` directories with their own `src/`

### 2. Present findings and ask

Summarise what's present and what's missing. Then take the sections in order — one section, one answer, then the next.

Lead each section with the recommended answer so the user can accept it in a word. Give a short explainer only when the choice genuinely branches; skip a section when exploration already settled it.

**Section A — Issue tracker.**

> Explainer: The "issue tracker" is where specs, tickets, issues, and wayfinder maps live for this repo. Skills like `to-spec`, `to-tickets`, `triage`, `code-review`, and `wayfinder` read from and write to it - they need to know whether to call `gh issue create`, write markdown under `.scratch/`, or follow some other workflow you describe. Pick the place you actually track work for this repo.

Default posture: these skills were designed for GitHub. If a `git remote` points at GitHub, propose that. If a `git remote` points at GitLab (`gitlab.com` or a self-hosted host), propose GitLab. Otherwise (or if the user prefers), offer:

- **GitHub** — issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **GitLab** — issues live in the repo's GitLab Issues (uses the [`glab`](https://gitlab.com/gitlab-org/cli) CLI)
- **Local markdown** — issues live as files under `.scratch/<feature>/` in this repo (good for solo projects or repos without a remote)
- **Other** (Jira, Linear, etc.) — ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

Record the choice in `docs/agents/issue-tracker.md`. The GitHub and GitLab templates default external PRs/MRs as a request surface to **off**; leave it off unless the user explicitly asks to triage external contributions as requests.

**Section B — Triage label vocabulary.** Skip this section if `triage` is not installed.

> Explainer: When the `triage` skill processes an incoming issue, it moves it through a state machine - needs evaluation, waiting on reporter, ready for an agent to pick up, ready for a human, or won't fix. To do that, it needs to apply labels (or the equivalent in your issue tracker) that match strings *you've actually configured*. If your repo already uses different label names (e.g. `bug:triage` instead of `needs-triage`), map them here so the skill applies the right ones instead of creating duplicates.

The five canonical roles:

- `needs-triage` — maintainer needs to evaluate
- `needs-info` — waiting on reporter
- `ready-for-agent` — fully specified, ready for an agent to pick up with no extra human context
- `ready-for-human` — needs human implementation
- `wontfix` — will not be actioned

Ask one question: “Do you want to keep the default triage labels?” (recommended: **yes**). Each role's default string equals its name. Only collect overrides when the user says no.

**Section C — Domain docs.**

> Explainer: Some skills (`improve-codebase-architecture`, `diagnosing-bugs`, `tdd`, `grill-with-docs`, `wayfinder`) read a `CONTEXT.md` file to learn the project's domain language, and `docs/adr/` for past architectural decisions. They need to know whether the repo has one global context or multiple (e.g. a monorepo with separate frontend/backend contexts) so they look in the right place.

Default to **single-context** without asking when exploration found no genuine monorepo signals. Offer the choice only for a monorepo:

- **Single-context** — one `CONTEXT.md` + `docs/adr/` at the repo root. Most repos are this.
- **Multi-context** — `CONTEXT-MAP.md` at the root pointing to per-context `CONTEXT.md` files (typically a monorepo).

### 3. Confirm and edit

Show the user a draft of:

- The `## Agent skills` block to add to whichever instruction file is being edited (see step 4 for selection rules)
- The contents of `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, and `docs/agents/triage-labels.md` when `triage` is installed

Let them edit before writing.

### 4. Write

**Pick the file to edit:**

- If `AGENTS.md` exists, edit it. This is the preferred canonical instruction file for the maintainer's repos.
- Else if `GEMINI.md`, `CLAUDE.md`, or `CODEX.md` exists, present the existing files and ask which one should become canonical. Recommend creating `AGENTS.md` unless the repo intentionally uses a tool-specific file.
- If none exists, ask before creating one. Recommend `AGENTS.md`.

Never treat an inherited or third-party `CLAUDE.md` as the user's personal instruction file without confirming. If the user says it came from upstream, create or update `AGENTS.md` instead.

If an `## Agent skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

The block:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout — "single-context" or "multi-context"]. See `docs/agents/domain.md`.
```

Include the triage-label block and file only when `triage` is installed. Then write the docs files using the seed templates in this skill folder as a starting point:

- [issue-tracker-github.md](./issue-tracker-github.md) — GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md) — GitLab issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md) — local-markdown issue tracker
- [triage-labels.md](./triage-labels.md) — label mapping
- [domain.md](./domain.md) — domain doc consumer rules + layout

For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's description.

### 5. Done

Tell the user the setup is complete and which engineering skills will now read from these files. Mention they can edit `docs/agents/*.md` directly later — re-running this skill is only necessary if they want to switch issue trackers or restart from scratch.
