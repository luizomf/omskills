---
name: prompt-comprehension-audits
description: Audit whether clean-context agents understand text as intended; for repository implementation units, also check tracer-bullet fit before autonomous work.
---

# Audit Prompt Comprehension

Test whether a fresh agent's interpretation is semantically equivalent to the intended request. The interpreter and reviewer provide advisory evidence; the audit coordinator owns the final status.

Prompt Audit is an Unattended-execution eligibility gate. It is not applicable to Direct Assisted work by default, even when that work selects exactly one Ticket; run it there only when the maintainer requests an audit for complex intent. Its absence never forces an Assisted request through triage, a dispatcher, a separate Ticket coordinator, or a writer.

For a tracked Ticket, read the configured issue tracker and triage-label mapping before delegation. If either is unavailable during an interactive invocation, run `setup-omskills` first and wait for its confirmed output. During a headless Ticket run, return a missing-setup blocker to the Ticket coordinator instead; never route setup through a Ticket dispatcher. Untracked prompt audits require neither configuration.

## Fix the reference intent

Before delegation, read the complete original request and every artifact it explicitly requires. For a tracked Ticket, also read the complete final Issue body, labels, comments, incorporated Agent Brief, relations, governing domain terms, ADRs, and repository rules. The final Ticket Issue must contain or identify every accepted outcome, scope boundary, required workflow or order, deliverable, acceptance criterion, relation, and completion condition; conversation and audit history supply no hidden implementation requirement.

Fix one reference intent for the exact contract version. Record its requested outcome, scope, required actions and order, deliverables, completion point, explicit deferrals, and ambiguities that could materially change any of them. Do not infer adjacent work. This step is complete only when the reference is stable before any delegated pass.

If the accepted sources do not determine material authority or the contract changes materially after the reference is fixed, choose `FAIL`, record it as specified below, and end. The changed contract requires a new Prompt Audit; evidence from the older version is stale.

When the maintainer explicitly waives the comprehension audit for the exact contract, skip the agent passes and consider only `BYPASS` or `FAIL` through the fit and status rules below. The waiver satisfies an execution gate; it does not select the Ticket into a Mission, cannot be inferred, and is never represented as `PASS`.

## Select isolated pass delivery

Every delegated pass is a fresh, independent, read-only, non-delegating leaf that performs its assigned comparison directly. A role or name does not grant isolation, tools, or delivery behavior. Never continue a prior pass session or give a later pass hidden access to it.

Before each launch, preflight the tools and providers required for that pass and the absence of inherited conversation. Where the active harness exposes lineage controls, set the child's maximum delegation depth to its assigned depth and its direct-child ceiling to zero. A depth-3 leaf cannot launch the required depth-4 clean pass. Any unavailable isolation, over-depth rejection, or capability mismatch before prompt acceptance requires `FAIL`; record it through the status process below and stop.

Choose delivery from the caller's role:

- A root interactive coordinator may use the active harness's documented asynchronous delivery. After acceptance it does not wait, sleep, or poll; it resumes the audit from the single deterministic completion notification.
- A print coordinator and a depth-2 coordinator that depends on the pass use direct delivery. Direct settlement returns once through the pending call and emits no later asynchronous completion notification.

Run the passes sequentially even when asynchronous delivery is available: the interpreter must settle before the reviewer starts. Never issue these passes as concurrent siblings or assess the interpreter for the reviewer.

For every pass, require a mechanically completed terminal outcome and a complete decision-bearing response. When terminal text is bounded, recover the complete response from the returned native session reference or another predeclared durable result channel before assessment. Reading persisted evidence does not add context to the child. If the pass is failed, interrupted, cancelled, missing its response, or cannot be recovered without weakening isolation, choose and durably record `FAIL`; do not fabricate evidence, treat a partial response as `PASS`, continue the child, or rerun the pass.

## Run two isolated agent passes

Start one fresh agent for the interpreter pass and, only after it settles, another fresh independent agent for the reviewer pass. Beyond baseline harness instructions, both passes receive only the inputs listed for their role. Neither receives parent conversational turns or hidden coordinator analysis.

### 1. Run the interpreter pass

Give the interpreter only:

- the original request;
- artifacts that the request explicitly requires; and
- this question: "What do you understand you are being asked to do?"

Require a reconstruction of the requested outcome, scope boundaries, required actions and order, deliverables, completion point, and ambiguities that could materially change any of those items. Keep the interpreter read-only and non-delegating. It explains the request as written without executing it, revising it, or adding unstated requirements.

