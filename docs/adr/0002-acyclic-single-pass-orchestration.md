# Acyclic single-pass orchestration

Specialist role prompts reward local objectives: writers keep changing code, reviewers keep finding concerns, and coordinators keep routing work. Returning review findings to a writer and then reviewing the correction creates a cycle with no role that owns convergence.

Repository delivery orchestration therefore uses this acyclic graph:

```text
coordinator -> writer -> coordinator -> reviewer -> coordinator
```

The writer and reviewer are fresh, isolated, single-pass leaf agents. They return evidence only to the coordinator and never exchange work directly. After review, the coordinator adjudicates every finding, performs all surviving corrections directly, verifies and integrates the result, and owns the stop or completion decision. There are no delegated correction or confirmation rounds.

Review limits bound specialist loops rather than coordinator authority. A current Prompt Audit `PASS` or explicit maintainer `BYPASS` transfers every in-scope implementation decision for that exact Ticket to the coordinator. The coordinator resolves source-determined divergences, chooses minor safe defaults, and does not open another user decision gate. If the authorized sources cannot determine a required behavior or external authority is unavailable, the Ticket is reported as blocked rather than widened or guessed; the coordinator continues with the next independent authorized Ticket when one exists, otherwise it reports the blocked mission without opening an interactive decision loop.

Authorization is non-transitive. The mission envelope fixes the authorized Ticket identities, scope, deferrals, frozen queue, and completion boundary. A query or queue source is resolved to its current Ticket identities once at mission start; later additions do not enter the run. Review findings or newly imagined adjacent work are reported without creating or implementing additional Tickets. Each completed work unit is a normal fresh-context boundary. Another authorized unit continues through `wormhole`, whose handoff identifies `orchestrate` as the governing contract for the fresh coordinator. A completed mission with no next unit ends with a report instead of opening an idle session.
