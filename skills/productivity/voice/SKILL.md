---
name: voice
description: Speak selected assistant responses using native speech or a configured TTS fallback.
disable-model-invocation: true
compatibility: Uses harness-native speech when available; otherwise needs the configured edgetts tool and local audio playback.
---

# Voice

Speak only strategically useful responses while this skill is active:
conclusions, meaningful milestones, blockers, or pauses requiring user input.
Keep routine acknowledgments and intermediate progress text-only.

## Workflow

1. **Choose an available speech route.** Prefer the active harness's native
   speech capability. Otherwise use the configured personal `edgetts` fallback
   through a transport the harness permits. Check actual capabilities rather
   than assuming a command or tool exists. If neither route is available, say
   so briefly and provide the written answer; voice unavailability does not
   block the underlying task. Route selection is complete when a supported
   path is identified or its unavailability is reported.

2. **Prepare the response.** Draft the normal written answer in the user's
   language, then adapt it for listening: remove Markdown syntax, describe
   links and code briefly, expand ambiguous abbreviations, and use short
   sentences. Preserve needed conclusions, warnings, questions, and next
   actions. This step is complete when the spoken version is understandable
   without a screen.

3. **Check privacy.** Account for the selected speech service and any retained
   transport input. The `edgetts` fallback sends text to Microsoft's online
   service; Queue input may be retained durably. Use a non-sensitive summary
   when needed. This step is complete when the text is safe for the actual
   disclosure and storage boundaries.

4. **Speak once through the selected route.** Use the native speech tool under
   its own contract, or the fallback below. A confirmed failure before
   acceptance may use another available permitted route. After acceptance or
   an ambiguous submission outcome, do not submit duplicate speech through
   another route. This step is complete when one submission is accepted, one
   foreground playback completes, or the failure/uncertain outcome is known.

5. **Return the written answer.** Report relevant unavailability or failure
   without claiming unverified playback. For background playback, acceptance
   is not evidence that audio was heard: follow the transport's completion
   contract without waiting, polling, or replaying accepted work. A playback
   completion notification is not itself another response to speak. Completion
   requires the written answer and an honest account of the speech outcome.

## Personal TTS fallback

Resolve the configured executable and inspect its input options, runtime,
working directory, playback dependencies, and environment needs without exposing
secrets. Preserve any configured playback serialization. Use an existing Queue
bridge when it supports the required route; otherwise an allowed finite
foreground command can play one response at a time. Do not create a new queue,
daemon, or background shell merely to speak.

Before using input or transport files, read
[Working files](../WORKING-FILES.md). First run
`cd '<loaded-skill-directory>' && pwd -P` and resolve the link from that physical
directory, following the source symlink before `..`. An `edgetts` input file is
UTF-8 and disposable; keep it available until the playback consumer is finished.
Supported input shapes include:

```text
edgetts --file <absolute-input-path> --quiet
edgetts --text <spoken-text-as-one-literal-argument> --quiet
```

Use the active harness's required submission mechanism. A shell-free scheduler
can pass `--file` or `--text` as literal arguments; it does not need stdin or a
queued shell. Supply any required outcome-conditioned reentry instructions and
keep successful playback callbacks silent. If a serialized Queue route is used,
preserve its `pi_voice_playback` label and `audio-playback` concurrency key; do
not invent unsupported tool fields. When the required mechanism cannot express
the route, use an allowed foreground call or report the fallback unavailable.
Raw `bq` is an option only when the harness permits it, not a way around its
scheduler rules.

## Mode

Remain in voice mode for the conversation until the user asks to stop speaking.
Apply this workflow only to strategic user-facing responses, not tool output,
hidden reasoning, routine progress, or playback callbacks.

## Example

Written response:

> Beleza. O teste passou, e não encontrei erros. O próximo passo é publicar a
> alteração.

Spoken text:

> Beleza. O teste passou e não encontrei erros. O próximo passo é publicar a
> alteração.
