from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from geoalchemy2.elements import WKTElement

from app.models.group.group import Group
from app.models.group.group_location import GroupLocation
from app.repositories.group.group_location_repository import GroupLocationRepository


class GroupLocationService:

    def __init__(self):
        self.group_location_repository = GroupLocationRepository()

    def create_location(
        self,
        db: Session,
        group_id: str,
        latitude: float,
        longitude: float,
        name: str | None,
    ) -> GroupLocation:

        group = db.get(Group, group_id)

        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found",
            )

        existing_location = self.group_location_repository.get_by_group_id(
            db,
            group_id,
        )

        if existing_location:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Group location already exists",
            )

        location = GroupLocation(
            group_id=group_id,
            location=WKTElement(
                f"POINT({longitude} {latitude})",
                srid=4326,
            ),
            name=name,
        )

        return self.group_location_repository.create(
            db,
            location,
        )

    def get_location(
        self,
        db: Session,
        group_id: str,
    ) -> dict:

        location = self.group_location_repository.get_by_group_id(
            db,
            group_id,
        )

        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group location not found",
            )

        latitude, longitude = (
            self.group_location_repository.get_coordinates(
                db,
                str(location.id),
            )
        )

        return {
            "id": str(location.id),
            "group_id": str(location.group_id),
            "latitude": latitude,
            "longitude": longitude,
            "name": location.name,
            "created_at": location.created_at,
            "updated_at": location.updated_at,
        }

    def update_location(
        self,
        db: Session,
        group_id: str,
        latitude: float | None,
        longitude: float | None,
        name: str | None,
    ) -> dict:

        location = self.group_location_repository.get_by_group_id(
            db,
            group_id,
        )

        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group location not found",
            )

        if latitude is not None or longitude is not None:
            current_latitude, current_longitude = (
                self.group_location_repository.get_coordinates(
                    db,
                    str(location.id),
                )
            )

            new_latitude = (
                latitude
                if latitude is not None
                else current_latitude
            )

            new_longitude = (
                longitude
                if longitude is not None
                else current_longitude
            )

            location.location = WKTElement(
                f"POINT({new_longitude} {new_latitude})",
                srid=4326,
            )

        if name is not None:
            location.name = name

        location = self.group_location_repository.update(
            db,
            location,
        )

        latitude_value, longitude_value = (
            self.group_location_repository.get_coordinates(
                db,
                str(location.id),
            )
        )

        return {
            "id": str(location.id),
            "group_id": str(location.group_id),
            "latitude": latitude_value,
            "longitude": longitude_value,
            "name": location.name,
            "created_at": location.created_at,
            "updated_at": location.updated_at,
        }

    def delete_location(
        self,
        db: Session,
        group_id: str,
    ) -> None:

        location = self.group_location_repository.get_by_group_id(
            db,
            group_id,
        )

        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group location not found",
            )

        self.group_location_repository.delete(
            db,
            location,
        )