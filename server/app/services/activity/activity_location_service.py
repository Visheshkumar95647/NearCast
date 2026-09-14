from fastapi import HTTPException, status
from geoalchemy2.elements import WKTElement
from sqlalchemy.orm import Session

from app.models.activity.activity_location import ActivityLocation
from app.repositories.activity.activity_location_repository import (
    ActivityLocationRepository,
)


class ActivityLocationService:
    def __init__(self):
        self.activity_location_repository = ActivityLocationRepository()

    def get_location_details(
        self,
        db: Session,
        activity_id: str,
    ) -> tuple[ActivityLocation, float, float]:

        location = self.activity_location_repository.get_by_activity_id(
            db,
            activity_id,
        )

        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activity location not found",
            )

        latitude, longitude = (
            self.activity_location_repository.get_coordinates(
                db,
                str(location.id),
            )
        )

        return location, latitude, longitude

    def create_or_update_location(
        self,
        db: Session,
        activity_id: str,
        latitude: float,
        longitude: float,
        name: str | None,
    ) -> ActivityLocation:

        location = self.activity_location_repository.get_by_activity_id(
            db,
            activity_id,
        )

        point = WKTElement(
            f"POINT({longitude} {latitude})",
            srid=4326,
        )

        if not location:
            location = ActivityLocation(
                activity_id=activity_id,
                location=point,
                name=name,
            )

            return self.activity_location_repository.create(
                db,
                location,
            )

        location.location = point

        if name is not None:
            location.name = name

        return self.activity_location_repository.update(
            db,
            location,
        )

    def delete_location(
        self,
        db: Session,
        activity_id: str,
    ) -> None:

        location = self.activity_location_repository.get_by_activity_id(
            db,
            activity_id,
        )

        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activity location not found",
            )

        self.activity_location_repository.delete(
            db,
            location,
        )