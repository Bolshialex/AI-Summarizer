from utils.summarize import summarize_transcript
from utils.timestamp import segments_to_prompt


def _transcript_for_llm(transcription: dict) -> str:
    segments = transcription.get("segments") or []
    if segments:
        return segments_to_prompt(segments)
    return transcription["text"]


def summarize_transcription(transcription: dict) -> dict:
    llm_input = _transcript_for_llm(transcription)
    summary = summarize_transcript(llm_input)

    return {
        "summary": summary,
        "transcript": transcription["text"],
        "segments": transcription.get("segments", []),
    }
