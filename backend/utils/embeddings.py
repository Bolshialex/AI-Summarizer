import asyncio

from openai import APIConnectionError, APITimeoutError, AsyncOpenAI

from config import settings

client = AsyncOpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    max_retries=0,
)

EMBED_MAX_ATTEMPTS = 4
EMBED_BACKOFF_BASE = 1.0


async def _create_with_retry(input_text: str | list[str]):
    for attempt in range(EMBED_MAX_ATTEMPTS):
        try:
            return await client.embeddings.create(
                model=settings.EMBEDDING_MODEL,
                input=input_text,
                encoding_format="float",
            )
        except (APIConnectionError, APITimeoutError) as exc:
            if attempt == EMBED_MAX_ATTEMPTS - 1:
                raise
            delay = EMBED_BACKOFF_BASE * (2 ** attempt)
            print(
                f"[embed] network error ({exc}); "
                f"retry {attempt + 1}/{EMBED_MAX_ATTEMPTS - 1} in {delay:.0f}s",
                flush=True,
            )
            await asyncio.sleep(delay)


async def embed_text(input_text: str | list[str]):
    response = await _create_with_retry(input_text)

    if isinstance(input_text, list):
        return [item.embedding for item in response.data]

    return response.data[0].embedding


async def embed_summary(summary: str):
    return await embed_text(summary)
