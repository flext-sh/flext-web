"""FLEXT Web - Django Enterprise Dashboard.

Copyright (c) 2025 FLEXT Team. All rights reserved.

Built on flext-core foundation for robust web interface.
Uses Django patterns with flext-core domain models.
"""

from __future__ import annotations

import importlib.metadata

try:
    __version__ = importlib.metadata.version("flext-web")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0-dev"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

try:
    from flext_web.config import WebConfig
    from flext_web.domain.entities import Deployment, Pipeline, Project
except ImportError:
    # Domain layer not yet fully refactored
    pass

# Configuration exports
import contextlib

with contextlib.suppress(ImportError):
    # Infrastructure layer not yet refactored
    from flext_web.infrastructure.container import WebContainerConfig as WebContainer

__all__ = [
    "Deployment",
    "Pipeline",
    # Domain entities (when available)
    "Project",
    # Configuration (when available)
    "WebConfig",
    "WebContainer",
    # Version
    "__version__",
    "__version_info__",
]
