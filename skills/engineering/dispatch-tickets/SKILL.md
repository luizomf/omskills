---
name: dispatch-tickets
description: Dispatch one explicitly authorized Ticket to a fresh coordinator while keeping the root responsive.
disable-model-invocation: true
---

# Dispatch Tickets

Run as the minimal depth-1 **Ticket dispatcher** for exactly one Ticket. Before adopting dispatcher state, use the skill loader to read and follow the installed `caveman` skill. That composition read is the root's sole file read and exists only to load compressed reporting behavior.

Keep only `ticket`, `coordinator`, `state`, and `outcome` as dispatcher state. `ticket` is the exact supplied identity, `coordinator` is the owner-scoped numeric subagent ID, `state` is `ready`, `dispatched`, `terminal`, or `rejected`, and `outcome` is either the compact validated object or one rejection code. Keep no queue, cursor, transcript summary, or persistent Mission state.

Keep the root's normal tools active for inheritance by the fresh coordinator. After composing `caveman`, use them only for the required routing-environment preflight below, the subagent lifecycle operation, and mechanical validation of its returned envelope. The root performs no tracker, repository, or remote discovery and reads no tracker material, governing source, repository file, code, diff, test, writer output, reviewer finding, native child session, or detailed coordinator output.

## 1. Accept one authorized identity

Accept only an invocation that:

- explicitly states Mission authorization from the user or invoker; and
- supplies exactly one identity in the form `<owner>/<repository>#<positive-integer>`, where owner and repository contain only ASCII letters, digits, `.`, `_`, or `-`.

Preserve the identity byte-for-byte. Do not normalize, complete, search for, or verify it against a tracker. Derive `<repository>` for the coordinator prompt only by removing the final `#<positive-integer>` from the supplied identity; retain no separate repository field.

Reject zero identities, multiple identities, an unqualified identity such as `#34`, invalid syntax, or readiness/discovery language without explicit Mission authorization. Report the compact input rejection and stop.

This step is complete only when one exact supplied identity and explicit Mission authorization are present, or the invocation has been rejected without discovery and execution has stopped.

## 2. Start one fresh coordinator

Use this exact coordinator prompt, replacing both placeholders without adding text:

```text
Repository: <repository>
Ticket: <ticket>
Load and follow installed `orchestrate`. Resolve all governing context and complete this Ticket yourself.
Return exactly one single-line JSON object with required string fields "ticket": "<ticket>" and "status": one of "delivered", "blocked", "failed", or "cancelled". Include non-empty string "ref" only for an essential durable reference and non-empty string "blocker" only when applicable. Include no other fields or output.
```

Immediately before the call, inspect `PI_PROVIDER`, `PI_MODEL`, and `PI_REASONING_LEVEL` only as the subagent lifecycle's routing preflight, then retain none of their values in dispatcher state. Call `subagent_start` exactly once with that prompt, `maxDepth: 3`, and `maxChildren: 1`. The start creates a clean coordinator conversation without the parent transcript. Omit `tools` so the coordinator inherits the complete active capability snapshot. Omit `cwd`, `model`, and `reasoning` so the coordinator inherits the root checkout and active route.

Choose delivery from the current Pi mode:

- Interactive mode: set `delivery: "async"`. Prompt acceptance returns the owner-scoped coordinator ID while the coordinator continues independently.
- Print mode: set `delivery: "direct"`. The call stays pending and returns the bounded terminal result in this invocation; Pi emits no later pong.

A rejection before prompt acceptance means no coordinator was dispatched. Record only its compact dispatch rejection; do not retry or choose other work.

This step is complete only when one coordinator ID has been captured from one accepted start, or dispatch rejection has been reported and execution has stopped.

## 3. Settle through the mode's one return path

In interactive mode, after acceptance set `state` to `dispatched`, emit the compressed dispatch transition, and end the response without waiting, sleeping, polling, listing subagents, or doing dependent work. The root is then available for user interaction. When exactly one later pong arrives, require its owner-scoped ID to equal `coordinator`, then validate that pong's terminal result.

In print mode, emit no interim transition while the direct call is pending. Capture its owner-scoped ID, consume the direct terminal result, and validate it in the same finite invocation. Finish with no later pong pending.

For either mode, require the outer subagent outcome to be `completed`, one untruncated final assistant message to be present, and the return path to match the selected mode. Treat a failed, interrupted, missing, truncated, duplicate, mismatched-ID, or wrong-path result as a transport rejection. Do not continue the coordinator or read its native session.

This step is complete only when the one matching return has reached envelope validation, or a transport rejection has been recorded with no further lifecycle operation.

