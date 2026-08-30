# Acyclic single-pass Ticket orchestration

Specialist role prompts reward local objectives: writers keep changing code, reviewers keep finding concerns, and coordinators keep routing work. Returning review findings to a writer and then reviewing the correction creates a cycle with no role that owns convergence.

Complete delivery of one Ticket therefore uses this acyclic graph:

```text
Ticket coordinator -> writer -> Ticket coordinator -> reviewer -> Ticket coordinator
```

The writer and reviewer are fresh, isolated, single-pass leaf agents. They return evidence only to the Ticket coordinator and never exchange work directly. After review, the Ticket coordinator adjudicates every finding, performs all surviving corrections directly, verifies and integrates the result, completes tracker and cleanup obligations, and owns the one-Ticket outcome. There are no delegated correction or confirmation rounds.

Review limits bound specialist loops rather than coordinator authority. A Ticket becomes eligible for autonomous execution only when it is `ready-for-agent` with a current Prompt Audit `PASS` or explicit maintainer `BYPASS`. Those gates do not select it into a Mission. Explicit Mission authorization selects the Ticket; after selection, the gate transfers every in-scope implementation decision for that exact contract to the Ticket coordinator. The coordinator resolves source-determined divergences and minor safe defaults without opening another user decision gate. If the authorized sources cannot determine required behavior, external authority is unavailable, or required repository setup is missing during the headless run, the coordinator returns a blocked Ticket outcome rather than widening, guessing, or starting interactive setup.

A separate Ticket dispatcher owns sequences. Its user or invoker supplies an explicit, already-resolved ordered Ticket identity list. The dispatcher is the only owner of that list, order, and cursor; it neither queries the tracker nor discovers or resolves work. It sends exactly one identity to each fresh Ticket coordinator, receives one compact outcome, advances only after a matching `delivered` outcome, and stops on any other terminal state. A coordinator never receives or selects later identities and never returns child-selected `next` work.

The managed dispatcher/coordinator lineage does not require interactive transport. `wormhole` and `tmux-worker` remain available and accurate as generic optional interactive transports outside that lineage, but they own no Ticket sequence state or cross-Ticket continuation in this architecture.

Authorization remains non-transitive. Review findings and newly imagined adjacent work are reported without creating or implementing additional Tickets. Mission completion requires every explicitly selected identity to be delivered; readiness, dispatch acceptance, and completion of one Ticket do not complete a longer Mission.
