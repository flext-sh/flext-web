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
        from flext_web import FlextWebServices
        result = FlextWebServices.create_web_service()
        service = result.unwrap_or_raise()

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

# =============================================================================
# FOUNDATION LAYER - Wildcard imports following flext-core pattern
# =============================================================================

from flext_web.config import *
from flext_web.config import FlextWebConfigs
from flext_web.constants import *
from flext_web.constants import FlextWebConstants
from flext_web.exceptions import *
from flext_web.exceptions import FlextWebExceptions
from flext_web.fields import *
from flext_web.fields import FlextWebFields
from flext_web.handlers import *
from flext_web.handlers import FlextWebHandlers
from flext_web.interfaces import *
from flext_web.interfaces import FlextWebInterfaces
from flext_web.models import *
from flext_web.models import FlextWebModels
from flext_web.protocols import *
from flext_web.protocols import FlextWebProtocols
from flext_web.services import *
from flext_web.services import FlextWebServices
from flext_web.typings import *
from flext_web.typings import FlextWebTypes
from flext_web.utilities import *
from flext_web.utilities import FlextWebUtilities

# Version information
__version__ = "0.9.0"

# Explicit __all__ definition following flext-core pattern - static for tools compatibility
__all__ = [
    # Configuration
    "FlextWebConfigs",
    # Constants
    "FlextWebConstants",
    # Exceptions
    "FlextWebExceptions",
    # Fields
    "FlextWebFields",
    # Handlers
    "FlextWebHandlers",
    # Interfaces
    "FlextWebInterfaces",
    # Models
    "FlextWebModels",
    # Protocols
    "FlextWebProtocols",
    # Services
    "FlextWebServices",
    # Types
    "FlextWebTypes",
    # Utilities
    "FlextWebUtilities",
]

# =============================================================================
# CONVENIENCE ALIASES - Following flext-core pattern
# =============================================================================

# No aliases needed - all functionality is accessible through main classes


# =============================================================================
# NO CONVENIENCE FUNCTIONS - Direct access through main classes only
# =============================================================================

# All functionality is accessible directly through the main classes:
# - FlextWebServices.create_web_service() for service creation
# - FlextWebConfigs.WebConfig() for configuration
# - FlextWebModels.WebApp() for models
# This eliminates wrapper functions and unnecessary redeclarations
