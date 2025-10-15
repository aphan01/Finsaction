from .base import *

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Keep CORS minimal for now; we’ll fill with your frontend origin later.
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = []
CSRF_TRUSTED_ORIGINS = []