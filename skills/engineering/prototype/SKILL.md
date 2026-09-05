---
name: prototype
description: Build a throwaway prototype to evaluate logic or state behavior, or to compare UI variants.
---

# Prototype

Build throwaway code that answers a design question.

Read-only inspection may establish the question and likely scope first. Before creating or changing prototype files, pass the adaptive Delivery mode gate. Honor topology and maintainer availability already stated semantically and ask only for a materially unresolved dimension. An untracked request or exactly one selected Ticket may remain Direct Assisted work with the conversational responsible agent; it does not require readiness, Prompt Audit, dispatcher, separate Ticket coordinator, or writer by default.

## Select one branch

Determine the question from the user's prompt and the surrounding code. If both branches remain plausible and the user is available, ask which question to answer.

- **Logic or state-model question:** follow [LOGIC.md](LOGIC.md). Build a tiny interactive terminal app that pushes the state machine through cases that are hard to reason about on paper.
- **UI appearance question:** follow [UI.md](UI.md). Build several radically different UI variants on one route, selectable through a URL search parameter and a floating bottom bar.

If both branches remain plausible and the user is unavailable, select logic for a backend module or UI for a page or component, and record that assumption at the top of the prototype.

## Rules for both branches

1. **Mark it as throwaway.** Put the prototype beside the module or page it evaluates, and name it so a casual reader can identify it as a prototype.
2. **Provide one run command.** Use the existing task runner, such as `pnpm <name>`, `python <path>`, or `bun <path>`.
3. **Keep state in memory by default.** If the stated question explicitly involves a database, use a scratch database or a local file with a clear `PROTOTYPE — wipe me` name.
4. **Implement only what is required to run the prototype and answer the question.** Do not add tests. Add no abstractions or error handling beyond what makes the prototype runnable.
5. **Expose state.** After every logic action or UI variant switch, print or render the full state relevant to the prototype question, including state that can affect later transitions or output.
6. **Capture the result.** Record the question, observed answer, and any prototype elements that may serve as reference or a starting point for later production work. The prototype remains non-production and is never promoted automatically. Preserve it on a clearly throwaway branch only when the user or repository requires the artifact. Production promotion is a separate, explicitly authorized implementation Ticket that may reuse the idea or code as a base but rewrites and tests it as needed.
