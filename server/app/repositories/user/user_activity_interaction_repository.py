from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user.user_activity_interaction import UserActivityInteraction


class UserActivityInteractionRepository:

    def create(
        self,
        db: Session,
        interaction: UserActivityInteraction,
    ) -> UserActivityInteraction:
        db.add(interaction)
        db.commit()
        db.refresh(interaction)

        return interaction

    def get_user_interactions(
        self,
        db: Session,
        user_id: str,
    ) -> list[UserActivityInteraction]:
        result = db.execute(
            select(UserActivityInteraction)
            .where(UserActivityInteraction.user_id == user_id)
            .order_by(UserActivityInteraction.occurred_at.desc())
        )

        return list(result.scalars().all())