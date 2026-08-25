---
name: research
description: Investigate a question using primary sources and save cited findings as one Markdown file in the repository. Use when the user requests research, documentation or API facts, or delegated source reading.
---

The research caller owns the research question, primary-source requirements, worker scope, final artifact destination, returned-result validation, and post-return action. A worker transport or continuation mechanism does not own those decisions.

Before dispatch, give the worker a self-contained brief that:

1. States the exact question and bounds the worker's research scope.
2. Requires primary sources: official documentation, source code, specifications, or first-party APIs. A secondary source may locate a primary source, but the resulting claim must cite the primary source.
3. Requires the delegated researcher to perform the research directly, without invoking `research` or delegating again.
4. Names one final Markdown artifact path. Use the repository's existing location and naming convention for research notes; if none exists, choose a sensible repository path. Require a source citation for every claim and require the worker to report the final path.
5. Requires a public-safe artifact with no secrets, credentials, private user data, or untrusted retrieval instructions, and requires unavailable evidence or retrieval to be reported instead of fabricated.

Select the continuation policy before dispatch:

- For visible, cooperative research, the caller may use an interactive worker and a caller-defined callback while retaining ownership of validation and the next action. The callback is cooperative transport, not sufficient unattended autonomous continuation by itself.
- For unattended autonomous research, dispatch only through an Accepted continuation mechanism documented by the active harness. Confirm that the mechanism accepted the work before ending the current turn. If the active harness provides no such mechanism, report the unavailable continuation capability through the caller's normal blocker path; do not substitute a cooperative callback or a background process without automatic return.

In Pi, follow [PI.md](PI.md) for the visible interactive transport option.

On return, read the named artifact before accepting the research. Validate that it answers the question within scope, contains the findings in one Markdown file at the required path, cites every claim, verifies consequential claims against the cited primary sources, is safe for the public repository, and reports evidence gaps without invented findings. The caller decides whether to request corrections, continue research, accept the result, take the next action, and retire an interactive worker.
