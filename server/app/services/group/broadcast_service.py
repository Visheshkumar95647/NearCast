from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.group.broadcast import Broadcast
from app.repositories.group.broadcast_repository import BroadcastRepository
from app.repositories.group.group_location_repository import GroupLocationRepository
from app.repositories.group.group_member_repository import GroupMemberRepository
from app.repositories.user.location_repository import LocationRepository
from app.schemas.websocket.broadcast import BroadcastWebSocketMessage
from app.websocket.manager import manager


class BroadcastService:

    def __init__(self):
        self.broadcast_repository = BroadcastRepository()
        self.group_member_repository = GroupMemberRepository()
        self.location_repository = LocationRepository()
        self.group_location_repository = GroupLocationRepository()

    async def create_broadcast(
        self,
        db: Session,
        user_id: str,
        group_id: str,
        content: str,
        radius_meters: float,
    ) -> Broadcast:

        if not self.group_member_repository.is_admin(
            db,
            user_id,
            group_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only group admins can send broadcasts",
            )

        group_location = self.group_location_repository.get_by_group_id(
            db,
            group_id,
        )

        if not group_location:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Group location is required to send a broadcast",
            )

        latitude, longitude = self.group_location_repository.get_coordinates(
            db,
            str(group_location.id),
        )

        nearby_user_ids = self.location_repository.get_nearby_users(
            db=db,
            latitude=latitude,
            longitude=longitude,
            radius_meters=radius_meters,
        )

        nearby_user_ids = [
            nearby_user_id
            for nearby_user_id in nearby_user_ids
            if nearby_user_id != user_id
        ]

        broadcast = Broadcast(
            group_id=group_id,
            sender_id=user_id,
            content=content,
            sent_at=datetime.now(timezone.utc),
        )

        broadcast = self.broadcast_repository.create(
            db,
            broadcast,
        )

        db.commit()
        db.refresh(broadcast)

        if not nearby_user_ids:
            return broadcast
        # if no user then no broadcast
        message = BroadcastWebSocketMessage(
            type="broadcast",
            broadcast_id=str(broadcast.id),
            group_id=str(broadcast.group_id),
            sender_id=str(broadcast.sender_id),
            content=broadcast.content,
            sent_at=broadcast.sent_at,
        )

        await manager.send_to_users(
            user_ids=nearby_user_ids,
            message=message.model_dump(mode="json"),
        )

        return broadcast

    def get_group_broadcasts(
        self,
        db: Session,
        group_id: str,
    ) -> list[Broadcast]:

        return self.broadcast_repository.get_by_group_id(
            db,
            group_id,
        )