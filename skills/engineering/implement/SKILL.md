---
name: implement
description: "Implement requested behavior from a specification, issue, or set of tickets."
---

# Implement

1. Identify the requested behavior and every acceptance criterion in the supplied spec, issue, or tickets. Implement only that work.
2. Use `tdd` when the behavior can be exercised at a test seam already confirmed in the request, specification, issue, tickets, or conversation. Pass that confirmation through; do not ask the user to reconfirm the same test seam.
3. Run typechecking regularly, single test files regularly, and the full test suite once after implementation is complete.
4. Verify the completed work against its acceptance criteria. Code review is outside this skill unless the user explicitly requests it.
5. Commit only when the user explicitly requested a commit or the repository's recorded workflow says this invocation should commit. Use a conventional commit when committing.
