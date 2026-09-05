---
name: handoff
description: Compact undocumented continuation state from the current conversation for a fresh agent.
---

# Handoff

Write a handoff for a fresh agent. Save it under a unique Markdown filename in the OS temporary directory, outside the current workspace, and return the exact path.

Include only continuation state that the referenced artifacts do not establish:

- the current goal and immediate next step;
- user intent, constraints, and preferences not recorded elsewhere;
- decisions and reasoning not yet recorded in a durable artifact;
- unresolved questions and blockers;
- Delivery topology and Maintainer availability when the conversation resolved them but no cited durable artifact records them; and
- relevant working-tree or external state that cannot be inferred safely from cited artifacts, including recoverable state required by an explicitly requested Assisted-to-Unattended transition.

Cite existing issues, specs, ADRs, documentation, commits, and diffs by path or URL instead of reproducing their content. Exclude tool logs, superseded exploration, and conversational transitions.

Include no recommendation, requirement, task, or follow-up that the conversation did not establish. A handoff preserves context only: it does not select a Ticket, grant Mission authorization, change availability, satisfy a Prompt Audit gate, or authorize implementation mutation.

If the user provides a next-session focus, order the established state required for that focus first without changing scope. Replace secrets with `[REDACTED]` and omit personal information that is not required for continuation.
