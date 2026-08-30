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

1. List every caller-visible test seam to be exercised.
2. Treat a test seam already confirmed in the accepted request, Spec, Ticket, repository sources, or conversation as confirmed. When those accepted sources and repository behavior determine the caller-visible interface and seam, record that evidence and proceed without asking for reconfirmation. Resolve a minor residual choice that does not change caller-visible coverage through established repository conventions.
3. Resolve each genuinely unconfirmed material seam through the applicable authority branch:
   - In standalone interactive use, ask the explicit Question: "What's the caller-visible interface, and which test seams should we exercise?" Obtain confirmation before writing the first test at that seam.
   - In a Mission-authorized Ticket with a current `PASS` or explicit maintainer `BYPASS`, stop and return the unresolved seam as a blocker directly to the Ticket coordinator. An audited writer, including a depth-3 writer, remains a single-pass leaf: it does not delegate or route the blocker through the Ticket dispatcher.
   - In any other print/headless invocation, report the unresolved seam to the caller and stop before writing tests. Print/headless execution never waits for a conversational answer.

Seam selection is complete only when every test seam is confirmed from accepted sources or interactive confirmation, or the applicable terminal blocker has been returned. Write behavior tests only at confirmed test seams. Do not bypass the caller-visible interface to test internal seams.

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
