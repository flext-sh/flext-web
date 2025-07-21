"""Simplified Django settings for flext-api.web.flext-web testing."""

import os
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Simple settings for testing

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-temporary-key-for-testing-please-change-in-production",
)
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]

# Application definition
INSTALLED_APPS = [
    # Django Core
    "django.contrib.REDACTED_LDAP_BIND_PASSWORD",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Local apps - now enabled with namespace fixes
    "flext_web.apps.dashboard",
    "flext_web.apps.users",
    "flext_web.apps.projects",
    "flext_web.apps.pipelines",
    "flext_web.apps.monitoring",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "flext_web.flext_web_legacy.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "flext_web.flext_web_legacy.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    },
}

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "staticfiles")
STATICFILES_DIRS = [BASE_DIR / "static"]

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR / "media")

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
