import app as app_module

def test_homepage():
    client = app_module.app.test_client()
    response = client.get("/")
    assert response.status_code == 200

def test_health():
    client = app_module.app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"
