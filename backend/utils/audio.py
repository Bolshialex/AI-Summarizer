import subprocess
from pathlib import Path


def normalize_to_flac(input_path: Path, output_path: Path) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(input_path),
            "-ac", "1",
            "-ar", "16000",
            "-c:a", "flac",
            str(output_path),
        ],
        check=True,
    )


def split_by_time(input_path: Path, output_dir: Path, seconds: int) -> list[Path]:
    pattern = output_dir / "chunk_%03d.flac"
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(input_path),
            "-f", "segment",
            "-segment_time", str(seconds),
            "-c", "copy",
            str(pattern),
        ],
        check=True,
    )
    return sorted(output_dir.glob("chunk_*.flac"))
