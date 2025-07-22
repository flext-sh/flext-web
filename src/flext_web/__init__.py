"""FLEXT Web - Django Enterprise Dashboard with simplified imports.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Version 0.0.0-dev - Django web interface with simplified public API:
- All common imports available from root: from flext_web import Pipeline, WebConfig
- Built on flext-core foundation for robust web interface
- Deprecation warnings for internal imports
"""

from __future__ import annotations

import contextlib
import importlib.metadata
import warnings

# Import from flext-core for foundational patterns
from flext_core import (
    BaseConfig,
    BaseConfig as WebBaseConfig,  # Configuration base
    DomainBaseModel,
    DomainBaseModel as BaseModel,  # Base for web models
    DomainError as WebError,  # Web-specific errors
    ServiceResult,
    ValidationError as ValidationError,  # Validation errors
)

try:
    __version__ = importlib.metadata.version("flext-web")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0-dev"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())


class FlextWebDeprecationWarning(DeprecationWarning):
    """Custom deprecation warning for FLEXT Web import changes."""


def _show_deprecation_warning(old_import: str, new_import: str) -> None:
    """Show deprecation warning for import paths."""
    message_parts = [
        f"⚠️  DEPRECATED IMPORT: {old_import}",
        f"✅ USE INSTEAD: {new_import}",
        "🔗 This will be removed in version 1.0.0",
        "📖 See FLEXT Web docs for migration guide",
    ]
    warnings.warn(
        "\n".join(message_parts),
        FlextWebDeprecationWarning,
        stacklevel=3,
    )


# ================================
# SIMPLIFIED PUBLIC API EXPORTS
# ================================

# Foundation patterns - ALWAYS from flext-core

# Domain layer exports - simplified imports
try:
    from flext_web.config import WebConfig
    from flext_web.domain.entities import Deployment, Pipeline, Project
except ImportError:
    # Domain layer not yet fully refactored - provide placeholders
    WebConfig = None
    Deployment = None
    Pipeline = None
    Project = None

# Infrastructure layer exports - simplified imports
with contextlib.suppress(ImportError):
    # Infrastructure layer not yet refactored
    from flext_web.infrastructure.container import WebContainerConfig as WebContainer

# ================================
# PUBLIC API EXPORTS
# ================================

__all__ = [
    "BaseModel",  # from flext_web import BaseModel
    # Domain Entities (simplified access)
    "Deployment",  # from flext_web import Deployment
    # Deprecation utilities
    "FlextWebDeprecationWarning",
    "Pipeline",  # from flext_web import Pipeline
    "Project",  # from flext_web import Project
    # Core Patterns (from flext-core)
    "ServiceResult",  # from flext_web import ServiceResult
    "ValidationError",  # from flext_web import ValidationError
    "WebBaseConfig",  # from flext_web import WebBaseConfig
    # Configuration (simplified access)
    "WebConfig",  # from flext_web import WebConfig
    "WebContainer",  # from flext_web import WebContainer
    "WebError",  # from flext_web import WebError
    # Version
    "__version__",
    "__version_info__",
]
