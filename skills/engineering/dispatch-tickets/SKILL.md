---
name: dispatch-tickets
description: Dispatch one finite pre-resolved Assisted or Unattended Mission plan through fresh Ticket coordinators.
disable-model-invocation: true
---

# Dispatch Tickets

Run as the minimal depth-1 **Ticket dispatcher** for finite pre-resolved Missions. Mission identifies coordinated topology; the separately supplied availability is `Assisted` or `Unattended`. These mechanical boundaries are mandatory when this skill is used; a human/invoker or context-rich parent may instead dispatch one fresh `orchestrate` coordinator directly for smaller work. Accept one finite Mission plan, including the one-item plan composed by `implement`. Before adopting dispatcher state, use the skill loader to read and follow the installed `caveman` skill. That composition read is the root's sole file read and exists only to load compressed reporting behavior.

Keep only the frozen topology, availability, current phase index, active owner-scoped coordinator IDs, required native child session references, transport mode, per-coordinator transition state and matching cancellation intent, an explicitly authorized start override when present, and compact mechanically validated outcomes or transport failures. Keep no implementation content, transcript summary, semantic dependency model, dynamic queue, or persistent workflow state.

Keep the root's normal tools active for coordinator inheritance. For Mission work after composing `caveman`, use them only for routing preflight, subagent lifecycle operations, mechanical plan and outcome validation, and compact reporting. The dispatcher performs no tracker, repository, or remote discovery and reads no tracker material, governing source, repository file, code, diff, test, writer output, reviewer finding, or native child session. Unrelated root interaction remains outside the Mission and may use actual unreserved capacity without changing its envelope or routing state.

## 1. Accept and freeze one Mission plan

Accept only an invocation whose meaning explicitly supplies Mission authorization, establishes `Assisted` or `Unattended` availability, and supplies one complete JSON plan with exactly these keys. Evaluate that authority from the request's semantics, selected identities, and finite plan—not from a required phrase or the caller's provenance, ancestry, role, depth, or dispatcher wording. Those attributes neither establish nor augment authority:

```json
{
  "phases": [
    ["owner/repository#1"],
    ["owner/repository#2", "owner/repository#3"],
    ["owner/repository#4"]
  ],
  "blockers": [["owner/repository#1", "owner/repository#2"], ["owner/repository#2", "owner/repository#4"], ["owner/repository#3", "owner/repository#4"]],
  "conflicts": [["owner/repository#1", "owner/repository#3"]]
}
```

