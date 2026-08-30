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

Before dispatch, establish one fresh isolated worker conversation. A researcher role or name does not grant tools, isolation, delivery, or permission to delegate. Preflight the required retrieval, read, and artifact-write tools and their providers; where the active harness exposes lineage controls, set the worker's maximum delegation depth to its assigned depth and its direct-child ceiling to zero. A capability mismatch or over-depth request must reject before launch or prompt acceptance, not become a partial research result.

Select the role-aware delivery and continuation policy before dispatch:

- A root interactive caller may use a visible cooperative worker or the active harness's documented asynchronous Accepted continuation mechanism. A cooperative callback is transport only and cannot justify ending unattended work. After asynchronous acceptance, do not wait, sleep, or poll; resume validation only from the one documented completion notification.
- A print caller and a depth-2 coordinator that depends on the artifact use direct delivery. Direct settlement returns once through the pending call and emits no later asynchronous completion notification.
- A depth-3 leaf does not launch a worker requiring depth 4. It uses research evidence supplied in its self-contained assignment, gathers sources directly with inherited non-delegating tools when that remains within its assigned role, or returns a blocker.

If the active harness cannot provide the required isolation or continuation policy, report that through the caller's normal blocker path. In Pi, follow [PI.md](PI.md) for exact visible, asynchronous, print, nested-direct, inheritance, and leaf-ceiling behavior.

On return, require a completed worker settlement and read the named artifact before accepting the research; bounded terminal text or a native session reference helps recover transport evidence but never substitutes for the artifact. Validate that the exact file exists, answers the question within scope, contains the findings in one Markdown file at the required path, cites every claim, verifies consequential claims against the cited primary sources, is safe for the public repository, and reports evidence gaps without invented findings. A failed, interrupted, missing, unsafe, or incomplete artifact is not research completion. The caller decides whether to request corrections, start another authorized fresh research pass, accept the result, take the next action, and retire an interactive worker; managed research assignments are never continued in a prior worker session.
