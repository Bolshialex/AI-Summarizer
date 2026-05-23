from pathlib import Path

from groq import Groq


client = Groq()


def transcribe(audio_path: Path) -> dict:
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
