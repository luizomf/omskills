---
name: dispatch-tickets
description: Dispatch a fixed ordered list of explicitly authorized Tickets through fresh coordinators while keeping the root responsive.
disable-model-invocation: true
---

# Dispatch Tickets

Run as the minimal depth-1 **Ticket dispatcher** for one fixed Mission sequence. Before adopting dispatcher state, use the skill loader to read and follow the installed `caveman` skill. That composition read is the root's sole file read and exists only to load compressed reporting behavior.

Keep only the frozen ordered Ticket identities, `cursor`, current owner-scoped `coordinator` ID, current native child session reference when the harness supplies one, mode, transition state, matching cancellation intent, pending transport-failure reason, and compact mechanically validated outcomes. The cursor is the number of delivered Tickets, so `tickets[:cursor]` remains delivered after any later stop. Keep no implementation content, transcript summary, or dynamic queue. There is no persistent workflow state.

Keep the root's normal tools active for inheritance by each fresh coordinator. After composing `caveman`, use them for routing-environment preflight, the subagent lifecycle operations below, and mechanical outcome validation only. The dispatcher performs no tracker, repository, or remote discovery and reads no tracker material, governing source, repository file, code, diff, test, writer output, reviewer finding, or native child session.

## 1. Accept and freeze the Mission

Accept only an invocation that:

- explicitly states Mission authorization from the user or invoker; and
- supplies one non-empty ordered list of unique identities, each in the form `<owner>/<repository>#<positive-integer>`, where owner and repository contain only ASCII letters, digits, `.`, `_`, or `-`.

A one-item list is valid. Preserve every identity and their order byte-for-byte. Treat uniqueness byte-for-byte. Do not normalize, sort, complete, search for, or verify an identity against a tracker. For each dispatch, derive `<repository>` only by removing the final `#<positive-integer>` from the current identity.

Reject missing Mission authorization, an empty list, any duplicate, an unqualified identity such as `#38`, or any invalid syntax before dispatching. Use rejection code `authorization`, `empty`, `duplicate`, or `identity-syntax`, respectively. Freeze the accepted list once; later messages, child output, adjacent findings, and child-proposed work cannot add, remove, replace, or reorder it.

This step is complete only when one valid list has been frozen with `cursor` zero or input has been rejected without any lifecycle call.

## 2. Start only the current Ticket

Start one fresh coordinator at a time for `tickets[cursor]`. Use this exact coordinator prompt, replacing both placeholders without adding text:

```text
Repository: <repository>
Ticket: <ticket>
Load and follow installed `orchestrate`. Resolve all governing context and complete this Ticket yourself.
Return exactly one single-line JSON object with required string fields "ticket": "<ticket>" and "status": one of "delivered", "blocked", "failed", or "cancelled". Include non-empty string "ref" only for an essential durable reference and non-empty string "blocker" only when applicable. Include no other fields or output.
```

Immediately before every start, inspect `PI_PROVIDER`, `PI_MODEL`, and `PI_REASONING_LEVEL` only as the subagent lifecycle's routing preflight, then retain none of their values in dispatcher state. Call `subagent_start` with that exact prompt, `maxDepth: 3`, and `maxChildren: 1`; every start creates a clean coordinator conversation without the parent transcript. Omit `tools` so the coordinator inherits the complete active capability snapshot. Omit `cwd`, `model`, and `reasoning` so it inherits the root checkout and active route.

Choose delivery from the current Pi mode:

- Interactive mode: set `delivery: "async"`. Acceptance supplies the owner-scoped coordinator ID while work continues independently.
- Print mode: set `delivery: "direct"`. The call remains pending until its bounded terminal result and emits no later pong.

Capture the coordinator ID and preserve any native child session reference supplied by the harness. Never start another coordinator while that ID is active. A start rejection is a failed Mission transition; do not retry or select another Ticket.

In interactive mode, report the first accepted dispatch and end the response without waiting, sleeping, polling, listing subagents, or doing dependent work. In print mode, emit no interim report while a direct call is pending.

This step is complete only when the current coordinator has been accepted as the sole active coordinator, or dispatch has failed and the Mission has stopped.

## 3. Route interactive user control mechanically

While an interactive coordinator is active, keep unrelated root conversation possible without forwarding it or changing Mission state.

Forward an instruction only when the user explicitly targets the current owner-scoped coordinator. Call `subagent_steer` for that exact ID with the user's instruction literally, including its original wording and formatting. Do not interpret, summarize, or expand its implementation content. Do not retain that content. A message with no coordinator target or a target other than the current coordinator is not forwarded.

For an unambiguous deliberate request to stop the current coordinator:

