"""Celery configuration for FLEXT Web."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

from flext_observability.logging import get_logger

if TYPE_CHECKING:
    from celery import Celery
    from celery.app.task import Task as CeleryTask
else:
    try:
        from celery import Celery  # type: ignore[import-untyped]
        from celery.app.task import Task as CeleryTask  # type: ignore[import-untyped]
    except ImportError:
        Celery = Any  # type: ignore[misc,assignment]
        CeleryTask = Any

logger = get_logger(__name__)

# Set the default Django settings module
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "flext_web.flext_web_legacy.settings.production",
)

# Create Celery app
app: Celery = Celery("flext_web")

# Load configuration from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()


@app.task(bind=True)  # type: ignore[misc]
def debug_task(self: CeleryTask) -> str:
    """Debug task for testing Celery functionality."""
    logger.info("Request: %r", self.request)
    return "Debug task completed"
