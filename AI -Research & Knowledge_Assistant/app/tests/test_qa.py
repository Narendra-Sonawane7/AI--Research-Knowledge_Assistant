from fastapi.testclient import (
    TestClient
)

from app.main import app

client = TestClient(
    app
)


def test_qa():

    response = client.post(
        "/qa",
        json={
            "question":
            "What is AI?"
        }
    )

    assert response.status_code == 200