from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user.refresh_token import RefreshToken


class RefreshTokenRepository:

    def create(
        self,
        db: Session,
        refresh_token: RefreshToken,
    ) -> RefreshToken:
        db.add(refresh_token)
        db.commit()
        db.refresh(refresh_token)

        return refresh_token

    def get_by_token(
        self,
        db: Session,
        token: str,
    ) -> RefreshToken | None:
        result = db.execute(
            select(RefreshToken).where(
                RefreshToken.token == token
            )
        )

        return result.scalar_one_or_none()

    def revoke(
        self,
        db: Session,
        refresh_token: RefreshToken,
    ) -> RefreshToken:
        refresh_token.revoked_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(refresh_token)

        return refresh_token