from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_prediction_endpoint_returns_disclaimer():
    response = client.post(
        "/predict",
        json={"features": {"temperature": 22.5, "humidity": 61.0, "pressure": 1012.4}},
    )
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["prediction"], float)
    assert body["model_version"] == "demo-0.1.0"
    assert "Synthetic demonstration" in body["disclaimer"]


def test_prediction_rejects_missing_feature():
    response = client.post("/predict", json={"features": {"temperature": 22.5}})
    assert response.status_code == 422
