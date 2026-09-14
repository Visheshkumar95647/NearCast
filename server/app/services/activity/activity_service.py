from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.activity.activity import Activity
from app.repositories.activity.activity_repository import ActivityRepository


class ActivityService:
    def __init__(self):
        self.activity_repository = ActivityRepository()

    def create_activity(
        self,
        db: Session,
        title: str,
        description: str | None,
        group_id: str | None,
        starts_at: datetime,
        ends_at: datetime | None,
        is_public: bool,
    ) -> Activity:

        if ends_at is not None and ends_at <= starts_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Activity end time must be after start time",
            )

        activity = Activity(
            title=title,
            description=description,
            group_id=group_id,
            starts_at=starts_at,
            ends_at=ends_at,
            is_public=is_public,
            is_active=True,
        )

        return self.activity_repository.create(db, activity)

    def get_activity(
        self,
        db: Session,
        activity_id: str,
    ) -> Activity:

        activity = self.activity_repository.get_by_id(db, activity_id)

        if not activity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activity not found",
            )

        return activity

    def update_activity(
        self,
        db: Session,
        activity_id: str,
        title: str | None,
        description: str | None,
        group_id: str | None,
        starts_at: datetime | None,
        ends_at: datetime | None,
        is_public: bool | None,
        is_active: bool | None,
    ) -> Activity:

        activity = self.get_activity(db, activity_id)

        new_starts_at = starts_at if starts_at is not None else activity.starts_at
        new_ends_at = ends_at if ends_at is not None else activity.ends_at

        if new_ends_at is not None and new_ends_at <= new_starts_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Activity end time must be after start time",
            )

        if title is not None:
            activity.title = title

        if description is not None:
            activity.description = description

        if group_id is not None:
            activity.group_id = group_id

        if starts_at is not None:
            activity.starts_at = starts_at

        if ends_at is not None:
            activity.ends_at = ends_at

        if is_public is not None:
            activity.is_public = is_public

        if is_active is not None:
            activity.is_active = is_active

        return self.activity_repository.update(db, activity)

    def delete_activity(
        self,
        db: Session,
        activity_id: str,
    ) -> None:

        activity = self.get_activity(db, activity_id)

        self.activity_repository.delete(db, activity)