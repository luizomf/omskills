---
name: write-a-skill
description: Create agent skills with SKILL.md, progressive disclosure, and bundled resources.
---

# Writing Skills

## Process

1. **Load the governing reference.** Before drafting, load and follow the installed `writing-great-skills` skill and its complete `GLOSSARY.md`. This step is complete only after the full reference has been read and its discovery, information-hierarchy, splitting, completion, and pruning rules govern the planned skill.

2. **Establish requirements and authority.** Resolve all of these questions:
   - What task or domain does the skill cover?
   - Which use cases must it handle?
   - Does it require executable scripts, instructions, or both?
   - Which reference materials must it include?
   - Will it remain user-only by default, or does it qualify as agent-discoverable under [Description and Discovery](#description-and-discovery)?
   - If it handles Tickets, does it preserve the boundary between readiness and explicit Mission authorization, route every finite pre-resolved Mission plan through `dispatch-tickets`, and use `implement` only to compose one selected Ticket as a one-item plan through that dispatcher?
   - If it selects among several user-only skills, is it a skill-selection Router Skill rather than a Ticket dispatcher?

   In standalone interactive use, resolve what the repository and conversation already establish, then ask the user a Question for each genuinely missing requirement. In a Mission-authorized Ticket with a current `PASS` or explicit maintainer `BYPASS`, resolve established requirements from the accepted Ticket, governing Spec, repository sources, and conversation without asking the user to reconfirm source-determined choices. Resolve minor residual choices through established repository conventions. If a material requirement remains genuinely unresolved, stop and return it as a blocker directly to the Ticket coordinator. An audited writer, including a depth-3 writer, remains a single-pass leaf: it does not delegate or route the blocker through the Ticket dispatcher. In any other print/headless invocation, report unresolved material requirements to the caller and stop rather than waiting for conversational input.

   This step is complete only when every requirement is resolved or the applicable terminal blocker has been returned and drafting has stopped.

3. **Draft the skill.** Create:
   - a `SKILL.md` containing the instructions required by every branch;
   - linked reference files when the governing information hierarchy assigns branch-specific reference behind a context pointer;
   - utility scripts when any condition under [When to Add Scripts](#when-to-add-scripts) applies.

   Follow [Splitting and Disclosure](#splitting-and-disclosure). This step is complete only when the draft represents every accepted use case and every required bundled resource exists and is directly referenced.

4. **Verify and review.** Apply every item in the [Review Checklist](#review-checklist), checking the decision-bearing content of every bundled resource against every accepted use case. In standalone interactive use, present the draft and, when useful, request user review; incorporate accepted feedback and repeat the exhaustive check. In audited or other print/headless work, return the draft and verification evidence to the caller without opening a user review Question.

   The skill is complete only when every accepted use case and every decision-bearing bundled resource is accounted for, every checklist item passes, and any requested interactive review is resolved.

## Skill Structure

Every skill requires `skill-name/SKILL.md`. Add `REFERENCE.md`, `EXAMPLES.md`, or `scripts/helper.js` under the same skill directory only when the conditions below require them.

## SKILL.md Template

```md
---
name: skill-name
description: One-sentence description of the operations or outcome.
disable-model-invocation: true
---
# Skill Name
## Quick start
[Minimal working example]
## Workflows
[Ordered processes and completion checklists]
## Advanced features
[Context pointer: See [REFERENCE.md](REFERENCE.md)]
```

## Description and Discovery

Every skill requires a description.

- **User-only** is the default. Set `disable-model-invocation: true`. Write one command-facing sentence that identifies the capability; this metadata is excluded from the agent's system context.
- **Agent-discoverable** requires observed use that demonstrates a need for autonomous selection plus maintainer approval of the permanent context load. Omit `disable-model-invocation`. State the capability first, followed by one trigger for each distinct branch that should select the skill.

A loaded skill may compose a user-only skill by its installed name; composition does not require agent discovery. Use relative paths only for files bundled with the current skill. A Router Skill selects an installed skill or disclosed reference to load; it does not accept Mission Ticket identities, own a Mission plan or cursor, or dispatch Ticket coordinators, which belong only to `dispatch-tickets`. `implement` is a one-Ticket convenience pointer to that dispatcher, and `orchestrate` is loaded only as its fresh coordinator.

Every description must:

- contain no more than 1024 characters;
- lead with a base-form capability verb;
- identify the operations or outcome the skill provides;
- omit automatic trigger phrasing when the skill is user-only.

- Agent-discoverable example: `Extract text and tables from PDF files, fill forms, and merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.`
- User-only example: `Extract text and tables from PDF files, fill forms, and merge documents.`
- Invalid example: `Helps with documents.` identifies neither an operation nor an outcome.

## When to Add Scripts

Add a utility script when at least one condition applies:

- the operation is deterministic, such as validation or formatting;
- the same code would otherwise be generated repeatedly;
- errors require explicit handling.

## Splitting and Disclosure

Use the `writing-great-skills` information hierarchy for progressive disclosure: keep instructions required by every branch in `SKILL.md`, and move branch-specific reference behind a direct context pointer.

Split only under the governing conditions:

- **By discovery:** the new skill has a distinct leading word for autonomous selection, observed use demonstrates the discovery need, and the maintainer approves its permanent context load.
- **By sequence:** an observed run ends a step early because visible post-completion steps pull attention forward, its completion criterion cannot be made checkable, and the later steps move across a real fresh-context boundary.

Line count, a separate domain, or rarity is not split evidence. Treat excess length as sprawl and apply the information hierarchy before considering a governed split.

## Review Checklist

After drafting, verify every item:

- [ ] Every accepted use case maps to explicit instructions.
- [ ] At least one concrete input/output or interaction example is included.
- [ ] Every ordered step has a checkable completion criterion, exhaustive where coverage is required.
- [ ] `disable-model-invocation: true` is present unless the skill qualifies as agent-discoverable under [Description and Discovery](#description-and-discovery).
- [ ] The description satisfies the format rules; an agent-discoverable description contains one trigger per distinct branch.
- [ ] Instructions contain no time-sensitive information, including current-date statements, unpinned `latest` values, expiring URLs, or versions that require future manual revision.
- [ ] Each concept has one term, used consistently; Router Skill wording cannot imply Ticket-dispatch ownership.
- [ ] Ticket routing, when present, treats readiness as eligibility and requires explicit Mission authorization.
- [ ] Every split has the required discovery or observed-sequence evidence.
- [ ] Every bundled context pointer links directly to its target, with no chained bundled reference.
- [ ] The decision-bearing content of every bundled resource has been inspected and agrees with every accepted use case and governing source.
