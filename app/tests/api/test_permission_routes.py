from fastapi.testclient import TestClient


def _create_user(client: TestClient, payload: dict[str, str]) -> dict[str, object]:
    response = client.post("/api/users", json=payload)
    assert response.status_code == 201
    return response.json()


def test_post_permissions_returns_201_for_valid_request(
    client: TestClient,
    valid_user_json_payload,
    valid_permission_json_payload,
) -> None:
    user = _create_user(client, valid_user_json_payload)
    valid_permission_json_payload["user_id"] = user["id"]

    response = client.post("/api/permissions", json=valid_permission_json_payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["type"] == valid_permission_json_payload["type"]
    assert data["granted_date"] == valid_permission_json_payload["granted_date"]
    assert data["user_id"] == user["id"]


def test_post_permissions_returns_404_if_user_does_not_exist(
    client: TestClient,
    valid_permission_json_payload,
) -> None:
    valid_permission_json_payload["user_id"] = 99999

    response = client.post("/api/permissions", json=valid_permission_json_payload)

    assert response.status_code == 404
    assert response.json() == {"detail": "User with ID 99999 not found"}


def test_grant_and_revoke_permission_success(
    client: TestClient,
    valid_user_json_payload,
    valid_permission_json_payload,
) -> None:
    user = _create_user(client, valid_user_json_payload)
    valid_permission_json_payload["user_id"] = user["id"]
    permission_response = client.post("/api/permissions", json=valid_permission_json_payload)
    permission_id = permission_response.json()["id"]

    assert permission_response.status_code == 201

    response = client.delete(f"/api/permissions/{permission_id}")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_permissions_returns_404_for_missing_permission(client: TestClient) -> None:
    response = client.delete("/api/permissions/99999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Permission with ID 99999 not found"}