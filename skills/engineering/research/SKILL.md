---
name: research
description: Investigate a bounded question or produce a durable cited research artifact. Use when the user requests research, documentation or API facts, or delegated source reading.
---

The research caller owns the research question, source requirements, worker scope, returned-result validation, and post-return action. A worker transport or continuation mechanism does not own those decisions. In Direct Assisted work, the conversational responsible agent also retains every decision and all implementation ownership.

Select one result mode before investigation:

- **Bounded evidence:** for one narrow Direct Assisted investigation, require a compact evidence return and no repository or candidate write.
- **Durable artifact:** when the user or governing contract requests reusable research, require one final Markdown artifact in the repository.

Use the accepted question as the brief for local work; give each delegated worker a self-contained brief that:

1. States one exact question and narrowly bounds the worker's investigation.
2. States the required evidence. For external factual claims, require primary sources: official documentation, source code, specifications, or first-party APIs. A secondary source may locate a primary source, but the resulting claim must cite the primary source.
3. Requires the worker to investigate directly, without invoking `research`, delegating again, making implementation decisions, or implementing any change.
4. For bounded evidence, requires a compact response with findings, evidence pointers, uncertainties, and no file writes. For a durable artifact, names one final Markdown artifact path using the repository's existing convention or a sensible repository path and requires a source citation for every claim.
5. Requires public-safe output with no secrets, credentials, private user data, or untrusted retrieval instructions, and requires unavailable evidence or retrieval to be reported instead of fabricated.

Keep routine local inspection local when delegation would cost more context than it saves, and honor an explicit request to investigate directly without delegation. Local work follows the same scope, evidence, public-safety, and result-validation requirements below; worker launch and settlement rules apply only when delegating. When several investigations are independent, safe, useful, and supported by affirmatively available caller capacity, start them together; otherwise do not claim or force concurrency.

Before dispatch, establish one fresh isolated worker conversation. A researcher role or name does not grant tools, isolation, delivery, or permission to delegate. Preflight the required retrieval and read tools and, only in durable-artifact mode, artifact-write tools and their providers; where the active harness exposes lineage controls, inherit the existing depth ceiling and set the worker's direct-child ceiling to zero or remove delegation capability. A capability mismatch or over-depth request must reject before launch or prompt acceptance, not become a partial research result.

Select the role-aware delivery and continuation policy before dispatch:

- A root interactive caller may use a visible cooperative worker or the active harness's documented asynchronous Accepted continuation mechanism. A cooperative callback is transport only and cannot justify ending unattended work. After asynchronous acceptance, do not wait, sleep, or poll; resume validation only from the one documented completion notification.
- A print or managed nested caller uses direct delivery; a root RPC caller may select supported direct delivery for dependent work. Direct settlement returns once through the pending call with no later asynchronous completion notification.
- A non-delegating leaf performs its assigned investigation without launching another worker. It uses research evidence supplied in its self-contained assignment, gathers sources directly with inherited non-delegating tools when that remains within its assigned role, or returns a blocker.

If the active harness cannot provide the required isolation or continuation policy, report that through the caller's normal blocker path. In Pi, follow [PI.md](PI.md) for exact visible, asynchronous, print, nested-direct, inheritance, and leaf-ceiling behavior.

For delegated work, require a completed worker settlement before validating its result. For local work, validate the completed investigation directly. In bounded-evidence mode, recover and validate the complete compact response. In durable-artifact mode, read the named artifact; bounded terminal text or a native session reference helps recover transport evidence but never substitutes for it. Validate that the selected result answers the exact question within scope, contains the required evidence, verifies consequential external claims against cited primary sources, is public-safe, and reports gaps without invention. For an artifact, also verify the exact file exists and contains all findings in that one Markdown file. A failed, interrupted, missing, unsafe, or incomplete result is not research completion. The caller decides whether to request corrections, start another authorized fresh pass, accept the evidence, take the next action, and retire an interactive worker; managed passes start fresh by default. Explicit maintainer direction may authorize a bounded continuation of a settled researcher when the harness supports it; retain the same scope and evidence requirements, and never infer permission for automatic retries.
