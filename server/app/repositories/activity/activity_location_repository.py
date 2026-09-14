from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.models.activity.activity_location import ActivityLocation


class ActivityLocationRepository:
    def get_by_activity_id(
        self,
        db: Session,
        activity_id: str,
    ) -> ActivityLocation | None:
        result = db.execute(
            select(ActivityLocation).where(
                ActivityLocation.activity_id == activity_id
            )
        )
        return result.scalar_one_or_none()

    def get_coordinates(
        self,
        db: Session,
        location_id: str,
    ) -> tuple[float, float]:
        result = db.execute(
            text(
                """
                SELECT
                    ST_Y(location::geometry),
                    ST_X(location::geometry)
                FROM activity_locations
                WHERE id = :location_id
                """
            ),
            {"location_id": location_id},
        )

        return result.one()

    def create(
        self,
        db: Session,
        activity_location: ActivityLocation,
    ) -> ActivityLocation:
        db.add(activity_location)
        db.commit()
        db.refresh(activity_location)
        return activity_location

    def update(
        self,
        db: Session,
        activity_location: ActivityLocation,
    ) -> ActivityLocation:
        db.add(activity_location)
        db.commit()
        db.refresh(activity_location)
        return activity_location

    def delete(
        self,
        db: Session,
        activity_location: ActivityLocation,
    ) -> None:
        db.delete(activity_location)
        db.commit()

    def get_nearby_activities(
        self,
        db: Session,
        latitude: float,
        longitude: float,
        radius_km: float,
    ):
        result = db.execute(
            text(
                """
                SELECT
                    a.id,
                    a.group_id,
                    a.title,
                    a.description,
                    a.starts_at,
                    a.ends_at,
                    a.is_public,
                    a.is_active,
                    ST_Distance(
                        al.location,
                        ST_SetSRID(
                            ST_MakePoint(:longitude, :latitude),
                            4326
                        )::geography
                    ) / 1000 AS distance_km
                FROM activities a
                JOIN activity_locations al
                    ON al.activity_id = a.id
                WHERE
                    a.is_active = TRUE
                    AND ST_DWithin(
                        al.location,
                        ST_SetSRID(
                            ST_MakePoint(:longitude, :latitude),
                            4326
                        )::geography,
                        :radius_meters
                    )
                ORDER BY distance_km ASC
                """
            ),
            {
                "latitude": latitude,
                "longitude": longitude,
                "radius_meters": radius_km * 1000,
            },
        )

        return result.mappings().all()