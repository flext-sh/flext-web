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

# Core aggregated imports with type safety
from flext_web.config import *  # type: ignore[unused-ignore,reportWildcardImportFromLibrary,assignment] # noqa: F403
from flext_web.constants import *  # type: ignore[unused-ignore,reportWildcardImportFromLibrary,assignment] # noqa: F403
from flext_web.exceptions import *  # type: ignore[unused-ignore,reportWildcardImportFromLibrary,assignment] # noqa: F403
from flext_web.fields import *  # type: ignore[unused-ignore,reportWildcardImportFromLibrary,assignment] # noqa: F403
from flext_web.handlers import *  # type: ignore[unused-ignore,reportWildcardImportFromLibrary,assignment] # noqa: F403
from flext_web.interfaces import *  # type: ignore[unused-ignore,reportWildcardImportFromLibrary,assignment] # noqa: F403
from flext_web.models import *  # type: ignore[unused-ignore,reportWildcardImportFromLibrary,assignment] # noqa: F403
from flext_web.protocols import *  # type: ignore[unused-ignore,reportWildcardImportFromLibrary,assignment] # noqa: F403
from flext_web.services import *  # type: ignore[unused-ignore,reportWildcardImportFromLibrary,assignment] # noqa: F403
from flext_web.typings import *  # type: ignore[unused-ignore,reportWildcardImportFromLibrary,assignment] # noqa: F403
from flext_web.utilities import *  # type: ignore[unused-ignore,reportWildcardImportFromLibrary,assignment] # noqa: F403

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

# Create consolidated __all__ following flext-core pattern
_all_items: list[str] = []
for _module in [
    _config,
    _constants,
    _exceptions,
    _fields,
    _handlers,
    _interfaces,
    _models,
    _protocols,
    _services,
    _typings,
    _utilities,
]:
    if hasattr(_module, "__all__"):
        _all_items += _module.__all__

# Remove duplicates and sort for consistency - explicit list type
_unique_items = sorted(set(_all_items))
__all__: list[str] = _unique_items  # noqa: PLE0605

# =============================================================================
# CONVENIENCE ALIASES - Following flext-core pattern
# =============================================================================

# Most commonly used factory functions as direct aliases
create_config = _config.FlextWebConfigs.create_web_config
create_service = _services.FlextWebServices.create_web_service
create_app = _models.FlextWebModels.create_web_app
FlextLogger = getattr(_utilities.FlextWebUtilities, "FlextLogger", lambda _: None)

# Add convenience aliases to __all__
__all__ += ["create_config", "create_service", "create_app", "FlextLogger"]
