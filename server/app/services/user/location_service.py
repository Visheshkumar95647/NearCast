from datetime import datetime, timezone

from fastapi import HTTPException, status
from geoalchemy2.elements import WKTElement
from sqlalchemy.orm import Session

from app.models.user.user_location import UserLocation
from app.repositories.user.location_repository import LocationRepository


class LocationService:
    def __init__(self):
        self.location_repository = LocationRepository()

    def get_current_location(
        self,
        db: Session,
        user_id: str,
    ) -> UserLocation:
        location = self.location_repository.get_current_location(
            db,
            user_id,
        )

        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User location not found",
            )

        return location

    def update_location(
        self,
        db: Session,
        user_id: str,
        latitude: float,
        longitude: float,
    ) -> UserLocation:
        location = self.location_repository.get_current_location(
            db,
            user_id,
        )

        point = WKTElement(
            f"POINT({longitude} {latitude})",
            srid=4326,
        )

        if not location:
            location = UserLocation(
                user_id=user_id,
                location=point,
                is_current=True,
                recorded_at=datetime.now(timezone.utc),
            )

            return self.location_repository.create(
                db,
                location,
            )

        location.location = point
        location.recorded_at = datetime.now(timezone.utc)

        return self.location_repository.update(
            db,
            location,
        )