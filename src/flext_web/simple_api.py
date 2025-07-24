"""Simple API for FLEXT Web Configuration.

Provides simple functions for web configuration and setup.
"""

from __future__ import annotations

from typing import Any

from flext_web.config import WebConfig

# 🚨 ARCHITECTURAL COMPLIANCE: Using módulo raiz imports
# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container for flext-core imports
from flext_web.infrastructure.di_container import get_service_result

ServiceResult = get_service_result()


def get_web_settings() -> WebConfig:
    """Get web settings configuration."""
    return WebConfig()


def setup_web(settings: WebConfig | None = None) -> ServiceResult[Any]:
    """Set up web application."""
    try:
        if settings is None:
            settings = WebConfig()

        # Basic setup logic here
        return ServiceResult.ok(True)
    except Exception as e:
        return ServiceResult.fail(f"Web setup failed: {e}")
