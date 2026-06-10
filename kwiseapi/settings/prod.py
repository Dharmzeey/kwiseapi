"""
Kwise World — production settings.

Usage:
    DJANGO_SETTINGS_MODULE=kwiseapi.settings.prod gunicorn kwiseapi.wsgi
"""
from .base import *  # noqa: F401, F403
import os

DEBUG = os.getenv('DEBUG', 'False') == 'True'

# ── Security ─────────────────────────────────────────────────────────────────
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# ── Database — PostgreSQL ─────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME":     os.environ["DB_NAME"],
        "USER":     os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST":     os.environ.get("DB_HOST", "localhost"),
        "PORT":     os.environ.get("DB_PORT", "5432"),
        "OPTIONS": {
            "connect_timeout": 10,
        },
    }
}

# ── Media storage — Backblaze B2 (S3-compatible) ──────────────────────────────
#
# Required env vars:
#   B2_KEY_ID          — Backblaze Application Key ID
#   B2_APPLICATION_KEY — Backblaze Application Key (secret)
#   B2_BUCKET_NAME     — Name of the B2 bucket
#   B2_ENDPOINT_URL    — e.g. https://s3.us-west-004.backblazeb2.com
#   B2_CUSTOM_DOMAIN   — (optional) CDN / public URL prefix for served files
#                        e.g. https://media.kwiseworld.com  or
#                             https://f004.backblazeb2.com/file/<bucket>
#
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

AWS_ACCESS_KEY_ID = os.environ.get('B2_APPLICATION_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('B2_APPLICATION_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('B2_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('B2_REALM', 'eu-central-003')
AWS_S3_ENDPOINT_URL = f'https://s3.{AWS_S3_REGION_NAME}.backblazeb2.com'

AWS_LOCATION = "media"
MEDIA_URL = f"https://{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/"

# AWS_S3_CUSTOM_DOMAIN = "media.kwiseworld.com"

STATIC_URL = "/static/"

# ── Logging ───────────────────────────────────────────────────────────────────
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "verbose": {
#             "format": "{levelname} {asctime} {module} {message}",
#             "style": "{",
#         },
#     },
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "formatter": "verbose",
#         },
#     },
#     "root": {
#         "handlers": ["console"],
#         "level": "WARNING",
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["console"],
#             "level": os.environ.get("DJANGO_LOG_LEVEL", "WARNING"),
#             "propagate": False,
#         },
#     },
# }