Interpreter settlement is complete only when its full decision-bearing response is available to the coordinator and can be passed unchanged to the reviewer.

### 2. Run the reviewer pass

After interpreter settlement, give the reviewer only:

- the complete final Ticket Issue and fixed reference intent for a tracked audit, or the original request and fixed reference intent for an untracked audit;
- artifacts explicitly required by that request; and
- the interpreter's complete response.

Withhold any coordinator assessment, desired verdict, or desired answer. Keep the reviewer read-only and non-delegating. Require `PASS` or `DIVERGENCE` with quoted or paraphrased evidence for every requested outcome, scope boundary, required action or order, deliverable, completion point, or material ambiguity it finds added, omitted, or changed. The reviewer compares semantic meaning and excludes requirements arising only from its preferred implementation workflow.

Reviewer settlement is complete only when its full decision-bearing response is available to the coordinator.

### 3. Adjudicate both passes

Only after both passes settle, compare the original request, fixed reference intent, interpreter response, and reviewer judgment. The coordinator, not either delegated agent, owns the result.

Treat a difference as material semantic divergence only when it changes the understood outcome, scope, required workflow or order, deliverables, or completion point. Compression or omission of an enumeration is not material when its governing boundary remains intact. Do not add release work, tests, artifacts, fallbacks, documentation, or implementation details unless the fixed reference intent requires them.

For every reported difference:

- If the fixed reference determines one clear meaning and the differing reading is not supported, record that adjudication and continue.
- If plausible readings materially differ, authority remains unresolved, or fixing the ambiguity would change the audited contract, choose `FAIL` and require a separate contract correction and fresh Prompt Audit.

Choose `PASS` only when no material semantic divergence survives adjudication. Do not edit the contract, run a confirmation pass, rerun a failed pass, or create another semantic-review loop in this invocation.

## Check implementation-unit fit when applicable

Treat any semantic `PASS` or explicit `BYPASS` above as provisional. When the audited contract is one repository code or behavior-changing Ticket, read `to-tickets` and confirm that it satisfies the tracer-bullet rules, including fit in one fresh agent context with room to understand the relevant behavior, implement the end-to-end change, and verify it. If it does not, choose `FAIL` and report that decomposition is required before autonomous delivery. Isolation failure, unresolved material authority, and one-context-fit failure always produce `FAIL`. For every other audited text, this check does not apply.

## Record the prompt audit status

Choose exactly one status:

- `PASS` — no material semantic divergence about outcome, scope, required workflow or order, deliverables, or completion survives audit-coordinator adjudication, and every applicable one-context-fit check succeeds.
- `BYPASS` — the maintainer explicitly waives `PASS` for this exact contract. Never infer this waiver or represent a bypass as a pass.
- `FAIL` — the audit cannot establish equivalent clean-context comprehension, including when isolation fails, material authority remains unresolved, a material divergence survives, or an applicable one-context-fit check fails.

When the execution contract is a tracked issue or an agent brief on one, post a new comment without editing prior audit history:

```markdown
## Prompt Audit

**Status:** PASS | BYPASS | FAIL
**Contract:** <issue or agent-brief reference>
**Basis:** <concise evidence or explicit maintainer authorization>
```

For an untracked prompt, report the same fields to the invoking workflow. A newer status supersedes an older one only when it applies to the same execution contract. A material change to the requested outcome, scope, required workflow or order, deliverables, acceptance criteria, relations, or completion point makes the prior status stale.

For a tracked code or behavior-changing Ticket, transition it to `ready-for-agent` only after its final body, Agent Brief, parent, blocking, and conflict relations are stable, it carries exactly one category role, and this audit returns `PASS` or an explicit maintainer `BYPASS`. Replace `needs-triage`; do not leave two state roles. A `FAIL` remains outside `ready-for-agent`. The audit never creates adjacent Tickets or extends the audited contract. `ready-for-agent` plus `PASS` or `BYPASS` establishes eligibility, not Mission authorization.

## End the audit invocation

After recording the status and applying any valid readiness transition, report the recorded `PASS`, `FAIL`, or explicit `BYPASS` and end the current invocation. A current `PASS` or `BYPASS` establishes eligibility for the exact unchanged contract but does not select work. Existing Mission authorization does not change this endpoint.

Prompt Audit never calls `dispatch-tickets`, invokes `orchestrate`, or performs Ticket implementation. A later, separately invoked workflow owns any authorized dispatch or delivery.

## Audit boundary

The audit evaluates communication of intent only. Runtime-readiness inspection, test execution, release preparation, and runtime-behavior establishment belong to later delivery work.
