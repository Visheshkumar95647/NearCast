from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user.user import User
from app.repositories.user.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_profile(self, db: Session, user_id: str) -> User:
        user = self.user_repository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    def update_profile(
        self,
        db: Session,
        user_id: str,
        username: str | None,
        email: str | None,
    ) -> User:
        user = self.user_repository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if username is not None and username != user.username:
            existing_user = self.user_repository.get_by_username(
                db,
                username,
            )

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already taken",
                )

            user.username = username

        if email is not None and email != user.email:
            existing_user = self.user_repository.get_by_email(
                db,
                email,
            )

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered",
                )

            user.email = email

        return self.user_repository.update(db, user)