---
name: writing-great-skills
description: Reference for writing and editing skill discovery, hierarchy, leading words, and pruning to produce predictable processes.
---

Optimize each skill for **predictability**: repeated runs should follow the same process, although their outputs may differ.

Before applying a bold term below, read its complete definition and constraints in [`GLOSSARY.md`](GLOSSARY.md).

## Discovery

Choose one discovery mode:

- **Agent-discoverable:** omit `disable-model-invocation`. The required **description** remains in system context and allows autonomous selection, adding **context load**.
- **User-only:** set `disable-model-invocation: true`. The description remains command-facing metadata but is excluded from system context. The user selects the skill, adding **cognitive load** instead of context load.

A loaded skill may compose a user-only skill through a **context pointer** that names the installed skill and the condition for loading it. Use direct paths only for disclosed references bundled with the current skill.

Use agent discovery only when observed use demonstrates a need for autonomous selection and a maintainer approves the permanent context load. Existing agent-discoverable omskills have met both conditions. Active status is independent: active user-only skills remain installed for direct selection without permanent context load, and every new skill remains user-only until promoted.

When the user cannot recall the applicable user-only skill without inspecting or searching the list, create one user-only **Router Skill**. Its context pointers must name each target and the condition for loading it. This is a skill-selection role only; it never owns Mission Ticket identities, topology or Ticket-coordinator dispatch. Mechanical Mission routing belongs to `dispatch-tickets` when used.

For skills that route Ticket execution, readiness and a current Prompt Audit gate establish eligibility but never Mission authorization. Supply every finite pre-resolved Mission plan to `dispatch-tickets`; `implement` may compose exactly one selected Ticket as a one-item plan through that dispatcher. For smaller work, an authorized human/invoker or context-rich parent may directly dispatch one fresh isolated `orchestrate` coordinator. It checks selected-Ticket authority, live gates and actual capabilities, not caller provenance or role/depth assertions; dispatcher mechanical boundaries remain mandatory when used. Neither skill discovery nor a ready-work query selects Mission work.

## Descriptions

For an agent-discoverable description:

- state the capability;
- place the skill's **leading word** before supporting detail;
- include exactly one trigger for each distinct **branch**;
- collapse synonyms that trigger the same branch;
- omit identity or process details already present in the body;
- retain a reach clause such as "when another skill needs..." only when it enables composition.

For a user-only description, write a command-facing capability summary and omit automatic trigger phrasing.

## Information Hierarchy

Classify content as **steps** or **reference** and place it on this hierarchy:

1. Ordered steps required during execution remain in `SKILL.md`.
2. Definitions, rules, and facts needed by every branch may remain as in-skill reference.
3. Reference needed by only some branches moves behind a context pointer to a disclosed file or an external artifact.

A flat set of peer rules is valid reference and does not require artificial sequencing.

End every step with a **completion criterion** that the agent can evaluate as true or false. When the task requires coverage, quantify the criterion over all required items, for example, "every modified model is accounted for." Apply an equivalent exhaustive criterion to flat reference when every rule must be checked. The criterion must require the **legwork** needed to satisfy every quantified item.

Use **progressive disclosure** by keeping content required by every branch in `SKILL.md` and moving branch-specific reference behind a pointer.

Within a file, apply **co-location**: put each concept's definition, rules, and exceptions under one heading.

## When to Split

Split only under one of these conditions:

- **By discovery:** the new skill has a distinct leading word that should trigger autonomous selection, and its discovery has met the approval condition above. Explicit composition alone requires a context pointer, not a discoverable skill.
- **By sequence:** an observed run ends a step early because visible **post-completion steps** pull attention forward, and the current completion criterion cannot be made checkable. Place the later steps across a fresh-context boundary; loading another skill in the same conversation does not hide them.

## Pruning

Apply these checks sentence by sentence:

1. Keep each meaning in one **single source of truth**.
2. Retain a sentence only when it still affects the skill's process, branch selection, output, boundary, or completion criterion.
3. Test each sentence in isolation: if removing it would not change agent behavior, delete the complete sentence rather than rephrasing it.

## Leading Words

Use a **leading word** when the established meaning of an existing pretrained concept preserves a repeated definition or set of qualities. Repeat the word where it anchors execution or discovery; do not repeat its full definition.

Inspect every skill for meanings restated in multiple places. Replace a restatement with a leading word only when the replacement preserves all conditions and distinctions. Examples:

- replace "fast, deterministic, low-overhead" with _tight_ only when _tight_ is defined to preserve all three requirements;
- replace "a loop you believe in" with _red_ when the required criterion is that the loop demonstrably fails on the bug.

## Failure Modes

Diagnose and correct each observed failure as follows:

- **Premature completion:** first make the completion criterion checkable. Split the sequence across a fresh context only when the criterion cannot be made checkable and an observed run still ends the step early.
- **Duplication:** retain one authoritative statement of the meaning and replace intentional recurrence with a leading word.
- **Sediment:** delete content that no longer affects current skill behavior.
- **Sprawl:** move branch-specific reference behind context pointers; apply [When to Split](#when-to-split) only if a split is still needed.
- **No-op:** delete any sentence whose removal does not change behavior. If a leading word is too weak to change behavior, replace it with a word that imposes an observable criterion, such as _red_, or remove it.
- **Negation:** state the required positive behavior. Retain a prohibition only for a hard boundary that has no equivalent positive formulation, and pair it with the required alternative.
