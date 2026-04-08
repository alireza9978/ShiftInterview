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


def test_list_users_returns_200_and_empty_list(client: TestClient) -> None:
    response = client.get("/api/users")

    assert response.status_code == 200
    assert response.json() == []


def test_create_user_and_get_user_success(client: TestClient) -> None:
    payload = {
        "family_name": "Doe",
        "given_name": "Jane",
        "birthdate": "1990-01-02",
        "email": "jane.doe@example.com",
    }

    create_response = client.post("/api/users", json=payload)
    assert create_response.status_code == 201

    created = create_response.json()
    assert created["id"] > 0
    assert created["family_name"] == payload["family_name"]
    assert created["given_name"] == payload["given_name"]
    assert created["birthdate"] == payload["birthdate"]
    assert created["email"] == payload["email"]

    get_response = client.get(f"/api/users/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json() == created


def test_create_user_validation_error_returns_422(client: TestClient) -> None:
    bad_payload = {
        "family_name": "Doe",
        "given_name": "Jane",
        "birthdate": "1990-01-02",
        "email": "not-an-email",
    }

    response = client.post("/api/users", json=bad_payload)

    assert response.status_code == 422


def test_get_user_not_found_returns_404(client: TestClient) -> None:
    response = client.get("/api/users/99999")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
