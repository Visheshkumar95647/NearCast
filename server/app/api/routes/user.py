from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user.user import User
from app.schemas.user.user import UserProfileResponse, UserProfileUpdate
from app.services.user.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

user_service = UserService()


@router.get(
    "/me",
    response_model=UserProfileResponse,
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = user_service.get_profile(
        db=db,
        user_id=str(current_user.id),
    )

    return UserProfileResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        is_active=user.is_active,
    )


@router.patch(
    "/me",
    response_model=UserProfileResponse,
)
def update_my_profile(
    data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = user_service.update_profile(
        db=db,
        user_id=str(current_user.id),
        username=data.username,
        email=data.email,
    )

    return UserProfileResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        is_active=user.is_active,
    )