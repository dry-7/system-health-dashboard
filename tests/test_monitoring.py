
import json

from app import app
from prometheus_client import REGISTRY


def test_metrics():
    with app.test_client() as client:
        response = client.get("/metrics")

        assert response.status_code == 200
        data = response.get_data(as_text=True)

        assert "http_requests_total" in data
        assert "http_request_duration_seconds" in data
        assert "app_info" in data


def test_request_counter():
    labels = {
        "method": "GET",
        "endpoint": "/health",
        "status": "200",
    }

    before = REGISTRY.get_sample_value(
        "http_requests_total", labels
    ) or 0

    with app.test_client() as client:
        client.get("/health")

    after = REGISTRY.get_sample_value(
        "http_requests_total", labels
    )

    assert after == before + 1


def test_fault_injection_disabled(monkeypatch):
    monkeypatch.delenv(
        "ENABLE_FAULT_INJECTION", raising=False
    )

    with app.test_client() as client:
        response = client.get("/simulate-error")

        assert response.status_code == 404


def test_fault_injection_enabled(monkeypatch):
    monkeypatch.setenv(
        "ENABLE_FAULT_INJECTION", "true"
    )

    with app.test_client() as client:
        response = client.get("/simulate-error")

        assert response.status_code == 500


def test_json_logging(capsys):
    with app.test_client() as client:
        client.get("/health")

    output = capsys.readouterr().out.strip()
    log = json.loads(output.splitlines()[-1])

    assert log["endpoint"] == "/health"
    assert log["method"] == "GET"
    assert log["status"] == 200
    assert log["level"] == "INFO"
    assert "timestamp" in log
    assert "environment" in log
