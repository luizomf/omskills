---
name: implement
description:
  Implement one selected Ticket in the current conversation through independent
  review and verified delivery.
disable-model-invocation: true
---

# Implement

Keep the selected Ticket with the current conversational owner, whether the
maintainer stays or authorizes work while away. This entry loads a procedure; it
does not launch another coordinator.

Before reading relative links, run `cd '<loaded-skill-directory>' && pwd -P`
with this file's directory, then resolve links from that physical base. Read
linked files even when absent from discovery.

1. Resolve the selected Ticket, repository, accepted scope, and requested
   stopping point. Reuse decisions already made in the conversation. Ask only
   for missing information that prevents progress. This step is complete when
   the work and delivery boundary are clear.
2. Read and follow [orchestrate](../orchestrate/SKILL.md) in this conversation:
   implement, obtain independent review, resolve findings, verify, and deliver
   through the authorized boundary. This step is complete at that boundary or
   when a genuine blocker prevents further in-scope progress.

If the request instead selects multiple Tickets, follow
[dispatch-tickets](../dispatch-tickets/SKILL.md) for that queue. An existing
multi-Ticket Mission keeps its dispatcher through completion, even when only one
Ticket remains.

Example: “Implement example/project#42; I'm leaving, continue through push”
keeps you responsible for #42 through review, corrections, verification, and
push. The maintainer's departure does not add a dispatcher, audit, or approval
step.
