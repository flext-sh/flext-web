"""Celery configuration for FLEXT Web."""

import os

from celery import Celery
from celery.app.task import Task

# Use centralized logger from flext-observability - ELIMINATE DUPLICATION
from flext_observability.logging import get_logger

logger = get_logger(__name__)

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flext_web.flext_web_legacy.settings.production")

# Create Celery app
app = Celery("flext_web")

# Load configuration from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()


@app.task(bind=True)  # type: ignore[misc]
def debug_task(self: Task) -> str:
    logger.info("Request: %r", self.request)
    return "Debug task completed"
