from fastapi import APIRouter
from pydantic import BaseModel

from controllers.chat_controller import DEFAULT_MATCH_COUNT, answer_question

router = APIRouter()


class ChatRequest(BaseModel):
    query: str
    match_count: int = DEFAULT_MATCH_COUNT


@router.post("/chat")
async def chat(request: ChatRequest):
    return await answer_question(request.query, request.match_count)
