"""Celery configuration for FLEXT Web."""

from __future__ import annotations

# Removed circular dependency - use DI pattern
# Resolved: Circular dependency issue using DI pattern
import logging
import os
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from celery import Celery
    from celery.app.task import Task as CeleryTask
else:
    try:
        from celery import Celery
        from celery.app.task import Task as CeleryTask
    except ImportError:
        Celery = Any
        CeleryTask = Any
logger = logging.getLogger(__name__)
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


@app.task(bind=True)
def debug_task(self: CeleryTask) -> str:
    """Debug task for testing Celery functionality."""
    logger.info("Request: %r", self.request)
    return "Debug task completed"
