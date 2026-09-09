from geoalchemy2 import Geography

from sqlalchemy.orm import Mapped, mapped_column


class LocationMixin:

    location: Mapped[object] = mapped_column(
        Geography(
            geometry_type="POINT",
            srid=4326,
            spatial_index=False,
            # we create spatial index manually in the migration script to avoid issues with Alembic autogenerate
        ),
        nullable=True,
    )