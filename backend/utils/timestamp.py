def format_timestamp(seconds: float) -> str:
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def segments_to_prompt(segments: list[dict]) -> str:
    return "\n".join(
        f"[{format_timestamp(s['start'])}] {s['text'].strip()}" for s in segments
    )
