from datetime import date
from unittest.mock import MagicMock

import pytest

from app.models.permission import Permission
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.permission import PermissionCreate
from app.services.permission_service import (
    PermissionNotFoundError,
    PermissionService,
    UserNotFoundError,
)


def _build_user() -> User:
    return User(
        family_name="Doe",
        given_name="Jane",
        birth_date=date(1990, 1, 2),
        email="jane.doe@example.com",
    )


def _build_permission() -> Permission:
    return Permission(
        type="admin",
        granted_date=date(2026, 4, 8),
        user_id=1,
    )


def test_permission_service_grant_permission_success(valid_permission_payload) -> None:
    db = MagicMock()
    db.refresh.return_value = None
    repository = MagicMock()
    repository.create.return_value = _build_permission()
    user_repository = MagicMock(spec=UserRepository)
    user_repository.get_by_id.return_value = _build_user()
    service = PermissionService(
        repository=repository,
        user_repository=user_repository,
        db=db,
    )
    payload = PermissionCreate(**valid_permission_payload)

    result = service.grant_permission(payload)

    assert result.user_id == 1
    repository.create.assert_called_once()
    user_repository.get_by_id.assert_called_once_with(1)
    db.commit.assert_called_once()


def test_permission_service_grant_permission_missing_user() -> None:
    db = MagicMock()
    user_repository = MagicMock(spec=UserRepository)
    user_repository.get_by_id.return_value = None
    service = PermissionService(
        repository=MagicMock(),
        user_repository=user_repository,
        db=db,
    )
    payload = PermissionCreate(type="admin", granted_date=date(2026, 4, 8), user_id=99)

    with pytest.raises(UserNotFoundError):
        service.grant_permission(payload)


def test_permission_service_revoke_permission_success() -> None:
    permission = _build_permission()
    repository = MagicMock()
    repository.get_by_id.return_value = permission
    db = MagicMock()
    service = PermissionService(
        repository=repository,
        user_repository=MagicMock(spec=UserRepository),
        db=db,
    )

    service.revoke_permission(1)

    repository.delete.assert_called_once_with(permission)
    db.commit.assert_called_once()


def test_permission_service_revoke_permission_not_found() -> None:
    repository = MagicMock()
    repository.get_by_id.return_value = None
    service = PermissionService(
        repository=repository,
        user_repository=MagicMock(spec=UserRepository),
        db=MagicMock(),
    )

    with pytest.raises(PermissionNotFoundError):
        service.revoke_permission(1)
