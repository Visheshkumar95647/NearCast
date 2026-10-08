from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.group.group_member import GroupMember
from app.models.user.user import User
from uuid import UUID

class GroupMemberRepository:

    def get_by_user_and_group(
        self,
        db: Session,
        user_id: str,
        group_id: UUID,
    ) -> GroupMember | None:

        result = db.execute(
            select(GroupMember).where(
                GroupMember.user_id == user_id,
                GroupMember.group_id == group_id,
            )
        )

        return result.scalar_one_or_none()

    def create(
        self,
        db: Session,
        group_member: GroupMember,
    ) -> GroupMember:

        db.add(group_member)
        db.commit()
        db.refresh(group_member)

        return group_member

    def delete(
        self,
        db: Session,
        group_member: GroupMember,
    ) -> None:

        db.delete(group_member)
        db.commit()

    def get_members(
        self,
        db: Session,
        group_id: UUID,
    ) -> list[tuple[GroupMember, User]]:

        result = db.execute(
            select(GroupMember, User)
            .join(User, User.id == GroupMember.user_id)
            .where(GroupMember.group_id == group_id)
            .order_by(GroupMember.joined_at.asc())
        )

        return list(result.all())

    def get_admins_by_group_id(
        self,
        db: Session,
        group_id: UUID,
    ) -> list[GroupMember]:

        result = db.execute(
            select(GroupMember).where(
                GroupMember.group_id == group_id,
                GroupMember.role == "admin",
            )
        )

        return list(result.scalars().all())

    def is_admin(
        self,
        db: Session,
        user_id: str,
        group_id: UUID,
    ) -> bool:

        result = db.execute(
            select(GroupMember.id).where(
                GroupMember.user_id == user_id,
                GroupMember.group_id == group_id,
                GroupMember.role == "admin",
            )
        )

        return result.scalar_one_or_none() is not None
    def get_user_ids_by_group_id(
    self,
    db: Session,
    group_id: UUID,
) -> list[str]:

        result = db.execute(
        select(GroupMember.user_id).where(
            GroupMember.group_id == group_id,
        )
    )

        return [str(user_id) for user_id in result.scalars().all()]