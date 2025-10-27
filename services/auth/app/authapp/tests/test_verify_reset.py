import json
import pytest
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator as pr_token
from authapp.tokens import email_verification_token

@pytest.mark.django_db
def test_verify_marks_user_verified(client):
    U = get_user_model()
    u = U.objects.create_user(email="v@test.dev", password="Passw0rd!", is_active=True, is_email_verified=False)
    # login to get access
    r = client.post("/api/v1/auth/login",
                    data=json.dumps({"email":"v@test.dev","password":"Passw0rd!"}),
                    content_type="application/json")
    access = r.json()["access"]

    # simulate request-verify: build link and call verify
    uid = urlsafe_base64_encode(force_bytes(u.pk))
    tok = email_verification_token.make_token(u)
    r = client.get(f"/api/v1/auth/verify?uid={uid}&tok={tok}")
    assert r.status_code == 200

    u.refresh_from_db()
    assert u.is_email_verified is True
    assert u.email_verified_at is not None

@pytest.mark.django_db
def test_reset_password_flow(client):
    U = get_user_model()
    u = U.objects.create_user(email="pw@test.dev", password="OldPassw0rd!", is_active=True)
    uid = urlsafe_base64_encode(force_bytes(u.pk))
    tok = pr_token.make_token(u)

    # reset-password
    r = client.post(f"/api/v1/auth/reset-password?uid={uid}&tok={tok}",
                    data=json.dumps({"password":"NewPassw0rd!"}),
                    content_type="application/json")
    assert r.status_code == 200

    # login with new password
    r = client.post("/api/v1/auth/login",
                    data=json.dumps({"email":"pw@test.dev","password":"NewPassw0rd!"}),
                    content_type="application/json")
    assert r.status_code == 200
    assert "access" in r.json()
