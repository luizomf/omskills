---
name: improve-codebase-architecture
description: Scan a codebase for deepening opportunities, write a visual HTML report, and develop a selected candidate through a decision interview.
---

# Improve Codebase Architecture

Identify **deepening opportunities**: refactors that place more behavior behind a smaller interface at a defined seam, improving testability and code navigation.

Use two authoritative vocabularies:

- Read `codebase-design` for **module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**, the deletion test, interface-as-test-surface, and adapter-count rules. Use those architecture terms in every candidate; do not substitute `component`, `service`, `API`, or `boundary`.
- Use domain terms from applicable `CONTEXT.md` files; when the glossary defines `Order`, write `Order intake module`, not an implementation class name or `Order service`. Treat ADRs in `docs/adr/` as decisions that remain in force unless the report supplies repository evidence for reopening one.

## Process

### 1. Scan

Read the applicable domain glossary and ADRs before scanning code.

Delegate the scan to exactly one new Explore worker with clean context through the active harness's isolated-worker mechanism. The worker directly inspects the repository and produces findings; the Explore role or name does not grant tools, isolation, delivery, or permission to delegate. In Pi, follow [PI.md](PI.md).

Before launch, preflight the repository-read and findings-write tools and providers. Where the harness exposes lineage controls, set the worker's maximum delegation depth to its assigned depth and its direct-child ceiling to zero. A root interactive caller may use documented visible or asynchronous delivery; a print caller and a depth-2 caller that depends on the findings use direct delivery. Direct settlement returns once and produces no later asynchronous completion notification. After asynchronous acceptance, do not wait, sleep, or poll; resume only from the documented completion notification. A depth-3 leaf does not request a depth-4 worker: it validates a complete Explore artifact supplied by its coordinator or returns a blocker.

The initial prompt must let the worker execute without inherited conversation context and include the worker role, repository path, authoritative domain and architecture references, scan scope, one exact findings-artifact path, and required finding fields. State that the worker is a non-delegating leaf, must not invoke this skill, and must report the artifact path. Do not create separate workers for candidates or alternatives. Treat an over-depth or capability rejection before prompt acceptance as no scan, not partial evidence.

The worker must follow repository references based on observed code rather than stop at a fixed directory or match quota. Use these categories to classify observed friction; they are neither an exhaustive navigation checklist nor a requirement to produce one finding per category:

- domain behavior that requires navigation across multiple modules;
- modules whose caller-visible interface exposes nearly every implementation decision;
- pure functions extracted for tests while defects can still arise in their call ordering or coordination;
- coupled modules where a change to one requires callers to know another module's implementation; and
- behavior with no test through the current interface, or whose tests must bypass that interface.

Apply the **deletion test** to each suspected shallow module: would deleting it concentrate complexity, or just move it? Treat concentration as a positive signal for a deepening candidate.

After the worker settles, require a completed result, read the exact findings artifact, and validate it before continuing. It must be non-empty, cover the requested scope, cite inspected repository paths for every candidate, include every required finding field, use the authoritative vocabularies, report evidence gaps, and contain no repository edits or private data. Bounded terminal output or a native session reference may recover transport evidence but never replaces the artifact. A failed, interrupted, missing, or invalid artifact blocks report generation.

### 2. Write and open the HTML report

Write one HTML file outside the repository:

- In Pi, use the temp location specified by [PI.md](PI.md).
- Otherwise use `$TMPDIR`, falling back to `/tmp` on Unix or `%TEMP%` on Windows.
- Name it `<tmpdir>/architecture-review-<timestamp>.html` so an existing report is not overwritten.

Use [HTML-REPORT.md](HTML-REPORT.md) for the HTML scaffold, diagram patterns, and styling constraints.

For each candidate, render one card containing:

- **Files:** every inspected file or module that supports the finding;
- **Problem:** the observed navigation, coupling, interface, or testing evidence;
- **Solution:** the behavior to concentrate and the proposed seam location, without defining an interface;
- **Benefits:** the expected change in locality, leverage, and tests, tied to the listed evidence;
- **Before / After:** side-by-side diagrams of the current and proposed responsibility distribution; and
- **Recommendation strength:** one of `Strong`, `Worth exploring`, or `Speculative`, rendered as a badge.

End with **Top recommendation**, naming the candidate to tackle first and explaining why.

If a candidate conflicts with an ADR, include it only when the observed friction is substantial enough to warrant revisiting that ADR. Add a warning naming the ADR and the supporting evidence.

Do not propose method signatures, parameter shapes, or other interfaces before step 3. After writing the file, read it back and apply the completion checks in [HTML-REPORT.md](HTML-REPORT.md). Only then attempt `xdg-open <path>` on Linux, `open <path>` on macOS, or `start <path>` on Windows. In headless or print operation, an unavailable opener or non-zero opener result is explicit and non-fatal once the complete report has been validated: report the failure, absolute path, and top recommendation. Do not treat a successful opener as report validation. If the invocation names a candidate to develop, continue to step 3. Otherwise stop; the validated report is the complete deliverable and no selection question is required.

### 3. Develop a selected candidate

After the user selects a candidate, use `grill-with-docs` to resolve constraints, dependencies, the deepened module's ownership, what remains behind the seam, which existing tests remain unchanged, and which tests use the resulting interface. Apply its bounded Question-frontier rounds only inside that selected candidate: a round may include no more than three independent Questions, and must never include Questions from another report candidate.

Maintain domain and decision docs while resolving the design:

- When the module is named after a domain concept absent from `CONTEXT.md`, add the confirmed term. Create the file only when adding the first term.
- When the user confirms a narrower or distinct meaning for an existing term, update that term in the same turn.
- Record an already-established rejection as an ADR only when the invocation authorizes documentation changes, the rejection rules out one or more candidate architectures, and future agents could otherwise repeat the rejected proposal. Do not record a rejection whose reason is represented directly in code or the domain glossary, or applies only to the current session.
- To compare alternative interfaces, follow `codebase-design` and its one-designer Design It Twice process.

This step is complete when the selected candidate has confirmed behavior ownership, seam placement, interface test surface, and applicable domain or ADR updates. It does not implement the refactor.
