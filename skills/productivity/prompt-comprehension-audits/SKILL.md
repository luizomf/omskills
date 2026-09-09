---
name: prompt-comprehension-audits
description: Audit whether clean-context agents understand text as intended. Use for Unattended Ticket eligibility or an explicitly requested comprehension audit.
---

# Audit Prompt Comprehension

Test whether a fresh agent's interpretation is semantically equivalent to the intended request. The interpreter and reviewer provide advisory evidence; the audit coordinator owns the final status.

Prompt Audit is an Unattended-execution eligibility gate. It is not applicable to Direct Assisted work by default, even when that work selects exactly one Ticket; run it there only when the maintainer requests an audit for complex intent. Its absence never forces an Assisted request through triage, a dispatcher, a separate Ticket coordinator, or a writer.

Resolve from the invocation whether this audit establishes Unattended eligibility or only supplies requested comprehension evidence; do not infer a readiness transition from an Assisted audit request. For a tracked Ticket, read the configured issue tracker before delegation, and read the triage-label mapping only when establishing Unattended eligibility. If required configuration is unavailable, follow [setup-omskills](../../engineering/setup-omskills/SKILL.md) and its scoped authorization gate before delegation, including in headless runs. Read-only audit leaves return missing prerequisites to their responsible caller instead of writing setup; never route setup through a Ticket dispatcher. Untracked prompt audits require neither configuration.

## Fix the reference intent

Before delegation, read the complete original request and every artifact it explicitly requires. For a tracked Ticket, also read the complete final Issue body, labels, comments, incorporated Agent Brief, relations, governing domain terms, ADRs, and repository rules. The final Ticket Issue must contain or identify every accepted outcome, scope boundary, required workflow or order, deliverable, acceptance criterion, relation, and completion condition; conversation and audit history supply no hidden implementation requirement.

Fix one reference intent for the exact contract version. Record its requested outcome, scope, required actions and order, deliverables, completion point, explicit deferrals, and ambiguities that could materially change any of them. Do not infer adjacent work. This step is complete only when the reference is stable before any delegated pass.

If the accepted sources do not determine material authority or the contract changes materially after the reference is fixed, choose `FAIL`, record it as specified below, and end. The changed contract requires a new Prompt Audit; evidence from the older version is stale.

When the maintainer explicitly waives the comprehension audit for the exact contract, skip the agent passes and consider only `BYPASS` or `FAIL` through the fit and status rules below. The waiver satisfies an execution gate; it does not select the Ticket into a Mission, cannot be inferred, and is never represented as `PASS`.

## Select isolated pass delivery

Read [model-routing](../model-routing/SKILL.md) before selecting models for the interpreter and reviewer. Before reading relative links, run `cd '<loaded-skill-directory>' && pwd -P` with this loaded file's directory to obtain the physical base, then resolve links against that printed directory. Resolve the source symlink before applying `..`; read linked files even when their skills are absent from the discovery list. Use model-routing's [Prompt Audit preference](../model-routing/SKILL.md#prompt-audit-preference) as an adaptable starting point, honoring explicitly selected routes and the actual comprehension/comparison task. Apply routing through lifecycle fields only, without adding coordinator assessments or routing rationale to either pass's restricted semantic inputs. A lower-tier model understanding a prompt is evidence for that run, not proof that every other model will interpret it identically.

Every delegated pass is a fresh, independent, read-only, non-delegating leaf that performs its assigned comparison directly. A role or name does not grant isolation, tools, or delivery behavior. Never continue a prior pass session or give a later pass hidden access to it. Explicit maintainer recovery may replace a mechanically settled but incomplete pass with a fresh isolated pass before terminal status recording. Keep the fixed reference and required role inputs unchanged, retain failed-attempt evidence in the audit record, and preserve interpreter-before-reviewer order. Unknown acceptance is not settled failure. This exception does not rerun a completed semantic judgment, edit the contract, or reopen a terminal audit.

Before each launch, preflight the tools and providers required for that pass and the absence of inherited conversation. Where the active harness exposes lineage controls, inherit the existing depth ceiling and set the child's direct-child ceiling to zero or remove delegation capability. A designated pass leaf performs its assigned comparison directly without launching another pass. Missing isolation or capability requires `FAIL` unless explicitly authorized recovery can establish a fresh valid pass; a role's absolute depth is not itself a failure.

Choose delivery from actual harness mode:

- A root interactive coordinator may use the active harness's documented asynchronous delivery. After acceptance it does not wait, sleep, or poll; it resumes the audit from the matching completion notification.
- A print or managed nested coordinator uses direct delivery, as may a root RPC coordinator for dependent work when supported. Direct settlement returns once through the pending call and emits no later asynchronous completion notification.

Run the passes sequentially even when asynchronous delivery is available: the interpreter must settle before the reviewer starts. Never issue these passes as concurrent siblings or assess the interpreter for the reviewer.

For every pass, require a mechanically completed terminal outcome and a complete decision-bearing response. When terminal text is bounded, recover the complete response from the returned native session reference or another predeclared durable result channel before assessment. Reading persisted evidence does not add context to the child. If the pass is failed, interrupted, cancelled, missing its response, or cannot be recovered without weakening isolation, apply only an already authorized fresh-pass recovery as defined above; otherwise record `FAIL` and end. A partial response cannot support `PASS`, and recovery cannot reuse the failed child's context.

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

Choose `PASS` only when no material semantic divergence survives adjudication. Adjudication does not edit the contract, run confirmation passes, or repeat semantic comparisons to obtain a preferred verdict. Fresh-pass recovery applies only to incomplete evidence under the explicit authorization above.

## Check implementation-unit fit when applicable

Treat any semantic `PASS` or explicit `BYPASS` above as provisional. When the audited contract is one repository code or behavior-changing Ticket, read [to-tickets](../../engineering/to-tickets/SKILL.md) and confirm that it satisfies the tracer-bullet rules, including fit in one fresh agent context with room to understand the relevant behavior, implement the end-to-end change, and verify it. If it does not, choose `FAIL` and report that decomposition is required before autonomous delivery. Isolation failure, unresolved material authority, and one-context-fit failure always produce `FAIL`. For every other audited text, this check does not apply.

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

Only when the invocation establishes Unattended eligibility for a tracked code or behavior-changing Ticket, transition it to `ready-for-agent` after its final body, Agent Brief, parent, blocking, and conflict relations are stable, it carries exactly one category role, and this audit returns `PASS` or explicit maintainer `BYPASS`. Replace `needs-triage`; do not leave two state roles. A `FAIL` must remain outside `ready-for-agent`; remove stale readiness when this eligibility audit fails. An Assisted-only audit records its status without changing triage labels or requiring an Agent Brief that the audited request did not incorporate. The audit never creates adjacent Tickets or extends the audited contract. `ready-for-agent` plus `PASS` or `BYPASS` establishes eligibility, not Mission authorization.

## End the audit invocation

After recording the status and applying any valid readiness transition, report the recorded `PASS`, `FAIL`, or explicit `BYPASS` and end the current invocation. A current `PASS` or `BYPASS` establishes eligibility for the exact unchanged contract but does not select work. Existing Mission authorization does not change this endpoint.

Prompt Audit never calls `dispatch-tickets`, invokes `orchestrate`, or performs Ticket implementation. A later, separately invoked workflow owns any authorized dispatch or delivery.

## Audit boundary

The audit evaluates communication of intent only. Runtime-readiness inspection, test execution, release preparation, and runtime-behavior establishment belong to later delivery work.
