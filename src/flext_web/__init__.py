"""FLEXT Web - Django Enterprise Dashboard.

Copyright (c) 2025 FLEXT Team. All rights reserved.

Built on flext-core foundation for robust web interface.
Uses Django patterns with flext-core domain models.
"""

from __future__ import annotations

__version__ = "0.1.0"

# Core exports
try:
    from flext_web.config import WebConfig
    from flext_web.domain.entities import Deployment, Pipeline, Project
except ImportError:
    # Domain layer not yet fully refactored
    pass

# Configuration exports
try:
    from flext_web.infrastructure.container import WebContainer
except ImportError:
    # Infrastructure layer not yet refactored
    pass

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
]
