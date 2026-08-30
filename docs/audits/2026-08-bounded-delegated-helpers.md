# Bounded delegated-helper compatibility evidence

This focused record reconstructs the delegated evidence-helper contracts against the delivered Pi runtime. It covers Ticket #37's runner boundary only; it is not a catalog-wide compatibility claim or an implementation of subagent mechanics.

## Runtime baseline

Runtime evidence comes from `luizomf/ompi` commit `bd64e683ff9a8c5bbab9d9f628babf8fee632951` on `main`. The following focused command was rerun against that exact clean checkout:

```sh
npm test -- \
  extensions/subagents/controller.test.ts \
  extensions/subagents/inheritance.test.ts \
  extensions/subagents/native-inheritance.test.ts \
  extensions/subagents/native-nesting.test.ts \
  extensions/subagents/presentation.test.ts
```

Outcome: **5 test files passed; 70 tests passed**. The checkout remained clean at the named commit.

## Runtime scenario reconstruction

| Scenario | Delivered runtime evidence | Helper consequence |
| --- | --- | --- |
| Root asynchronous | `controller.test.ts` verifies return after prompt acceptance and exactly one later completed/interrupted pong after process close. | A root may end or do independent work after acceptance, then validate evidence from the one completion notification; it never polls. |
| Print direct | `inheritance.test.ts` verifies print start and continuation remain pending, return terminal results directly, and enqueue no pong. | Print helpers consume the pending result before continuing. |
| Nested direct | `native-nesting.test.ts` runs a depth-2 coordinator through a dependent direct depth-3 turn, observes the same coordinator process before and after the leaf, and reads both persisted sessions. | A dependent coordinator requests direct delivery and validates the returned evidence in the same turn. |
| No later direct pong | `controller.test.ts` and `inheritance.test.ts` verify direct start/continuation return exactly once; message/pong counts do not increase after settlement. | A direct caller must not wait for a second notification. |
| Over-depth rejection | `controller.test.ts` and `inheritance.test.ts` verify a depth-3 start is rejected before child launch and before any RPC invocation. | A leaf never invokes a helper requiring depth 4; supplied evidence, direct leaf tools, or a blocker are the only valid branches. |
| Cancellation | Direct cancellation settles as `interrupted` with a session reference; native nesting verifies cancellation recursively ends the depth-2/depth-3 lineage. Spontaneous abort remains `failed`. | A Prompt Audit interruption cannot be converted into evidence or `PASS`; it records `FAIL`. Other helpers treat the pass as incomplete. |
| Provider/tool inheritance and preflight | `inheritance.test.ts` verifies each then-active tool and extension provider is inherited, names have no hidden capability effect, restrictions only narrow, and mismatches reject before prompt acceptance. | Runner briefs declare required capabilities; roles do not grant them. Preflight rejection means no worker pass occurred. |
| Clean native sessions | `native-inheritance.test.ts` verifies only explicit child prompts enter a new session while project instructions, skill discovery, cwd, environment, tools, and providers are inherited. Parent transcript and compaction state are absent. | Every evidence worker starts fresh; recovery reads its persisted output without continuing or contaminating the child. |
| Bounded result recovery | `presentation.test.ts` verifies terminal text is marked when truncated to 8,000 characters and retains the session reference for completion, failure, and interruption. `native-nesting.test.ts` uses that reference to read complete leaf evidence. | Decision-bearing terminal evidence is recovered from the native session when bounded; research and architecture still require their named artifacts. |

## Role-specific completion reconstruction

The distributed skill contracts close the runtime scenarios as follows:

- **Code review:** one fresh read-only leaf returns one complete Standards/Spec pass. The caller recovers bounded findings before adjudication. No delegated correction, confirmation, or re-review follows.
- **Research:** one fresh researcher writes the exact public-safe Markdown artifact. Completion requires a successful settlement plus caller read-back and primary-source validation; terminal text is not a substitute.
- **Architecture Explore:** one fresh Explore leaf writes findings only. The caller validates those findings, adjudicates cited repository evidence, writes and validates the HTML report, and only then attempts the platform opener.
- **Headless opener:** after a complete report passes artifact checks, an unavailable or non-zero opener is reported with the absolute path and top recommendation and remains non-fatal. Opener success is never validation. No alternate browser or HTML-security work is introduced.
- **Prompt Audit:** interpreter, coordinator assessment, reviewer, and the optional one post-repair confirmation remain sequential. Each pass receives only its asymmetric declared inputs. Missing isolation, preflight rejection, failure, interruption, cancellation, missing output, or unrecoverable bounded evidence records `FAIL` through the normal durable status path.
- **Design It Twice:** the optional designer is one clean leaf only when the invoking workflow and current depth authorize that role. The accepted one-Ticket writer/reviewer graph does not silently gain a third specialist; a depth-3 leaf resolves accepted sources directly or returns a blocker.

These contracts consume Pi's delivered delivery, inheritance, lineage, cancellation, and session behavior. They do not reproduce those mechanics in skill text.
