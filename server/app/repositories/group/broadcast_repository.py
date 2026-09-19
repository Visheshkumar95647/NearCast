from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.group.broadcast import Broadcast


class BroadcastRepository:

    def create(
    self,
    db: Session,
    broadcast: Broadcast,
    ) -> Broadcast:

        db.add(broadcast)
        db.flush()
        db.refresh(broadcast)
        # here we don't do commit because we have other service have to then only we have to store the broadcast into the database services like postgis and websocket suppose if broadcast save and later on webscoket don't to solve this.
        return broadcast

    def get_by_id(
        self,
        db: Session,
        broadcast_id: str,
    ) -> Broadcast | None:

        return db.get(Broadcast, broadcast_id)

    def get_by_group_id(
        self,
        db: Session,
        group_id: str,
    ) -> list[Broadcast]:

        result = db.execute(
            select(Broadcast)
            .where(Broadcast.group_id == group_id)
            .order_by(Broadcast.sent_at.desc())
        )

        return list(result.scalars().all())