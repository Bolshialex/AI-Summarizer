import subprocess
from pathlib import Path


def normalize_audio(input_path: Path, output_path: Path) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(input_path),
            "-vn",
            "-ac", "1",
            "-ar", "16000",
            "-c:a", "aac",
            "-b:a", "64k",
            str(output_path),
        ],
        check=True,
    )


def split_by_time(
    input_path: Path, output_dir: Path, seconds: int
) -> list[tuple[Path, float]]:
    pattern = output_dir / "chunk_%03d.m4a"
    list_path = output_dir / "segments.csv"
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(input_path),
            "-f", "segment",
            "-segment_time", str(seconds),
            "-segment_list", str(list_path),
            "-segment_list_type", "csv",
            # Re-encode (not -c copy): stream-copying produces chunks with broken
            # headers that the transcription API can't decode.
            "-c:a", "aac",
            "-b:a", "64k",
            str(pattern),
        ],
        check=True,
    )

    chunks = sorted(output_dir.glob("chunk_*.m4a"))
    starts = _parse_segment_starts(list_path)
    return list(zip(chunks, starts))


def _parse_segment_starts(list_path: Path) -> list[float]:
    # Each CSV row is: filename,start_seconds,end_seconds
    starts: list[float] = []
    with open(list_path) as f:
        for line in f:
            line = line.strip()
            if line:
                starts.append(float(line.split(",")[1]))
    return starts
