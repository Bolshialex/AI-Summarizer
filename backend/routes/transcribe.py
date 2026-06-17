from fastapi import APIRouter, UploadFile
from utils.upload import transcription_from_upload

router = APIRouter()


@router.post("/transcribe")
async def transcribe_upload(file: UploadFile):
    return await transcription_from_upload(file)
