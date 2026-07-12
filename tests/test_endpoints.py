from fastapi.testclient import TestClient


def test_post_events(client: TestClient) -> None:
    json1 = {
        "camera_id": "CAM-01",
        "timestamp": "2026-06-01T09:00:00+00:00",
        "event_type": "intrusion",
        "confidence": 0.95,
    }
    response = client.post("/events", json=json1)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 0
    assert data["event"]["camera_id"] == "CAM-01"


def test_get_event(client: TestClient) -> None:
    json1 = {
        "camera_id": "CAM-01",
        "timestamp": "2026-06-01T09:00:00+00:00",
        "event_type": "loitering",
        "confidence": 0.9,
    }
    client.post("/events", json=json1)
    response = client.get("/events/0")
    assert response.status_code == 200
    data = response.json()
    assert data["camera_id"] == "CAM-01"
    assert data["event_type"] == "loitering"


def test_get_nonexistent(client: TestClient) -> None:
    response = client.get("/events/9999")
    assert response.status_code == 404


async def test_receive_broadcast(client: TestClient) -> None:
    with client.websocket_connect("/ws/events") as c1:
        with client.websocket_connect("/ws/events") as c2:
            json1 = {
                "camera_id": "CAM-01",
                "timestamp": "2026-06-01T09:00:00+00:00",
                "event_type": "departure",
                "confidence": 0.85,
            }
            client.post("/events", json=json1)
            j1 = c1.receive_json()
            j2 = c2.receive_json()
            assert j1["event_type"] == "departure"
            assert j2["event_type"] == "departure"
