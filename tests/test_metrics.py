from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    content = response.text
    assert "cpu_usage_percent" in content
    assert "memory_usage_percent" in content

