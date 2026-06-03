from fastapi import APIRouter, UploadFile

from controllers.summary_controller import summarize_transcription
from utils.upload import transcription_from_upload

router = APIRouter()


@router.post("/summarize")
async def summarize_upload(file: UploadFile):
    transcription = await transcription_from_upload(file)
    return summarize_transcription(transcription)