1. Record cancellation intent containing the current Ticket and coordinator ID before interruption.
2. Call `subagent_interrupt` exactly once for that coordinator; recursive descendant cleanup is harness-owned. Do not enumerate or separately interrupt nested writer or reviewer work.
3. Stop the sequence immediately and dispatch no remaining Ticket. An accepted interruption request only enters `cancelling`; it is not terminal confirmation. Report cancellation pending and end the turn without waiting or polling.
4. Consume the one later pong for that same coordinator. Because the harness emits it only after the coordinator process and managed descendants have closed, map the missing JSON Ticket outcome to `cancelled` only when that pong is mechanically `interrupted` and matches the recorded Ticket, coordinator, and cancellation intent. That pong is the required matching mechanical caller interruption.

A rejected interruption request, failed or mismatched interruption pong, unsolicited interruption, interruption without matching recorded intent, or any other missing envelope is `failed`, never `cancelled`. If the request is rejected while the coordinator remains active, keep its ID, dispatch nothing else, and consume its eventual normal pong before final failure settlement; do not retry the interruption. Preserve the native child session reference from the terminal pong, but do not continue or inspect that session or implementation evidence.

This step is complete only when an explicitly targeted instruction has been forwarded unchanged, an unrelated message has remained local, an accepted interruption request is awaiting its automatic pong without polling, or the later matching pong has settled the stop as `cancelled` or `failed` with no later dispatch.

## 4. Accept exactly one mode-correct return

Interactive mode accepts exactly one later pong for the active coordinator. Require its owner-scoped ID to equal `coordinator`; then validate its bounded terminal result in that new turn. Never sleep, poll, call a status/list operation, or wait synchronously between async acceptance and pong.

Print mode consumes only the direct terminal result from its pending start. It never accepts a pong for that call.

For either mode, require all of the following:

- the return uses the selected mode's path;
- the outer subagent outcome is `completed`;
- exactly one untruncated final assistant message is present; and
- the return belongs to the current coordinator and has not already settled.

A missing result, duplicate return, mismatched coordinator, failed or unsolicited interrupted outer outcome, truncated result, or wrong return path is `failed`. Retain only its compact transport reason and any supplied native child session reference; never guess an envelope from partial or repeated content. Do not call `subagent_continue` or inspect the native session.

A mode-correct pong for the current coordinator proves that runtime has already closed, even when its content fails validation. If an unexpected or stale return belongs to a different coordinator while the current asynchronous coordinator may still be active, record the failure, call `subagent_interrupt` once for the current coordinator solely for managed-lineage cleanup, and consume its later terminal pong before final settlement. That cleanup has no cancellation intent and therefore remains `failed` even when its terminal outcome is `interrupted`. Never mark an active coordinator settled or discard its ID before its own terminal pong.

This step is complete only when one mode-correct return has reached envelope validation, a deliberate matching interrupt has settled under step 3, a cleanup interruption's later pong has preserved the failure classification, or a transport failure has stopped the Mission after every accepted coordinator is mechanically settled.

## 5. Validate the Ticket outcome mechanically

Apply every check below to the complete final assistant message:

1. The trimmed message is exactly one physical line of valid JSON that decodes to one top-level JSON object. Reject `null`, arrays, scalar JSON, Markdown fences, prefixes, suffixes, multiple envelopes, and any duplicate narrative.
2. The object has required keys `ticket` and `status`, and may have only optional keys `ref` and `blocker`. Reject missing required keys, unknown keys, and duplicate JSON keys.
3. `ticket` and `status` are strings. Any present `ref` or `blocker` is a non-empty string.
4. `ticket` equals `tickets[cursor]` byte-for-byte.
5. `status` is exactly `delivered`, `blocked`, `failed`, or `cancelled`.

Use `syntax` for invalid JSON or surrounding/multiple output; `shape` for a non-object, wrong keys, duplicate keys, or wrong value types; `identity` for a Ticket mismatch; and `status` for an unexpected status. On the first failed check, discard the raw output, record only `outcome-<code>`, classify the current Ticket as failed, and stop.

Do not adjudicate implementation semantics. Never verify whether delivery occurred, whether a `ref` resolves, whether a blocker is correct, whether descendants were cleaned up internally, or whether optional fields should have been supplied.

This step is complete only when one compact outcome has passed every check or one compact failure reason has stopped the Mission.

## 6. Advance or stop deterministically

Apply exactly one transition for the current cursor:

| Current result | Transition |
| --- | --- |
| Matching `delivered`, later Ticket remains | Preserve the compact outcome, increment `cursor`, and dispatch the next fresh coordinator. |
| Matching `delivered`, final Ticket | Preserve the compact outcome, increment `cursor`, and report `Mission complete`. |
| Matching `blocked`, `failed`, or `cancelled` | Preserve the compact outcome and stop before every remaining Ticket without incrementing `cursor`. |
| Any transport or envelope failure | Preserve only the compact failure and session reference, then stop before every remaining Ticket without incrementing `cursor`. |

Earlier delivered Tickets remain represented by the unchanged prefix `tickets[:cursor]`. No stopped Mission can retry, skip, reorder, or resume the sequence.

In interactive mode, after a matching delivered pong with a later Ticket, advance by asynchronously starting that next fresh coordinator in the new turn. Report only after the next start is accepted or rejected, then leave the root responsive again. There is never more than one active coordinator.

