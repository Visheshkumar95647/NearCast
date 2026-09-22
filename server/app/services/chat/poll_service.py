from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.chat.poll import Poll
from app.models.chat.poll_option import PollOption
from app.models.chat.poll_vote import PollVote

from app.repositories.chat.chat_repository import ChatRepository
from app.repositories.chat.poll_repository import PollRepository
from app.repositories.chat.poll_option_repository import PollOptionRepository
from app.repositories.chat.poll_vote_repository import PollVoteRepository
from app.repositories.group.group_member_repository import GroupMemberRepository

from app.schemas.websocket.poll import PollWebSocketMessage
from app.schemas.websocket.poll_vote import PollVoteWebSocketMessage
from app.schemas.websocket.poll_state import (
    PollOptionVoteCount,
    PollStateWebSocketMessage,
)
from app.schemas.websocket.poll_close import PollCloseWebSocketMessage

from app.websocket.manager import manager


class PollService:
    def __init__(self):
        self.poll_repository = PollRepository()
        self.poll_option_repository = PollOptionRepository()
        self.poll_vote_repository = PollVoteRepository()
        self.chat_repository = ChatRepository()
        self.group_member_repository = GroupMemberRepository()

    async def create_poll(
        self,
        db: Session,
        user_id: str,
        chat_id: str,
        question: str,
        options: list[str],
        is_multiple_choice: bool,
    ) -> Poll:
        chat = self.chat_repository.get_by_id(
            db=db,
            chat_id=chat_id,
        )

        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )

        group_member = self.group_member_repository.get_by_user_and_group(
            db=db,
            user_id=user_id,
            group_id=str(chat.group_id),
        )

        if not group_member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this group",
            )

        if len(options) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A poll must have at least two options",
            )

        poll = Poll(
            chat_id=chat_id,
            creator_id=user_id,
            question=question,
            is_multiple_choice=is_multiple_choice,
            is_closed=False,
        )

        poll = self.poll_repository.create(
            db=db,
            poll=poll,
        )

        for position, option_text in enumerate(options):
            option = PollOption(
                poll_id=poll.id,
                option_text=option_text,
                position=position,
            )

            self.poll_option_repository.create(
                db=db,
                option=option,
            )

        member_user_ids = self.group_member_repository.get_user_ids_by_group_id(
            db=db,
            group_id=str(chat.group_id),
        )

        websocket_message = PollWebSocketMessage(
            type="poll_created",
            poll_id=str(poll.id),
            chat_id=str(poll.chat_id),
            creator_id=str(poll.creator_id),
            question=poll.question,
            is_multiple_choice=poll.is_multiple_choice,
            is_closed=poll.is_closed,
            created_at=poll.created_at,
        )

        await manager.send_to_users(
            user_ids=member_user_ids,
            message=websocket_message.model_dump(mode="json"),
        )

        return poll

    async def vote(
        self,
        db: Session,
        user_id: str,
        poll_id: str,
        option_id: str,
    ) -> PollVote:
        poll = self.poll_repository.get_by_id(
            db=db,
            poll_id=poll_id,
        )

        if not poll:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Poll not found",
            )

        if poll.is_closed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Poll is closed",
            )

        chat = self.chat_repository.get_by_id(
            db=db,
            chat_id=str(poll.chat_id),
        )

        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )

        group_member = self.group_member_repository.get_by_user_and_group(
            db=db,
            user_id=user_id,
            group_id=str(chat.group_id),
        )

        if not group_member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this group",
            )

        option = self.poll_option_repository.get_by_id(
            db=db,
            option_id=option_id,
        )

        if not option:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Poll option not found",
            )

        if str(option.poll_id) != str(poll.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Poll option does not belong to this poll",
            )

        existing_votes = self.poll_vote_repository.get_by_poll_and_user(
            db=db,
            poll_id=str(poll.id),
            user_id=user_id,
        )

        if not poll.is_multiple_choice and existing_votes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already voted in this poll",
            )

        for existing_vote in existing_votes:
            if str(existing_vote.option_id) == str(option.id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You have already selected this option",
                )

        vote = PollVote(
            poll_id=poll.id,
            option_id=option.id,
            user_id=user_id,
            voted_at=datetime.now(timezone.utc),
        )

        vote = self.poll_vote_repository.create(
            db=db,
            vote=vote,
        )

        member_user_ids = self.group_member_repository.get_user_ids_by_group_id(
            db=db,
            group_id=str(chat.group_id),
        )

        vote_counts = self.poll_vote_repository.get_vote_counts_by_poll_id(
            db=db,
            poll_id=str(vote.poll_id),
        )

        poll_state_message = PollStateWebSocketMessage(
            type="poll_state",
            poll_id=str(vote.poll_id),
            counts=[
                PollOptionVoteCount(
                    option_id=option_id,
                    vote_count=vote_count,
                )
                for option_id, vote_count in vote_counts
            ],
        )

        websocket_message = PollVoteWebSocketMessage(
            type="poll_vote",
            poll_id=str(vote.poll_id),
            option_id=str(vote.option_id),
            user_id=str(vote.user_id),
            voted_at=vote.voted_at,
        )

        await manager.send_to_users(
            user_ids=member_user_ids,
            message=websocket_message.model_dump(mode="json"),
        )

        await manager.send_to_users(
            user_ids=member_user_ids,
            message=poll_state_message.model_dump(mode="json"),
        )

        return vote

    def get_poll(
        self,
        db: Session,
        user_id: str,
        poll_id: str,
    ) -> Poll:
        poll = self.poll_repository.get_by_id(
            db=db,
            poll_id=poll_id,
        )

        if not poll:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Poll not found",
            )

        chat = self.chat_repository.get_by_id(
            db=db,
            chat_id=str(poll.chat_id),
        )

        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )

        group_member = self.group_member_repository.get_by_user_and_group(
            db=db,
            user_id=user_id,
            group_id=str(chat.group_id),
        )

        if not group_member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this group",
            )

        return poll

    def get_chat_polls(
        self,
        db: Session,
        user_id: str,
        chat_id: str,
    ) -> list[Poll]:
        chat = self.chat_repository.get_by_id(
            db=db,
            chat_id=chat_id,
        )

        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )

        group_member = self.group_member_repository.get_by_user_and_group(
            db=db,
            user_id=user_id,
            group_id=str(chat.group_id),
        )

        if not group_member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this group",
            )

        return self.poll_repository.get_by_chat_id(
            db=db,
            chat_id=chat_id,
        )

    async def close_poll(
        self,
        db: Session,
        user_id: str,
        poll_id: str,
    ) -> Poll:
        poll = self.poll_repository.get_by_id(
            db=db,
            poll_id=poll_id,
        )

        if not poll:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Poll not found",
            )

        if str(poll.creator_id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the poll creator can close the poll",
            )

        if poll.is_closed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Poll is already closed",
            )

        chat = self.chat_repository.get_by_id(
            db=db,
            chat_id=str(poll.chat_id),
        )

        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )

        poll.is_closed = True

        poll = self.poll_repository.update(
            db=db,
            poll=poll,
        )

        member_user_ids = self.group_member_repository.get_user_ids_by_group_id(
            db=db,
            group_id=str(chat.group_id),
        )

        websocket_message = PollCloseWebSocketMessage(
            type="poll_closed",
            poll_id=str(poll.id),
            chat_id=str(poll.chat_id),
            closed_by=user_id,
            closed_at=datetime.now(timezone.utc),
        )

        await manager.send_to_users(
            user_ids=member_user_ids,
            message=websocket_message.model_dump(mode="json"),
        )

        return poll