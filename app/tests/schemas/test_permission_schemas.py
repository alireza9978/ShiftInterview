from datetime import date
from typing import Any

from app.schemas.permission import PermissionCreate


def test_valid_permission_payload(valid_permission_payload: dict[str, Any]) -> None:
    payload = PermissionCreate(**valid_permission_payload)

    assert payload.type == "admin"
    assert payload.granted_date == date(2026, 4, 8)
    assert payload.user_id == 1
