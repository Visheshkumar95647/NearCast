from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.chat.poll_option import PollOption
from app.models.chat.poll_vote import PollVote


class PollVoteRepository:
    def create(
        self,
        db: Session,
        vote: PollVote,
    ) -> PollVote:
        db.add(vote)
        db.commit()
        db.refresh(vote)
        return vote

    def get_by_poll_and_user(
        self,
        db: Session,
        poll_id: str,
        user_id: str,
    ) -> list[PollVote]:
        result = db.execute(
            select(PollVote).where(
                PollVote.poll_id == poll_id,
                PollVote.user_id == user_id,
            )
        )
        return list(result.scalars().all())

    def get_by_poll_and_option(
        self,
        db: Session,
        poll_id: str,
        option_id: str,
    ) -> list[PollVote]:
        result = db.execute(
            select(PollVote).where(
                PollVote.poll_id == poll_id,
                PollVote.option_id == option_id,
            )
        )
        return list(result.scalars().all())

    def get_vote_counts_by_poll_id(
        self,
        db: Session,
        poll_id: str,
    ) -> list[tuple[str, int]]:
        result = db.execute(
            select(
                PollOption.id,
                func.count(PollVote.id),
            )
            .select_from(PollOption)
            .outerjoin(
                PollVote,
                PollVote.option_id == PollOption.id,
            )
            .where(PollOption.poll_id == poll_id)
            .group_by(PollOption.id)
            .order_by(PollOption.position.asc())
        )

        return [
            (str(option_id), vote_count)
            for option_id, vote_count in result.all()
        ]