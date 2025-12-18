from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "cpu" in data
    assert "memory" in data
    assert 0 <= data["cpu"] <= 100
    assert 0 <= data["memory"] <= 100
