from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.activity.saved_activity import SavedActivity
from app.repositories.activity.activity_repository import ActivityRepository
from app.repositories.activity.saved_activity_repository import (
    SavedActivityRepository,
)


class SavedActivityService:

    def __init__(self):
        self.saved_activity_repository = SavedActivityRepository()
        self.activity_repository = ActivityRepository()

    def save_activity(
        self,
        db: Session,
        user_id: str,
        activity_id: str,
    ) -> SavedActivity:

        activity = self.activity_repository.get_by_id(
            db,
            activity_id,
        )

        if not activity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activity not found",
            )

        existing_saved_activity = (
            self.saved_activity_repository.get_by_user_and_activity(
                db,
                user_id,
                activity_id,
            )
        )

        if existing_saved_activity:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Activity already saved",
            )

        saved_activity = SavedActivity(
            user_id=user_id,
            activity_id=activity_id,
        )

        return self.saved_activity_repository.create(
            db,
            saved_activity,
        )

    def unsave_activity(
        self,
        db: Session,
        user_id: str,
        activity_id: str,
    ) -> None:

        saved_activity = (
            self.saved_activity_repository.get_by_user_and_activity(
                db,
                user_id,
                activity_id,
            )
        )

        if not saved_activity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activity is not saved",
            )

        self.saved_activity_repository.delete(
            db,
            saved_activity,
        )

    def get_saved_activities(
        self,
        db: Session,
        user_id: str,
    ) -> list[SavedActivity]:

        return self.saved_activity_repository.get_saved_activities(
            db,
            user_id,
        )