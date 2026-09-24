from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user.user import User
from app.repositories.chat.poll_option_repository import PollOptionRepository
from app.repositories.chat.poll_vote_repository import PollVoteRepository
from app.schemas.chat.poll import PollResponse, PollVoteResponse
from app.services.chat.poll_service import PollService


router = APIRouter(
    prefix="/chat",
    tags=["Chat Polls"],
)


poll_service = PollService()
poll_option_repository = PollOptionRepository()
poll_vote_repository = PollVoteRepository()


class PollCreate(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=1000,
    )
    options: list[str] = Field(
        min_length=2,
        max_length=20,
    )
    is_multiple_choice: bool = False


class PollVoteCreate(BaseModel):
    option_id: str


@router.post(
    "/{chat_id}/polls",
    response_model=PollResponse,
)
def create_poll(
    chat_id: str,
    poll_data: PollCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return poll_service.create_poll(
        db=db,
        user_id=str(current_user.id),
        chat_id=chat_id,
        question=poll_data.question,
        options=poll_data.options,
        is_multiple_choice=poll_data.is_multiple_choice,
    )


@router.post(
    "/polls/{poll_id}/vote",
    response_model=PollVoteResponse,
)
def vote_on_poll(
    poll_id: str,
    vote_data: PollVoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return poll_service.vote(
        db=db,
        user_id=str(current_user.id),
        poll_id=poll_id,
        option_id=vote_data.option_id,
    )


@router.get(
    "/polls/{poll_id}",
)
def get_poll(
    poll_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    poll = poll_service.get_poll(
        db=db,
        user_id=str(current_user.id),
        poll_id=poll_id,
    )

    options = poll_option_repository.get_by_poll_id(
        db=db,
        poll_id=poll_id,
    )

    vote_counts = poll_vote_repository.get_vote_counts_by_poll_id(
        db=db,
        poll_id=poll_id,
    )

    my_votes = poll_vote_repository.get_by_poll_and_user(
        db=db,
        poll_id=poll_id,
        user_id=str(current_user.id),
    )

    return {
        "poll": poll,
        "options": options,
        "vote_counts": vote_counts,
        "my_votes": [
            str(vote.option_id)
            for vote in my_votes
        ],
    }


@router.get(
    "/{chat_id}/polls",
    response_model=list[PollResponse],
)
def get_chat_polls(
    chat_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return poll_service.get_chat_polls(
        db=db,
        user_id=str(current_user.id),
        chat_id=chat_id,
    )


@router.patch(
    "/polls/{poll_id}/close",
    response_model=PollResponse,
)
def close_poll(
    poll_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return poll_service.close_poll(
        db=db,
        user_id=str(current_user.id),
        poll_id=poll_id,
    )