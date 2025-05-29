import pytest
from fastapi.testclient import TestClient
from app.main import app
import numpy as np

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "timestamp" in response.json()
    assert "model_loaded" in response.json()

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "cpu_usage_percent" in response.text
    assert "memory_usage_percent" in response.text

def test_system_current():
    response = client.get("/system/current")
    assert response.status_code == 200
    data = response.json()
    assert "timestamp" in data
    assert "cpu_usage" in data
    assert "memory_usage" in data
    assert "memory_available" in data
    assert 0 <= data["cpu_usage"] <= 100
    assert 0 <= data["memory_usage"] <= 100

def test_predict():
    # First ensure we have a model
    response = client.get("/health")
    if not response.json()["model_loaded"]:
        pytest.skip("Model not loaded")
    
    response = client.get("/predict")
    assert response.status_code == 200
    data = response.json()
    assert "timestamp" in data
    assert "current_cpu" in data
    assert "predicted_cpu" in data
    assert "prediction_horizon" in data
    assert 0 <= data["predicted_cpu"] <= 100

def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "timestamp" in data
    assert "current_metrics" in data
    assert "last_prediction" in data
    assert "scaling_decision" in data
    assert "model_status" in data
    assert data["scaling_decision"] in ["scale_up", "scale_down", "no_action", "No prediction available"]

def test_invalid_endpoint():
    response = client.get("/invalid")
    assert response.status_code == 404 