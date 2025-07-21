"""URL configuration for FLEXT Web Django application.

This module defines the main URL routing for the FLEXT Web interface,
including REDACTED_LDAP_BIND_PASSWORD interface, dashboard, and API endpoints for the
enterprise Meltano platform.
"""

from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import REDACTED_LDAP_BIND_PASSWORD
from django.urls import include, path

urlpatterns = [
    path("REDACTED_LDAP_BIND_PASSWORD/", REDACTED_LDAP_BIND_PASSWORD.site.urls),
    # Working dashboard for Django functionality testing
    path("", include("flext_web.apps.dashboard.urls_simple")),
    # Enterprise app URLs - now enabled
    path("pipelines/", include("flext_web.apps.pipelines.urls")),
    path("monitoring/", include("flext_web.apps.monitoring.urls")),
    path("projects/", include("flext_web.apps.projects.urls")),
    path("users/", include("flext_web.apps.users.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
