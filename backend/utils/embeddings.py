from openai import AsyncOpenAI

from config import settings

# OpenRouter embedding model. Free Nvidia Nemotron embed endpoint.
EMBEDDING_MODEL = "nvidia/llama-nemotron-embed-vl-1b-v2:free"

client = AsyncOpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)


async def embed_text(input_text: str | list[str]):
    response = await client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=input_text,
    )

    if isinstance(input_text, list):
        return [item.embedding for item in response.data]

    return response.data[0].embedding


async def embed_summary(summary: str):
    return await embed_text(summary)