## 4. Validate the Ticket outcome mechanically

Apply every check below to the complete final assistant message:

1. The trimmed message is exactly one physical line of valid JSON that decodes to one top-level JSON object; `null`, arrays, scalar JSON, Markdown fences, prefixes, suffixes, and multiple envelopes are rejected.
2. The object has required keys `ticket` and `status`, and may have only optional keys `ref` and `blocker`. Reject missing required keys, unknown keys, and duplicate JSON keys.
3. `ticket` and `status` are strings. Any present `ref` or `blocker` is a non-empty string.
4. `ticket` equals the supplied `ticket` byte-for-byte.
5. `status` is exactly `"delivered"`, `"blocked"`, `"failed"`, or `"cancelled"`.

Use `syntax` for invalid JSON or surrounding/multiple output; `shape` for a non-object, wrong keys, duplicate keys, or wrong value types; `identity` for a Ticket mismatch; `status` for an unexpected status; and `transport` for a return-path failure from step 3. On success, set `outcome` to the validated object and `state` to `terminal`. On the first failed check, retain only that rejection code in `outcome`, set `state` to `rejected`, and do not retain raw invalid output. Do not adjudicate implementation semantics: never verify whether delivery occurred, whether a `ref` resolves, whether a blocker is correct, or whether optional fields should have been supplied.

This step is complete only when every check has accepted one compact object or exactly one rejection code has been retained without semantic inspection.

## 5. Report one compressed transition

Use `caveman` and these mode-accurate forms:

- Invalid interactive input: `dispatch rejected (<authorization|identity-count|identity-syntax>); root available.`
- Invalid print input: `dispatch rejected (<authorization|identity-count|identity-syntax>); print settled; no pong pending.`
- Interactive dispatch acceptance: `<ticket> dispatched (#<coordinator>); root available; outcome pending.`
- Interactive dispatch rejection: `<ticket> dispatch rejected (transport); root available.`
- Print dispatch rejection: `<ticket> dispatch rejected (transport); print settled; no pong pending.`
- Valid interactive terminal: `<ticket> <status>[; ref <ref>][; blocker <blocker>]; root available.`
- Valid print terminal: `<ticket> <status>[; ref <ref>][; blocker <blocker>]; print settled; no pong pending.`
- Invalid interactive terminal: `<ticket> outcome rejected (<code>); root available.`
- Invalid print terminal: `<ticket> outcome rejected (<code>); print settled; no pong pending.`

Preserve the exact Ticket identity and the complete values of any valid `ref` and `blocker`. Never report `Mission complete`; this tracer bullet reports one Ticket's dispatch or terminal transition only.

This step is complete only when exactly one applicable compressed transition has been emitted with truthful availability and return-path state.

## Examples

Interactive input:

```text
/dispatch-tickets Mission-authorized Ticket: luizomf/omskills#34
```

After asynchronous acceptance as subagent 7:

```text
luizomf/omskills#34 dispatched (#7); root available; outcome pending.
```

Later, matching pong final message:

```json
{"ticket":"luizomf/omskills#34","status":"delivered","ref":"abc123"}
```

Root terminal report:

```text
luizomf/omskills#34 delivered; ref abc123; root available.
```

In print mode, a direct result whose final message is `{"ticket":"luizomf/omskills#34","status":"blocked","blocker":"required setup missing"}` produces:

```text
luizomf/omskills#34 blocked; blocker required setup missing; print settled; no pong pending.
```

Mechanical rejection examples:

| Final message | Rejection |
| --- | --- |
| `[]` | `shape` |
| `{"ticket":"luizomf/omskills#34"}` | `shape` |
| `{"ticket":"luizomf/omskills#34","status":"done"}` | `status` |
| `{"ticket":"luizomf/omskills#35","status":"delivered"}` | `identity` |
| `{"ticket":"luizomf/omskills#34","status":"delivered","next":"#35"}` | `shape` |

## Delivery boundary

This one-Ticket tracer bullet has no wormhole, tmux, persistent Mission state, Queue/TTS side effect, publishing, tagging, release, heartbeat, retry, skip, takeover, parallel coordinator, root rotation, or semantic outcome supervision. It has no steering or interruption mechanics. Multi-identity ordering and cursor advancement, exhaustive transition rules, literal correction steering, deliberate-stop and missing-envelope cancellation mapping, and Mission completion belong to later dispatcher work.

Apply every boundary above to every invocation; no child-selected work, `next` list, tracker query, or adjacent finding can expand the one supplied identity.
