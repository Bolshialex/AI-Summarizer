from fastapi import APIRouter, UploadFile

from controllers.summary_controller import summarize_transcription
from utils.upload import transcription_from_upload
from utils.embeddings import embed_summary
from db import create_summary

router = APIRouter()


@router.post("/summarize")
async def summarize_upload(file: UploadFile):
    transcription = await transcription_from_upload(file)

    result = summarize_transcription(transcription)
    summary_text = result["summary"]

    embedding = await embed_summary(summary_text)

    record = await create_summary(
        video_name=file.filename or "untitled",
        summary=summary_text,
        embedding=embedding,
        source=file.filename,
    )

    return {
        "id": record["id"] if record else None,
        "video_name": file.filename,
        "summary": summary_text,
        "segments": result["segments"],
    }
