"""Legacy interfaces facade - temporary compatibility layer.

This module provides backward compatibility for interfaces that have been
consolidated into protocols.py. Following the STRICT protocol pattern for
gradual migration without breaking imports.

All interfaces here are deprecated and redirect to protocols.py.
Modern code should import directly from protocols module.
"""

from __future__ import annotations

import warnings

# Import consolidated interfaces from protocols
from flext_web.protocols import (
    AppRepositoryInterface,
    MiddlewareInterface,
    MonitoringInterface,
    TemplateEngineInterface,
    WebServiceInterface,
)


def _deprecation_warning(old_name: str, new_name: str) -> None:
    """Issue a deprecation warning for legacy interface imports."""
    warnings.warn(
        f"Importing {old_name} from interfaces is deprecated, use 'from flext_web.protocols import {new_name}' instead",
        DeprecationWarning,
        stacklevel=3,
    )


# Legacy facade exports with deprecation warnings
def __getattr__(name: str) -> object:
    """Handle legacy attribute access with deprecation warnings."""
    interface_map = {
        "WebServiceInterface": WebServiceInterface,
        "AppRepositoryInterface": AppRepositoryInterface,
        "MiddlewareInterface": MiddlewareInterface,
        "TemplateEngineInterface": TemplateEngineInterface,
        "MonitoringInterface": MonitoringInterface,
    }

    if name in interface_map:
        _deprecation_warning(name, name)
        return interface_map[name]

    msg = f"module '{__name__}' has no attribute '{name}'"
    raise AttributeError(msg)


# Export for backward compatibility
__all__ = [
    "AppRepositoryInterface",
    "MiddlewareInterface",
    "MonitoringInterface",
    "TemplateEngineInterface",
    "WebServiceInterface",
]
