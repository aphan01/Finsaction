from .base import *

DEBUG = False
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = ["finsaction.com", 
                 "www.finsaction.com",
                 "127.0.0.1",
                 "localhost",
]

# CORS + CSRF
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://app.finsaction.com",
]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "https://app.finsaction.com",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
# Database uses env vars injected in Docker/Render/etc.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("PG_HOST"),
        "PORT": os.getenv("PG_PORT", "5432"),
        "NAME": os.getenv("PG_DB"),
        "USER": os.getenv("PG_USER"),
        "PASSWORD": os.getenv("PG_PASSWORD"),
    }
}


# Email: real provider in prod
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("SENDGRID_USER")
EMAIL_HOST_PASSWORD = os.getenv("SENDGRID_PASS")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "no-reply@finsaction.com"

# JWT lifetimes (shorter for access)
from datetime import timedelta
SIMPLE_JWT.update({
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
})


REST_FRAMEWORK.update({
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "user": "100/min",   # adjust later
        "anon": "30/min",
    },
})