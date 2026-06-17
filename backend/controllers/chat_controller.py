from db import supabase
from utils.embeddings import embed_text

DEFAULT_MATCH_COUNT = 5
DEFAULT_SIMILARITY_THRESHOLD = 0.0


async def retrieve_relevant_summaries(
    query: str, 
    match_count: int = DEFAULT_MATCH_COUNT, 
    similarity_threshold: float = DEFAULT_SIMILARITY_THRESHOLD, ) -> list[dict]:
    if supabase is None:
        raise RuntimeError("Supabase client is not configured")

    query_embedding = await embed_text(query)

    response = supabase.rpc(
        "match_summarizations",
        {
            "query_embedding": query_embedding,
            "match_count": match_count,
            "similarity_threshold": similarity_threshold,
        },
    ).execute()

    return response.data or []


async def answer_question(query: str,match_count: int = DEFAULT_MATCH_COUNT,) -> dict:
    matches = await retrieve_relevant_summaries(query, match_count)

    return {
        "query": query,
        "matches": matches,
    }
