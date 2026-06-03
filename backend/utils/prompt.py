def build_summary_prompt(transcript: str) -> str:
    return f"""
Summarize the following video transcript.

Requirements:
- Provide a concise overall summary.
- Extract the most important points.
- Use bullet points for key takeaways.
- Ignore filler words, repeated phrases, and off-topic chatter.
- Keep factual details intact.

Transcript:
{transcript}

Output format:

Summary:
<summary>

Key Points:
- point 1
- point 2
- point 3
"""