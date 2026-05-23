import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, UploadFile

from utils.audio import normalize_to_flac
from utils.transcribe import transcribe

router = APIRouter()


@router.post("/transcribe")
async def transcribe_upload(file: UploadFile):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        suffix = Path(file.filename or "").suffix
        upload_path = tmp / f"upload{suffix}"
        with open(upload_path, "wb") as out:
            shutil.copyfileobj(file.file, out)

        audio_path = tmp / "audio.flac"
        normalize_to_flac(upload_path, audio_path)

        return transcribe(audio_path)
