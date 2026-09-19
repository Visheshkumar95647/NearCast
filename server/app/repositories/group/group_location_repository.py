from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.models.group.group_location import GroupLocation


class GroupLocationRepository:

    def get_by_group_id(
        self,
        db: Session,
        group_id: str,
    ) -> GroupLocation | None:
        result = db.execute(
            select(GroupLocation).where(
                GroupLocation.group_id == group_id,
            )
        )

        return result.scalar_one_or_none()

    def create(
        self,
        db: Session,
        group_location: GroupLocation,
    ) -> GroupLocation:
        db.add(group_location)
        db.commit()
        db.refresh(group_location)

        return group_location

    def update(
        self,
        db: Session,
        group_location: GroupLocation,
    ) -> GroupLocation:
        db.add(group_location)
        db.commit()
        db.refresh(group_location)

        return group_location

    def delete(
        self,
        db: Session,
        group_location: GroupLocation,
    ) -> None:
        db.delete(group_location)
        db.commit()

    def get_coordinates(
        self,
        db: Session,
        location_id: str,
    ) -> tuple[float, float]:
        result = db.execute(
            text("""
                SELECT
                    ST_Y(location::geometry),
                    ST_X(location::geometry)
                FROM group_locations
                WHERE id = :location_id
            """),
            {"location_id": location_id},
        )

        latitude, longitude = result.one()

        return latitude, longitude