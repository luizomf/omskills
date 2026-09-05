---
name: implement
description: Compose one explicitly authorized Ticket as a one-item Assisted or Unattended Mission through dispatch-tickets.
disable-model-invocation: true
---

# Implement

Accept exactly one semantically explicit Mission-authorized Ticket identity, independently resolved `Assisted` or `Unattended` availability, and explicit confirmation that all external blockers and conflicts are resolved. Required authority comes from the request's meaning, not caller provenance, ancestry, role, depth, dispatcher wording, or a magic phrase. In this same root invocation, load and follow installed `dispatch-tickets` with the identity unchanged in this complete one-item Mission plan:

```json
{"phases":[["<owner>/<repository>#<ticket>"]],"blockers":[],"conflicts":[]}
```

Forward the authorization, availability, and confirmation with the plan; do not infer any of them from Ticket selection alone. The dispatcher then validates and freezes the plan and creates the fresh `orchestrate` Ticket coordinator.

If the selected identity, authorization, availability, or external-relations confirmation is missing or invalid, report the missing or invalid input and stop before loading the dispatcher. Do not read Ticket or repository content, call `orchestrate`, create a child, or perform implementation, coordination, review, verification, or delivery here. This skill is only an optional one-Ticket Mission convenience entry and owns no execution path independent of `dispatch-tickets`; ordinary Direct Assisted work does not require it.
