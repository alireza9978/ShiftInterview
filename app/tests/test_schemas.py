from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas.permission import Permission, PermissionCreate
from app.schemas.user import User, UserCreate


def test_user_create_parses_required_fields() -> None:
    user = UserCreate(
        family_name="Doe",
        given_name="Jane",
        birthdate=date(1990, 1, 2),
        email="jane.doe@example.com",
    )

    assert user.family_name == "Doe"
    assert user.given_name == "Jane"
    assert user.birthdate == date(1990, 1, 2)
    assert user.email == "jane.doe@example.com"


def test_user_model_supports_from_attributes() -> None:
    class UserRecord:
        def __init__(self) -> None:
            self.id = 1
            self.family_name = "Doe"
            self.given_name = "Jane"
            self.birthdate = date(1990, 1, 2)
            self.email = "jane.doe@example.com"

    user = User.model_validate(UserRecord())

    assert user.id == 1
    assert user.family_name == "Doe"
    assert user.given_name == "Jane"
    assert user.birthdate == date(1990, 1, 2)
    assert user.email == "jane.doe@example.com"


def test_user_create_rejects_invalid_email() -> None:
    with pytest.raises(ValidationError):
        UserCreate(
            family_name="Doe",
            given_name="Jane",
            birthdate=date(1990, 1, 2),
            email="not-an-email",
        )


def test_permission_create_parses_required_fields() -> None:
    permission = PermissionCreate(type="admin", granted_date=date(2026, 4, 8))

    assert permission.type == "admin"
    assert permission.granted_date == date(2026, 4, 8)


def test_permission_model_supports_from_attributes() -> None:
    class PermissionRecord:
        def __init__(self) -> None:
            self.id = 99
            self.type = "admin"
            self.granted_date = date(2026, 4, 8)

    permission = Permission.model_validate(PermissionRecord())

    assert permission.id == 99
    assert permission.type == "admin"
    assert permission.granted_date == date(2026, 4, 8)
