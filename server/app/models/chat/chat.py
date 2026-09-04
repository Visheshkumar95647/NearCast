import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class Chat(TimestampMixin, Base):
    __tablename__ = "chats"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("groups.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
