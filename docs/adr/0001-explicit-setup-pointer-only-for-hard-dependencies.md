# Explicit `/setup-omskills` pointer only for hard dependencies

Engineering skills depend on per-repo configuration for issue-tracker operations, triage-label vocabulary, and domain-document layout. Some skills cannot produce correct output without it; others use it only to sharpen output and can degrade gracefully.

We split these into **hard-dependency** and **soft-dependency** skills:

- **Hard dependency** (`to-spec`, `to-tickets`, `triage`, `code-review`, `orchestrate`, `wayfinder`, plus `prompt-comprehension-audits` when it audits a tracked Ticket) — when required configuration is missing, load `setup-omskills` and follow its authorization gate before continuing. Read-only leaves report the missing prerequisite to their responsible caller rather than writing setup.
- **Soft dependency** (`diagnosing-bugs`, `tdd`, `improve-codebase-architecture`, `grill-with-docs`) — reference "the project's domain glossary" and "ADRs in the area you're touching" in general prose only. If those docs do not exist, the skill still works; output is merely less precise.

Explicit task or standing setup authorization may permit standard setup, including required missing triage labels, on repositories within its stated scope without repeated approval. Repository access, ownership, content, and skill use alone do not grant that authority. Preserve existing configuration and label metadata; fill only authorized gaps using established choices and deterministic defaults. Material conflicts or unresolved authority require interactive confirmation, or a blocker when headless. `setup-omskills` owns the detailed gate and defaults.

A Ticket dispatcher neither runs, inspects, nor mediates setup. A headless responsible agent or Ticket coordinator may complete separately authorized, deterministic setup; otherwise it returns a blocker rather than opening setup Questions. Setup permission never selects Tickets, widens Mission implementation scope, bypasses execution gates, or overrides read-only and shared-resource boundaries.

This scoped-authorization amendment supersedes the unconditional headless missing-setup blocker in delivered #39 and related guidance; historical delivery and audit records remain unchanged.

The split keeps soft-dependency skills token-light while making the hard-dependency failure path explicit for both interactive use and autonomous Ticket delivery.
