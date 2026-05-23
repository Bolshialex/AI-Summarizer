import tempfile
from pathlib import Path

from groq import Groq

from utils.audio import split_by_time


client = Groq()

MAX_BYTES = 25 * 1024 * 1024
CHUNK_SECONDS = 20 * 60


def transcribe(audio_path: Path) -> dict:
    if audio_path.stat().st_size <= MAX_BYTES:
        return _transcribe_single(audio_path)

    with tempfile.TemporaryDirectory() as tmpdir:
        chunks = split_by_time(audio_path, Path(tmpdir), CHUNK_SECONDS)
        text_parts = []
        segments = []
        for i, chunk_path in enumerate(chunks):
            offset = i * CHUNK_SECONDS
            result = _transcribe_single(chunk_path)
            text_parts.append(result["text"])
            segments.extend(
                {"start": s["start"] + offset, "end": s["end"] + offset, "text": s["text"]}
                for s in result["segments"]
            )
        return {"text": " ".join(text_parts).strip(), "segments": segments}


def _transcribe_single(audio_path: Path) -> dict:
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            file=(audio_path.name, f.read()),
            model="whisper-large-v3-turbo",
            response_format="verbose_json",
            timestamp_granularities=["segment"],
        )
    return {
        "text": result.text,
        "segments": [
            {"start": s["start"], "end": s["end"], "text": s["text"]}
            for s in result.segments
        ],
    }
