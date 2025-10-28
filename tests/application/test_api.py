from fastapi.testclient import TestClient


def test_get_satellites(client: TestClient):
    response = client.get("/satellites?page=0&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_space_objects(client: TestClient):
    response = client.get("/space-objects?page=0&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
