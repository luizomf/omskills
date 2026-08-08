# Acyclic single-pass orchestration

Specialist role prompts reward local objectives: writers keep changing code, reviewers keep finding concerns, and coordinators keep routing work. Returning review findings to a writer and then reviewing the correction creates a cycle with no role that owns convergence.

Repository delivery orchestration therefore uses this acyclic graph:

```text
coordinator -> writer -> coordinator -> reviewer -> coordinator
```

The writer and reviewer are fresh, isolated, single-pass leaf agents. They return evidence only to the coordinator and never exchange work directly. After review, the coordinator adjudicates every finding, performs all surviving corrections directly, verifies and integrates the result, and owns the stop or completion decision. There are no delegated correction or confirmation rounds.

Review limits bound specialist loops rather than coordinator authority. Inside accepted scope, the coordinator resolves source-determined divergences and chooses minor safe, reversible defaults consistent with repository conventions. It asks the user only for a material unresolved decision, a change outside approved scope, or genuinely external authority.

Each completed work unit is a normal fresh-context boundary. Another authorized unit continues through `wormhole`, whose handoff identifies `orchestrate` as the governing contract for the fresh coordinator. A completed mission with no next unit ends with a report instead of opening an idle session.
