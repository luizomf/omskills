---
name: tdd
description: Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.
---

# Test-Driven Development

Use a red → green → refactor loop. Apply the test-seam, test-quality, anti-pattern, and loop rules below during every cycle.

When exploring the codebase, read `CONTEXT.md` if it exists and use its domain terms in test names and interface vocabulary. Follow ADRs that apply to the code under test.

## Test criteria

A test must exercise behavior through a confirmed **test seam** and assert a caller-visible result. It must not depend on private methods or internal structure. Name the test for the capability and condition it verifies, such as `user can checkout with valid cart`.

Use [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Test seams

Use the architecture meaning of **seam** from `codebase-design`: a location where behavior can be altered without editing code at that location. A **test seam** is a seam exposed through the caller-visible interface that production callers and behavior tests share.

Before writing any test:

1. List the test seams to be exercised.
2. Treat a test seam already confirmed in the request, specification, issue, ticket, or conversation as approved.
3. For each unconfirmed test seam, ask the user: "What's the caller-visible interface, and which test seams should we exercise?" Obtain confirmation before writing its first test.

Write behavior tests only at confirmed test seams. Do not bypass the caller-visible interface to test internal seams.

## Anti-patterns

- **Implementation-coupled:** the test mocks internal collaborators, invokes private methods, or verifies through a side channel such as querying the database instead of using the confirmed interface. It fails after an internal refactor even though observable behavior is unchanged.
- **Tautological:** the assertion derives its expected value with the same operation as the implementation, such as `expect(add(a, b)).toBe(a + b)`, a hand-built snapshot produced by the same steps, or a constant compared with itself. Derive expected values from an independent source: a known-good literal, a worked example, or the specification.
- **Horizontal slicing:** multiple tests are written before any corresponding implementation. Use vertical slices instead: one failing test → its minimal implementation → the next test.

## Loop

For each vertical slice, in this order:

1. **Red:** write one test at one confirmed test seam and run it. Proceed only when it fails because the requested behavior is absent.
2. **Green:** add only the implementation required to make that test pass. Run the current test and every relevant previously passing test until they all pass. Do not implement behavior reserved for a later test.
3. **Refactor:** improve the test and implementation structure without changing observable behavior or adding behavior reserved for a later slice. Rerun the same tests until they all pass again.
4. Start the next slice only after the refactored slice and all relevant prior tests pass.

A vertical slice is complete only after red demonstrated the missing behavior, green supplied it, and refactor preserved it with passing tests.
