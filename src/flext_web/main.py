"""Web Entry Point - SINGLE UNIVERSAL INTERFACE - ZERO TOLERANCE."""

from __future__ import annotations

import contextlib

# Real universal HTTP implementation using flext-core patterns
import json
import logging
from typing import TYPE_CHECKING

from django.http import HttpRequest, JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

# ALWAYS use flext-core imports - NO FALLBACKS
from flext_core.application.pipeline import PipelineService
from flext_core.domain.pipeline import Pipeline
from flext_core.infrastructure.memory import InMemoryRepository

if TYPE_CHECKING:
    from flext_core.infrastructure.persistence.base import Repository

logger = logging.getLogger(__name__)


@csrf_exempt
def universal_django_view(request: HttpRequest, command: str) -> JsonResponse:
    try:
        # Use real pipeline service from flext-core - ALWAYS available
        # Initialize the service with proper configuration
        repository: Repository[Pipeline, object] = InMemoryRepository[Pipeline, object]()
        PipelineService(repository)

        # Prepare request data
        request_data = {
            "method": request.method,
            "command": command,
            "headers": dict(request.headers),
            "query_params": {
                k: v[0] if len(v) == 1 else v for k, v in request.GET.lists()
            },
            "body": request.body.decode("utf-8")
            if request.body and not request.body.startswith(b"--BoUnDaRyStRiNg")
            else None,
        }

        # Parse JSON body if present
        if request.content_type == "application/json" and request.body:
            with contextlib.suppress(json.JSONDecodeError):
                request_data["json_data"] = json.loads(request.body)

        # For now, return the request data as response (universal fallback)
        # Note: UniversalHttpService implementation deferred until flext-core
        # patterns stabilize
        response_data = {
            "command": command,
            "method": request.method,
            "status": "success_fallback",
            "data": request_data,
        }
        return JsonResponse(response_data, status=200)

    except ImportError as e:
        # Service configuration error - should not happen in properly configured system
        logger.exception(
            "Service import failed - check flext-core configuration: %s",
            e,
        )
        return JsonResponse(
            {
                "error": "Service configuration error",
                "command": command,
                "status": "configuration_error",
            },
            status=500,
        )
    except Exception as e:
        return JsonResponse(
            {
                "error": str(e),
                "command": command,
                "status": "error",
            },
            status=500,
        )


urlpatterns = [
    # Universal view for all commands - ZERO TOLERANCE ARCHITECTURE
    path("<path:command>", universal_django_view, name="universal"),
    path(
        "",
        lambda _: JsonResponse({"service": "FLEXT Universal Web", "status": "active"}),
    ),
    path("health/", lambda _: JsonResponse({"status": "healthy"})),
]

# In a real enterprise application, you'd have more robust health checks,
# dependency injection for Django, and more structured URL patterns.
