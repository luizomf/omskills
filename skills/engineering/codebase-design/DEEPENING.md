# Deepening

How to deepen a cluster of shallow modules safely, given its dependencies. Assumes the vocabulary in [SKILL.md](./SKILL.md) — **module**, **interface**, **seam**, **adapter**.

## Dependency categories

When assessing a candidate for deepening, classify its dependencies. The category determines how the deepened module is tested across its seam.

### 1. In-process

Pure computation, in-memory state, no I/O. Always deepenable — merge the modules and test through the new interface directly. No adapter needed.

### 2. Local-substitutable

Dependencies that have local test stand-ins (PGLite for Postgres, in-memory filesystem). Deepenable if the stand-in exists. The deepened module is tested with the stand-in running in the test suite. The seam is internal; no port at the module's external interface.

### 3. Remote but owned (Ports & Adapters)

Your own services across a network boundary (microservices, internal APIs). Define a **port** (interface) at the seam. The deep module owns the logic; the transport is injected as an **adapter**. Tests use an in-memory adapter. Production uses an HTTP/gRPC/queue adapter.

Recommendation shape: *"Define a port at the seam, implement an HTTP adapter for production and an in-memory adapter for testing, so the logic sits in one deep module even though it's deployed across a network."*

### 4. True external (Mock)

Third-party services (Stripe, Twilio, etc.) you don't control. The deepened module takes the external dependency as an injected port; tests provide a mock adapter.

## Seam discipline

- **One adapter means a hypothetical seam. Two adapters means a real one.** Introduce a port only when at least two adapters are justified (typically production + test).
- **Internal seams vs external seams.** A deep module can have internal seams (private to its implementation, used by its own implementation-level tests) as well as the external test seam at its interface. Don't expose internal seams through the interface just because implementation-level tests use them.

## Testing strategy: replace, don't layer

Replace-don't-layer describes the target test surface, not permission to delete tests early.

1. Inventory the observable behavior covered by each old test before changing it.
2. Write and run behavior tests through the resulting caller-visible interface. Coverage through an internal seam, direct implementation access, or a failing test does not establish equivalence.
3. Map every behavior in an old test to passing coverage through that interface. Delete the old test only when the complete mapping demonstrates equivalent observable behavior.
4. Preserve an old test while any behavior it covers remains unique. If the behavior cannot be exercised through the resulting interface, either the interface is missing required behavior or the test belongs to a different module; resolve that before deletion.

The **interface is the test surface**. Assert observable outcomes rather than internal state so the replacement tests survive internal refactors. The final suite should avoid redundant implementation-level tests, but unique behavior coverage survives until an equivalent interface-level replacement passes.
