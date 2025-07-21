"""WSGI configuration for FLEXT Web Django application.

This module provides the WSGI application callable for deployment to
production web servers like Gunicorn, uWSGI, or Apache mod_wsgi.

It exposes the WSGI callable as a module-level variable named ``application``
which is used by Django-compatible web servers to serve the application.
"""

from __future__ import annotations

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flext_web.settings.production")

application = get_wsgi_application()
