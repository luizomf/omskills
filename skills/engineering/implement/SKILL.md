---
name: implement
description:
  Compose one selected Ticket as a one-item Assisted or Unattended Mission
  through dispatch-tickets.
disable-model-invocation: true
---

# Implement

Use this convenience entry for one selected Mission Ticket. Ordinary Direct
Assisted work can stay with its conversational owner.

Before reading relative links, run `cd '<loaded-skill-directory>' && pwd -P`
with this file's directory, then resolve links from that physical base. Read
linked files even when absent from discovery.

1. Resolve exactly one Ticket identity, repository, implementation
   authorization, and `Assisted` or `Unattended` availability from the accepted
   request. Preserve established choices and ask only about a materially missing
   input. This step is complete when the selected work and availability are
   clear.
2. In this same conversation, read and follow
   [dispatch-tickets](../dispatch-tickets/SKILL.md) with that one-item queue and
   the relevant user instructions. The dispatcher checks live relations and
   existing ownership, starts or resumes the responsible `orchestrate`
   conversation, and verifies its delivery. This step is complete when the
   dispatcher has taken responsibility for that queue or reported its concrete
   blocker.

Example: “Implement example/project#42; I'll be available for Questions”
supplies one selected Ticket and Assisted availability. Forward that request to
the dispatcher; its tracker checks establish whether #42 can start.
