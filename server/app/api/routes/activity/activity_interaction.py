from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user.user import User
from app.schemas.activity.interaction import (
    ActivityInteractionRequest,
    ActivityInteractionResponse,
)
from app.services.activity.interaction_service import (
    ActivityInteractionService,
)


router = APIRouter(
    prefix="/activities",
    tags=["Activity Interactions"],
)

interaction_service = ActivityInteractionService()


@router.post(
    "/{activity_id}/interactions",
    response_model=ActivityInteractionResponse,
    status_code=status.HTTP_201_CREATED,
)
def record_activity_interaction(
    activity_id: str,
    data: ActivityInteractionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    interaction = interaction_service.record_interaction(
        db=db,
        user_id=str(current_user.id),
        activity_id=activity_id,
        interaction_type=data.interaction_type,
    )

    return ActivityInteractionResponse(
        id=str(interaction.id),
        user_id=str(interaction.user_id),
        activity_id=str(interaction.activity_id),
        interaction_type=interaction.interaction_type,
        occurred_at=interaction.occurred_at,
    )