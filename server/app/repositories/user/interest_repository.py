from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user.interest import Interest


class InterestRepository:
    def get_by_id(
        self,
        db: Session,
        interest_id: str,
    ) -> Interest | None:
        return db.get(Interest, interest_id)

    def get_by_name(
        self,
        db: Session,
        name: str,
    ) -> Interest | None:
        result = db.execute(
            select(Interest).where(Interest.name == name)
        )
        return result.scalar_one_or_none()

    def create(
        self,
        db: Session,
        interest: Interest,
    ) -> Interest:
        db.add(interest)
        db.commit()
        db.refresh(interest)
        return interest