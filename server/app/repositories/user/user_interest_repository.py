from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user.interest import Interest
from app.models.user.user_interest import UserInterest


class UserInterestRepository:
    def get_by_user_and_interest(
        self,
        db: Session,
        user_id: str,
        interest_id: str,
    ) -> UserInterest | None:
        result = db.execute(
            select(UserInterest).where(
                UserInterest.user_id == user_id,
                UserInterest.interest_id == interest_id,
            )
        )
        return result.scalar_one_or_none()

    def create(
        self,
        db: Session,
        user_interest: UserInterest,
    ) -> UserInterest:
        db.add(user_interest)
        db.commit()
        db.refresh(user_interest)
        return user_interest

    def get_user_interests(
        self,
        db: Session,
        user_id: str,
    ) -> list[Interest]:
        result = db.execute(
            select(Interest)
            .join(
                UserInterest,
                UserInterest.interest_id == Interest.id,
            )
            .where(UserInterest.user_id == user_id)
        )
        return list(result.scalars().all())

    def delete(
        self,
        db: Session,
        user_interest: UserInterest,
    ) -> None:
        db.delete(user_interest)
        db.commit()