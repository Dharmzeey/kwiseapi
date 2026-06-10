"""
Kwise World — development settings.

Usage:
    DJANGO_SETTINGS_MODULE=kwiseapi.settings.dev python manage.py runserver
"""
from .base import *  # noqa: F401, F403

DEBUG = True

# Dev uses a fixed insecure key — override SECRET_KEY from base if not set
import os
if not os.environ.get("SECRET_KEY"):
    SECRET_KEY = "django-insecure-dev-only-kwise-world-2026"  # noqa: F811

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "*"]

# SQLite — zero config for local development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

# Local media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"  # noqa: F405

# Loose CORS for local frontend dev servers
CORS_ALLOWED_ORIGINS = [  # noqa: F811
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Include ngrok tunnels if provided (comma-separated in DEV_EXTRA_HOSTS env var)
import os as _os
_extra = _os.environ.get("DEV_EXTRA_HOSTS", "")
if _extra:
    ALLOWED_HOSTS += [h.strip() for h in _extra.split(",") if h.strip()]
