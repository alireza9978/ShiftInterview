from datetime import date
from typing import Any

import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate


def test_valid_user_creation_payload(valid_user_payload: dict[str, Any]) -> None:
    payload = UserCreate(**valid_user_payload)

    assert payload.family_name == "Doe"
    assert payload.given_name == "Jane"
    assert payload.birth_date == date(1990, 1, 2)
    assert str(payload.email) == "jane.doe@example.com"


def test_invalid_user_email_is_rejected(valid_user_payload: dict[str, Any]) -> None:
    payload = valid_user_payload.copy()
    payload["email"] = "not-an-email"

    with pytest.raises(ValidationError) as exc:
        UserCreate(**payload)

    assert "email" in str(exc.value)


def test_missing_required_user_fields_are_rejected() -> None:
    with pytest.raises(ValidationError) as exc:
        UserCreate.model_validate({"email": "jane.doe@example.com"})

    error_message = str(exc.value)
    assert "family_name" in error_message
    assert "given_name" in error_message
    assert "birth_date" in error_message
