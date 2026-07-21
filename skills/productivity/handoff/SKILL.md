---
name: handoff
description: Compact the useful, undocumented state of the current conversation for a fresh agent.
disable-model-invocation: true
---

# Handoff

Write a concise handoff for a fresh agent, then save it as a uniquely named Markdown file in the OS temporary directory, outside the current workspace. Return the exact path.

Capture only state needed to continue:

- current goal and immediate next step;
- user intent, constraints, and preferences not recorded elsewhere;
- decisions and reasoning not yet made durable;
- unresolved questions or blockers;
- relevant working-tree or external state that cannot be inferred safely.

Reference existing issues, specs, ADRs, docs, commits, and diffs by path or URL. Do not duplicate them. Omit tool logs, superseded exploration, conversational filler, and facts recoverable from referenced artifacts.

Preserve scope. Do not add recommendations, requirements, tasks, or speculative follow-up work that the conversation did not establish.

If the user provides a next-session focus, use it only to prioritize the summary. Redact secrets and unnecessary personal information.
