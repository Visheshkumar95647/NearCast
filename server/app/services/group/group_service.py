from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.group.group import Group
from app.repositories.group.group_repository import GroupRepository
from app.models.group.group_member import GroupMember
from datetime import datetime, timezone

from app.models.group.group_member import GroupMember


class GroupService:

    def __init__(self):
        self.group_repository = GroupRepository()

    def create_group(
        self,
        db: Session,
        user_id: str,
        name: str,
        description: str | None,
        is_private: bool,
    ) -> Group:

        group = Group(
            name=name,
            description=description,
            is_private=is_private,
            is_active=True,
        )

        self.group_repository.create(
            db,
            group,
        )

        group_member = GroupMember(
            user_id=user_id,
            group_id=group.id,
            role="admin",
            joined_at=datetime.now(timezone.utc),
        )     

        db.add(group_member)
        db.commit()

        return group

    def get_group(
        self,
        db: Session,
        group_id: str,
    ) -> Group:

        group = self.group_repository.get_by_id(
            db,
            group_id,
        )

        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found",
            )

        return group

    def get_groups(
        self,
        db: Session,
    ) -> list[Group]:

        return self.group_repository.get_all(db)

    def update_group(
        self,
        db: Session,
        group_id: str,
        name: str | None,
        description: str | None,
        is_private: bool | None,
        is_active: bool | None,
    ) -> Group:

        group = self.group_repository.get_by_id(
            db,
            group_id,
        )

        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found",
            )

        if name is not None:
            group.name = name

        if description is not None:
            group.description = description

        if is_private is not None:
            group.is_private = is_private

        if is_active is not None:
            group.is_active = is_active

        return self.group_repository.update(
            db,
            group,
        )

    def delete_group(
        self,
        db: Session,
        group_id: str,
    ) -> None:

        group = self.group_repository.get_by_id(
            db,
            group_id,
        )

        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found",
            )

        self.group_repository.delete(
            db,
            group,
        )
