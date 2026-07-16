---
name: supervise-async-codex-task
description: Supervise a separate long-running Codex executor task through adaptive heartbeats, compact progress state, evidence-based steering, stall recovery, completion verification, and bounded post-run improvement of the skills involved. Use when the user asks Codex to act in their place, create or monitor another Codex task, watch an asynchronous implementation/review workflow, make routine decisions, detect stalls, or improve the supervising and executor workflows after observing waste or failure. Do not use for ordinary in-thread implementation, simple status checks, or passive reminders without an executor task.
---

# Supervise Async Codex Task

Act as the user's decision-making supervisor. Keep this task read-only with respect to project code. The executor task and its agents own implementation writes.

## Establish supervision

1. Read repository instructions and the user's execution policy.
2. Preserve a short **intent brief** separately from the tracker item: the user's
   original outcome, why it matters, and the simplest result that would satisfy
   them. An issue is an implementation artifact, not infallible product intent.
3. Inspect the tracker, Git state, open PRs, automations, executor threads, and workflow state. Refuse duplicate ownership.
4. Compare the issue with the intent brief before dispatch. Flag **scope
   amplification** when generated or refined acceptance criteria add substantial
   infrastructure, fault injection, hardening, or verification of the test
   harness itself beyond what the requested outcome needs. Security requirements
   that protect real boundaries remain valid, but an opt-in local tool should not
   silently acquire production-grade assurance. If the amplification would
   materially change cost or design, consult the user before execution with a
   smaller recommended scope. Do not promote nearby conversation context into a
   requirement merely because it mentions production, deployment, credentials,
   or security; require an explicit causal link to the requested outcome.
5. Assess issue size before dispatch:
   - **Compact:** one seam and one coherent verification surface.
   - **Compound:** several tightly coupled surfaces whose value depends on one integrated delivery.
   - **Oversized:** independently shippable outcomes or too many unrelated boundaries for one writer to hold and verify reliably.
6. Keep a compound issue whole when integration is the point, but partition review surfaces and choose a realistic correction budget. If an oversized issue has a clean tracer-bullet split, ask before changing tracker scope.
7. Create a separate project executor task in a worktree. Give it the intent brief as well as the complete issue, policy, authority, stop conditions, definition of done, and required orchestration skill. Require it to report its ledger path and compact phase checkpoints.
8. Initialize the supervisor ledger with `scripts/supervisor_state.py`. Store state outside Git.
9. Create a heartbeat attached to the supervisor task. Store its automation id in the ledger.

Resolve bundled script paths relative to this `SKILL.md`.

```sh
python3 scripts/supervisor_state.py --state-root STATE_ROOT init RUN_ID \
  --executor-thread THREAD_ID \
  --repository OWNER/REPO \
  --objective 'Verifiable completion outcome' \
  --automation-id AUTOMATION_ID
```

Read [references/supervisor-state.md](references/supervisor-state.md) when recovering a run or interpreting its metrics.

## Give the executor one complete mission

- Treat the issue as the implementation unit. One writer owns the complete issue and resolves local test failures and micro-adjustments before delivery.
- Require reviewers to inspect their complete assigned surfaces and return one consolidated report each, even after finding a blocker.
- Require the orchestrator to wait for every required review, deduplicate all findings, and send one complete adjudicated blocker set to one corrector.
- Forbid leaf implementers, correctors, and reviewers from spawning agents or invoking multi-agent skills.
- Do not create a new agent for a test failure, single finding, status check, or small follow-up that the active role can finish safely.
- Preserve exact-SHA review barriers and the configured correction limit.

## Monitor cheaply

On each heartbeat:

1. Load the supervisor ledger.
2. Read executor metadata minimally: status, update time, current phase, active role, ledger event sequence, and SHA. Do not include tool outputs or reread the full turn by default.
3. Record the observation:

```sh
python3 scripts/supervisor_state.py --state-root STATE_ROOT observe RUN_ID \
  --phase PHASE \
  --executor-status STATUS \
  --executor-updated-at VALUE \
  --event-sequence VALUE \
  --sha SHA \
  --active-role ROLE \
  --activity-class normal
```

4. If the fingerprint is unchanged, perform a real no-op: do not reread the conversation, rescan the repository, or requery GitHub. Return a quiet heartbeat.
5. If it changed, read only the new evidence. Revalidate GitHub and project state only at meaningful transitions such as delivery, new SHA, completed review, correction, integration, or blocker.
6. Read the full executor turn only when evidence is ambiguous, a question needs adjudication, or a blocker/stall must be diagnosed. Record full reads and interventions in the ledger.

Never use a subagent to monitor another task. Never duplicate an executor because progress is slow.

## Adapt heartbeat timing

Choose timing from the next expected evidence, not a fixed global interval. Ask the executor to state the current activity and expected next checkpoint when that is not inferable.

Use these ranges as defaults, then adjust to observed runtimes:

