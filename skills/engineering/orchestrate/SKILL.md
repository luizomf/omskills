---
name: orchestrate
description:
  Carry a bounded change through implementation, independent review, and
  verified delivery in the current conversation. Use when responsible for
  completing one request or Ticket.
---

# Orchestrate

You are the responsible agent. Loading this skill means following the delivery
procedure here, not launching another orchestrator. Keep the reasoning and
responsibility established with the user through implementation and delivery.
The default flow is:

```text
current owner: investigate → implement and test → independent reviewer
             → adjudicate and correct → verify and deliver
```

For multiple selected Tickets, [dispatch-tickets](../dispatch-tickets/SKILL.md)
provides Mission supervision and starts or resumes each Ticket's owner. An owner
launched by that dispatcher follows this same procedure; it does not add another
coordinator. Preserve existing ownership when resuming work. A context that
performed a Prompt Audit of an implementation contract hands that implementation
to a fresh owner under the audit's isolation rules.

Before reading any relative link, run
`python3 -c 'from pathlib import Path; import sys; print((Path(sys.argv[1]).resolve().parent / sys.argv[2]).resolve())' '<loaded-file-path>' '<relative-link>'`
with this file's actual path and the link, then read the printed path. Pass
resolved skill paths to fresh agents.

## 1. Establish the work and stopping point

Read repository instructions, affected code/tests, and the accepted request. For
tracked work, read the complete Ticket, relevant comments, configured tracker
operations, governing sources, and dependency results. Follow
[setup-omskills](../setup-omskills/SKILL.md) if required configuration is
missing. An untracked request needs no Ticket or tracker setup merely to use
this skill.

Reuse established scope, decisions, verification requirements, and delivery
boundary. The user's presence changes how unresolved Questions are handled, not
who owns the work. “I'm leaving; continue through X” keeps this conversation
responsible through X. Record the decisions and recoverable state needed to
continue; absence alone adds no Mission, readiness, or Prompt Audit gate. Honor
an audit or other gate when the accepted task or repository requires it.

Inspect the live repository and candidate ownership. Use the existing checkout
when appropriate for direct work. Each Mission Ticket owns an exclusive branch
and worktree. Follow [WORKTREES.md](WORKTREES.md) when creating, reusing, or
cleaning temporary artifacts. Record the candidate path, branch, starting HEAD,
and fixed review base; preserve unrelated work. For integration, verify each
predecessor's exact produced commit and delivery evidence before combining it.

This step is complete when scope, candidate, capabilities, and stopping point
permit work, or the concrete missing prerequisite is identified.

## 2. Implement and verify

Investigate, implement, test, and debug while retaining technical ownership. Use
[diagnosing-bugs](../diagnosing-bugs/SKILL.md) for reproduction-first bug work
and [tdd](../tdd/SKILL.md) for test-first changes. Bounded assistance and
explicit user delegation choices can support the work without transferring the
owner's decisions or introducing a coordinator layer.

Apply user steering directly to the work and relevant helpers. Update affected
durable authority when the contract changes materially. Resolve routine choices
from accepted sources; consult an available maintainer when missing input blocks
progress. While the maintainer is away, continue what the established authority
resolves and preserve a concrete blocker for what it does not.

Check candidate identity before consequential changes, inspect the complete
diff, and run the relevant checks. Failing checks and correctable defects are
work to finish, not reasons to hand responsibility elsewhere or request routine
approval. For every Mission Ticket, including integration, commit the complete
candidate and record the exact full base and review SHAs. Review the whole
base-to-review range, including committed predecessor inputs. Direct work may
instead use complete WIP review when that state contains the entire candidate;
otherwise use the complete committed range under the review contract.

This step is complete when the candidate covers the accepted requirements and is
ready for independent review, or a genuine blocker has a recoverable handoff.

## 3. Obtain independent review and resolve findings

Follow [code-review](../code-review/SKILL.md) for one fresh independent
adversarial review of the complete candidate. Supply its resolved skill path,
the concise contract, repository instructions, candidate identity and complete
range/state, and verification results. Use the environment's isolated subagents
or [tmux-worker](../../productivity/tmux-worker/SKILL.md); read
[model-routing](../../productivity/model-routing/SKILL.md) before a
model-selectable launch and honor active harness authorization and inheritance.

Follow the transport's actual result-delivery contract. After asynchronous
acceptance, retain the review identity and release the turn; resume from its
matching completed result without requiring user approval. Unknown acceptance
requires evidence recovery before another launch. Recover the full findings and
completed outcome; partial or interrupted review is not completed review.

Adjudicate every finding, fix confirmed in-scope problems, and verify
corrections in this conversation. Review is a one-way findings handoff, not an
approval loop: continue resolving the work without sending corrections back for
reviewer approval. Record the reviewed and final states honestly, including
later changes.

This step is complete when the independent pass is complete, every finding has
an evidence-based disposition, and confirmed in-scope corrections are verified.

## 4. Deliver to the authorized boundary

Verify final candidate identity, status, complete diff, acceptance criteria, and
required checks; reuse results only where relevant inputs are unchanged. Record
reviewed/final states, findings/dispositions, checks, and limitations in the
appropriate delivery evidence. Follow the requested delivery method and
repository conventions; stop before publication if that is the agreed boundary.

- For a branch artifact, push and record its remote reference and exact full
  commit; preserve it for its integration consumer.
- For target delivery, use the agreed direct-push or PR method. A PR is optional
  unless required. When used, squash-merge, verify target/content equivalence,
  and record source-to-squash mapping.
- For integration, review and verify the complete combined candidate and record
  exact predecessor-to-result mappings before dependents proceed.

Complete applicable tracker obligations and eligible cleanup under
[WORKTREES.md](WORKTREES.md). Preserve protected artifacts with reasons. If an
operation fails, check what actually completed before recovery; publication
alone does not prove the whole requested delivery is complete.

Continue through the user's stopping point without inserting approvals between
implementation, review, corrections, and delivery. Progress messages need not
pause work. Report there, on an explicit stop, or when a genuine blocker
prevents further authorized progress. Transport-required turn release is
continuation, not a request for the user to restart the task.

Return concise evidence and any remaining obligation to the user or dispatcher.
For incomplete work, retain candidate state, conversation, checks, hypothesis,
and next action; prefer the same owner on resumption. Settle prior writing
activity before any replacement. Protect private operational notes and secrets.

This step is complete when the agreed boundary is verified and required cleanup
is complete, or the precise blocker/recovery state has been reported.

## Example

After discussing #42, the user says, “Fix it and push; I'll be away.” Keep #42
here, reproduce the bug, implement and test the fix, and obtain an independent
review. Resolve its findings, verify, push, and clean eligible temporary
artifacts before reporting. Neither the user's departure nor loading this skill
creates another coordinator. For a dispatched Ticket, return the same delivery
evidence to the supervising dispatcher.
