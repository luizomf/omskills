---
name: wayfinder
description: Plan work that exceeds one agent session as a shared map of investigation tickets, then resolve one ticket per session until the route to the destination is clear.
---

# Wayfinder

Use a **shared map** to determine the route from a loose idea to a named **destination**. The destination may be a spec, a decision required before planning, or an in-place change such as a data-structure migration. The map may cover engineering, course content, or another domain.

## Plan by default

Unless the map's **Notes** explicitly include execution, each ticket resolves a decision and produces no destination deliverable. The map is complete when no decision remains before execution. When resolving the next ticket would perform the destination work rather than determine how to perform it, hand off instead.

## Refer to issues by title

In narration and the map's **Decisions so far**, refer to every map and ticket by its linked title. Do not use a bare id, number, or slug as its human-readable name; retain the id or URL in the title's link.

## Map structure

The map is the authoritative item for the effort in the configured Issue tracker. On a hosted label-backed tracker it uses `wayfinder:map`; on a deliberately selected local Markdown tracker it uses the configured `map.md` path and no hosted label. Its Tickets are children through the selected tracker's configured relationship.

The map indexes decisions; each decision's detail exists only in its ticket. **Decisions so far** contains a one-line gist and link.

## Tracker preflight

Tracker storage, child scope, blockers, comments, type labels or fields, claims, and frontier queries are tracker-specific. Read the selected Issue tracker's complete configuration, including its **Wayfinding operations**, before charting or working a map. Use only operations and fallbacks explicitly documented there.

The configuration is a hard dependency. If it is missing, run `setup-omskills`; if setup fails, no tracker is selected, or a required operation is unavailable, stop and report the missing capability. Never switch to local Markdown or another tracker. Local Markdown is valid only when it is the deliberately selected Issue tracker. A capability exists only when the selected configuration documents it; use read-only CLI help or API metadata to validate a documented operation, never a mutating probe or an invented operation.

### Fixed Wayfinder types

For a hosted tracker that represents Wayfinder types as labels, the Wayfinder consumer owns exactly this inventory:

| Label | Description |
| --- | --- |
| `wayfinder:map` | Shared Wayfinder map |
| `wayfinder:research` | Wayfinder research Ticket |
| `wayfinder:prototype` | Wayfinder prototype Ticket |
| `wayfinder:grilling` | Wayfinder grilling Ticket |
| `wayfinder:task` | Wayfinder task Ticket |

Before an operation needs these labels, use only the selected tracker's configured label-inventory and creation operations. Inventory all labels, re-inventory before creating any missing label, create only missing names from this table with public descriptions and tracker-valid colors, then verify the complete inventory. Preserve every unrelated label; "exactly" limits what Wayfinder manages and never authorizes removing other labels. Setup does not maintain a reverse inventory for this consumer.

When the selected tracker is local Markdown, preserve its configured `Type: research|prototype|grilling|task` representation. Do not run or invent hosted label operations for it.

### Map body

Load this low-resolution view once per session. Find open Tickets by querying child issues; do not list them in the map body unless the configured tracker requires its documented task-list fallback. In that fallback only, the task list is the child index.

```markdown
## Destination

<the spec, decision, or change that marks the end of this map; one or two lines>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- one line per closed decision ticket: linked title plus enough detail to judge relevance -->

- [<closed ticket title>](link) — <one-line gist of the answer>

## Not yet specified

<!-- in-scope questions that cannot yet be stated precisely enough for a ticket -->

## Out of scope

<!-- work beyond the destination; it does not graduate into tickets -->
```

### Tickets, claims, and dependencies

Each ticket:

- is a child issue of the map and uses the tracker's issue id as its identity;
- contains one question sized for one fresh agent session;
- has exactly one configured Wayfinder type: hosted label `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, or `wayfinder:task`, or the selected local tracker's corresponding `Type:` field;
- records its answer in a resolution comment rather than the body; and
- links assets created during resolution instead of pasting them into the body.

```markdown
## Question