- Preflight, dispatch, merge, or short tracker transition: 2-5 minutes.
- Normal implementation, correction, or focused review: 8-12 minutes.
- Docker builds, browser E2E, full suites, or other heavy local gates: 15-25 minutes.
- Hosted checks, webhook waits, quotas, or external barriers: 20-40 minutes or event-driven wakeup.
- Suspected stall after expected evidence is late: 3-5 minutes until resolved.
- Terminal complete or blocked state: remove the heartbeat.

Update the heartbeat schedule only when the phase class changes, the executor supplies a materially different expectation, or stall risk changes. Do not churn the automation on every heartbeat. The ledger returns a recommended interval; use judgment when the evidence supports another value.

## Detect and heal stalls

Elapsed time alone is not a stall. Heavy commands and adversarial checks may be legitimately quiet.

Treat a stall as evidence-based:

- expected checkpoint missed beyond a reasonable grace period;
- no ledger event or executor update;
- no known active command, agent, hosted check, or external barrier;
- the same condition persists across two observations.

At the first missed checkpoint, send one compact probe asking for phase, active operation, last evidence, next evidence, and blockers. At the second confirmed miss, steer or stop the stale operation within existing authority. Never broaden authority, spawn a duplicate writer, or consume a correction merely to recover orchestration.

Handle duplicate events, stale SHAs, duplicate claims, and unchanged state as no-ops. Revalidate before acting on delayed messages.

## Decide for the user

Continue autonomously when the action is safe, reversible, within delegated authority, and consistent with the issue. Prefer, in order:

1. explicit issue criteria;
2. security and product boundaries;
3. smallest complete change;
4. smallest dependency and coordination surface;
5. existing repository patterns.

## Adjudicate a blocked executor

The executor's correction limit is a circuit breaker for the inner
code/review loop. It returns control to the supervisor before agents repeat the
same strategy indefinitely; it is not the supervisor's own blocker and does not
by itself justify involving the user.

When an executor stops or exhausts its budget:

1. Revalidate the evidence and deduplicate the final findings.
2. Compare every blocker against both the issue and the preserved intent brief.
3. Classify each finding as:
   - required for the requested outcome or a real security boundary;
   - required only by amplified issue scope;
   - reviewer overreach, speculative hardening, or non-blocking quality work;
   - a genuine product, authority, or safety decision.
4. Reject non-blockers explicitly. Do not let a reviewer silently redefine the
   product or turn a local harness into a production subsystem.
5. Evaluate the cheapest safe paths, including accepting the current result,
   a fresh bounded recovery cycle, simplifying the implementation, or revising
   amplified issue/PR scope back to the original intent.
6. Take the routine decision on the user's behalf. Record why the previous loop
   stopped, change the strategy when needed, then authorize a new bounded
   executor cycle with its own explicit implementation/review limit. Never just
   keep incrementing the failed loop's counter or resend the same instructions.
7. Continue supervising through the new cycle. A repeated technical failure
   triggers another diagnosis and strategy check, not automatic escalation.

Consult the user only after this adjudication shows a real boundary the
supervisor cannot decide: a genuine product/PRD choice, no safe path that still
satisfies the original intent, or missing external authority. A tracker edit or
issue split that merely removes agent-created scope amplification is routine
recovery when it preserves the intent brief; record it clearly and proceed.

When a real human boundary exists, deliver a decision-ready package:
recommendation first, accepted and rejected findings, concrete options,
cost/risk of each, and the smallest authorization needed. Never merely announce
that the executor stopped or ask whether to "try another correction."

## Verify completion

Do not accept the executor's final claim alone. Revalidate tracker closure, squash merge, exact merged SHA, required reviews, gates, cleanup, branch deletion, and clean synchronized base branch. Remove the heartbeat only after completion or a genuine blocked state that requires user action.

## Improve after the run

Run one compact postmortem after completion or blocking. Use ledger evidence, not intuition. Measure:

- wall time by phase;
- executor and leaf-agent count;
- nested delegation attempts;
- SHAs and correction rounds;
- repeated full gates and full-thread reads;
- unchanged heartbeats;
- unique blockers found per review round;
- stalls, recoveries, and user interruptions.

Classify each problem as issue sizing, role contract, duplicated verification, heartbeat timing, state visibility, tool failure, or unavoidable task complexity.

Invocation of this skill authorizes low-risk instruction-only improvements to skills used by the run unless the user opts out. Apply them only after the run, with these limits:

- Require direct evidence linking the observed problem to the changed instruction.
- Make at most one small coherent patch per involved skill per run.
- Prefer clarifying role ownership, batching findings, preventing nested delegation, reducing duplicate reads/checks, or improving checkpoint contracts.
- Never weaken security, tests, review barriers, authorization boundaries, completion criteria, or correction limits automatically.
- Never change project code, tracker scope, model choice, reasoning effort, or external permissions as self-improvement.
- Validate every changed skill and run its bundled tests. Report the evidence, files changed, expected benefit, and rollback path.
- If the improvement changes policy or quality/cost tradeoffs, propose it to the user instead of applying it.

Do not launch an expensive forward-test merely to validate a token-saving tweak. Prefer the next real run as the comparison unless a cheap isolated test can prove the behavior.
