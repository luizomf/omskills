---
name: implement
description: Implement one authorized code or behavior-changing Ticket with a current Prompt Audit PASS or explicit BYPASS.
---

# Implement

1. Read the exact Ticket, its governing Spec, repository instructions, live dependency and conflict state, and newest applicable Prompt Audit status. Proceed only when the Ticket is `ready-for-agent`, fits one fresh context, and has a current `PASS` or explicit maintainer `BYPASS`; otherwise report that it is not authorized.
2. Treat `PASS` or `BYPASS` as delegated authority for every in-scope implementation decision. Resolve those decisions from the accepted sources and repository evidence without opening another user decision gate. If required behavior cannot be determined or external authority is unavailable, report the Ticket as blocked rather than widening or guessing.
3. Implement only the Ticket. Findings outside its scope remain findings and do not become new code, Tickets, or follow-up work during this invocation.
4. Use `tdd` when an established test seam can exercise the behavior. Pass through any seam already confirmed by the Ticket or its sources; do not ask the user to reconfirm it.
5. Run the smallest relevant repository-defined checks during development and the repository's applicable complete verification before completion. Do not assume typechecking or a conventional test suite exists.
6. Verify every acceptance criterion. Code review remains outside this skill unless the accepted workflow explicitly includes it.
7. Commit and push only when the accepted repository workflow or user direction requires them, using a conventional commit.
