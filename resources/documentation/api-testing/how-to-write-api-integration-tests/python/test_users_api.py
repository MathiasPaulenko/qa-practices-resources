import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture()
def created_user():
    response = client.post("/api/users", json={
        "name": "John",
        "email": "john@test.dev",
    })
    assert response.status_code == 201
    user_id = response.json()["id"]
    yield user_id
    client.delete(f"/api/users/{user_id}")


class TestUserAPI:
    def test_crud_flow(self, created_user):
        response = client.get(f"/api/users/{created_user}")
        assert response.status_code == 200
        assert response.json()["name"] == "John"

        response = client.put(f"/api/users/{created_user}", json={
            "name": "Jane",
        })
        assert response.status_code == 200
        assert response.json()["name"] == "Jane"

        response = client.delete(f"/api/users/{created_user}")
        assert response.status_code == 204

        response = client.get(f"/api/users/{created_user}")
        assert response.status_code == 404
