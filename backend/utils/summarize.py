from openai import OpenAI

from config import settings
from utils.prompt import build_summary_prompt

client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)


def summarize_transcript(transcript: str) -> str:
    prompt = build_summary_prompt(transcript)

    response = client.chat.completions.create(
        model="meta-llama/llama-3.3-70b-instruct:free",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert summarization assistant. "
                    "Create concise summaries and key takeaways from transcripts."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content