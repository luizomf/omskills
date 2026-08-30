# Explicit `/setup-omskills` pointer only for hard dependencies

Engineering skills depend on per-repo configuration for issue-tracker operations, triage-label vocabulary, and domain-document layout. Some skills cannot produce correct output without it; others use it only to sharpen output and can degrade gracefully.

We split these into **hard-dependency** and **soft-dependency** skills:

- **Hard dependency** (`to-spec`, `to-tickets`, `triage`, `code-review`, `orchestrate`, `wayfinder`, plus `prompt-comprehension-audits` when it audits a tracked Ticket) — an interactive invocation points to `setup-omskills` when required configuration is missing and waits for that separate setup workflow to finish. During a headless Ticket run, missing required configuration returns a blocker to the Ticket coordinator instead; the run does not open setup Questions.
- **Soft dependency** (`diagnosing-bugs`, `tdd`, `improve-codebase-architecture`, `grill-with-docs`) — reference "the project's domain glossary" and "ADRs in the area you're touching" in general prose only. If those docs do not exist, the skill still works; output is merely less precise.

`setup-omskills` is an interactive repository-configuration workflow: it inspects evidence, obtains user confirmation, and writes the approved setup. A Ticket dispatcher neither runs it nor mediates it. The dispatcher does not read repository setup at all; a headless Ticket coordinator reports the missing hard dependency through its normal blocked outcome.

The split keeps soft-dependency skills token-light while making the hard-dependency failure path explicit for both interactive use and autonomous Ticket delivery.
