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

The root checks each option against repository and domain constraints, may combine compatible strengths, and chooses the simplest design that preserves the required flexibility. Resolve architecture tradeoffs directly from the accepted intent and repository evidence; do not hand the decision back to the user.
