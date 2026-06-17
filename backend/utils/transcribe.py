import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, Optional

from groq import Groq

from config import settings
from utils.audio import probe_duration, split_by_time


client = Groq(api_key=settings.GROQ_API_KEY)

MAX_BYTES = 25 * 1024 * 1024
CHUNK_SECONDS = 20 * 60
MAX_WORKERS = 4

# Called with (done, total) as each chunk finishes, so callers can report
# transcription progress.
ProgressFn = Callable[[int, int], None]


def transcribe(audio_path: Path, on_progress: Optional[ProgressFn] = None) -> dict:
    if audio_path.stat().st_size <= MAX_BYTES:
        if on_progress:
            on_progress(0, 1)
        result = _transcribe_single(audio_path)
        if on_progress:
            on_progress(1, 1)
        return result

    with tempfile.TemporaryDirectory() as tmpdir:
        chunks = split_by_time(audio_path, Path(tmpdir), CHUNK_SECONDS)
        total = len(chunks)
        if on_progress:
            on_progress(0, total)


        offsets = []
        acc = 0.0
        for chunk_path in chunks:
            offsets.append(acc)
            acc += probe_duration(chunk_path)

        # Transcribe chunks concurrently, storing each result at its chunk index.
        results: list[Optional[dict]] = [None] * total
        done = 0
        lock = threading.Lock()
        with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, total)) as executor:
            futures = {
                executor.submit(_transcribe_single, chunk_path): i
                for i, chunk_path in enumerate(chunks)
            }
            for future in as_completed(futures):
                i = futures[future]
                results[i] = future.result()
                if on_progress:
                    with lock:
                        done += 1
                        on_progress(done, total)

        # Stitch results in chunk order, applying each chunk's time offset.
        text_parts = []
        segments = []
        for result, offset in zip(results, offsets):
            assert result is not None  # every future resolved above
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