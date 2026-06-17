import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, Optional

from groq import APIConnectionError, APIStatusError, APITimeoutError, Groq

from config import settings
from utils.audio import split_by_time


client = Groq(api_key=settings.GROQ_API_KEY, timeout=180.0, max_retries=0)

MAX_BYTES = 25 * 1024 * 1024
CHUNK_SECONDS = 10 * 60
MAX_WORKERS = 6
TRANSCRIBE_MAX_ATTEMPTS = 4
TRANSCRIBE_BACKOFF_BASE = 2.0

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

        chunk_paths = [path for path, _ in chunks]
        offsets = [start for _, start in chunks]

        results: list[Optional[dict]] = [None] * total
        done = 0
        lock = threading.Lock()
        with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, total)) as executor:
            futures = {
                executor.submit(_transcribe_single, path): i
                for i, path in enumerate(chunk_paths)
            }
            for future in as_completed(futures):
                i = futures[future]
                results[i] = future.result()
                if on_progress:
                    with lock:
                        done += 1
                        on_progress(done, total)

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
    for attempt in range(TRANSCRIBE_MAX_ATTEMPTS):
        try:
            return _transcribe_once(audio_path)
        except (APIConnectionError, APITimeoutError, APIStatusError) as exc:
            # Only retry transient errors: connection/timeout, or 5xx. A 4xx
            # (429 rate-limit, 400 bad request) is not transient — surface it.
            if isinstance(exc, APIStatusError) and exc.status_code < 500:
                raise
            if attempt == TRANSCRIBE_MAX_ATTEMPTS - 1:
                raise
            delay = TRANSCRIBE_BACKOFF_BASE * (2 ** attempt)
            print(
                f"[transcribe] transient error ({exc}); "
                f"retry {attempt + 1}/{TRANSCRIBE_MAX_ATTEMPTS - 1} in {delay:.0f}s",
                flush=True,
            )
            time.sleep(delay)


def _transcribe_once(audio_path: Path) -> dict:
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