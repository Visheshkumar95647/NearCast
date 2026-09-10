from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user.user_location import UserLocation


class LocationRepository:
    def get_current_location(
        self,
        db: Session,
        user_id: str,
    ) -> UserLocation | None:
        result = db.execute(
            select(UserLocation).where(
                UserLocation.user_id == user_id,
                UserLocation.is_current.is_(True),
            )
        )
        return result.scalar_one_or_none()

    def create(
        self,
        db: Session,
        location: UserLocation,
    ) -> UserLocation:
        db.add(location)
        db.commit()
        db.refresh(location)
        return location

    def update(
        self,
        db: Session,
        location: UserLocation,
    ) -> UserLocation:
        db.add(location)
        db.commit()
        db.refresh(location)
        return location