from pathlib import Path
from utils.transcribe import transcribe
from utils.summarize import summarize_transcript

def summarize_video(audio_path: Path) -> dict:
    transcription = transcribe(audio_path)

    summary = summarize_transcript(
        transcription["text"]
    )

    return {
        "summary": summary,
        "transcript": transcription["text"],
        "segments": transcription["segments"],
    }