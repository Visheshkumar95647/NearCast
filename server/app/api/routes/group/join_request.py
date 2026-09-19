from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user.user import User
from app.schemas.group.group_member import JoinRequestResponse
from app.services.common.join_request_service import JoinRequestService


router = APIRouter(
    prefix="/groups",
    tags=["Join Requests"],
)

join_request_service = JoinRequestService()


@router.get(
    "/{group_id}/join-requests",
    response_model=list[JoinRequestResponse],
)
def get_group_requests(
    group_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return join_request_service.get_group_requests(
        db=db,
        user_id=str(current_user.id),
        group_id=group_id,
    )


@router.get(
    "/{group_id}/join-request/me",
    response_model=JoinRequestResponse | None,
)
def get_my_request(
    group_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return join_request_service.get_user_request(
        db=db,
        user_id=str(current_user.id),
        group_id=group_id,
    )


@router.patch(
    "/join-requests/{request_id}/approve",
    response_model=JoinRequestResponse,
)
def approve_request(
    request_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return join_request_service.approve_request(
        db=db,
        user_id=str(current_user.id),
        request_id=request_id,
    )


@router.patch(
    "/join-requests/{request_id}/reject",
    response_model=JoinRequestResponse,
)
def reject_request(
    request_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return join_request_service.reject_request(
        db=db,
        user_id=str(current_user.id),
        request_id=request_id,
    )