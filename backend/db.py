from supabase import create_client

from config import settings

supabase = None

if settings.SUPABASE_URL and settings.SUPABASE_SERVICE_ROLE_KEY:
    supabase = create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_SERVICE_ROLE_KEY,
    )


async def create_summary(
    video_name: str,
    summary: str,
    embedding: list[float],
    source: str | None = None,
):
    if supabase is None:
        raise RuntimeError("Supabase client is not working")

    response = (
        supabase.table("summarizations")
        .insert(
            {
                "video_name": video_name,
                "summary": summary,
                "embedding": embedding,
                "source": source,
            }
        )
        .execute()
    )

    return response.data[0] if response.data else None
