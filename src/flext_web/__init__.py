"""FLEXT Web - Flask-based web interface for FLEXT ecosystem.

Production-ready web service providing management dashboard and REST API
for FLEXT platform with enterprise-grade Clean Architecture implementation.

Architecture:
    - Domain Layer: Core business entities and rules
    - Application Layer: Use cases and configuration management
    - Infrastructure Layer: Framework integration and external services

Key Features:
    - RESTful API for application lifecycle management
    - Web dashboard for visual management
    - Enterprise configuration management
    - Comprehensive validation and error handling
    - Production-ready logging and monitoring
    - Flask integration with Clean Architecture

Usage:
    Basic service creation:
        from flext_web import create_service
        service = create_service()

    Configuration management:
        from flext_web import FlextWebConfigs
        config = FlextWebConfigs.WebConfig()

    Model operations:
        from flext_web import FlextWebModels
        app = FlextWebModels.WebApp(...)

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Core aggregated imports with explicit imports to avoid F405 errors
from flext_web.config import FlextWebConfigs
from flext_web.constants import FlextWebConstants
from flext_web.exceptions import FlextWebExceptions
from flext_web.fields import FlextWebFields
from flext_web.handlers import FlextWebHandlers
from flext_web.interfaces import FlextWebInterfaces
from flext_web.models import FlextWebModels
from flext_web.protocols import FlextWebProtocols
from flext_web.services import FlextWebServices
from flext_web.typings import FlextWebTypes
from flext_web.utilities import FlextWebUtilities

# Version information
__version__ = "0.9.0"

# Aggregate all __all__ from all modules following flext-core pattern
import flext_web.config as _config
import flext_web.constants as _constants
import flext_web.exceptions as _exceptions
import flext_web.fields as _fields
import flext_web.handlers as _handlers
import flext_web.interfaces as _interfaces
import flext_web.models as _models
import flext_web.protocols as _protocols
import flext_web.services as _services
import flext_web.typings as _typings
import flext_web.utilities as _utilities

# Explicit __all__ following flext-core pattern (avoids PyRight warnings)
__all__ = [
    # Main unified classes
    "FlextWebConfigs",
    "FlextWebModels",
    "FlextWebServices",
    "FlextWebHandlers",
    "FlextWebProtocols",
    "FlextWebTypes",
    "FlextWebConstants",
    "FlextWebExceptions",
    "FlextWebFields",
    "FlextWebInterfaces",
    "FlextWebUtilities",
    # Convenience functions
    "create_service",
    "get_web_settings",
]

# =============================================================================
# CONVENIENCE ALIASES - Following flext-core pattern
# =============================================================================

# No aliases needed - all functionality is accessible through main classes


# =============================================================================
# CONVENIENCE FUNCTIONS - For backward compatibility and ease of use
# =============================================================================


def create_service(
    config: FlextWebConfigs.WebConfig | None = None,
) -> FlextWebServices.WebService:
    """Create a configured FLEXT Web Service instance.

    This is a convenience function that wraps FlextWebServices.create_web_service()
    for easier access and backward compatibility.

    Args:
        config: Optional web service configuration. If None, uses default config.

    Returns:
        Configured FlextWebServices.WebService instance.

    Raises:
        RuntimeError: If service creation fails.

    """
    result = FlextWebServices.create_web_service(config)
    if result.is_failure:
        msg = f"Failed to create web service: {result.error}"
        raise RuntimeError(msg)
    return result.value


def get_web_settings() -> FlextWebConfigs.WebConfig:
    """Get default web service settings.

    Returns:
        Default FlextWebConfigs.WebConfig instance.

    """
    return FlextWebConfigs.WebConfig()
