from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def _create_user(client: TestClient, email: str = "jane.doe@example.com") -> dict:
    payload = {
        "family_name": "Doe",
        "given_name": "Jane",
        "birthdate": "1990-01-02",
        "email": email,
    }
    response = client.post("/api/users", json=payload)
    assert response.status_code == 201
    return response.json()


def test_grant_permission_and_get_permission_success(client: TestClient) -> None:
    user = _create_user(client)
    payload = {
        "type": "admin",
        "granted_date": "2026-04-08",
        "user_id": user["id"],
    }

    create_response = client.post("/api/permissions", json=payload)
    assert create_response.status_code == 201

    created = create_response.json()
    assert created["id"] > 0
    assert created["type"] == payload["type"]
    assert created["granted_date"] == payload["granted_date"]
    assert created["user_id"] == payload["user_id"]

    get_response = client.get(f"/api/permissions/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json() == created


def test_grant_permission_validation_error_returns_422(client: TestClient) -> None:
    user = _create_user(client)
    bad_payload = {
        "type": "admin",
        "granted_date": "not-a-date",
        "user_id": user["id"],
    }

    response = client.post("/api/permissions", json=bad_payload)

    assert response.status_code == 422


def test_grant_permission_for_missing_user_returns_404(client: TestClient) -> None:
    payload = {
        "type": "admin",
        "granted_date": "2026-04-08",
        "user_id": 99999,
    }

    response = client.post("/api/permissions", json=payload)

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_get_permission_not_found_returns_404(client: TestClient) -> None:
    response = client.get("/api/permissions/99999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Permission not found"}


def test_list_permissions_can_filter_by_user_id(client: TestClient) -> None:
    user_1 = _create_user(client, email="jane.one@example.com")
    user_2 = _create_user(client, email="jane.two@example.com")

    permission_1 = {
        "type": "admin",
        "granted_date": "2026-04-08",
        "user_id": user_1["id"],
    }
    permission_2 = {
        "type": "viewer",
        "granted_date": "2026-04-09",
        "user_id": user_2["id"],
    }

    r1 = client.post("/api/permissions", json=permission_1)
    r2 = client.post("/api/permissions", json=permission_2)
    assert r1.status_code == 201
    assert r2.status_code == 201

    response = client.get(f"/api/permissions?user_id={user_1['id']}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == user_1["id"]
    assert data[0]["type"] == "admin"
