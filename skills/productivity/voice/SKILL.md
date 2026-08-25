---
name: voice
description: Speak assistant responses through queued text-to-speech playback.
disable-model-invocation: true
compatibility: Requires the private OMQueue bq CLI and edgetts with local audio playback.
---

# Voice

Speak each user-facing response while this skill is active.

## Workflow

1. Draft the normal response in the user's language. Keep it concise unless the
   task requires detail. This step is complete when the written response is
   ready.
2. Create a spoken version that sounds natural when heard without a screen:
   remove Markdown syntax, describe links and code briefly instead of reading
   them character by character, expand ambiguous abbreviations, and use short
   sentences. Preserve every conclusion, warning, question, and next action the
   user needs. This step is complete when the spoken version is understandable
   on its own.
3. Check the spoken version for secrets, credentials, private data, or other
   content that should not be sent to Microsoft Edge's online TTS service or
   stored as durable Queue input. Speak only a non-sensitive summary when
   needed. This step is complete when all queued text is safe for those two
   boundaries.
4. Submit exactly one playback command for the response. Pass the text through
   stdin without a queued shell, label it `pi_voice_playback`, and always use
   the `audio-playback` concurrency key:

   ```sh
   bq --stdin --label pi_voice_playback --concurrency-key audio-playback -- edgetts --stdin --quiet <<'VOICE_TEXT'
   Your natural spoken response goes here.
   VOICE_TEXT
   ```

   Choose a heredoc delimiter absent from the spoken text. Invoke `bq` directly
   from the current shell exactly as shown; never wrap the submission in
   `bash -lc`, `zsh -lc`, or another login shell. If the harness requires a
   command prefix, apply it directly to `bq` (for example, `rtk bq ...`) rather
   than wrapping the whole command. Preserve the label and
   `--concurrency-key audio-playback`; the key serializes responses so two
   recordings do not play simultaneously. This step is complete when `bq`
   accepts one submission.
5. Return the normal written response. Do not wait for, poll, inspect, or replay
   the Queue job after acceptance. If submission fails before acceptance, say
   so briefly in writing rather than claiming audio was queued. This step is
   complete when the user receives the written response and an accepted audio
   submission, or an accurate written failure notice.

## Mode

Remain in voice mode for the conversation until the user asks to stop speaking
responses. Do not speak tool output, hidden reasoning, progress-only updates, or
content that is not part of a user-facing answer.

## Example

Written response:

> Beleza. O teste passou, e não encontrei erros. O próximo passo é publicar a
> alteração.

Spoken text:

> Beleza. O teste passou e não encontrei erros. O próximo passo é publicar a
> alteração.
