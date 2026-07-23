---
name: improve-codebase-architecture
description: Scan a codebase for deepening opportunities, write a visual HTML report, and develop a selected candidate through a decision interview.
---

# Improve Codebase Architecture

Identify **deepening opportunities**: refactors that place more behavior behind a smaller interface at a defined seam, improving testability and code navigation.

Use two authoritative vocabularies:

- Read [`codebase-design`](../codebase-design/SKILL.md) for **module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**, the deletion test, interface-as-test-surface, and adapter-count rules. Use those architecture terms in every candidate; do not substitute `component`, `service`, `API`, or `boundary`.
- Use domain terms from applicable `CONTEXT.md` files. Treat ADRs in `docs/adr/` as decisions that remain in force unless the report supplies repository evidence for reopening one.

## Process

### 1. Scan

Read the applicable domain glossary and ADRs before scanning code.

Delegate the scan to exactly one new Explore worker with clean context through the active harness's isolated-worker mechanism. In Pi, follow [PI.md](PI.md). The initial prompt must let the worker execute without inherited conversation context and include the worker role, repository path, authoritative domain and architecture references, scan scope, and required finding fields. State that the worker is a leaf and must not delegate. Do not create separate workers for candidates or alternatives.

The worker must follow repository references based on observed code rather than stop at a fixed directory or match quota. Use these categories to classify observed friction; they are neither an exhaustive navigation checklist nor a requirement to produce one finding per category:

- domain behavior that requires navigation across multiple modules;
- modules whose caller-visible interface exposes nearly every implementation decision;
- pure functions extracted for tests while defects can still arise in their call ordering or coordination;
- coupled modules where a change to one requires callers to know another module's implementation; and
- behavior with no test through the current interface, or whose tests must bypass that interface.

Apply the **deletion test** to each suspected shallow module: would deleting it concentrate complexity, or just move it? Treat concentration as a positive signal for a deepening candidate.

### 2. Write and open the HTML report

Write one self-contained HTML file outside the repository:

- In Pi, use the temp location specified by [PI.md](PI.md).
- Otherwise use `$TMPDIR`, falling back to `/tmp` on Unix or `%TEMP%` on Windows.
- Name it `<tmpdir>/architecture-review-<timestamp>.html` so an existing report is not overwritten.

Use Tailwind through its CDN for layout and styling. Use Mermaid through its CDN when call, dependency, flow, or sequence relationships form a graph. Use CSS, HTML, or SVG for non-graph comparisons such as module depth, cross-sections, or collapse views. Every candidate must have a before/after visualization.

For each candidate, render one card containing:

- **Files:** every inspected file or module that supports the finding;
- **Problem:** the observed navigation, coupling, interface, or testing evidence;
- **Solution:** the behavior to concentrate and the proposed seam location, without defining an interface;
- **Benefits:** the expected change in locality, leverage, and tests, tied to the listed evidence;
- **Before / After:** side-by-side diagrams of the current and proposed responsibility distribution; and
- **Recommendation strength:** one of `Strong`, `Worth exploring`, or `Speculative`, rendered as a badge.

End with **Top recommendation**, naming the candidate to tackle first and explaining why.

Use `CONTEXT.md` terms for domain concepts and `codebase-design` terms for architecture. For example, when the glossary defines `Order`, write `Order intake module`, not an implementation class name or `Order service`.

If a candidate conflicts with an ADR, include it only when the observed friction is substantial enough to warrant revisiting that ADR. Add a warning naming the ADR and the supporting evidence.

Use [HTML-REPORT.md](HTML-REPORT.md) for the HTML scaffold, diagram patterns, and styling constraints.

Do not propose method signatures, parameter shapes, or other interfaces during the scan. After writing the file, open it with `xdg-open <path>` on Linux, `open <path>` on macOS, or `start <path>` on Windows. Report its absolute path and the top recommendation. If the invocation names a candidate to develop, continue to step 3. Otherwise stop; the report is the complete deliverable and no selection question is required.

### 3. Develop a selected candidate

After the user selects a candidate, use [`grill-with-docs`](../grill-with-docs/SKILL.md) to resolve constraints, dependencies, the deepened module's ownership, what remains behind the seam, which existing tests remain unchanged, and which tests use the resulting interface.

Maintain domain and decision docs while resolving the design:

- When the module is named after a domain concept absent from `CONTEXT.md`, add the confirmed term. Create the file only when adding the first term.
- When the user confirms a narrower or distinct meaning for an existing term, update that term in the same turn.
- Record an already-established rejection as an ADR only when the invocation authorizes documentation changes, the rejection rules out one or more candidate architectures, and future agents could otherwise repeat the rejected proposal. Do not record a rejection whose reason is represented directly in code or the domain glossary, or applies only to the current session.
- To compare alternative interfaces, follow [`codebase-design`](../codebase-design/SKILL.md) and its one-designer Design It Twice process.

This step is complete when the selected candidate has confirmed behavior ownership, seam placement, interface test surface, and applicable domain or ADR updates. It does not implement the refactor.
