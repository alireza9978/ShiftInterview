from sqlalchemy.orm import Session

from app.models.permission import Permission
from app.models.user import User
from app.repositories.permission_repository import PermissionRepository
from app.schemas.permission import PermissionCreate


class PermissionNotFoundError(Exception):
    """Raised when trying to access a permission that doesn't exist."""

    pass


class UserNotFoundError(Exception):
    """Raised when trying to grant permission to a user that doesn't exist."""

    pass


class PermissionService:
    """
    Service layer for Permission logic.
    """

    def __init__(self, repository: PermissionRepository, db: Session) -> None:
        self.repository = repository
        self.db = db

    def list_permissions(self, user_id: int | None = None) -> list[Permission]:
        """
        Get permissions, optionally filtered by user.
        """
        if user_id is not None:
            return self.repository.list_by_user(user_id)
        return self.repository.list_all()

    def get_permission(self, permission_id: int) -> Permission:
        """
        Get a permission by ID.
        """
        permission = self.repository.get_by_id(permission_id)
        if permission is None:
            raise PermissionNotFoundError(
                f"Permission with ID {permission_id} not found"
            )
        return permission

    def grant_permission(self, payload: PermissionCreate) -> Permission:
        """
        Create and Grant a permission to a user.
        """
        # user must exist
        user = self.db.get(User, payload.user_id)
        if user is None:
            raise UserNotFoundError(f"User with ID {payload.user_id} not found")

        # Create new Permission model from validated schema data
        permission = Permission(
            type=payload.type,
            granted_date=payload.granted_date,
            user_id=payload.user_id,
        )

        # Persist to database
        self.repository.create(permission)
        self.db.commit()
        self.db.refresh(permission)
        return permission

    def revoke_permission(self, permission_id: int) -> None:
        """
        Revoke and Delete a permission by ID.
        """
        permission = self.repository.get_by_id(permission_id)
        if permission is None:
            raise PermissionNotFoundError(
                f"Permission with ID {permission_id} not found"
            )

        self.repository.delete(permission)
        self.db.commit()
