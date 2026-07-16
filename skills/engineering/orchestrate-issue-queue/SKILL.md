---
name: orchestrate-issue-queue
description: Orchestrate an ordered queue of repository issues through fresh-context implementation, independent review, bounded correction, verification, and integration. Use when Codex must deliver several issues or PRs sequentially, preserve exact-SHA review barriers, keep one writer at a time, resume long-running work safely, or maintain a durable execution ledger and diagnostic event log across turns. Also trigger for requests to run an implement-review-correct-merge loop with subagents. Do not use for a single small edit, review-only work, or issue triage without implementation.
---

# Orchestrate Issue Queue

Coordinate the queue; do not implement or approve changes as the orchestrator. Keep tracker and Git state authoritative, and keep local orchestration state as a resumable cache and audit trail.

## Establish the run

1. Read all applicable repository instructions completely.
2. Inspect Git, the configured issue tracker, open PRs, active automation, and any existing run state before dispatching work.
3. Refuse duplicate ownership when another live writer or automation already owns an issue.
4. Determine the ordered issue list, review policy (`single` or `dual`), and automatic correction limit. Default to one correction attempt. Use `dual` for security boundaries or when the user requires independent adversarial and standards/spec reviews.
5. Initialize the ledger with `scripts/run_state.py`. Store it outside Git unless the user explicitly requests otherwise.
6. Create a persisted Codex goal only when the user explicitly requests Goal mode. Keep that goal on the orchestrator task; do not create goals for leaf implementers, correctors, or reviewers. A complete role prompt supplies their outcome, constraints, verification, and return contract without adding automatic continuation. The ledger works with or without a goal.

Resolve every bundled script path relative to this `SKILL.md`, not relative to the target repository.

```sh
python3 scripts/run_state.py init RUN_ID \
  --repository OWNER/REPO \
  --goal 'Verifiable completion outcome' \
  --issues 101 102 103 \
  --review-policy dual \
  --max-corrections 1
```

Read [references/state-schema.md](references/state-schema.md) before recovering a run, diagnosing orchestration behavior, or modifying the state script.

## Run one issue at a time

For each issue, enforce this sequence:

1. **Preflight:** Revalidate the issue, base branch, repository cleanliness, active ownership, dependencies, and acceptance criteria.
2. **Implement:** Dispatch one fresh-context writer. Require it to read repository instructions, the issue, primary evidence, and relevant code before editing. Require reproduction or an equivalent regression test, the smallest safe change, relevant checks, a commit, and an exact report. Do not let it merge or approve itself.
3. **Verify delivery:** Inspect the writer's result. Record the branch, PR identifier, and exact remote SHA; do not trust a claimed SHA without revalidation.
4. **Review:** Dispatch fresh-context, read-only reviewers against that exact SHA. Wait for every required reviewer before adjudicating.
5. **Correct:** If concrete blocking findings remain, dispatch a new fresh-context writer with only the issue sources and adjudicated findings. Any push invalidates all approvals for the previous SHA. Dispatch fresh reviewers for the new SHA.
6. **Integrate:** Merge only when all required reviews passed the current remote SHA, required checks pass, repository rules permit integration, and the issue will close. Revalidate closure before advancing the queue.

Use [references/subagent-contracts.md](references/subagent-contracts.md) for the role prompts. Use a repository-provided implementation or code-review skill only when it preserves the assigned role, whole-issue pass, agent budget, and no-delegation rule. Do not give a leaf agent a skill that spawns more agents; extract the applicable instructions into its prompt instead.

## Prefer whole-issue passes

Treat the issue, not an individual finding or failed command, as the unit of work.

- Give one implementer the complete issue and all acceptance criteria. It owns local iteration until the whole issue is implemented and verified. A local test failure, missing assertion, or small defect stays with that implementer; it does not create another agent, delivery, or correction round.
- Require one complete delivery per writer turn. Local commits are allowed when repository conventions require them, but do not push or record an intermediate SHA as delivered before the full assigned scope and relevant gates are complete.
- Require every reviewer to inspect its entire assigned surface even after finding a blocker. Each reviewer returns one final consolidated report, not findings piecemeal.
- Wait for every required reviewer. Deduplicate and adjudicate their complete reports before dispatching any correction.
- Give one corrector the complete adjudicated blocker set for that SHA. It owns all related local iteration and delivers one corrected SHA after all accepted blockers and relevant gates are complete.
- A later review may find a genuinely new blocker; that is the reason correction rounds exist. Do not manufacture rounds from micro-adjustments that the current role can finish safely in its existing turn.

