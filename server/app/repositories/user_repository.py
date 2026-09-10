from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user.user import User


class UserRepository:
    def get_by_email(self, db: Session, email: str) -> User | None:
        result = db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    def get_by_username(self, db: Session, username: str) -> User | None:
        result = db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    def get_by_id(self, db: Session, user_id: str) -> User | None:
        return db.get(User, user_id)

    def create(self, db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user