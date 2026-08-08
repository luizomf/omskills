---
name: prototype
description: Build a throwaway prototype to evaluate logic or state behavior, or to compare UI variants.
---

# Prototype

Build throwaway code that answers a design question.

## Select one branch

Determine the question from the user's prompt and the surrounding code. If both branches remain plausible and the user is available, ask which question to answer.

- **Logic or state-model question:** follow [LOGIC.md](LOGIC.md). Build a tiny interactive terminal app that pushes the state machine through cases that are hard to reason about on paper.
- **UI appearance question:** follow [UI.md](UI.md). Build several radically different UI variants on one route, selectable through a URL search parameter and a floating bottom bar.

If both branches remain plausible and the user is unavailable, select logic for a backend module or UI for a page or component, and record that assumption at the top of the prototype.

## Rules for both branches

1. **Mark it as throwaway.** Put the prototype in a clearly named prototype-only location near the module or page it evaluates. For UI work, obey the source/build exclusion boundary in [UI.md](UI.md).
2. **Provide one run command.** Use an existing task runner when possible, such as `pnpm <name>`, `python <path>`, or `bun <path>`. Do not edit shared runner configuration unless the current execution contract authorizes that edit.
3. **Keep state in memory by default.** If the stated question explicitly involves a database, use a scratch database or a local file with a clear `PROTOTYPE — wipe me` name.
4. **Implement only what is required to run the prototype and answer the question.** Do not add tests. Add no abstractions or error handling beyond what makes the prototype runnable.
5. **Expose state.** After every logic action or UI variant switch, print or render the full state relevant to the prototype question, including state that can affect later transitions or output.
6. **Stay inside the execution contract.** A prototype-only contract autonomously authorizes creating and running only the throwaway artifacts needed for its accepted question and repository scope. It does not authorize production behavior changes, tracker writes, commits, or branch creation. Perform those actions only when the current execution contract already authorizes them. Do not ask for separate confirmation before ordinary in-scope prototype creation.
7. **Capture only the decision.** Record the question, answer, and relevant reasoning in the prototype or another artifact already authorized by the current contract. Preserve or remove the throwaway artifact only through already-authorized actions. Do not automatically promote production code, create a throwaway branch, or mutate an implementation issue.
8. **Promote separately.** Production promotion is a separate repository implementation unit with its own current Prompt Audit `PASS` or explicit maintainer-authorized `BYPASS`. During that unit, implement the validated behavior anew under production constraints, do not copy prototype code directly, and add applicable tests. Before completing UI promotion, remove or disconnect the entire prototype-only subtree and route machinery, then verify through the host's production build, route manifest, bundle/module graph, or closest deterministic equivalent that none of it remains.
