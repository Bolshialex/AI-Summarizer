# Development Notes — Transcription Timestamps

## The plan

`/transcribe` returns timestamps as raw seconds (floats), not pretty strings. Example: a 1h15m mark comes back as `4521.0`, not `"1:15:21"`.

So the plan is:

1. **Store the raw float in the database.** Don't store formatted strings — floats are sortable, queryable, and easy to do math on.
2. **Format the float into `H:MM:SS` only when we need to show it** (UI display, or feeding it to the summary LLM).

Two small utility functions handle the formatting. The DB never sees a formatted string.

---

## What just got fixed

The old chunking code assumed every 20-minute chunk was exactly 1200 seconds long. It isn't always — `ffmpeg` cuts on audio frame boundaries, so chunks can be a few milliseconds off. Over a 3-hour podcast that drift adds up.

Fix: we now measure each chunk's real length with `ffprobe` and use that as the offset. Timestamps stay accurate end-to-end.

Files changed: `backend/utils/audio.py` and `backend/utils/transcribe.py`.

---

## The two new utils

Both live in `backend/utils/timestamp.py`. They're pure functions — no DB, no API calls, just transform data.

### `format_timestamp(seconds: float) -> str`

Turns a float into a clean string for display. Drops the hour when it's zero so short clips look natural.

| Input | Output |
|---|---|
| `12.4` | `"0:12"` |
| `127.44` | `"2:07"` |
| `4521.0` | `"1:15:21"` |

Use it in the API layer when sending segments to the frontend.

### `segments_to_prompt(segments: list[dict]) -> str`

Joins all segments into one string with inline timestamps. This is what we feed the summary LLM so it can say things like "around the 1-hour mark, they discussed X."

Input:
```python
[
  {"start": 0.0,   "end": 4.2,  "text": "First segment of speech"},
  {"start": 127.44, "end": 131.8, "text": "Something else happened"},
]
```

Output:
```
[0:00] First segment of speech
[2:07] Something else happened
```

---

## Suggested DB schema 

```
transcripts:
  id              uuid PK
  audio_id        uuid
  full_text       text
  created_at      timestamptz

transcript_segments:
  id              uuid PK
  transcript_id   uuid FK -> transcripts.id
  segment_index   int
  start_seconds   float8
  end_seconds     float8
  text            text
```

Index on `(transcript_id, start_seconds)` for fast lookups.

---

## RAG later

When we build RAG retrieval:
- Embed `segment.text` by itself (no timestamps inside the embedding).
- Store `start_seconds` and `end_seconds` as metadata on the vector.
- At query time, return the matching segment and use `start_seconds` to build a "jump to this moment" link.

Storing raw floats keeps this clean. Storing formatted strings would mean parsing them back every time.

---

## Status

| Done? | Item |
|---|---|
| Done | Fix chunk offset drift (`probe_duration` in `audio.py`) |
| Done | `format_timestamp()` util |
| Done | `segments_to_prompt()` util |
| TODO (DB team) | `transcripts` + `transcript_segments` tables |
| TODO (future) | RAG embeddings with timestamp metadata |
