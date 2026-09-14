from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.activity.activity_participant import ActivityParticipant
from app.models.user.user import User


class ActivityParticipantRepository:

    def get_by_user_and_activity(
        self,
        db: Session,
        user_id: str,
        activity_id: str,
    ) -> ActivityParticipant | None:
        result = db.execute(
            select(ActivityParticipant).where(
                ActivityParticipant.user_id == user_id,
                ActivityParticipant.activity_id == activity_id,
            )
        )

        return result.scalar_one_or_none()

    def create(
        self,
        db: Session,
        participant: ActivityParticipant,
    ) -> ActivityParticipant:
        db.add(participant)
        db.commit()
        db.refresh(participant)

        return participant

    def delete(
        self,
        db: Session,
        participant: ActivityParticipant,
    ) -> None:
        db.delete(participant)
        db.commit()

    def get_participants(
        self,
        db: Session,
        activity_id: str,
    ) -> list[tuple[ActivityParticipant, User]]:
        result = db.execute(
            select(ActivityParticipant, User)
            .join(
                User,
                User.id == ActivityParticipant.user_id,
            )
            .where(ActivityParticipant.activity_id == activity_id)
            .order_by(ActivityParticipant.joined_at.asc())
        )

        return list(result.all())