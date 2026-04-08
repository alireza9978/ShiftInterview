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
        birthdate=date(1990, 1, 2),
        email="jane.doe@example.com",
    )


def test_user_service_create_user_success(valid_user_payload) -> None:
    repository = MagicMock()
    repository.get_by_email.return_value = None
    created_user = _build_user()
    repository.get_by_id.return_value = created_user
    db = MagicMock()
    service = UserService(repository=repository, db=db)
    payload = UserCreate(**valid_user_payload)

    db.refresh.return_value = None

    result = service.create_user(payload)
    fetched = service.get_user(1)

    assert result.family_name == created_user.family_name
    assert result.given_name == created_user.given_name
    assert result.birthdate == created_user.birthdate
    assert result.email == created_user.email
    assert fetched is created_user
    repository.create.assert_called_once()
    repository.get_by_id.assert_called_once_with(1)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(repository.create.call_args.args[0])


def test_user_service_get_user_not_found() -> None:
    repository = MagicMock()
    repository.get_by_id.return_value = None
    service = UserService(repository=repository, db=MagicMock())

    with pytest.raises(UserNotFoundError):
        service.get_user(1)


def test_user_service_delete_user_success() -> None:
    user = _build_user()
    repository = MagicMock()
    repository.get_by_id.return_value = user
    db = MagicMock()
    service = UserService(repository=repository, db=db)

    service.delete_user(1)

    repository.delete.assert_called_once_with(user)
    db.commit.assert_called_once()


def test_user_service_delete_user_not_found() -> None:
    repository = MagicMock()
    repository.get_by_id.return_value = None
    service = UserService(repository=repository, db=MagicMock())

    with pytest.raises(UserNotFoundError):
        service.delete_user(1)

