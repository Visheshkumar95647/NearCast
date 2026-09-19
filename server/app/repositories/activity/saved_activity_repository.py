from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.activity.saved_activity import SavedActivity


class SavedActivityRepository:

    def get_by_user_and_activity(
        self,
        db: Session,
        user_id: str,
        activity_id: str,
    ) -> SavedActivity | None:
        result = db.execute(
            select(SavedActivity).where(
                SavedActivity.user_id == user_id,
                SavedActivity.activity_id == activity_id,
            )
        )

        return result.scalar_one_or_none()

    def create(
        self,
        db: Session,
        saved_activity: SavedActivity,
    ) -> SavedActivity:
        db.add(saved_activity)
        db.commit()
        db.refresh(saved_activity)

        return saved_activity

    def delete(
        self,
        db: Session,
        saved_activity: SavedActivity,
    ) -> None:
        db.delete(saved_activity)
        db.commit()

    def get_saved_activities(
        self,
        db: Session,
        user_id: str,
    ) -> list[SavedActivity]:
        result = db.execute(
            select(SavedActivity)
            .where(SavedActivity.user_id == user_id)
            .order_by(SavedActivity.created_at.desc())
        )

        return list(result.scalars().all())