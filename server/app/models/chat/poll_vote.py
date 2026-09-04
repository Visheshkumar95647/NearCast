import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class PollVote(TimestampMixin, Base):
    __tablename__ = "poll_votes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    poll_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("polls.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    option_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("poll_options.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    voted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "poll_id",
            "option_id",
            "user_id",
            name="uq_vote_poll_option_user",
        ),
    )