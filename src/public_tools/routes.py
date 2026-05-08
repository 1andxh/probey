from fastapi import APIRouter, Request
from .services import get_quick_check
from .schemas import QuickCheckResponse

tool_router = APIRouter()


@tool_router.get("/quick-check", response_model=QuickCheckResponse)
async def quick_check(req: Request, url: str):
    return await get_quick_check(req, url)
