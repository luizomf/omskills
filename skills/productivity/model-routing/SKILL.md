---
name: model-routing
description:
  Select a model and supported reasoning level for delegated work within the
  user's authorized routes.
disable-model-invocation: true
---

# Model Routing

Select the route for a future delegation; the invoking agent still owns the
task, dispatch, evidence, and next action. Use this skill for any
model-selectable subagent, not only Mission roles. It does not create a worker
or change the model of the conversation already running.

## 1. Identify the delegated work

Use the assignment the child will actually receive. Consider remaining
uncertainty, impact of mistakes, and how directly the result can be checked.
Length alone is not complexity: transcribing a long recording or applying many
mechanical edits does not automatically require frontier reasoning.

Prefer a suitable deterministic or specialized tool when it already solves the
task. Speech-to-text requires audio support; cleaning up an existing transcript
is text work. Check modality and context/output requirements separately from
reasoning difficulty.

A detailed plan can make implementation suitable for a smaller model, but does
not eliminate new design decisions, debugging, or verification. A Ticket owner
handles investigation, implementation, tests, review adjudication, corrections,
and delivery. A Mission dispatcher handles queue decisions, blocker recovery,
and delivery verification. Classify the responsibility being delegated, not the
role label alone.

This step is complete when the assignment's uncertainty, impact, verification
needs and required modalities are known from the available brief and relevant
Ticket evidence.

## 2. Select the route

This skill is provider-neutral. Read model/effort preferences from the user's
instructions or applicable configuration. Keep personal routing preferences in
user-local configuration rather than this shared skill.

Apply these choices in order:

1. Honor an explicit user model/reasoning choice or incorporated standing
   agreement within its stated scope. A task-based routing instruction can
   authorize selection for future calls without reconfirming every child.
2. Otherwise apply routing guidance from applicable documents, skills, and user
   or project configuration within the caller's provider, model and budget scope.
3. Without applicable guidance, choose an available model and supported reasoning
   level using the task's difficulty, uncertainty, impact, cost, and verification
   needs. Use judgment rather than assuming every child needs the parent's model
   or the most capable model. Stay with the current provider unless another is
   allowed; selection does not authorize enabling credentials or purchasing access.
4. Only when the preceding sources and task-based judgment leave a value
   undecided, use the harness's normal inheritance for that value. Honor actual
   harness constraints and state any limitation that prevents the selected route.
   If a requested candidate is unavailable, use an already authorized available
   alternative appropriate to the task; otherwise ask only for the missing route
   decision or return the caller's blocker. Do not silently fall back to an
   unrestricted frontier model.

Resolve the selected model's identifier to the actual harness route using its
exposed catalog, a known working route, or explicit user configuration. Provider
prefixes and aliases vary by harness. Use supported lifecycle values, not
guessed spellings or prompt text pretending to change a model. Apply model and
reasoning independently: an explicit model does not authorize changing an
explicitly pinned reasoning value. Provider effort labels are not equivalent
compute budgets.

This step is complete when there is one authorized, available model and
supported effort selection (or deliberate inheritance), or the missing
authority/capability has been reported. Model capability claims do not establish
account access or harness support.

### Independent review

Independent review is judgment work. Within the selection precedence above, use
a model capable of challenging assumptions and reasoning about the task's risks.
A small diff, settled implementation plan, capable author, or passing checks does
not make review mechanical or bounded implementation. The reviewer must challenge the work independently,
not merely confirm execution of the plan. This is a capability requirement, not
a requirement to use a different model from the author or maximum effort.
Report any authorization or availability limitation rather than silently
claiming the preferred route.

### Prompt Audit preference

Interpreting intent, authorization, and completion boundaries is judgment work,
not mechanical extraction. Choose a capable interpreter within the selection
precedence above and apply the Independent review rule to comparison. The audit
coordinator retains final adjudication, with comprehension evidence specific to
the tested run.

## 3. Apply and evaluate

Supply the selected route through the existing launch mechanism on every start
and continuation. Standing instructions remain applicable within their stated
scope until superseded; a user need not repeat them per dispatch. A one-call
exception does not replace a standing policy. Reapply selected values when the
harness inherits omitted fields from the parent rather than retaining the
child's previous route. Preserve the caller's tools, workspace, isolation,
depth/child limits, result channel and workflow obligations. For a child that
will delegate again, include any applicable standing routing instruction and
the resolved path of this `SKILL.md`
in its brief; fresh conversations do not receive the parent's transcript and may
not list this hidden skill. Resolve file pointers from their referring file's
physical directory (follow symlinks) before forwarding them, not from the
child's workspace. In Prompt Audit, routing stays in lifecycle configuration,
not extra semantic hints in the interpreter/reviewer inputs.

Report the selected model/effort and a short task-based reason in the caller's
normal dispatch summary or evidence record. Reuse an explicit current choice
without turning reporting into an approval gate. Helpers whose model is
internally controlled cannot be routed by these settings; state that limitation
rather than claiming a cheaper model was selected.

If output is confused, progress stalls, or rework becomes material, reassess the
brief, decomposition and route. Escalate only within established authorization
and the owning workflow's recovery rules; there is no fixed failed-attempt quota
or automatic restart. Keep independent review and verification regardless of the
writer's model.

This step is complete when the next launch has the selected route and its
reason, or the routing limitation is explicit. Only the owning workflow decides
whether the child result is acceptable or the work is delivered.

## Examples

- A long transcript needs cleanup: when selection is authorized, a text-capable
  model suited to routine editing may suffice. Actual audio transcription needs
  an audio-capable tool or model.
- A settled design needs code and tests: choose for implementation and
  verification; unresolved architecture may require stronger reasoning.
- A dispatcher launches `orchestrate`: classify the full technical ownership,
  including investigation and review adjudication, not merely task forwarding.
- A user pins the reviewer to a supported model and effort: preserve that choice
  rather than replacing it with an inferred preference.
