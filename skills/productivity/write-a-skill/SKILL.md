---
name: write-a-skill
description: Create agent skills with SKILL.md, progressive disclosure, and bundled resources.
---

# Writing Skills

## Process

1. **Gather requirements.** Establish answers to these questions, asking the user for any answer not already provided:
   - What task or domain does the skill cover?
   - Which use cases must it handle?
   - Does it require executable scripts, instructions, or both?
   - Which reference materials must it include?
   - Will it remain user-only by default, or does it qualify as agent-discoverable under [Description and Discovery](#description-and-discovery)?

2. **Draft the skill.** Create:
   - a `SKILL.md` containing the instructions required by every branch;
   - linked reference files when a condition under [When to Split Files](#when-to-split-files) applies;
   - utility scripts when any condition under [When to Add Scripts](#when-to-add-scripts) applies.

3. **Review with the user.** Present the draft and ask whether it covers every required use case, contains missing or ambiguous instructions, or needs a specified section expanded or reduced.

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
- **Agent-discoverable** requires observed use that demonstrates a need for autonomous selection plus the maintainer's approval of the permanent context load. Omit `disable-model-invocation`. State the capability first, followed by one trigger for each distinct branch that should select the skill.

A loaded skill may compose a user-only skill by linking directly to its `SKILL.md`; composition does not require agent discovery.

Every description must:

- contain no more than 1024 characters;
- use third person;
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

## When to Split Files

Move content from `SKILL.md` into a linked file when at least one condition applies:

- retaining it would make `SKILL.md` 100 lines or longer;
- it applies to a separate domain, such as finance rather than sales schemas;
- advanced features are rarely needed.

## Review Checklist

After drafting, verify every item:

- [ ] `disable-model-invocation: true` is present unless the skill qualifies as agent-discoverable under [Description and Discovery](#description-and-discovery).
- [ ] The description satisfies the format rules; an agent-discoverable description contains one trigger per distinct branch.
- [ ] `SKILL.md` contains fewer than 100 lines.
- [ ] Instructions contain no time-sensitive information, including current-date statements, unpinned `latest` values, expiring URLs, or versions that require future manual revision.
- [ ] Each concept has one term, used consistently.
- [ ] At least one concrete input/output or interaction example is included.
- [ ] Each bundled context pointer links directly to its target, and no bundled reference requires another reference file.

## Design Reference

See [writing-great-skills](../writing-great-skills/SKILL.md) for discovery, hierarchy, leading words, and pruning rules.
