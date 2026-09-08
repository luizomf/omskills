# Task-to-model candidates

Use the column for the authorized provider. These are practical starting choices,
not measured cross-provider parity, a universal ranking, or proof of availability.
Models in the same row are candidates for the same kind of work, not equally
capable models. Project evidence and explicit user choices take precedence.

## Quick selection table

| Delegated task | OpenAI candidate | Anthropic candidate | Google candidate |
| --- | --- | --- | --- |
| Mechanical edits, extraction, formatting, transcript cleanup, short grounded summaries | GPT-5.6 Luna — low | Claude Sonnet 5 — low | Gemini 3.8 Flash — low |
| Bounded code/test implementation with settled design and clear acceptance checks | GPT-5.6 Terra — medium | Claude Sonnet 5 — high | Gemini 3.8 Flash — medium |
| Thin dispatch of an already resolved plan, without implementation decisions | GPT-5.6 Terra — low | Claude Sonnet 5 — medium | Gemini 3.8 Flash — low |
| Substantive investigation, grounded planning, general code review, or Ticket coordination with adjudication/corrections | GPT-5.6 Sol — medium | Claude Opus 5 — high | Gemini 3.8 Flash — medium |
| Ambiguous architecture, difficult cross-system trade-offs, or complex integration decisions | GPT-6 Astra — medium | Claude Fable 5.1 — high | Gemini 3.8 Flash — high; evaluate on the workload |
| Elusive causal bugs, novel algorithms, or high-risk security/concurrency/migration analysis requiring deep reasoning | GPT-6 Astra — high | Claude Fable 5.1 — high | Gemini 3.8 Flash — high; capability must be established for the risk |

Use the more demanding row when mistakes are consequential or the brief leaves
material decisions unresolved. Do not raise the row merely because the input is
long. For large grounded summaries, preserve evidence coverage and chunking; if
reconciling conflicting claims requires judgment, use the investigation row.
A high-effort recommendation is a starting choice, not an automatic escalation
from the user's pinned route. Maximum effort is not the default.

For speech-to-text, use a dedicated transcription capability or an audio-capable
model with verified input limits. The text-cleanup row assumes a transcript
already exists; none of the OpenAI entries above is an audio-transcription model.

## Model identifiers and controls

These are API IDs, not universal harness-qualified route strings. Resolve the
provider prefix and supported lifecycle controls in the active harness.

| Display name | API model ID |
| --- | --- |
| GPT-5.6 Luna | `gpt-5.6-luna` |
| GPT-5.6 Terra | `gpt-5.6-terra` |
| GPT-5.6 Sol | `gpt-5.6-sol` |
| GPT-6 Astra | `gpt-6-astra` |
| Claude Sonnet 5 | `claude-sonnet-5` |
| Claude Opus 5 | `claude-opus-5` |
| Claude Fable 5.1 | `claude-fable-5-1` |
| Gemini 3.8 Flash | `gemini-3.8-flash` |

- GPT-5.6 Luna/Terra/Sol support API `reasoning.effort` values `none`, `low`,
  `medium`, `high`, `xhigh`, and `max`; their documented default is `medium`.
  GPT-6 Astra supports `low`, `medium`, `high`, `xhigh`, and `max`, not `none`.
- Claude Sonnet 5, Opus 5 and Fable 5.1 support `output_config.effort` values
  `low`, `medium`, `high`, `xhigh`, and `max`; the documented default is `high`.
  Thinking mode is a separate control; do not pass `adaptive` as effort.
- Gemini 3.8 Flash supports `thinking_level` values `low`, `medium`, and `high`,
  with `medium` as default; `minimal` is unsupported.

Matching effort labels do not establish matching reasoning capacity or compute.
API support also does not establish support in a particular harness or account.

## Source basis and maintenance

Source snapshot: 2026-09-08. This is an intentionally maintained model catalog;
update model names and controls here when verified vendor changes or project
evaluations warrant it, rather than spreading names through workflow skills.
Task assignments in the quick table are engineering recommendations, not vendor
benchmarks. No comparative evaluation is claimed.

- [Luna model](https://developers.openai.com/api/docs/models/gpt-5.6-luna): high-volume tier, corresponding roughly to earlier nano models; model ID, modalities and effort support.
- [Terra model](https://developers.openai.com/api/docs/models/gpt-5.6-terra): intelligence/capability balance, corresponding roughly to earlier mini models; model ID and effort support.
- [Sol model](https://developers.openai.com/api/docs/models/gpt-5.6-sol): flagship complex-work tier; `gpt-5.6` is an alias for Sol; model ID, modalities and effort support.
- [Astra model](https://developers.openai.com/api/docs/models/gpt-6-astra): hardest end-to-end work, model ID, modalities and effort support.
- [Claude model catalog](https://platform.claude.com/docs/en/models/overview): Sonnet speed/intelligence, Opus complex agentic coding, Fable demanding reasoning and long-horizon work; model IDs.
- [Claude effort guide](https://platform.claude.com/docs/en/build-with-claude/effort): supported values, provider defaults and model-specific effort recommendations.
- [Gemini 3.8 Flash guide](https://ai.google.dev/gemini-api/docs/latest-model): model ID, software-engineering scope and low/medium/high thinking guidance. The same candidate appears across rows because this provider guidance uses tunable effort; it is not a claim of parity with every other model.
