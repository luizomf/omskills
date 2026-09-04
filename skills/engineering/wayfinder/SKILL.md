---
name: wayfinder
description: Plan work that exceeds one agent session as a shared map of investigation tickets, then resolve one ticket per session until the route to the destination is clear.
---

# Wayfinder

Use a **shared map** to determine the route from a loose idea to a named **destination**. The destination may be a spec, a decision required before planning, or an in-place change such as a data-structure migration. The map may cover engineering, course content, or another domain.

## Plan by default

Unless the map's **Notes** explicitly include execution, each ticket resolves a decision and produces no destination deliverable. The map is complete when no decision remains before execution. When resolving the next ticket would perform the destination work rather than determine how to perform it, hand off instead. A mapped or ready Ticket is not Mission-authorized until the user or invoker explicitly selects it.

## Refer to issues by title

In narration and the map's **Decisions so far**, refer to every map and ticket by its linked title. Do not use a bare id, number, or slug as its human-readable name; retain the id or URL in the title's link.

## Map structure

The map is the authoritative issue for the effort in the configured tracker, labelled `wayfinder:map`. Its tickets are child issues.

The map indexes decisions; each decision's detail exists only in its ticket. **Decisions so far** contains a one-line gist and link.

Tracker storage, child relationships, blocking, and frontier queries are tracker-specific. Read the configured issue tracker's "Wayfinding operations" section. If configuration is missing during an interactive invocation, run `setup-omskills` and wait for its confirmed output; if the approved configuration selects local markdown, use it. During a headless Ticket run, return a missing-setup blocker to the Ticket coordinator instead and never route setup through a Ticket dispatcher.

### Map body

Load this low-resolution view once per session. Find open tickets by querying child issues; include a child index in the map body only when the configured tracker requires it as the relationship fallback.

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
- contains a single tracked resolution target sized for one fresh agent session;
- has exactly one `wayfinder:<type>` label: `research`, `prototype`, `grilling`, or `task`;
- records its answer in a resolution comment rather than the body; and
- links assets created during resolution instead of pasting them into the body.

```markdown
## Question

<the decision or investigation this ticket resolves>
```

The `## Question` field states the tracked Ticket's resolution target; it is not a conversational **Question**. A `wayfinder:grilling` Ticket may need several Question rounds to resolve that single target.

An open, unassigned ticket is unclaimed; assigning it to the developer driving the map claims it. Concurrent sessions skip claimed tickets.

Use the tracker's native dependency relationship for blocking. Use a body convention only when the tracker has no native blocking relation. A ticket is **unblocked** when every ticket blocking it is closed. The **frontier** is the set of open, unblocked, unclaimed child tickets.

## Ticket types

Every ticket is either **HITL** (requires live input from a human speaking for themselves) or **AFK** (the agent can resolve it without live human input). An agent must not supply the human side of a HITL exchange.

- **Research** (AFK): use when resolving the question requires knowledge outside the current working directory, such as external documentation, third-party APIs, or a local knowledge base. Produce and link a Markdown summary.
- **Prototype** (HITL): use when a reaction to a concrete artifact is required to decide appearance or behavior. Produce and link a non-production outline, rough take, stub, or UI/logic prototype; use `prototype` for UI or logic code. The ticket resolves the design question only; promoting any result requires a separate implementation Ticket.
- **Grilling** (HITL): use `grill-with-docs` and its bounded Question-frontier rounds. Keep every round inside the selected Ticket; several rounds may resolve that one Ticket, but no round may include Questions for another Ticket. Use this type when the other type conditions do not apply.
- **Task** (HITL or AFK): use only for work that must finish before a later decision can be made, when the work itself contains no research, prototype, or decision. Examples: provision access, sign up for a service so its API can be evaluated, or move data so its shape can be inspected. The agent performs the task alone where it can; otherwise it gives the human a checklist. Resolve the ticket when the work is complete, recording what changed and any facts later tickets require, such as credential location, URLs, or row counts.

## Fog of war and scope

The map is intentionally incomplete. Create a ticket when its `## Question` can state the decision or investigation precisely, even if it cannot yet be answered or is blocked. Otherwise put the in-scope item in **Not yet specified**.

For each fog item, record the suspected question or area to revisit and any currently known constraint; ticket structure is not required. One fog item may later produce zero, one, or multiple tickets. When it meets the ticket condition, create the corresponding ticket or tickets and remove that item from **Not yet specified**. That section excludes decided items, live tickets, and out-of-scope work.

The destination defines scope. Put work beyond the destination in **Out of scope**, not **Not yet specified**. An out-of-scope item can return only if the destination changes, and then it starts a new effort.

If an existing ticket is found to be beyond the destination, close it, add one line to **Out of scope** with its linked title and the reason, and omit it from **Decisions so far**.

## Invocation

Use one of the following modes. In either mode, resolve no more than one Ticket per session. Question rounds used while charting stay inside the one active map request; rounds used while working through a map stay inside the one selected Ticket and never combine separate Tickets.

### Chart the map

Use when the user provides a loose idea.

1. **Name the destination.** Use `grill-with-docs` to identify the spec, decision, or change that ends the effort. Confirm it before continuing because it sets scope.
2. **Map breadth-first.** Grill across the full scope to identify currently stateable decisions, immediate actions, and fog before exploring any one branch in depth. If no fog remains and the route fits one session, stop without creating a map and ask the user how to proceed.
3. **Create the map.** Apply `wayfinder:map`; fill **Destination**, **Notes**, **Not yet specified**, and **Out of scope**; leave **Decisions so far** empty.
4. **Create stateable tickets.** Create all current child tickets first, then add blocking relationships in a second pass so every relationship can use a real issue id. Leave questions that cannot yet be stated in **Not yet specified**.
5. Stop after the map and initial tickets exist; resolve no ticket in the charting session.

### Work through the map

Use when the user provides a map URL or number. A specific ticket is optional.

1. Load the map body without preloading every ticket.
2. If the user named a ticket, select it. Otherwise select the first ticket in frontier order. Assign it to the developer driving the map before any other work.
3. Resolve only that Ticket, including as many Question rounds as it needs. Do not select or resume another Ticket in this session. Load related or closed Ticket bodies only as needed and run every skill named in **Notes**. If in doubt, use `grill-with-docs`.
4. Post the answer as a resolution comment, close the ticket, and append its linked title plus a one-line gist to **Decisions so far**.
5. Create newly stateable tickets before adding their blocking relationships. Remove each graduated fog item from **Not yet specified**. Close and record out-of-scope tickets as specified above. Update or delete tickets invalidated by the resolution.

Other sessions may modify the tracker concurrently. Treat frontier tickets as independent only when repository, tracker, or user-confirmed evidence demonstrates no material conflict; shared decisions, artifacts, or integration assumptions indicate that independence has not been established. Unblocked status alone is insufficient.
