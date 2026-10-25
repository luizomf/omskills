---
name: voice
description: Fire-and-forget speech through bq directly, with no preflight checks or completion callbacks.
disable-model-invocation: true
compatibility: Requires configured bq, voicept/voiceen, and local audio playback.
---

# Voice

Voice stays on until the user asks to stop. Keep providing the written answer.
Speak supplied text when asked to read it; otherwise speak the useful answer or
question. Keep routine progress silent.

Treat `bq`, `voicept`, and `voiceen` as already configured and maintained by the
user. Submit directly: no executable discovery, script reads, environment
inspection, or runtime checks.

Invoke the raw `bq` CLI once through the ordinary shell tool. This is
**fire-and-forget**: do not use `scheduler_submit`, scheduled reminders, managed
processes, or completion callbacks for speech. Use this exact command for
Portuguese:

```bash
bq --label pi-voice --json --cwd "$(pwd)" --concurrency-key audio-playback --stdin -- bash -lc voicept <<< "Filhote, agora eu consigo gritar, mano."
```

Replace only the spoken text, shell-quoted as literal data. For English, also
change `voicept` to `voiceen`. Keep the text safe for the configured voice
service and retained Queue input.

Once `bq` accepts the submission, continue immediately: no playback wait,
polling, or completion announcement. Acceptance means queued, not confirmed
playback.

If the submission itself reports an error, briefly tell the user and continue
in writing. Leave repairs to the user; do not investigate playback, switch
engines, retry, or run playback in the foreground. An uncertain submission must
not be duplicated.
