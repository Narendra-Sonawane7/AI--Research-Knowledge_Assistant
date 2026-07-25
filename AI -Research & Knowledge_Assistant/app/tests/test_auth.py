from fastapi.testclient import (
    TestClient
)

from app.main import app

client = TestClient(
    app
)


def test_login():

    response = client.post(
        "/auth/login",
        json={
            "username":
            "admin",
            "password":
            "admin"
        }
    )

    assert response.status_code == 200