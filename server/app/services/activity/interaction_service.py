from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.activity.activity import Activity
from app.models.user.user_activity_interaction import UserActivityInteraction
from app.repositories.activity.activity_repository import ActivityRepository
from app.repositories.user.user_activity_interaction_repository import (
    UserActivityInteractionRepository,
)


class ActivityInteractionService:

    def __init__(self):
        self.interaction_repository = UserActivityInteractionRepository()
        self.activity_repository = ActivityRepository()

    def record_interaction(
        self,
        db: Session,
        user_id: str,
        activity_id: str,
        interaction_type: str,
    ) -> UserActivityInteraction:

        activity = self.activity_repository.get_by_id(
            db,
            activity_id,
        )

        if not activity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activity not found",
            )

        interaction = UserActivityInteraction(
            user_id=user_id,
            activity_id=activity_id,
            interaction_type=interaction_type,
            occurred_at=datetime.now(timezone.utc),
        )

        return self.interaction_repository.create(
            db,
            interaction,
        )
    
    def get_user_interactions(
        self,
        db: Session,
        user_id: str,
    ) -> list[UserActivityInteraction]:

        return self.interaction_repository.get_user_interactions(
            db,
            user_id,
        )