import asyncio
import json

from fastapi import APIRouter, UploadFile
from fastapi.responses import StreamingResponse

from controllers.summary_controller import summarize_transcription
from utils.upload import transcription_from_bytes
from utils.embeddings import embed_summary
from db import create_summary

router = APIRouter()


@router.post("/summarize")
async def summarize_upload(file: UploadFile):
    name = file.filename or "untitled"
    data = await file.read()

    loop = asyncio.get_running_loop()
    queue: asyncio.Queue = asyncio.Queue()

    def emit(event: str, **payload):
        loop.call_soon_threadsafe(queue.put_nowait, {"event": event, **payload})

    async def run():
        try:
            def transcribe_with_progress():
                emit("stage", stage="transcribing", message="Transcribing audio")
                return transcription_from_bytes(
                    name,
                    data,
                    on_progress=lambda done, total: emit(
                        "progress", stage="transcribing", done=done, total=total
                    ),
                )

            transcription = await asyncio.to_thread(transcribe_with_progress)

            emit("stage", stage="summarizing", message="Summarizing transcript")
            result = await asyncio.to_thread(summarize_transcription, transcription)
            summary_text = result["summary"]

            emit("stage", stage="embedding", message="Generating embedding")
            embedding = await embed_summary(summary_text)

            emit("stage", stage="saving", message="Saving summary")
            record = await create_summary(
                video_name=name,
                summary=summary_text,
                embedding=embedding,
                source=name,
            )

            emit(
                "result",
                id=record["id"] if record else None,
                video_name=name,
                summary=summary_text,
                segments=result["segments"],
            )
        except Exception as exc:
            emit("error", message=str(exc))
        finally:
            loop.call_soon_threadsafe(queue.put_nowait, None)

    async def event_stream():
        task = asyncio.create_task(run())
        try:
            while True:
                item = await queue.get()
                if item is None:
                    break
                yield f"data: {json.dumps(item)}\n\n"
        finally:
            await task

    return StreamingResponse(event_stream(), media_type="text/event-stream")
