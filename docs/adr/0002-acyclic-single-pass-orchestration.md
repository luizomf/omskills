# Acyclic single-pass orchestration

Specialist role prompts reward local objectives: writers keep changing code, reviewers keep finding concerns, and coordinators keep routing work. Returning review findings to a writer and then reviewing the correction creates a cycle with no role that owns convergence.

Repository delivery orchestration therefore uses this acyclic graph:

```text
coordinator -> writer -> coordinator -> reviewer -> coordinator
```

The writer and reviewer are fresh, isolated, single-pass leaf agents. They return evidence only to the coordinator and never exchange work directly. After review, the coordinator adjudicates every finding, performs all surviving corrections directly, verifies and integrates the result, and owns the stop or completion decision. There are no delegated correction or confirmation rounds.

Every code-delivery path starts only after its execution contract has a current Prompt Audit `PASS` or explicit maintainer-authorized `BYPASS`. A missing, stale, or `FAIL` status stops before writer dispatch or code and exposes the audit and explicit-bypass choices. The fixed read-only interpreter, reviewer, and confirmation prompts within the audit protocol are exempt from this gate so the audit does not recurse.

Direct implementation of one small unit uses `coordinator -> writer -> coordinator` when the harness provides clean writer isolation. The writer is an isolated single-pass leaf. The coordinator inspects and adjudicates its result, performs every surviving correction, verifies, integrates, and owns completion. When clean writer isolation is unavailable, the coordinator may implement the already-audited or explicitly bypassed unit directly, discloses that limitation, and retains the same completion ownership without adding a user gate, reviewer pass, or delegated correction loop.

Review limits bound specialist loops rather than coordinator authority. Inside accepted scope, the coordinator resolves source-determined divergences and chooses minor safe, reversible defaults consistent with repository conventions. It asks the user only for a material unresolved decision, a change outside approved scope, or genuinely external authority.

Each completed work unit is a normal fresh-context boundary. Another authorized unit continues through `wormhole`, whose handoff identifies `orchestrate` as the governing contract for the fresh coordinator. A completed mission with no next unit ends with a report instead of opening an idle session.
