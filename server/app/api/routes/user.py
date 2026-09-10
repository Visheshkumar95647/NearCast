from fastapi import APIRouter, Depends, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user.user import User

from app.schemas.user.interest import (
    AddInterestRequest,
    InterestResponse,
)
from app.schemas.user.location import (
    LocationResponse,
    LocationUpdateRequest,
)
from app.schemas.user.preference import (
    PreferenceResponse,
    PreferenceUpdateRequest,
)
from app.schemas.user.user import (
    UserProfileResponse,
    UserProfileUpdate,
)

from app.services.user.interest_service import InterestService
from app.services.user.location_service import LocationService
from app.services.user.preference_service import PreferenceService
from app.services.user.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


user_service = UserService()
interest_service = InterestService()
preference_service = PreferenceService()
location_service = LocationService()


# =========================
# User Profile
# =========================

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


# =========================
# User Interests
# =========================

@router.post(
    "/me/interests",
    response_model=InterestResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_interest(
    data: AddInterestRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    interest = interest_service.add_interest(
        db=db,
        user_id=str(current_user.id),
        name=data.name,
    )

    return InterestResponse(
        id=str(interest.id),
        name=interest.name,
    )


@router.get(
    "/me/interests",
    response_model=list[InterestResponse],
)
def get_my_interests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    interests = interest_service.get_user_interests(
        db=db,
        user_id=str(current_user.id),
    )

    return [
        InterestResponse(
            id=str(interest.id),
            name=interest.name,
        )
        for interest in interests
    ]


@router.delete(
    "/me/interests/{interest_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_interest(
    interest_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    interest_service.remove_interest(
        db=db,
        user_id=str(current_user.id),
        interest_id=interest_id,
    )


# =========================
# User Preferences
# =========================

@router.get(
    "/me/preferences",
    response_model=PreferenceResponse,
)
def get_my_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    preference = preference_service.get_preferences(
        db=db,
        user_id=str(current_user.id),
    )

    return PreferenceResponse(
        id=str(preference.id),
        max_distance_km=preference.max_distance_km,
        preferred_group_size=preference.preferred_group_size,
        preferred_activity_type=preference.preferred_activity_type,
        notifications_enabled=preference.notifications_enabled,
    )


@router.patch(
    "/me/preferences",
    response_model=PreferenceResponse,
)
def update_my_preferences(
    data: PreferenceUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    preference = preference_service.update_preferences(
        db=db,
        user_id=str(current_user.id),
        max_distance_km=data.max_distance_km,
        preferred_group_size=data.preferred_group_size,
        preferred_activity_type=data.preferred_activity_type,
        notifications_enabled=data.notifications_enabled,
    )

    return PreferenceResponse(
        id=str(preference.id),
        max_distance_km=preference.max_distance_km,
        preferred_group_size=preference.preferred_group_size,
        preferred_activity_type=preference.preferred_activity_type,
        notifications_enabled=preference.notifications_enabled,
    )


# =========================
# User Location
# =========================

@router.get(
    "/me/location",
    response_model=LocationResponse,
)
def get_my_location(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    location = location_service.get_current_location(
        db=db,
        user_id=str(current_user.id),
    )

    latitude, longitude = db.execute(
        select(
            func.ST_Y(location.location),
            func.ST_X(location.location),
        )
    ).one()

    return LocationResponse(
        latitude=latitude,
        longitude=longitude,
    )


@router.patch(
    "/me/location",
    response_model=LocationResponse,
)
def update_my_location(
    data: LocationUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    location = location_service.update_location(
        db=db,
        user_id=str(current_user.id),
        latitude=data.latitude,
        longitude=data.longitude,
    )

    return LocationResponse(
        latitude=data.latitude,
        longitude=data.longitude,
    )