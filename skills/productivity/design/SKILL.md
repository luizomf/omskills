---
name: design
description: Design and refine context-fit user interfaces, then verify the rendered result.
disable-model-invocation: true
argument-hint: "What should be designed or refined?"
---

# Design

Create a visually coherent interface that fits its users, task, content, product, and existing system. Treat beauty as contextual fitness plus deliberate craft, not conformance to a fashionable style.

## Process

1. **Ground the direction.** Inspect the current interface, repository conventions, reusable components, supplied references, and real content. State one sentence covering the audience, primary task, and material constraints. Existing product decisions outrank novelty unless redesign is explicitly in scope. This step is complete when every visible design decision can be traced to the product, content, reference, or stated direction.

2. **Choose a visual thesis.** Define one sentence for the intended character and hierarchy. Select a coherent typography, color, spacing, shape, imagery, and motion treatment; introduce at most one signature move unless the reference requires more. Prefer purposeful composition over decorative filler, repeated card grids, or fashionable effects without a product role. This step is complete when the thesis distinguishes the interface without competing with its primary task.

3. **Design the whole requested surface.** Preserve accurate content and information hierarchy. Reuse the established design system before adding tokens or components. Cover the relevant initial, loading, empty, error, success, disabled, selected, and responsive states instead of polishing only the ideal screenshot. Use clearly labeled mock data when real data is unavailable; product claims and user data remain grounded in supplied material. This step is complete when every in-scope state and primary interaction has an intentional presentation.

4. **Clear the usability floor.** Use semantic controls, keyboard operation, visible focus, sufficient contrast, useful labels, reduced-motion behavior, and layouts that survive narrow widths, zoom, long content, and missing content. Consult the relevant authoritative source when a component contract or accessibility requirement is uncertain. This step is complete when no known floor failure blocks the primary task.

5. **Render and iterate.** Inspect the actual result rather than inferring it from source code. Exercise the primary interaction, check desktop and a narrow viewport, and compare against the visual thesis and any supplied reference. Make focused corrections to hierarchy, typography, spacing, color, states, overflow, and interaction feedback. Distinguish rendered observations from code-based inference and name anything that could not be verified. This step is complete when no material mismatch or usability-floor failure remains within scope.

## Response

Report the visual thesis, the material choices or changes, the rendered checks performed, and any unverified limitation. Keep the explanation shorter than the design work.

## Example

```text
/skill:design Refine the transaction dashboard. Keep the existing components,
make failed payments easier to scan, and verify desktop and mobile states.
```
