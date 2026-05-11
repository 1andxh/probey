from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.users.models import User
from .utils import (
    create_access_token,
    verify_password,
    ACCESS_TOKEN_EXPIRY,
    REFRESH_TOKEN_EXPIRY_DAYS,
    decode_token,
)
from .schemas import Token
from datetime import timedelta
from src.users.service import UserService

service = UserService()


class AuthService:
    def _build_token_payload(self, user: User) -> dict:
        return {"email": user.email, "user_id": str(user.id)}

    async def authenticate_user(
        self, email: str, password: str, session: AsyncSession
    ) -> User:
        user = await service._get_user_by_email(email, session)
        if user is None or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        return user
