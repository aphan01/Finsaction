from .base import *

SECRET_KEY = "ci-only-secret-key"
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "testdb.sqlite3",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
CORS_ALLOW_ALL_ORIGINS = True