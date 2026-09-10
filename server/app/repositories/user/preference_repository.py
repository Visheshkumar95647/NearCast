from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user.user_preference import UserPreference


class PreferenceRepository:
    def get_by_user_id(
        self,
        db: Session,
        user_id: str,
    ) -> UserPreference | None:
        result = db.execute(
            select(UserPreference).where(
                UserPreference.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    def create(
        self,
        db: Session,
        preference: UserPreference,
    ) -> UserPreference:
        db.add(preference)
        db.commit()
        db.refresh(preference)
        return preference

    def update(
        self,
        db: Session,
        preference: UserPreference,
    ) -> UserPreference:
        db.add(preference)
        db.commit()
        db.refresh(preference)
        return preference