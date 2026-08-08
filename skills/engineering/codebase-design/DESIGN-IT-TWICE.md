# Design It Twice

When alternative interfaces would expose a real tradeoff, ask one clean designer to produce two or three genuinely different options in a single pass. The root compares them and recommends one.

## Frame the problem

Collect the constraints, callers, dependencies, domain vocabulary, relevant code paths, and what the proposed module should hide. Include the vocabulary from [SKILL.md](./SKILL.md) and dependency guidance from [DEEPENING.md](./DEEPENING.md).

## Dispatch one clean designer

Create exactly one new designer with clean context. Give it a compact, self-contained initial prompt with the role, authoritative sources, constraints, relevant code paths, expected options, and this contract:

```text
Design two or three materially different interfaces for this module. Vary seam placement or the primary optimization—not merely names. For each option show the interface, caller example, hidden implementation, dependency/adapters strategy, invariants and error modes, and tradeoffs in depth, locality, and leverage. Recommend one option. Do not edit code, spawn, or delegate.
```

Useful contrasting optimizations include minimal interface, simplest common caller, or extensibility. Use only contrasts that fit the actual problem.

## Decide

The root checks each option against repository and domain constraints and may combine compatible strengths. When the remaining choices are materially equivalent under the accepted behavior and repository evidence, choose the simplest design that preserves the required flexibility.

Do not autonomously resolve a genuinely material tradeoff that the accepted intent and repository evidence leave open. Keep it unresolved in the `grill-with-docs` decision inventory and make it the next one-question-at-a-time user decision, with a recommendation and the supporting evidence or tradeoff. Do not add a separate confirmation gate or ask the user for facts the repository can establish.
