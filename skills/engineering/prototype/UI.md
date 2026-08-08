# UI Prototype

Generate **several radically different UI variations** in a prototype-only entrypoint, switchable through a URL search parameter and a floating bottom bar.

If the question is about logic/state rather than what something looks like — wrong branch. Use [LOGIC.md](LOGIC.md).

## When this is the right shape

- "What should this page look like?"
- "I want to see a few options for this dashboard before committing."
- "Try a different layout for the settings screen."
- Any time the user would otherwise spend a day picking between three vague mockups in their head.

## Establish the source/build boundary first

Put every prototype-only element behind a source/build boundary that excludes it from the production module and route graph. This includes all variant components and subtrees, URL variant-selection logic, the switcher, keyboard controls, and any throwaway route and route registration. The production page and router must not import that boundary.

Use an existing prototype source set, excluded entrypoint, or build target whose files are omitted from production build inputs. A hidden control, unreachable route, dynamic runtime check, or `NODE_ENV !== 'production'` condition is insufficient: those approaches can leave prototype modules in production output.

If the host cannot provide this exclusion without changing production code outside the accepted contract, use a standalone prototype-only harness or entrypoint. It may consume public production components or fixture data, but it must not register itself in the production source or route graph.

## Two sub-shapes — strongly prefer sub-shape A

A UI prototype is much easier to judge when it is **butting up against the rest of the app** — real header, real sidebar, representative data, real density. Default to sub-shape A whenever an existing prototype-only boundary can compose the relevant page safely.

### Sub-shape A — adjustment to an existing page (preferred)

Use the prototype-only entrypoint to render the variants at the same logical URL with `?variant=` selection. Reuse read-only production components or data adapters where the boundary permits it, but keep the production page unchanged and keep every variant-selection import in the prototype source graph.

If the proposed UI would naturally live inside an existing page, mount it in the prototype entrypoint's representation of that page rather than editing the production route to host it.

### Sub-shape B — a new page (last resort)

Use this only when the thing being prototyped genuinely has no existing page to live inside, such as an entirely new top-level surface or a flow that cannot be embedded anywhere sensible.

Create an obviously named throwaway route only in the prototype route graph. Follow the host's routing conventions inside that graph, and use the same `?variant=` pattern. Do not add the route or its registration to production routing.

## Process

### 1. State the question and pick N

Default to **3 variants**. More than 5 stops being radically different and starts being noise — cap there.

Write down the plan in one line, in the prototype's location or a top-of-file comment:

> "Three variants of the settings page, switchable via `?variant=`, on the existing `/settings` route."

### 2. Generate radically different variants

Draft each variant. Hold each one to:

- The page's purpose and the data it has access to.
- The project's component library / styling system (TailwindCSS, shadcn, MUI, plain CSS, whatever).
- A clear exported component name, e.g. `VariantA`, `VariantB`, `VariantC`.

Variants must be **structurally different** — different layout, different information hierarchy, different primary affordance, not just different colours. If two drafts come out too similar, redo one with explicit "do not use a card grid" guidance.

### 3. Wire them together

Inside the prototype-only source set, create a single switcher component on the prototype route or entrypoint:

```tsx
// pseudo-code — adapt to the project's framework
const variant = searchParams.get('variant') ?? 'A';
return (
  <>
    {variant === 'A' && <VariantA {...data} />}
    {variant === 'B' && <VariantB {...data} />}
    {variant === 'C' && <VariantC {...data} />}
    <PrototypeSwitcher variants={['A','B','C']} current={variant} />
  </>
);
```

For sub-shape A (existing page): compose the needed read-only data in the prototype entrypoint above the switcher; only its rendered subtree changes per variant. The production route remains unchanged.

For sub-shape B (new page): the throwaway route mounts the same switcher inside the prototype route graph.

### 4. Build the floating switcher

A small fixed-position bar at the bottom-centre of the screen with three pieces:

- **Left arrow** — cycles to the previous variant (wraps around).
- **Variant label** — shows the current variant key and, if the variant exports a name, that name too. e.g. `B — Sidebar layout`.
- **Right arrow** — cycles forward (wraps around).

Behaviour:

- Clicking an arrow updates the URL search param (use the framework's router — `router.replace` on Next, `navigate` on React Router, etc) so the variant is shareable and reload-stable.
- Keyboard: `←` and `→` arrow keys also cycle. Don't intercept arrow keys when an `<input>`, `<textarea>`, or `[contenteditable]` is focused.
- Visually distinct from the page (e.g. high-contrast pill, subtle shadow) so it's obviously not part of the design being evaluated.
- Present only in the prototype build. Source/build exclusion, not a runtime condition, must keep it and its imports out of production output.

Put the switcher in one prototype-only shared component so both sub-shapes can reuse it. Do not place it in a shared production UI barrel or another module reachable from a production entry.

### 5. Hand it over

Surface the URL (and the `?variant=` keys). The user will flip through whenever they get to it. The interesting feedback is usually **"I want the header from B with the sidebar from C"** — that's the actual design they want.

### 6. Capture the answer and clean up

Once a variant has won, record which variant won and why through an action already authorized by the current contract. Preserve or remove the throwaway files only as that contract permits; do not promote them automatically.

If a separately audited production unit later promotes the decision, follow the [SKILL](SKILL.md): reimplement the behavior under production constraints and add applicable tests rather than copying a winning variant. Before that unit is complete, remove or disconnect the whole prototype-only subtree and route machinery. Run the host's production build and inspect its route manifest, bundle/module graph, or closest deterministic equivalent to prove the variant components, URL selection, switcher, keyboard controls, and throwaway route registration are absent.

## Anti-patterns

- **Sharing too much code between variants.** A shared `<Header>` is fine; a shared `<Layout>` defeats the point. Each variant should be free to throw out the layout.
- **Wiring variants to real mutations.** Read-only prototypes are fine. If a variant needs to mutate, point it at a stub — the question is "what should this look like", not "does the backend work".
- **Runtime-disabling prototype modules.** Hiding the switcher or making its route unreachable still permits the complete subtree to enter production output; exclude it at the source/build boundary.
- **Promoting the prototype directly to production.** The variant code was written under prototype constraints (no tests, minimal error handling). Promotion is a separate audited implementation unit that rewrites and tests the validated behavior.
