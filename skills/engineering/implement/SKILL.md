---
name: implement
description: "Implement a piece of work based on a spec, issue, or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec, issue, or tickets.

Use /tdd where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, use /code-review to review the work.

Only commit when the user explicitly asked for a commit, or when the repo's recorded workflow says this invocation should commit. If committing, use a conventional commit.
