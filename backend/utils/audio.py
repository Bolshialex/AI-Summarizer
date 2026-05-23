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
