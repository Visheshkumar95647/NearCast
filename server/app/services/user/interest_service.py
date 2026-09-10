from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user.interest import Interest
from app.models.user.user_interest import UserInterest
from app.repositories.user.interest_repository import InterestRepository
from app.repositories.user.user_interest_repository import UserInterestRepository


class InterestService:
    def __init__(self):
        self.interest_repository = InterestRepository()
        self.user_interest_repository = UserInterestRepository()

    def add_interest(
        self,
        db: Session,
        user_id: str,
        name: str,
    ) -> Interest:
        interest = self.interest_repository.get_by_name(
            db,
            name,
        )

        if not interest:
            interest = self.interest_repository.create(
                db,
                Interest(name=name),
            )

        existing_user_interest = (
            self.user_interest_repository.get_by_user_and_interest(
                db,
                user_id,
                str(interest.id),
            )
        )

        if existing_user_interest:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Interest already added",
            )

        user_interest = UserInterest(
            user_id=user_id,
            interest_id=interest.id,
        )

        self.user_interest_repository.create(
            db,
            user_interest,
        )

        return interest

    def get_user_interests(
        self,
        db: Session,
        user_id: str,
    ) -> list[Interest]:
        return self.user_interest_repository.get_user_interests(
            db,
            user_id,
        )

    def remove_interest(
        self,
        db: Session,
        user_id: str,
        interest_id: str,
    ) -> None:
        user_interest = (
            self.user_interest_repository.get_by_user_and_interest(
                db,
                user_id,
                interest_id,
            )
        )

        if not user_interest:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interest not associated with user",
            )

        self.user_interest_repository.delete(
            db,
            user_interest,
        )