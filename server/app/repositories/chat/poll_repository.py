from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chat.poll import Poll


class PollRepository:
    def create(self, db: Session, poll: Poll) -> Poll:
        db.add(poll)
        db.commit()
        db.refresh(poll)
        return poll

    def update(self, db: Session, poll: Poll) -> Poll:
        db.commit()
        db.refresh(poll)
        return poll

    def get_by_id(self, db: Session, poll_id: str) -> Poll | None:
        return db.get(Poll, poll_id)

    def get_by_chat_id(self, db: Session, chat_id: str) -> list[Poll]:
        result = db.execute(
            select(Poll)
            .where(Poll.chat_id == chat_id)
            .order_by(Poll.created_at.asc())
        )

        return list(result.scalars().all())