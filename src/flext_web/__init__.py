"""FLEXT Web - Enterprise Web Interface Platform.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Modern web interface platform following Clean Architecture and Domain-Driven Design.
Built on Python 3.13 with unified dashboards, APIs, and management interfaces.
"""

from __future__ import annotations

import importlib.metadata

# Import from flext-core for foundational patterns
from flext_core import FlextContainer, FlextResult

try:
    __version__ = importlib.metadata.version("flext-web")
except importlib.metadata.PackageNotFoundError:
    __version__ = "1.0.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

# Web API
from flext_web.api import FlextWebAPI, create_app

# Application services
from flext_web.application.services import (
    FlextDashboardService,
    FlextTemplateService,
    FlextWebAPIService,
)

# Domain entities
from flext_web.domain.entities import (
    FlextDashboard,
    FlextResponse,
    FlextTemplate,
    FlextWebApp,
)

# Platform
from flext_web.platform import FlextWebPlatform

# Simple API
from flext_web.simple_api import (
    create_flext_dashboard,
    create_flext_response,
    create_flext_template,
    create_flext_web_app,
)

# Simple web helpers
from flext_web.simple_web import (
    FlextSimpleTemplate,
    create_error_response,
    create_response,
    create_template,
    format_pagination,
    validate_request_data,
)

# Legacy web interface
from flext_web.web_interface import FlextCoreManager

# Main FlextWeb aliases
FlextWeb = FlextWebPlatform
FlextWebResult = FlextResult

# Prefixed helper functions
flext_web_create_dashboard = create_flext_dashboard
flext_web_create_response = create_flext_response
flext_web_create_template = create_flext_template
flext_web_create_app = create_flext_web_app
flext_web_create_error_response = create_error_response
flext_web_validate_request = validate_request_data


def create_flext_web_platform(
    config: dict[str, object] | None = None,
) -> FlextWebPlatform:
    """Create unified FLEXT Web platform instance.

    Args:
        config: Optional configuration dictionary

    Returns:
        Configured FlextWebPlatform instance

    """
    return FlextWebPlatform(config or {})


flext_web_create_platform = create_flext_web_platform

__all__ = [
    "FlextContainer",
    "FlextCoreManager",
    "FlextDashboard",
    "FlextDashboardService",
    "FlextResponse",
    "FlextResult",
    "FlextSimpleTemplate",
    "FlextTemplate",
    "FlextTemplateService",
    "FlextWeb",
    "FlextWebAPI",
    "FlextWebAPIService",
    "FlextWebApp",
    "FlextWebPlatform",
    "FlextWebResult",
    "__version__",
    "__version_info__",
    "create_app",
    "create_error_response",
    "create_flext_dashboard",
    "create_flext_response",
    "create_flext_template",
    "create_flext_web_app",
    "create_flext_web_platform",
    "create_response",
    "create_template",
    "flext_web_create_app",
    "flext_web_create_dashboard",
    "flext_web_create_error_response",
    "flext_web_create_platform",
    "flext_web_create_response",
    "flext_web_create_template",
    "flext_web_validate_request",
    "format_pagination",
    "validate_request_data",
]

# Module metadata
__architecture__ = "Clean Architecture + DDD"
