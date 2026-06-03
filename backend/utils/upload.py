import shutil
import tempfile
from pathlib import Path
from fastapi import UploadFile
from utils.audio import normalize_to_flac
from utils.transcribe import transcribe

async def transcription_from_upload(file: UploadFile) -> dict:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        suffix = Path(file.filename or "").suffix
        upload_path = tmp / f"upload{suffix}"
        with open(upload_path, "wb") as out:
            shutil.copyfileobj(file.file, out)

        audio_path = tmp / "audio.flac"
        normalize_to_flac(upload_path, audio_path)

        return transcribe(audio_path)