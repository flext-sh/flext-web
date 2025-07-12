"""Simple API for FLEXT Web Configuration.

Provides simple functions for web configuration and setup.
"""

from __future__ import annotations

from flext_core import ServiceResult
from flext_web.config import WebConfig


def get_web_settings() -> WebConfig:
    """Get web settings configuration."""
    return WebConfig()


def setup_web(settings: WebConfig | None = None) -> ServiceResult[bool]:
    """Setup web application."""
    try:
        if settings is None:
            settings = WebConfig()

        # Basic setup logic here
        return ServiceResult.success(True)
    except Exception as e:
        return ServiceResult.fail(f"Web setup failed: {e}")
