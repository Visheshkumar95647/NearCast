from sqlalchemy import select, text
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

    def get_nearby_users(
        self,
        db: Session,
        latitude: float,
        longitude: float,
        radius_meters: float,
    ) -> list[str]:

        result = db.execute(
            text("""
                SELECT user_id
                FROM user_locations
                WHERE is_current = TRUE
                AND ST_DWithin(
                    location,
                    ST_SetSRID(
                        ST_MakePoint(:longitude, :latitude),
                        4326
                    )::geography,
                    :radius_meters
                )
            """),
            {
                "latitude": latitude,
                "longitude": longitude,
                "radius_meters": radius_meters,
            },
        )

        return [str(row.user_id) for row in result]