from app.models.permission import Permission
from app.repositories.permission_repository import PermissionRepository
from app.repositories.user_repository import UserRepository
from app.schemas.permission import PermissionCreate


class PermissionNotFoundError(Exception):
    """Raised when trying to access a permission that doesn't exist."""

    pass


class UserNotFoundError(Exception):
    """Raised when trying to grant permission to a user that doesn't exist."""

    pass


class DuplicatePermissionError(Exception):
    """Raised when trying to grant a duplicate permission type to the same user."""

    pass


class PermissionService:
    """
    Service layer for Permission logic.
    """

    def __init__(
        self,
        repository: PermissionRepository,
        user_repository: UserRepository,
    ) -> None:
        self.repository = repository
        self.user_repository = user_repository

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
        user = self.user_repository.get_by_id(payload.user_id)
        if user is None:
            raise UserNotFoundError(f"User with ID {payload.user_id} not found")

        existing_permission = self.repository.get_by_user_and_type(
            payload.user_id,
            payload.type,
        )
        if existing_permission is not None:
            raise DuplicatePermissionError(
                f"User with ID {payload.user_id} already has permission type '{payload.type}'"
            )

        # Create new Permission model from validated schema data
        permission = Permission(
            type=payload.type,
            granted_date=payload.granted_date,
            user_id=payload.user_id,
        )

        # Persist to database
        return self.repository.create(permission)

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