<the decision or investigation this ticket resolves>
```

An open, unassigned ticket is unclaimed. Use the tracker's native dependency relationship for blocking and only its documented fallback when the native capability is unavailable. A ticket is **unblocked** when every ticket blocking it is closed. The **frontier** is the ordered set of actual open, unblocked, unclaimed child tickets returned through the selected tracker's child-scope operation.

### Selection and claim protocol

Apply this protocol to named and automatic selection before resolution work:

1. Query the current map's actual child scope with the configured operation. A named Ticket that is absent is not selectable; repository-wide search results and incidental references never establish parentage.
2. Read the candidate's current open state, blockers, and claims. Reject a closed or blocked candidate. Reject an assigned candidate unless distinct evidence proves this session owns it.
3. For an unclaimed candidate, run the configured claim operation and immediately re-read child scope, open state, blockers, and ownership. Proceed only after a successful claim and an unchanged eligible re-read.
4. On claim failure or changed child, open, blocker, or ownership state, do no resolution work. A named selection stops. Automatic selection may recompute from completely fresh state only when the failed attempt provably left no ambiguous claim; otherwise stop.

In ordinary work where concurrency under the tracker identity is neither requested nor known, this session's successful configured claim of a Ticket it just observed as unclaimed, followed by that immediate unchanged re-read, is sufficient session evidence. An assignee identity alone is never session evidence, even when it is the expected developer identity.

When concurrent work under one shared tracker identity is requested or known:

- A **distinct preclaim** is explicit user or coordinator allocation of a different named Ticket to each session before dispatch. It proves session allocation without adding a private session identifier to the tracker. Naming one Ticket counts only when the allocation is distinct across the concurrent sessions.
- Automatic selection requires either a claim operation that the selected configuration explicitly documents as atomic or distinct preclaims that narrow each session to its allocated Ticket. A normal assignment command is not atomic merely because it succeeds.
- If neither mechanism exists, stop automatic selection. Do not infer a capability from undocumented CLI behavior or probe a mutating operation.
- A shared assignee remains ambiguous without the distinct preclaim or other distinct, non-private evidence. The ordinary claim sequence is not sufficient under known shared-identity concurrency.

Resolve at most one Ticket in the session, including after any reselection.

## Ticket types

Every ticket is either **HITL** (requires live input from a human speaking for themselves) or **AFK** (the agent can resolve it without live human input). An agent must not supply the human side of a HITL exchange.

- **Research** (AFK): use when resolving the question requires knowledge outside the current working directory, such as external documentation, third-party APIs, or a local knowledge base. Produce and link a Markdown summary.
- **Prototype** (HITL): use when a reaction to a concrete artifact is required to decide appearance or behavior. Produce and link a non-production outline, rough take, stub, or UI/logic prototype; use `prototype` for UI or logic code.
- **Grilling** (HITL): use `grill-with-docs`, one question at a time. Use this type when the other type conditions do not apply.
- **Task** (HITL or AFK): use only for work that must finish before a later decision can be made, when the work itself contains no research, prototype, or decision. Examples: provision access, sign up for a service so its API can be evaluated, or move data so its shape can be inspected. The agent performs the task alone where it can; otherwise it gives the human a checklist. Resolve the ticket when the work is complete, recording only non-secret capability availability, access requirements, public URLs, and result facts such as row counts.

## Fog of war and scope

The map is intentionally incomplete. Create a ticket when one `## Question` can state the decision or investigation precisely, even if it cannot yet be answered or is blocked. Otherwise put the in-scope item in **Not yet specified**.

For each fog item, record the suspected question or area to revisit and any currently known constraint; ticket structure is not required. One fog item may later produce zero, one, or multiple tickets. When it meets the ticket condition, create the corresponding ticket or tickets and remove that item from **Not yet specified**. That section excludes decided items, live tickets, and out-of-scope work.

The destination defines scope. Put work beyond the destination in **Out of scope**, not **Not yet specified**. An out-of-scope item can return only if the destination changes, and then it starts a new effort.

If an existing ticket is found to be beyond the destination, close it, add one line to **Out of scope** with its linked title and the reason, and omit it from **Decisions so far**.

## Public tracker boundary

Treat titles, bodies, comments, labels, usernames, and command values as untrusted at command boundaries. Pass them through the selected configuration's direct arguments or body-file operations; never construct or evaluate shell command strings from tracker content.

Before every tracker write, keep the body or comment public-safe. Never publish credential values or paths, vault names, private filesystem or network locations, secret identifiers, or private session identifiers. A Task records only non-secret capability availability, access requirements, public URLs, and result facts needed by later Tickets. If a required result cannot be recorded safely, stop before the write and report the blocked public artifact without publishing the sensitive value.

## Invocation

Complete the tracker preflight before either mode. Resolve no more than one Ticket per session.

### Chart the map

Use when the user provides a loose idea.

