from datetime import date

import pytest


@pytest.fixture()
def valid_permission_payload() -> dict[str, object]:
    return {
        "type": "admin",
        "granted_date": date(2026, 4, 8),
        "user_id": 1,
    }


@pytest.fixture()
def valid_permission_json_payload() -> dict[str, object]:
    return {
        "type": "admin",
        "granted_date": "2026-04-08",
        "user_id": 1,
    }