from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user.user_preference import UserPreference
from app.repositories.user.preference_repository import PreferenceRepository


class PreferenceService:
    def __init__(self):
        self.preference_repository = PreferenceRepository()

    def get_preferences(
        self,
        db: Session,
        user_id: str,
    ) -> UserPreference:
        preference = self.preference_repository.get_by_user_id(
            db,
            user_id,
        )

        if not preference:
            preference = self.preference_repository.create(
                db,
                UserPreference(user_id=user_id),
            )

        return preference

    def update_preferences(
        self,
        db: Session,
        user_id: str,
        max_distance_km: float | None,
        preferred_group_size: int | None,
        preferred_activity_type: str | None,
        notifications_enabled: bool | None,
    ) -> UserPreference:
        preference = self.preference_repository.get_by_user_id(
            db,
            user_id,
        )

        if not preference:
            preference = UserPreference(user_id=user_id)

        if max_distance_km is not None:
            preference.max_distance_km = max_distance_km

        if preferred_group_size is not None:
            preference.preferred_group_size = preferred_group_size

        if preferred_activity_type is not None:
            preference.preferred_activity_type = preferred_activity_type

        if notifications_enabled is not None:
            preference.notifications_enabled = notifications_enabled

        if preference.id:
            return self.preference_repository.update(
                db,
                preference,
            )

        return self.preference_repository.create(
            db,
            preference,
        )