---
name: codebase-design
description: Design or improve deep modules. Use when shaping a module interface, deepening modules, placing a seam, reducing coupling, designing for testability, or when another skill requires the deep-module vocabulary.
---

# Codebase Design

Design **deep modules**: modules whose callers can exercise multiple required behaviors through a smaller interface at a defined seam. Apply the terms and rules below when designing or restructuring code. The target outcomes are leverage across callers, locality of changes and defects, and tests that use the same interface as production callers.

## Glossary

Use these architecture terms as defined here. Do not substitute `component`, `service`, `API`, or `boundary`, because those words identify different or narrower concepts.

**Module** — any unit with exactly one interface and an implementation, including a function, class, package, or tier-spanning slice. This term does not imply scale. Avoid `unit`, `component`, and `service` for this concept.

**Interface** — every fact a caller must know to use a module correctly: type signatures, invariants, ordering constraints, error modes, required configuration, and performance characteristics. `API` and `signature` name only part of this surface.

**Implementation** — code inside a module. Use **adapter** instead when discussing the role a concrete implementation fills at a seam. Implementation size and adapter size are independent; for example, a Postgres repository can be a small adapter with a large implementation, while an in-memory fake can be a large adapter with a small implementation.

**Depth** — behavior a caller or test can exercise relative to the interface facts it must learn. A module is **deeper** than an alternative when it preserves required behavior while exposing fewer methods, parameters, invariants, ordering constraints, error modes, configuration requirements, or performance obligations. It is **shallow** when callers must supply or coordinate the implementation's intermediate states and steps.

**Seam** _(Michael Feathers)_ — a location where behavior can be altered without editing code at that location. Seam placement and the behavior behind the seam are separate decisions. A seam may be internal to a module. Avoid `boundary`, which also refers to a DDD bounded context.

**Test seam** — a seam exposed through the caller-visible interface that production callers and behavior tests share. Tests may use a different adapter at that seam, but do not bypass the interface to reach an internal seam.

**Adapter** — a concrete module that satisfies an interface at a seam. The term identifies the role, not the implementation technology.

**Leverage** — reuse of behavior behind one interface across multiple callers or tests. A change behind the interface applies without reproducing the rule at each caller.

**Locality** — concentration of a behavior's code, required knowledge, defects, changes, and verification in one module rather than its callers.

## Deep and shallow modules

A deep module exposes a smaller interface than the behavior it contains:

```text
┌─────────────────────┐
│   Small Interface   │  ← fewer caller-visible facts
├─────────────────────┤
│                     │
│  Deep Implementation│  ← behavior hidden from callers
│                     │
└─────────────────────┘
```

A shallow module exposes an interface that repeats most implementation decisions:

```text
┌─────────────────────────────────┐
│       Large Interface           │  ← many caller-visible facts
├─────────────────────────────────┤
│  Thin Implementation            │  ← forwards or rearranges inputs
└─────────────────────────────────┘
```

When comparing interface designs, check:

- whether multiple methods can become one operation without losing required behavior;
- whether the module can derive or own any current parameters;
- whether invariants, ordering, configuration, errors, or performance obligations can move behind the interface; and
- whether the reduced surface still supports every required caller and test behavior.

## Principles

- **Depth is a property of a module relative to its interface.** Internal composition does not make an external interface shallow. A module may use internal seams available only to its implementation and implementation-level tests while exposing one external seam to callers.
- **Deletion test.** Model deleting the module while preserving required behavior. If no caller must absorb rules or knowledge, the module was a pass-through. If rules or knowledge must be copied or coordinated across callers, the module provides locality or leverage.
- **The interface is the test surface.** Production callers and behavior tests use the same test seam. A test that must bypass the interface is evidence that the interface does not expose required behavior or that the tested behavior belongs to another module.
- **One adapter is a hypothetical seam; two adapters make variation observable.** Treat a seam as worth designing only when at least two adapters exist.

## Designing for testability

### Accept dependencies instead of constructing them inside the behavior

```typescript
// Dependency can vary at the seam.
function processOrder(order, paymentGateway) {}

// Dependency selection is coupled to this implementation.
function processOrder(order) {
  const gateway = new StripeGateway();
}
```

### Return results instead of producing side effects

```typescript
// The result is observable without inspecting mutation.
function calculateDiscount(cart): Discount {}

// Verification requires observing mutation and hidden discount state.
function applyDiscount(cart): void {
  cart.total -= discount;
}
```

### Minimize the caller-visible surface

A smaller caller-visible surface generally requires fewer tests and simpler setup.

## Rejected framings

- **Implementation-lines divided by interface-lines:** this metric can increase by adding implementation code without adding behavior. Evaluate depth by caller-visible facts and exercised behavior instead.

## Progressive references

- For deepening a cluster with known dependencies, read [DEEPENING.md](./DEEPENING.md) for dependency categories, seam discipline, and replace-don't-layer testing.
- For comparing alternative interfaces, read [DESIGN-IT-TWICE.md](./DESIGN-IT-TWICE.md) for the optional one-designer comparison process. Use it only when the invoking workflow authorizes that designer role and the current caller can dispatch a non-delegating leaf within its inherited depth. A depth-3 leaf resolves accepted sources directly or returns a blocker; it never requests depth 4.
- To scan an entire repository for candidates, use `improve-codebase-architecture`.
