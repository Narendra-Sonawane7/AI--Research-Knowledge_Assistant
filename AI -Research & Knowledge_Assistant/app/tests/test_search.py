from fastapi.testclient import (
    TestClient
)

from app.main import app

client = TestClient(
    app
)


def test_search():

    response = client.post(
        "/search",
        json={
            "query":
            "machine learning"
        }
    )

    assert response.status_code == 200