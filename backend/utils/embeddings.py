from openai import AsyncOpenAI

from config import settings

client = AsyncOpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)


async def embed_text(input_text: str | list[str]):
    # encoding_format="float" is required: the OpenRouter embeddings endpoint
    # does not support the SDK's default base64 encoding and otherwise returns
    # no parseable embedding data.
    response = await client.embeddings.create(
        model=settings.EMBEDDING_MODEL,
        input=input_text,
        encoding_format="float",
    )

    if isinstance(input_text, list):
        return [item.embedding for item in response.data]

    return response.data[0].embedding


async def embed_summary(summary: str):
    return await embed_text(summary)
