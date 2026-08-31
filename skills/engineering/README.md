# Engineering

Core skills for code work, issue workflow, and architecture decisions. The groups describe the typical selection path; `dispatch-tickets` is user-only and the other current skills in this bucket remain agent-discoverable. Readiness and a current Prompt Audit gate make a Ticket eligible but do not select it: route one explicitly Mission-authorized Ticket directly to `orchestrate`, or supply one already-resolved ordered list of Mission-authorized identities to `dispatch-tickets` for fixed-sequence dispatch from a responsive root.

## Typically user-selected

- **[grill-with-docs](./grill-with-docs/SKILL.md)** - Run bounded Question rounds while maintaining domain language and ADRs.
- **[triage](./triage/SKILL.md)** - Move issues and external PRs through a state machine of triage roles.
- **[improve-codebase-architecture](./improve-codebase-architecture/SKILL.md)** - Scan a codebase for deepening opportunities, present a visual report, then grill through the selected candidate.
- **[setup-omskills](./setup-omskills/SKILL.md)** - Configure per-repo tracker, triage-label, and domain-document operations.
- **[to-spec](./to-spec/SKILL.md)** - Turn the current conversation context into a spec and publish it to the issue tracker.
- **[to-tickets](./to-tickets/SKILL.md)** - Break a plan, spec, or conversation into tracer-bullet tickets with blocking and conflict edges.
- **[implement](./implement/SKILL.md)** - Implement one audited, authorized code or behavior-changing Ticket and verify its acceptance criteria.
- **[orchestrate](./orchestrate/SKILL.md)** - Coordinate complete delivery of one explicitly authorized Ticket through single-pass writer and reviewer agents.
- **[dispatch-tickets](./dispatch-tickets/SKILL.md)** - Dispatch a fixed ordered list of Mission-authorized Tickets from a minimal responsive root through fresh coordinators.
- **[wayfinder](./wayfinder/SKILL.md)** - Map a huge or foggy effort into investigation tickets on the issue tracker.

## Typically agent-selected

- **[prototype](./prototype/SKILL.md)** - Build a throwaway prototype to validate logic, state, or UI alternatives.
- **[diagnosing-bugs](./diagnosing-bugs/SKILL.md)** - Disciplined diagnosis loop for hard bugs and performance regressions.
- **[research](./research/SKILL.md)** - Investigate a question against high-trust primary sources and save cited findings in the repo.
- **[tdd](./tdd/SKILL.md)** - Red -> green -> refactor development at confirmed test seams.
- **[codebase-design](./codebase-design/SKILL.md)** - Shared vocabulary and principles for designing deep modules.
- **[code-review](./code-review/SKILL.md)** - Review a committed range or complete WIP candidate along Standards and Spec axes.
- **[resolving-merge-conflicts](./resolving-merge-conflicts/SKILL.md)** - Resolve an in-progress git merge or rebase conflict.