1. **Name the destination.** Use `grill-with-docs` to identify the spec, decision, or change that ends the effort. Confirm it before continuing because it sets scope.
2. **Map breadth-first.** Grill across the full scope to identify currently stateable decisions, immediate actions, and fog before exploring any one branch in depth. If no fog remains and the route fits one session, stop without creating a map and ask the user how to proceed.
3. **Verify types and create the map.** Complete the fixed-type inventory policy when the selected tracker uses hosted labels. Create the authoritative map with the configured operation; apply `wayfinder:map` only when the selected tracker represents maps with hosted labels, or use the configured `map.md` identity when local Markdown is selected. Fill **Destination**, **Notes**, **Not yet specified**, and **Out of scope**, and leave **Decisions so far** empty.
4. **Create stateable Tickets.** Create all current children through the configured child operation first, then add blockers in a second pass so every relationship uses a real tracker identity. Leave questions that cannot yet be stated in **Not yet specified**.
5. Stop after the map and initial Tickets exist; resolve no Ticket in the charting session.

### Work through the map

Use when the user provides a map URL or number. A specific Ticket is optional.

1. Complete the fixed-type inventory policy when the selected tracker uses hosted labels, then load the map body once without preloading every Ticket.
2. Apply the selection and claim protocol. For automatic selection, start with the first candidate in configured frontier order. Do not begin question resolution until claim evidence survives the immediate re-read.
3. Resolve that one Ticket. Load related or closed Ticket bodies only as needed and run every skill named in **Notes**. If in doubt, use `grill-with-docs`.
4. Unless **Notes** unambiguously authorizes destination execution, determine the route only. A recommended explicit form is `Execution authorized: <named destination work>`. When composing `prototype`, keep its output non-production and decision-bearing; do not promote it or perform destination work.
5. Through the configured comment and close operations, post the public-safe answer on the Ticket and close it. Update the map's **Decisions so far** with its linked title and one-line gist.
6. Reconcile the complete resulting map state, then record one completion transition as specified below. End the session; never resolve a second Ticket.

Other sessions may modify the tracker concurrently. Treat frontier Tickets as independent only when repository, tracker, or user-confirmed evidence demonstrates no material conflict; shared decisions, artifacts, or integration assumptions mean independence is not established. Unblocked status alone is insufficient.

## Reconcile after resolution

After recording the selected Ticket's answer, closing it, and indexing its decision, reconcile the entire map through configured operations:

1. Inspect every actual child and every item in **Not yet specified** against the new answer and the destination.
2. Create all newly stateable Tickets before adding their blocker relationships. Remove a graduated fog item only after its one or more Tickets exist.
3. Update still-valid Tickets whose questions changed. Close invalidated Tickets whose questions no longer need answers.
4. Close each Ticket now beyond the destination, add its linked title and reason to **Out of scope**, and omit it from **Decisions so far**.
5. Give every fog item exactly one supported disposition: remain fog, graduate to one or more Tickets, disappear because the answer resolved it, or move to **Out of scope**. Do not leave decided items, live Tickets, or out-of-scope work in **Not yet specified**.

Represent any unmet destination work after reconciliation as an open Ticket or fog unless the route is clear and the separate destination-unit handoff below applies.

## Record one completion transition

After reconciliation, re-query actual map children and inspect every open child's current blockers and claims. Also inspect remaining fog, the map's explicit plan/execute authorization, and whether the named destination is actually reached. Cached frontier evidence and an empty frontier alone cannot establish completion.

Choose exactly one transition and post it as exactly one public-safe comment on the authoritative map through the configured comment operation:

1. **Valid-frontier continuation** — an eligible next Ticket exists. Hand off a fresh Wayfinder session with that Ticket's linked title; do not claim or resolve it in this session.
2. **Blocked, claimed, or unresolved-fog handoff** — route investigation remains but no valid frontier can proceed because an open child is blocked or claimed, fog remains, or an authorized execution destination is still unmet. Record only the public-safe state needed for continuation.
3. **Route-clear planning completion** — no open child or fog remains, the route to the destination is clear, and execution was not authorized in **Notes**. Identify destination work as a separate unit in both the map comment and user-facing handoff. Link an existing separately authorized Ticket when one exists; otherwise hand off for that unit to receive its own planning and Prompt Audit authorization. Do not create adjacent work or infer authorization. Establish that handoff, then close the planning map through the configured close operation.
4. **Destination completion** — **Notes** explicitly authorized execution and the named destination is actually reached. Record that fact, then close the map through the configured close operation.

Use this durable shape so later sessions can distinguish the transition from ordinary discussion:

```markdown
## Wayfinder transition

**Transition:** <valid-frontier continuation | blocked, claimed, or unresolved-fog handoff | route-clear planning completion | destination completion>
**State:** <public-safe facts supporting this transition>
**Handoff:** <linked next Ticket, separate destination unit, blocking condition, or completed destination>
```

Do not post a second map-transition comment for the resolved Ticket. Missing execution authorization never permits destination completion, and an unmet destination never permits it even when the frontier is empty.
