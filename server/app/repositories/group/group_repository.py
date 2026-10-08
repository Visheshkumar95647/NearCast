from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.group.group import Group
from app.models.group.group_member import GroupMember


class GroupRepository:

    def get_by_id(
        self,
        db: Session,
        group_id: str,
    ) -> Group | None:
        return db.get(Group, group_id)

    def get_all_by_user(
        self,
        db: Session,
        user_id: str,
    ) -> list[Group]:
        result = db.execute(
            select(Group)
            .join(
                GroupMember,
                GroupMember.group_id == Group.id,
            )
            .where(
                GroupMember.user_id == user_id,
                Group.is_active.is_(True),
            )
            .order_by(Group.created_at.desc())
        )

        return list(result.scalars().all())

    def get_all(
        self,
        db: Session,
    ) -> list[Group]:
        result = db.execute(
            select(Group)
            .where(Group.is_active.is_(True))
            .order_by(Group.created_at.desc())
        )

        return list(result.scalars().all())

    def create(
        self,
        db: Session,
        group: Group,
    ) -> Group:
        db.add(group)
        db.commit()
        db.refresh(group)

        return group

    def update(
        self,
        db: Session,
        group: Group,
    ) -> Group:
        db.add(group)
        db.commit()
        db.refresh(group)

        return group

    def delete(
        self,
        db: Session,
        group: Group,
    ) -> None:
        db.delete(group)
        db.commit()