from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user.user import User
from app.schemas.activity.participant import ActivityParticipantResponse
from app.services.activity.activity_participant_service import (
    ActivityParticipantService,
)

router = APIRouter(
    prefix="/activities",
    tags=["Activity Participants"],
)

activity_participant_service = ActivityParticipantService()


@router.post(
    "/{activity_id}/participants",
    response_model=ActivityParticipantResponse,
    status_code=status.HTTP_201_CREATED,
)
def join_activity(
    activity_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    participant = activity_participant_service.join_activity(
        db=db,
        user_id=str(current_user.id),
        activity_id=activity_id,
    )

    return ActivityParticipantResponse(
        id=str(participant.id),
        user_id=str(participant.user_id),
        activity_id=str(participant.activity_id),
        username=current_user.username,
        status=participant.status,
        joined_at=participant.joined_at,
    )


@router.get(
    "/{activity_id}/participants",
    response_model=list[ActivityParticipantResponse],
)
def get_activity_participants(
    activity_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    participants = activity_participant_service.get_participants(
        db=db,
        activity_id=activity_id,
    )

    return [
        ActivityParticipantResponse(
            id=str(participant.id),
            user_id=str(user.id),
            activity_id=str(participant.activity_id),
            username=user.username,
            status=participant.status,
            joined_at=participant.joined_at,
        )
        for participant, user in participants
    ]


@router.delete(
    "/{activity_id}/participants",
    status_code=status.HTTP_204_NO_CONTENT,
)
def leave_activity(
    activity_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    activity_participant_service.leave_activity(
        db=db,
        user_id=str(current_user.id),
        activity_id=activity_id,
    )