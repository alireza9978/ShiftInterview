from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.permission import Permission


class PermissionRepository:
    """
    Repository for Permission persistence operations.
    Handles all database queries for Permission entities.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[Permission]:
        """Fetch all permissions from database."""
        stmt = select(Permission)
        return list(self.db.scalars(stmt).all())

    def list_by_user(self, user_id: int) -> list[Permission]:
        """Fetch all permissions for a specific user."""
        stmt = select(Permission).where(Permission.user_id == user_id)
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, permission_id: int) -> Permission | None:
        """Fetch a permission by ID. Returns None if not found."""
        return self.db.get(Permission, permission_id)

    def create(self, permission: Permission) -> Permission:
        """
        Add a permission to the database session.
        """
        self.db.add(permission)
        return permission

    def delete(self, permission: Permission) -> None:
        """
        Mark a permission for deletion in the database session.
        """
        self.db.delete(permission)