For dual review, partition the work while retaining independent judgment:

- **Adversarial:** attack security boundaries, unsafe inputs, bypasses, concurrency, resource exhaustion, timeout, interruption, cleanup, and information leakage. Run focused synthetic checks needed to prove or reject those risks.
- **Standards/spec:** review every acceptance criterion, observable behavior, tests, documentation, portability, repository rules, and maintainability. Run focused checks needed to prove compliance.
- Do not make both reviewers rerun the full formatter, typecheck, build, and test suite by default. The orchestrator records the repository-defined verification once on the accepted SHA after reviews pass. A reviewer may rerun a full gate when necessary to verify a concrete concern.

## Bound agent interactions

Only the orchestrator may dispatch agents. Implementers, correctors, and reviewers are leaf roles: they must not spawn, delegate, or invoke another multi-agent workflow.

Per issue and SHA:

- Dispatch exactly one implementer for the initial delivery.
- Dispatch exactly the reviewers required by the configured policy: one `reviewer`, or one `adversarial` plus one `standards-spec`.
- Dispatch exactly one corrector for each authorized correction round.
- Never create an agent for a single test failure, single finding, status check, or micro-adjustment.
- Never add extra reviewers because a required reviewer already found a blocker. Let every required reviewer finish, then consolidate.
- Honor stricter runtime thread limits. Agent availability does not justify expanding this logical budget.

## Record transitions

Run the state command after verifying each real transition, not before it occurs:

```sh
python3 scripts/run_state.py dispatch-implementation RUN_ID ISSUE --agent-id AGENT_ID
python3 scripts/run_state.py deliver RUN_ID ISSUE --branch BRANCH --pr PR --sha SHA --agent-id AGENT_ID
python3 scripts/run_state.py dispatch-review RUN_ID ISSUE --sha SHA --role reviewer --agent-id REVIEWER_ID
python3 scripts/run_state.py record-review RUN_ID ISSUE --sha SHA --role reviewer --outcome passed --agent-id REVIEWER_ID
python3 scripts/run_state.py record-verification RUN_ID ISSUE --sha SHA --outcome passed --checks format typecheck test build
python3 scripts/run_state.py dispatch-correction RUN_ID ISSUE --agent-id AGENT_ID
python3 scripts/run_state.py deliver RUN_ID ISSUE --sha NEW_SHA --agent-id AGENT_ID
python3 scripts/run_state.py mark-merged RUN_ID ISSUE --sha NEW_SHA --issue-closed
```

Record a successful preflight before dispatching implementation. For `dual` review, record both `adversarial` and `standards-spec` roles. Never edit `state.json` or `events.jsonl` manually. Use `show` to inspect the current state.

## Enforce the review barrier

- Treat reviewer conclusions as evidence, not authority; adjudicate every finding.
- Require concrete, reproducible findings with a verification path. Separate blockers from non-blocking observations.
- Require each reviewer to finish its whole assigned review and return one consolidated report. Do not dispatch a correction from an interim finding.
- Never merge while a required review is pending.
- Never transfer approval between SHAs, even for a small corrective push.
- Never allow two writers in the same worktree.
- After the configured correction limit, wait for all required reviewers to finish, consolidate the surviving blockers, pause Goal mode if active, and request human direction once. Never merge to escape the limit.

## Pause only at real external barriers

Continue while a safe local action is executable. When waiting for a webhook, hosted runner, asynchronous reviewer, checks, quota recovery, or user decision:

1. Record the barrier with `goal-pause`.
2. Pause the Codex goal if one is active.
3. End the turn rather than polling through automatic continuations.
4. On the relevant event, revalidate external state, record `goal-resume`, and continue.

Do not pause merely because an in-process subagent can be awaited in the current turn. Do not use Goal mode as a polling mechanism.

## Preserve diagnostic evidence

Keep `events.jsonl` metadata-only and append-only. Record roles, phases, issue IDs, PR identifiers, exact SHAs, outcomes, counts, transition rejections, and concise reasons. Never record secrets, credentials, cookies, private keys, terminal content, raw user data, full prompts, complete diffs, or unfiltered logs.

## Finish the run

Complete only when every queued issue is integrated and closed, no writer or review is pending, the base branch is clean and synchronized, and all final repository-defined gates pass. If the same concrete blocker survives the allowed correction cycle, record it and stop for human direction.