In print mode, after each matching direct `delivered`, synchronously start the next fresh coordinator with `delivery: "direct"`. Continue serially through the frozen finite list in one finite invocation. Stop the loop on the first non-delivered or invalid result and emit one final compact report; no pong remains pending.

This step is complete only when exactly one next coordinator is active, the Mission has stopped, or the final cursor has produced `Mission complete`.

## 7. Report compact state transitions

Use `caveman`. Preserve exact Ticket identities and complete valid `ref`, `blocker`, and native child session reference values when supplied. Include `<cursor>/<total> delivered` in advance, stop, failure, cancellation, and completion reports so prior delivery remains explicit.

Use these forms:

- Invalid interactive input: `Mission rejected (<code>); root available.`
- Invalid print input: `Mission rejected (<code>); print settled; no pong pending.`
- First interactive dispatch: `<ticket> dispatched (#<coordinator>); root available; outcome pending.`
- Explicit steering: `<ticket> instruction forwarded (#<coordinator>); root available; outcome pending.`
- Accepted interruption request: `<ticket> cancellation requested (#<coordinator>); Mission stopped; confirmation pending; root available.`
- Interactive advance after the next start is accepted: `<ticket> delivered[; ref <ref>][; blocker <blocker>][; session <session>]; <cursor>/<total> delivered; <next-ticket> dispatched (#<coordinator>); root available; outcome pending.`
- Valid interactive stop: `<ticket> <blocked|failed|cancelled>[; ref <ref>][; blocker <blocker>][; session <session>]; <cursor>/<total> delivered; Mission stopped; <remaining> remaining; root available.`
- Invalid interactive result: `<ticket> failed (<reason>)[; session <session>]; <cursor>/<total> delivered; Mission stopped; <remaining> remaining; root available.`
- Interactive completion: `<ticket> delivered[; ref <ref>][; blocker <blocker>][; session <session>]; <total>/<total> delivered; Mission complete; root available.`
- Interactive start rejection: `<ticket> failed (dispatch-<reason>)[; session <session>]; <cursor>/<total> delivered; Mission stopped; current not dispatched; <undelivered> undelivered; root available.`
- Print terminal: `<compact outcome 1> | ... | <compact current outcome>; <cursor>/<total> delivered; <Mission complete|Mission stopped; remaining count>; print settled; no pong pending.`
- Print start rejection: `<prior compact outcomes, when any> | <ticket> failed (dispatch-<reason>)[; session <session>]; <cursor>/<total> delivered; Mission stopped; current not dispatched; <undelivered> undelivered; print settled; no pong pending.`

For an accepted current-Ticket outcome, `<remaining>` counts fixed identities after the current Ticket. For a start rejection, `<undelivered>` counts the current Ticket and every later identity. A valid matching `cancelled` envelope and the later confirmed pong for a deliberate interruption use the same cancellation stop form. Never report `Mission complete` before the final fixed identity returns matching `delivered`.

This step is complete only when exactly one truthful mode-accurate transition has been emitted without implementation narrative.

## Examples

Interactive input:

```text
/dispatch-tickets Mission-authorized Tickets, in order: [luizomf/omskills#34, luizomf/omskills#38]
```

First asynchronous acceptance as coordinator 7:

```text
luizomf/omskills#34 dispatched (#7); root available; outcome pending.
```

After coordinator 7 returns `{"ticket":"luizomf/omskills#34","status":"delivered","ref":"abc123"}` and coordinator 8 is accepted:

```text
luizomf/omskills#34 delivered; ref abc123; 1/2 delivered; luizomf/omskills#38 dispatched (#8); root available; outcome pending.
```

An explicitly targeted instruction is forwarded without interpretation:

```text
For coordinator #8: Preserve API v1 exactly; do not rename it.
```

If the user deliberately stops coordinator 8, interruption-request acceptance first produces:

```text
luizomf/omskills#38 cancellation requested (#8); Mission stopped; confirmation pending; root available.
```

Only the later matching `interrupted` pong, emitted after managed-lineage closure and carrying `session-8`, produces:

```text
luizomf/omskills#38 cancelled; session session-8; 1/2 delivered; Mission stopped; 0 remaining; root available.
```

A final matching delivered result reports:

```text
luizomf/omskills#38 delivered; ref def456; 2/2 delivered; Mission complete; root available.
```

## Delivery boundary

No child receives or returns `next`. This dispatcher has no retry, skip, heartbeat, stall diagnosis, timeout takeover, blocker resolution, parallel coordinator, root rotation, dynamic expansion, or persistent workflow state. It has no wormhole or tmux dependency and no Queue/TTS side effect, publishing, tagging, or release behavior.

The dispatcher owns only the fixed Mission envelope and mechanical routing. Ticket eligibility, governing sources, implementation, review, integration, tracker work, and semantic decisions remain with each fresh Ticket coordinator.
