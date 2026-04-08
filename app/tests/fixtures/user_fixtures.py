from datetime import date

import pytest


@pytest.fixture()
def valid_user_payload() -> dict[str, object]:
    return {
        "family_name": "Doe",
        "given_name": "Jane",
        "birthdate": date(1990, 1, 2),
        "email": "jane.doe@example.com",
    }


@pytest.fixture()
def valid_user_json_payload() -> dict[str, str]:
    return {
        "family_name": "Doe",
        "given_name": "Jane",
        "birthdate": "1990-01-02",
        "email": "jane.doe@example.com",
    }