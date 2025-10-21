import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all("description" in v for v in data.values())

def test_signup_and_duplicate():
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"
    # First signup should succeed
    res1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert res1.status_code == 200
    # Duplicate signup should fail
    res2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert res2.status_code == 400
    assert "already signed up" in res2.json()["detail"].lower()

def test_unregister():
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser2@mergington.edu"
    # Signup
    client.post(f"/activities/{activity}/signup?email={email}")
    # Unregister
    res = client.post(f"/activities/{activity}/unregister?email={email}")
    assert res.status_code == 200
    # Unregister again should fail
    res2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert res2.status_code == 400
    assert "not signed up" in res2.json()["detail"].lower()
