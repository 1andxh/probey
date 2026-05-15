import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import require_admin
from src.db.session import get_session
from src.users.models import User

from .service import admin_service

admin = Annotated[User, Depends(require_admin)]
session = Annotated[AsyncSession, Depends(get_session)]

admin_router = APIRouter()


@admin_router.get("/stats")
async def get_platform_stats(_: admin, session: session):
    return await admin_service.get_platform_stats(session)


@admin_router.get("/users")
async def get_all_users(_: admin, session: session):
    return await admin_service.get_users_with_monitor_count(session)


@admin_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users(user_id: uuid.UUID, _: admin, session: session):
    if user_id == _.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account",
        )
    await admin_service.delete_user(user_id, session)
