from datetime import date
from unittest.mock import MagicMock

import pytest

from app.models.user import User
from app.schemas.user import UserCreate
from app.services.user_service import UserNotFoundError, UserService


def _build_user() -> User:
    return User(
        family_name="Doe",
        given_name="Jane",
        birth_date=date(1990, 1, 2),
        email="jane.doe@example.com",
    )


def test_user_service_create_user_success(valid_user_payload) -> None:
    repository = MagicMock()
    repository.get_by_email.return_value = None
    created_user = _build_user()
    created_user.id = 1
    repository.create.return_value = created_user
    repository.get_by_id.return_value = created_user
    service = UserService(repository=repository)
    payload = UserCreate(**valid_user_payload)

    result = service.create_user(payload)
    fetched = service.get_user(1)

    assert result.family_name == created_user.family_name
    assert result.given_name == created_user.given_name
    assert result.birth_date == created_user.birth_date
    assert result.email == created_user.email
    assert fetched is created_user
    repository.create.assert_called_once()
    repository.get_by_id.assert_called_once_with(1)


def test_user_service_get_user_not_found() -> None:
    repository = MagicMock()
    repository.get_by_id.return_value = None
    service = UserService(repository=repository)

    with pytest.raises(UserNotFoundError):
        service.get_user(1)


def test_user_service_delete_user_success() -> None:
    user = _build_user()
    repository = MagicMock()
    repository.get_by_id.return_value = user
    service = UserService(repository=repository)

    service.delete_user(1)

    repository.delete.assert_called_once_with(user)


def test_user_service_delete_user_not_found() -> None:
    repository = MagicMock()
    repository.get_by_id.return_value = None
    service = UserService(repository=repository)

    with pytest.raises(UserNotFoundError):
        service.delete_user(1)


def test_user_service_search_users_by_family_name() -> None:
    repository = MagicMock()
    matched_users = [_build_user()]
    repository.search_by_family_name.return_value = matched_users
    service = UserService(repository=repository)

    result = service.search_users_by_family_name("Doe")

    assert result == matched_users
    repository.search_by_family_name.assert_called_once_with("Doe")
