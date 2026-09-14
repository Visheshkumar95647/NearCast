from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.activity.activity_participant import ActivityParticipant
from app.repositories.activity.activity_participant_repository import (
    ActivityParticipantRepository,
)
from app.repositories.activity.activity_repository import ActivityRepository


class ActivityParticipantService:

    def __init__(self):
        self.activity_participant_repository = ActivityParticipantRepository()
        self.activity_repository = ActivityRepository()

    def join_activity(
        self,
        db: Session,
        user_id: str,
        activity_id: str,
    ) -> ActivityParticipant:

        activity = self.activity_repository.get_by_id(
            db,
            activity_id,
        )

        if not activity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activity not found",
            )

        if not activity.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Activity is inactive",
            )

        existing_participant = (
            self.activity_participant_repository.get_by_user_and_activity(
                db,
                user_id,
                activity_id,
            )
        )

        if existing_participant:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already joined this activity",
            )

        participant = ActivityParticipant(
            user_id=user_id,
            activity_id=activity_id,
            status="confirmed",
            joined_at=datetime.now(timezone.utc),
        )

        return self.activity_participant_repository.create(
            db,
            participant,
        )

    def leave_activity(
        self,
        db: Session,
        user_id: str,
        activity_id: str,
    ) -> None:

        participant = (
            self.activity_participant_repository.get_by_user_and_activity(
                db,
                user_id,
                activity_id,
            )
        )

        if not participant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User is not a participant of this activity",
            )

        self.activity_participant_repository.delete(
            db,
            participant,
        )

    def get_participants(
        self,
        db: Session,
        activity_id: str,
    ) -> list[tuple[ActivityParticipant, object]]:

        activity = self.activity_repository.get_by_id(
            db,
            activity_id,
        )

        if not activity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activity not found",
            )

        return self.activity_participant_repository.get_participants(
            db,
            activity_id,
        )