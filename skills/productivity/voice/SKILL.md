---
name: voice
description: Queue speech through bq using voicept or voiceen, without waiting for playback.
disable-model-invocation: true
compatibility: Requires configured bq, voicept/voiceen, and local audio playback.
---

# Voice

Voice stays on until the user asks to stop. Keep providing the written answer.
Speak supplied text when asked to read it; otherwise speak the useful answer or
question. Keep routine progress and playback callbacks silent.

Choose by the conversation's language: `voicept` for Portuguese, `voiceen` for
English. These commands own voice configuration; the user maintains them.

Submit the spoken text literally through stdin to the serialized audio queue.
For Portuguese:

```bash
bq --cwd "$PWD" --label pi-voice --concurrency-key audio-playback --stdin bash -c 'voicept' <<'VOICE_TEXT'
<spoken text>
VOICE_TEXT
```

For English, change only `voicept` to `voiceen`. Choose a heredoc delimiter
absent from the spoken text. Keep the text safe for the configured voice service
and retained Queue input.

Once `bq` accepts the submission, continue immediately: no playback wait,
polling, or completion announcement. Acceptance means queued, not confirmed
playback.

If unavailable or failed, briefly tell the user and continue in writing. Leave
repairs to the user; do not switch engines, retry, or run playback in the
foreground. An uncertain submission must not be duplicated.
