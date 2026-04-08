from fastapi.testclient import TestClient


def test_get_users_returns_200(client: TestClient) -> None:
    response = client.get("/api/users")

    assert response.status_code == 200
    assert response.json() == []


def test_post_users_returns_201_with_valid_payload(client: TestClient, valid_user_json_payload) -> None:
    response = client.post("/api/users", json=valid_user_json_payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["family_name"] == valid_user_json_payload["family_name"]
    assert data["given_name"] == valid_user_json_payload["given_name"]
    assert data["birthdate"] == valid_user_json_payload["birthdate"]
    assert data["email"] == valid_user_json_payload["email"]


def test_post_users_returns_422_for_invalid_payload(client: TestClient, valid_user_json_payload) -> None:
    valid_user_json_payload["email"] = "not-an-email"

    response = client.post("/api/users", json=valid_user_json_payload)

    assert response.status_code == 422


def test_get_user_returns_200_for_existing_user(client: TestClient, valid_user_json_payload) -> None:
    create_response = client.post("/api/users", json=valid_user_json_payload)
    user_id = create_response.json()["id"]

    response = client.get(f"/api/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_get_user_returns_404_for_missing_user(client: TestClient) -> None:
    response = client.get("/api/users/99999")

    assert response.status_code == 404
    assert response.json() == {"detail": "User with ID 99999 not found"}


def test_delete_user_returns_204(client: TestClient, valid_user_json_payload) -> None:
    create_response = client.post("/api/users", json=valid_user_json_payload)
    user_id = create_response.json()["id"]

    response = client.delete(f"/api/users/{user_id}")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_user_returns_404_for_missing_user(client: TestClient) -> None:
    response = client.delete("/api/users/99999")

    assert response.status_code == 404
    assert response.json() == {"detail": "User with ID 99999 not found"}