from fastapi import status, HTTPException
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User
from .utils import normalize_email
from src.auth.utils import (
    ACCESS_TOKEN_EXPIRY,
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)

REFRESH_TOKEN_EXPIRY_DAYS = 7


class UserService:
    async def _get_user_by_email(
        self, email: str, session: AsyncSession
    ) -> User | None:
        normalized_email = normalize_email(email)
        stmt = await session.execute(select(User).where(User.email == normalized_email))
        return stmt.scalar_one_or_none()

    async def _verify_user(self, user: User, session: AsyncSession) -> User:
        user.is_verified = True
        await session.flush()
        await session.refresh(user)
        return user
