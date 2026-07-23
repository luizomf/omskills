---
name: tdd
description: Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.
---

# Test-Driven Development

Use a red → green loop. Apply the seam, test-quality, anti-pattern, and loop rules below during every cycle.

When exploring the codebase, read `CONTEXT.md` if it exists and use its domain terms in test names and interface vocabulary. Follow ADRs that apply to the code under test.

## Test criteria

A test must exercise behavior through a public interface and assert an externally observable result. It must not depend on private methods or internal structure. Name the test for the capability and condition it verifies, such as `user can checkout with valid cart`.

Use [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Seams

A **seam** is the public boundary through which a test supplies input and observes behavior.

Before writing any test:

1. List the seams to be tested.
2. Ask the user: "What's the public interface, and which seams should we test?"
3. Obtain confirmation for each listed seam.

Write tests only at confirmed seams. Do not test internal boundaries.

## Anti-patterns

- **Implementation-coupled:** the test mocks internal collaborators, invokes private methods, or verifies through a side channel such as querying the database instead of using the confirmed interface. It fails after an internal refactor even though observable behavior is unchanged.
- **Tautological:** the assertion derives its expected value with the same operation as the implementation, such as `expect(add(a, b)).toBe(a + b)`, a hand-built snapshot produced by the same steps, or a constant compared with itself. Derive expected values from an independent source: a known-good literal, a worked example, or the specification.
- **Horizontal slicing:** multiple tests are written before any corresponding implementation. Use vertical slices instead: one failing test → its minimal implementation → the next test.

## Loop

For each vertical slice, in this order:

1. **Red:** write one test at one confirmed seam and run it. Proceed only when it fails because the requested behavior is absent.
2. **Green:** add only the implementation required to make that test pass, then run it until it passes. Do not implement behavior reserved for a later test.
3. Start the next slice only after the current test passes.

Do not refactor during this loop. Refactoring belongs to the review stage; see [`code-review`](../code-review/SKILL.md).
