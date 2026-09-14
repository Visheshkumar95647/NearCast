from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.activity.activity import Activity


class ActivityRepository:
    def get_by_id(self, db: Session, activity_id: str) -> Activity | None:
        return db.get(Activity, activity_id)

    def create(self, db: Session, activity: Activity) -> Activity:
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return activity

    def update(self, db: Session, activity: Activity) -> Activity:
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return activity

    def delete(self, db: Session, activity: Activity) -> None:
        db.delete(activity)
        db.commit()