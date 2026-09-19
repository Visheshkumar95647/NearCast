from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user.user import User
from app.schemas.group.broadcast import BroadcastCreate, BroadcastResponse
from app.services.group.broadcast_service import BroadcastService


router = APIRouter(
    prefix="/groups",
    tags=["Group Broadcasts"],
)


broadcast_service = BroadcastService()


@router.post(
    "/{group_id}/broadcasts",
    response_model=BroadcastResponse,
)
async def create_broadcast(
    group_id: str,
    data: BroadcastCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return await broadcast_service.create_broadcast(
        db=db,
        user_id=str(current_user.id),
        group_id=group_id,
        content=data.content,
        radius_meters=data.radius_meters,
    )


@router.get(
    "/{group_id}/broadcasts",
    response_model=list[BroadcastResponse],
)
def get_group_broadcasts(
    group_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return broadcast_service.get_group_broadcasts(
        db=db,
        group_id=group_id,
    )