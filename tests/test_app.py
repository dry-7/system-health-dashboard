from app import app


# Test 1: Health endpoint
def test_health():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "UP"}


# Test 2: Version endpoint
def test_version():
    client = app.test_client()
    response = client.get("/version")

    assert response.status_code == 200
    assert response.get_json() == {"version": "1.0.0"}


# Test 3: Environment endpoint
def test_environment(monkeypatch):
    monkeypatch.setenv("APP_ENV", "testing")

    client = app.test_client()
    response = client.get("/environment")

    assert response.status_code == 200
    assert response.get_json() == {"environment": "testing"}