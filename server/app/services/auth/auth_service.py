from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.user.refresh_token import RefreshToken
from app.models.user.user import User
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository


class AuthService:

    def __init__(self):
        self.user_repository = UserRepository()
        self.refresh_token_repository = RefreshTokenRepository()

    def register(
        self,
        db: Session,
        username: str,
        email: str,
        password: str,
    ) -> User:
        existing_user = self.user_repository.get_by_email(
            db,
            email,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            is_active=True,
        )

        return self.user_repository.create(
            db,
            user,
        )

    def login(
        self,
        db: Session,
        email: str,
        password: str,
    ) -> tuple[str, str]:
        user = self.user_repository.get_by_email(
            db,
            email,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        access_token = create_access_token(
            subject=str(user.id)
        )

        refresh_token = create_refresh_token(
            subject=str(user.id)
        )

        refresh_token_record = RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=(
                datetime.now(timezone.utc)
                + timedelta(
                    days=settings.jwt_refresh_expire_days
                )
            ),
        )

        self.refresh_token_repository.create(
            db,
            refresh_token_record,
        )

        return access_token, refresh_token

    def refresh(
        self,
        db: Session,
        refresh_token: str,
    ) -> str:
        try:
            payload = jwt.decode(
                refresh_token,
                settings.jwt_refresh_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        stored_token = self.refresh_token_repository.get_by_token(
            db,
            refresh_token,
        )

        if not stored_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not found",
            )

        if stored_token.revoked_at is not None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked",
            )

        if stored_token.expires_at <= datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired",
            )

        if str(stored_token.user_id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        return create_access_token(
            subject=user_id
        )

    def logout(
        self,
        db: Session,
        refresh_token: str,
    ) -> None:
        stored_token = self.refresh_token_repository.get_by_token(
            db,
            refresh_token,
        )

        if not stored_token:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Refresh token not found",
            )

        if stored_token.revoked_at is not None:
            return

        self.refresh_token_repository.revoke(
            db,
            stored_token,
        )

    def get_current_user(
        self,
        db: Session,
        token: str,
    ) -> User:
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        user = self.user_repository.get_by_id(
            db,
            user_id,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        return user