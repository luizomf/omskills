---
name: write-a-skill
description: Create agent skills with proper structure, progressive disclosure, and bundled resources.
---

# Writing Skills

## Process

1. **Gather requirements** - ask user about:
   - What task/domain does the skill cover?
   - What specific use cases should it handle?
   - Does it need executable scripts or just instructions?
   - Any reference materials to include?
   - Keep it user-only (default), or is there observed use that justifies agent discovery?

2. **Draft the skill** - create:
   - SKILL.md with concise instructions
   - Additional reference files if content exceeds 500 lines
   - Utility scripts if deterministic operations needed

3. **Review with user** - present draft and ask:
   - Does this cover your use cases?
   - Anything missing or unclear?
   - Should any section be more/less detailed?

## Skill Structure

```
skill-name/
├── SKILL.md           # Main instructions (required)
├── REFERENCE.md       # Detailed docs (if needed)
├── EXAMPLES.md        # Usage examples (if needed)
└── scripts/           # Utility scripts (if needed)
    └── helper.js
```

## SKILL.md Template

```md
---
name: skill-name
description: Brief human-readable description of the capability.
disable-model-invocation: true
---

# Skill Name

## Quick start

[Minimal working example]

## Workflows

[Step-by-step processes with checklists for complex tasks]

## Advanced features

[Link to separate files: See [REFERENCE.md](REFERENCE.md)]
```

## Description and Discovery

Every skill requires a description. Discovery determines who sees it:

- **User-only** (default): set `disable-model-invocation: true`. The description is command-facing metadata hidden from the agent's system context. Keep it to a concise human-readable capability summary.
- **Agent-discoverable**: omit `disable-model-invocation` only when observed use justifies permanent context load. The description becomes the agent's trigger: state the capability and the distinct branches that should select it.

Another loaded skill can compose a user-only skill explicitly by linking its `SKILL.md`; explicit composition does not require agent discovery.

**Format**:

- Max 1024 chars
- Write in third person
- For user-only skills: one concise sentence describing the capability
- For agent-discoverable skills: capability first, then specific trigger branches

**Agent-discoverable example**:

```
Extract text and tables from PDF files, fill forms, and merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**User-only example**:

```
Extract text and tables from PDF files, fill forms, and merge documents.
```

**Bad example**:

```
Helps with documents.
```

The bad example does not identify a useful capability for either the user or the agent.

## When to Add Scripts

Add utility scripts when:

- Operation is deterministic (validation, formatting)
- Same code would be generated repeatedly
- Errors need explicit handling

Scripts save tokens and improve reliability vs generated code.

## When to Split Files

Split into separate files when:

- SKILL.md exceeds 100 lines
- Content has distinct domains (finance vs sales schemas)
- Advanced features are rarely needed

## Review Checklist

After drafting, verify:

- [ ] `disable-model-invocation: true` is present unless agent discovery was explicitly justified
- [ ] Description is concise; agent-discoverable descriptions include distinct triggers
- [ ] SKILL.md under 100 lines
- [ ] No time-sensitive info
- [ ] Consistent terminology
- [ ] Concrete examples included
- [ ] References one level deep

## See also

This skill is the *process* for building a skill. For the *vocabulary and design principles* behind why a skill works — predictability, context vs cognitive load, the information hierarchy, leading words, and common failure modes — see the [writing-great-skills](../writing-great-skills/SKILL.md) reference.
