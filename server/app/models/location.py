from geoalchemy2 import Geography
from sqlalchemy.orm import Mapped, mapped_column


class LocationMixin:
    location: Mapped[object] = mapped_column(
        Geography(
            geometry_type="POINT",
            srid=4326,
            spatial_index=True,
        ),
        nullable=True,
    )