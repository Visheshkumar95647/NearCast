from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chat.poll_option import PollOption


class PollOptionRepository:
    def create(self, db: Session, option: PollOption) -> PollOption:
        db.add(option)
        db.commit()
        db.refresh(option)
        return option

    def get_by_id(
        self,
        db: Session,
        option_id: str,
    ) -> PollOption | None:
        return db.get(PollOption, option_id)

    def get_by_poll_id(
        self,
        db: Session,
        poll_id: str,
    ) -> list[PollOption]:
        result = db.execute(
            select(PollOption)
            .where(PollOption.poll_id == poll_id)
            .order_by(PollOption.position.asc())
        )

        return list(result.scalars().all())