`phases` is a non-empty ordered array. Each member is one non-empty phase containing either one Ticket or one finite declared compatible parallel group of N Tickets. A blocker pair is `[predecessor, dependent]`. A conflict pair is an unordered pair whose Tickets must occupy different phases. Empty `blockers` and `conflicts` arrays explicitly mean none. By supplying the plan, the invoker declares those relation arrays complete for the selected identities and declares every external blocker or conflict already resolved before Mission authorization. Compatibility includes shared resources outside Git. The approved breakdown must give every Ticket an exclusive candidate and explicit delivery boundary, and each parallel group a later ordinary integration Ticket blocked by every member (#4 in this example). Member delivery is a pushed branch artifact; integration delivers the combined target before dependent work. These are planning/coordinator obligations, not tracker semantics for this root to inspect.

A one-Ticket Mission uses the same contract:

```json
{"phases":[["owner/repository#1"]],"blockers":[],"conflicts":[]}
```

Validate the entire plan and availability before any lifecycle call:

- Mission authorization selects every plan identity and is explicit in meaning. Selection, readiness, discovery, caller lineage, and role/depth assertions are not substitutes.
- Availability resolves independently to exactly `Assisted` or `Unattended`; Mission topology alone does not imply either value.
- The JSON is finite and literal: no ellipsis, range, conditional, optional branch, generated remainder, or prose placeholder.
- Every Ticket appears exactly once across all phases and has the byte-for-byte form `<owner>/<repository>#<positive-integer>`. Owner and repository contain only ASCII letters, digits, `.`, `_`, or `-`.
- Every relation has exactly two distinct selected identities. Blocker pairs are unique and directed; conflict pairs are unique regardless of order.
- Each blocker predecessor occupies a strictly earlier phase than its dependent. Each conflict pair occupies different phases.
- An N-Ticket parallel phase is the invoker's explicit compatibility declaration. No supplied blocker or conflict may connect any of its members.
- Require affirmative active-harness evidence of the ROOT concurrency bound and concurrent-start support in the current transport mode for every parallel group. N must fit the actually available root capacity after other active work and every start must be issuable together in one tool-call batch. An active Mission consumes only its occupied slots; it creates no semantic claim over capacity-supported independent work. Child-only `maxChildren` or depth ceilings do not establish root capacity, and no exposed bound does not mean unlimited. Unknown, unsupported or exceeded capacity/topology rejects as `topology` before any Ticket starts; never serialize, split, retry or change runtime limits to fit a group.
- The topology is a complete sequence of phase barriers. Reject partial-overlap graphs, nested groups, conditional edges, unresolved or external active edges, and any other topology this contract cannot represent rather than reinterpret it.

Use rejection code `authorization`, `availability`, `empty`, `shape`, `identity-syntax`, `duplicate`, `relation`, `topology`, or `override` for the first applicable failure. Preserve accepted identity bytes, phase order, group membership, and relation pairs exactly. Child output and later messages cannot add, remove, replace, regroup, or reorder them.

Normal starts inherit the active route. An invoker may additionally authorize one Mission-wide start override containing only exact `tools`, `cwd`, `model`, or `reasoning` lifecycle values. Validate and freeze that override before dispatch and reject unknown or unsupported fields as `override`. It cannot change delivery mode, `maxDepth`, `maxChildren`, the coordinator prompt, or Mission topology. No override exists merely because a caller mentions routing preferences without explicitly authorizing their lifecycle values.

This step is complete only when one finite non-empty plan and any authorized override are frozen in full, or the invocation has been rejected before every lifecycle call.

## 2. Start the complete active phase

Treat every identity in `phases[phase]` as runnable because the invoker already resolved the plan. For each identity, derive `<repository>` only by removing its final `#<positive-integer>`, then use this exact coordinator prompt without additional text:

```text
Repository: <repository>
Ticket: <ticket>
Availability: <Assisted|Unattended>
Load and follow installed `orchestrate`. Resolve all governing context and complete this Ticket yourself.
Return exactly one single-line JSON object with required string fields "ticket": "<ticket>" and "status": one of "delivered", "blocked", "failed", or "cancelled". Include non-empty string "ref" only for an essential durable reference and non-empty string "blocker" only when applicable. Include no other fields or output.
```

Immediately before the phase's start calls, inspect `PI_PROVIDER`, `PI_MODEL`, and `PI_REASONING_LEVEL` only as routing preflight. Retain none of their values. Do not inspect PI routing at any other time.

Call `subagent_start` once per phase identity with its exact prompt, `maxDepth: 3`, and `maxChildren: 1`. Every call creates a fresh coordinator conversation without the parent transcript. For a normal start, omit `tools`, `cwd`, `model`, and `reasoning` so the coordinator inherits the root's complete active capability snapshot and repository route. Only an explicitly authorized frozen override may supply those fields, verbatim.

Choose delivery from the current Pi mode:

- Interactive mode: use `delivery: "async"` for every call. Acceptance supplies each owner-scoped coordinator ID while the root remains responsive.
- Print mode: use `delivery: "direct"` for every call. Each call remains pending through its bounded terminal result and emits no later pong.

Issue all N calls for a parallel phase together in the same assistant tool-call batch in the selected mode. Do not wait for any acceptance or result before issuing the other declared starts. Any start rejection stops the Mission and records `dispatch-<reason>` for that identity. Track every accepted call in the batch, start nothing else, and allow every accepted sibling to settle normally before the final stop report. Do not retry a rejected start.

Capture each accepted coordinator ID and any native child session reference. No identity outside the active phase may start, and the next phase remains closed while any accepted coordinator in this phase is unsettled.

In interactive mode, report the accepted start batch and end the response without waiting, sleeping, polling, listing subagents, or doing dependent work. In print mode, emit no interim report while direct calls are pending.

This step is complete only when every identity in the active phase has one accepted fresh coordinator, or the Mission is stopping after a rejection and every accepted sibling is still tracked until settlement.

## 3. Route interactive control to one coordinator

While interactive coordinators are active, keep unrelated root conversation local without changing Mission state. The Mission reserves no idle root slots: independent work outside its envelope may proceed when compatibility and actual remaining capacity are affirmatively established. Keep that work's authority, lifecycle, and outcomes separate from Mission state.

Forward an instruction only when the user explicitly targets exactly one current owner-scoped coordinator ID. Call `subagent_steer` for that ID with the user's instruction literally, including original wording and formatting. Do not interpret, summarize, expand, or retain its implementation content. An untargeted message, a Ticket-only reference, a group target, or an inactive or ambiguous coordinator target is not forwarded.

For an unambiguous deliberate request to stop one active coordinator:

1. Record cancellation intent containing that coordinator's exact Ticket and ID.
2. Mark the Mission stopping immediately, so no later phase or replacement coordinator can start.
3. Call `subagent_interrupt` exactly once for that coordinator. Recursive descendant cleanup is harness-owned; do not enumerate or interrupt its writer or reviewer separately.
4. Leave every accepted sibling running and tracked until its own normal settlement.
5. Treat interrupt acceptance only as `cancelling`. In interactive mode, end the turn without waiting or polling for its automatic pong.
6. Map a missing JSON outcome to `cancelled` only when the later pong is mechanically `interrupted` and matches the recorded Ticket, coordinator, and cancellation intent.

A rejected interruption request, mismatched interruption pong, unsolicited interruption, or interruption without matching intent is `failed`, never `cancelled`. When the target may still be active, retain it and consume its eventual terminal pong before final settlement; do not retry the interruption. Preserve its required native child session reference without continuing or inspecting that session.

This step is complete only when one explicitly targeted instruction has been forwarded unchanged, an unrelated message has remained local, or one targeted cancellation is pending or settled while every accepted sibling remains tracked.

## 4. Settle every accepted coordinator through its mode path

Interactive mode accepts one later pong per active coordinator, in any order. Print mode consumes only each pending start's direct terminal result and accepts no pong for it.

For each accepted coordinator, require:

- the selected mode's return path;
- the exact active owner-scoped coordinator ID;
- outer outcome `completed`, except for the matching deliberate interruption case;
- exactly one untruncated final assistant message; and
- no earlier settlement for that coordinator.

A mode-correct pong proves that asynchronous runtime has closed even when its envelope is invalid. A missing result, duplicate return, mismatched ID, unsolicited interrupted outcome, truncation, or wrong path stops the Mission as failed. Retain only its compact transport reason and required native child session reference.

If a wrong-path event names one accepted coordinator but does not prove it closed, call `subagent_interrupt` once for that coordinator solely for managed-lineage cleanup and consume its terminal path before marking it settled. That cleanup has no cancellation intent and remains failed even if its terminal outcome is `interrupted`. An unexpected or stale ID settles none of the active coordinators; record the transport failure and let every accepted coordinator settle through its own path. Do not interrupt accepted siblings. Never discard an active ID before its own terminal settlement, call `subagent_continue`, inspect a native session, sleep, poll, or use a status/list operation.

After any failure or non-delivered result, launch nothing new. Continue consuming only the already accepted active phase results. Preserve every sibling's mechanically valid compact outcome even though that outcome cannot restart or complete the stopped Mission.

This step is complete only when a running Mission has all active phase coordinators settled for transition, or a stopping Mission has every coordinator accepted before the stop mechanically settled.

## 5. Validate each Ticket outcome mechanically

Apply every check below to the complete final assistant message for its coordinator:

1. The trimmed message is exactly one physical line of valid JSON decoding to one top-level object. Reject `null`, arrays, scalar JSON, Markdown fences, prefixes, suffixes, multiple envelopes, and duplicate narrative.
2. The object has required keys `ticket` and `status`, with only optional `ref` and `blocker`. Reject missing keys, unknown keys, or duplicate JSON keys.
3. `ticket` and `status` are strings. A present `ref` or `blocker` is a non-empty string.
4. `ticket` equals that coordinator's frozen Ticket byte-for-byte.
5. `status` is exactly `delivered`, `blocked`, `failed`, or `cancelled`.

Use `syntax`, `shape`, `identity`, or `status` for the first failed check, discard the raw output, and retain only `outcome-<code>`. Classify that identity as failed and stop the Mission from starting more work.

Do not adjudicate implementation semantics. Never verify delivery, resolve a `ref`, assess a blocker, inspect descendants, or decide whether an optional field should exist.

This step is complete only when each settled coordinator has one compact valid outcome or one compact mechanical failure and no raw invalid output remains.

## 6. Advance, stop, or complete

Apply these phase-barrier transitions:

- A matching `delivered` preserves that identity's compact outcome immediately. While a declared sibling remains active, keep the current phase open and start nothing.
- When every identity in the active phase has matching `delivered` and no stop occurred, advance the phase index exactly once. Start the complete next phase under step 2, or report `Mission complete` when no phase remains.
- A matching `blocked`, `failed`, or `cancelled`, any invalid return, any transport failure, or any start rejection stops later dispatch immediately. Let all coordinators already accepted in the active phase settle, preserve every valid outcome, and then report the Mission stopped.
- A delivered sibling cannot erase a stop, satisfy a failed identity, or authorize a later phase. No stopped Mission retries, skips, resumes, changes topology, or starts replacement work.

Count progress by matching delivered identities across all frozen phases, including a delivered sibling in a phase that later stops. Count `not started` only from frozen identities whose coordinator was never accepted. Mission complete requires one matching delivered outcome for every frozen identity and no recorded stop or invalid transition.

Parallelism exists only inside a declared, capacity-supported N-Ticket phase. Never overlap phases, invent concurrency, or silently serialize a declared group.

This step is complete only when exactly one next phase is active, every accepted coordinator has settled into a stopped Mission, or all frozen identities have matching delivered outcomes and the Mission is complete.

## 7. Report compact mechanical state

Use `caveman`. Preserve exact Ticket identities and complete valid `ref`, `blocker`, and required native session reference values when supplied. Render a compact outcome as:

```text
<ticket> <delivered|blocked|failed|cancelled>[ (<reason>)][; ref <ref>][; blocker <blocker>][; session <session>]
```

Use these mode-accurate transition shapes:

- Rejection: `Mission rejected (<code>); <root available|print settled; no pong pending>.`
- Interactive phase start: `Phase <phase>/<phases> dispatched: <ticket> (#<coordinator>)[, ...]; <delivered>/<total> delivered; root available; outcomes pending.`
- Steering: `<ticket> instruction forwarded (#<coordinator>); root available; outcome pending.`
- Accepted cancellation: `<ticket> cancellation requested (#<coordinator>); Mission stopping; <active> accepted coordinator(s) settling; root available.`
- Active phase settlement: `<new compact outcome(s)>; <delivered>/<total> delivered; phase <phase>/<phases> settling: <ticket> (#<coordinator>)[, ...]; root available.`
- Stop with accepted work pending: `<new compact outcome(s)>; <delivered>/<total> delivered; Mission stopping; settling <ticket> (#<coordinator>)[, ...]; root available.`
- Interactive advance: `<new compact outcome(s)>; <delivered>/<total> delivered; phase <next>/<phases> dispatched: <ticket> (#<coordinator>)[, ...]; root available; outcomes pending.`
- Interactive terminal stop: `<new compact outcome(s)>; <delivered>/<total> delivered; Mission stopped; <not-started> not started; root available.`
- Interactive completion: `<new compact outcome(s)>; <total>/<total> delivered; Mission complete; root available.`
- Print terminal: `<compact outcome 1> | ... | <compact outcome n>; <delivered>/<total> delivered; <Mission complete|Mission stopped; <not-started> not started>; print settled; no pong pending.`

For a phase start with mixed acceptance and rejection, report each accepted ID and each `dispatch-<reason>`, state `Mission stopping`, and name every accepted coordinator still settling. Emit a terminal stop only after all accepted siblings settle. Report each new valid outcome once; retained compact state and cumulative delivered count preserve earlier progress without repeating implementation narrative.

This step is complete only when one truthful compact transition has been emitted for every accepted start batch, control action, settlement turn, rejection, stop, or completion.

## Example

Interactive invocation:

```text
/dispatch-tickets
This request authorizes the complete Mission plan below with Assisted availability. All affecting blocker and conflict relations are supplied; external relations are already resolved.
{"phases":[["luizomf/omskills#60"],["luizomf/omskills#61","luizomf/omskills#62","luizomf/omskills#63"],["luizomf/omskills#64"]],"blockers":[["luizomf/omskills#60","luizomf/omskills#61"],["luizomf/omskills#61","luizomf/omskills#64"],["luizomf/omskills#62","luizomf/omskills#64"],["luizomf/omskills#63","luizomf/omskills#64"]],"conflicts":[["luizomf/omskills#60","luizomf/omskills#62"]]}
```

Here #64 is the preplanned integration Ticket for #61–#63. Assuming affirmative evidence of at least three available ROOT coordinator slots and same-batch starts in interactive mode, after the first phase delivers and all three parallel starts are accepted:

```text
luizomf/omskills#60 delivered; ref https://github.com/luizomf/omskills/issues/60; 1/5 delivered; phase 2/3 dispatched: luizomf/omskills#61 (#7), luizomf/omskills#62 (#8), luizomf/omskills#63 (#9); root available; outcomes pending.
```

If coordinator 7 returns blocked while coordinators 8 and 9 are active:

```text
luizomf/omskills#61 blocked; blocker dependency unavailable; 1/5 delivered; Mission stopping; settling luizomf/omskills#62 (#8), luizomf/omskills#63 (#9); root available.
```

If coordinator 8 then delivers its branch artifact, preserve it while 9 settles:

```text
luizomf/omskills#62 delivered; ref https://github.com/luizomf/omskills/issues/62; 2/5 delivered; Mission stopping; settling luizomf/omskills#63 (#9); root available.
```

If coordinator 9 also delivers, neither sibling revives the Mission; integration #64 remains unstarted:

```text
luizomf/omskills#63 delivered; ref https://github.com/luizomf/omskills/issues/63; 3/5 delivered; Mission stopped; 1 not started; root available.
```

Had every member delivered without a stop, phase 3 would dispatch #64 through the same coordinator route. Unknown root capacity, only child-limit evidence, or fewer than three available root slots instead rejects this entire plan before #60 starts.

## Delivery boundary

No child receives or returns `next`. This dispatcher has no tracker discovery, semantic scheduler, retry, skip, heartbeat, stall diagnosis, timeout takeover, blocker resolution, runtime workflow engine, persistent workflow state, publishing, tagging, or release behavior. It has no wormhole or tmux dependency and no Queue/TTS side effect.

The dispatcher owns only the frozen Mission envelope and mechanical routing. Ticket eligibility, governing sources, implementation, review, integration, tracker work, and semantic decisions remain with each fresh Ticket coordinator.
