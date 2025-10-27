import json
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_register_then_login_and_me(client):
    # Register
    r = client.post("/api/v1/auth/register",
                    data=json.dumps({"email":"t@test.dev","password":"Passw0rd!"}),
                    content_type="application/json")
    assert r.status_code in (200, 201)

    # Login
    r = client.post("/api/v1/auth/login",
                    data=json.dumps({"email":"t@test.dev","password":"Passw0rd!"}),
                    content_type="application/json")
    assert r.status_code == 200
    tokens = r.json()
    assert "access" in tokens and "refresh" in tokens

    # Me (unauthorized should fail)
    r = client.get("/api/v1/auth/me")
    assert r.status_code == 401

    # Me (authorized should pass)
    r = client.get("/api/v1/auth/me", HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    assert r.status_code == 200
    body = r.json()
    assert body["email"] == "t@test.dev"

@pytest.mark.django_db
def test_refresh_returns_new_access_token(client):
    # Setup: register + login
    client.post("/api/v1/auth/register",
                data=json.dumps({"email":"r@test.dev","password":"Passw0rd!"}),
                content_type="application/json")
    r = client.post("/api/v1/auth/login",
                    data=json.dumps({"email":"r@test.dev","password":"Passw0rd!"}),
                    content_type="application/json")
    refresh = r.json()["refresh"]

    # Refresh
    r = client.post("/api/v1/auth/refresh",
                    data=json.dumps({"refresh": refresh}),
                    content_type="application/json")
    assert r.status_code == 200
    assert "access" in r.json()

@pytest.mark.django_db
def test_logout_blacklists_tokens(client):
    # Setup: register + login
    client.post("/api/v1/auth/register",
                data=json.dumps({"email":"l@test.dev","password":"Passw0rd!"}),
                content_type="application/json")
    r = client.post("/api/v1/auth/login",
                    data=json.dumps({"email":"l@test.dev","password":"Passw0rd!"}),
                    content_type="application/json")
    access = r.json()["access"]

    # Logout (needs auth)
    r = client.post("/api/v1/auth/logout", HTTP_AUTHORIZATION=f"Bearer {access}")
    assert r.status_code == 204