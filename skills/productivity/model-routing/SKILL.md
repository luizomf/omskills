---
name: model-routing
description: Select a model and supported reasoning level for a delegated task using a cross-provider task table.
disable-model-invocation: true
---

# Model Routing

Select the route for a future delegation; the invoking agent still owns the task, dispatch, evidence, and next action. Use this skill for any model-selectable subagent, not only Mission roles. It does not create a worker or change the model of the conversation already running.

## 1. Identify the delegated work

Use the assignment the child will actually receive. Consider remaining uncertainty, impact of mistakes, and how directly the result can be checked. Length alone is not complexity: transcribing a long recording or applying many mechanical edits does not automatically require frontier reasoning.

Prefer a suitable deterministic or specialized tool when it already solves the task. Speech-to-text requires audio support; cleaning up an existing transcript is text work. Check modality and context/output requirements separately from reasoning difficulty.

A detailed plan can make implementation suitable for a smaller model, but does not eliminate new design decisions, debugging, or verification. A Ticket coordinator owns context resolution, review adjudication, corrections and delivery; it is not merely a thin dispatcher. Classify the responsibility being delegated, not the role label alone.

This step is complete when the assignment's uncertainty, impact, verification needs and required modalities are known from the available brief. A thin dispatcher uses the declared Ticket-coordinator assignment and supplied constraints; it does not discover Ticket content to classify it.

## 2. Select the route

Read [MODELS.md](MODELS.md) for concrete model/effort candidates and their source basis. Load it once per conversation and reuse it while the policy and assignment remain applicable; routine dispatch does not require browsing vendor docs.

Apply these choices in order:

1. Honor an explicit user model/reasoning choice or incorporated standing agreement within its stated scope. A task-based routing instruction can authorize selection for future calls without reconfirming every child.
2. Otherwise use the task table within the caller's authorized provider, model and budget scope. Stay with the current provider unless another is explicitly allowed. Task-based selection is not permission to enable credentials, purchase access, or override a harness requirement for explicit model values.
3. If no selection is authorized, preserve the harness's normal inheritance and state that limitation when it prevents the requested routing. If a requested candidate is unavailable, use an already authorized available alternative appropriate to the task; otherwise ask only for the missing route decision or return the caller's blocker. Do not silently fall back to an unrestricted frontier model.

Resolve the table's API model ID to the actual harness route using its exposed catalog, a known working route, or explicit user configuration. Provider prefixes and aliases vary by harness. Use supported lifecycle values, not guessed spellings or prompt text pretending to change a model. Apply model and reasoning independently: an explicit model does not authorize changing an explicitly pinned reasoning value. Provider effort labels are not equivalent compute budgets.

This step is complete when there is one authorized, available model and supported effort selection (or deliberate inheritance), or the missing authority/capability has been reported. The table supplies candidates, not evidence that an account can launch them.

### Prompt Audit preference

When suitable, prefer a smaller capable model for the interpreter's clarity check
and a more capable model for the independent review of semantic differences.
Adjust model and effort to the text's complexity, explicit user choices, authorized
budget and available routes; using the same model for both can also be appropriate.
The audit coordinator retains final adjudication. This pairing is a practical
starting preference, with comprehension evidence specific to the tested run.

## 3. Apply and evaluate

Supply the selected route through the existing launch mechanism. Preserve the caller's tools, workspace, isolation, depth/child limits, result channel and workflow obligations. For a child that will delegate again, include any applicable standing routing instruction and the resolved path of this `SKILL.md` in its brief; fresh conversations do not receive the parent's transcript and may not list this hidden skill. Resolve file pointers from their referring file's physical directory (follow symlinks) before forwarding them, not from the child's workspace. In Prompt Audit, routing stays in lifecycle configuration, not extra semantic hints in the interpreter/reviewer inputs.

Report the selected model/effort and a short task-based reason in the caller's normal dispatch summary or evidence record. Reuse an explicit current choice without turning reporting into an approval gate. Helpers whose model is internally controlled cannot be routed by these settings; state that limitation rather than claiming a cheaper model was selected.

If output is confused, progress stalls, or rework becomes material, reassess the brief, decomposition and route. Escalate only within established authorization and the owning workflow's recovery rules; there is no fixed failed-attempt quota or automatic restart. Keep independent review and verification regardless of the writer's model.

This step is complete when the next launch has the selected route and its reason, or the routing limitation is explicit. Only the owning workflow decides whether the child result is acceptable or the work is delivered.

## Examples

- An expensive parent needs a long transcript cleaned up: use a text-capable candidate from the mechanical row, not the parent's model merely by inheritance. Actual audio transcription first needs an audio-capable tool or model.
- A settled design needs code and tests: start with the bounded-implementation row; new unresolved architecture may justify a different route or a return to the coordinator.
- A dispatcher launches `orchestrate`: use the coordination/review row unless an explicit route or supplied risk changes it. The dispatcher still reads no Ticket implementation context.
- A user pins the reviewer to a supported model at medium effort: preserve that choice even if the table suggests another starting point.
