"""Legacy compatibility facade for flext-web.

This module provides backward compatibility for APIs that may have been refactored
or renamed during the Pydantic modernization process. It follows the same pattern
as flext-core's legacy.py to ensure consistent facade patterns across the ecosystem.

All imports here should be considered deprecated and may issue warnings.
Modern code should import directly from the appropriate modules.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings

from flext_web import (
    create_app,
    create_service,
    get_web_settings,
    reset_web_settings,
)

# Import modern implementations to re-export under legacy names
from flext_web.config import FlextWebConfig
from flext_web.exceptions import (
    FlextWebAuthenticationError,
    FlextWebConfigurationError,
    FlextWebConnectionError,
    FlextWebError,
    FlextWebMiddlewareError,
    FlextWebRoutingError,
    FlextWebSessionError,
    FlextWebTemplateError,
    FlextWebValidationError,
)
from flext_web.models import (
    FlextWebApp,
    FlextWebAppHandler,
    FlextWebAppStatus,
)
from flext_web.services import FlextWebService


def _deprecation_warning(old_name: str, new_name: str) -> None:
    """Issue a deprecation warning for legacy imports."""
    warnings.warn(
        f"{old_name} is deprecated, use {new_name} instead",
        DeprecationWarning,
        stacklevel=3,
    )


# Legacy aliases for main web service classes - commonly used names
def WebConfig(*args: object, **kwargs: object) -> FlextWebConfig:  # noqa: N802
    """Legacy alias for FlextWebConfig."""
    _deprecation_warning("WebConfig", "FlextWebConfig")
    return FlextWebConfig(*args, **kwargs)  # type: ignore[arg-type]


def WebService(*args: object, **kwargs: object) -> FlextWebService:  # noqa: N802
    """Legacy alias for FlextWebService."""
    _deprecation_warning("WebService", "FlextWebService")
    return FlextWebService(*args, **kwargs)  # type: ignore[arg-type]


def WebApp(*args: object, **kwargs: object) -> FlextWebApp:  # noqa: N802
    """Legacy alias for FlextWebApp."""
    _deprecation_warning("WebApp", "FlextWebApp")
    return FlextWebApp(*args, **kwargs)  # type: ignore[arg-type]


def WebAppHandler(*args: object, **kwargs: object) -> FlextWebAppHandler:  # noqa: N802
    """Legacy alias for FlextWebAppHandler."""
    _deprecation_warning("WebAppHandler", "FlextWebAppHandler")
    return FlextWebAppHandler(*args, **kwargs)


def AppStatus(*args: object, **kwargs: object) -> FlextWebAppStatus:  # noqa: N802
    """Legacy alias for FlextWebAppStatus."""
    _deprecation_warning("AppStatus", "FlextWebAppStatus")
    return FlextWebAppStatus(*args, **kwargs)


# Legacy aliases for Flask-specific names that might have been used
def FlaskService(*args: object, **kwargs: object) -> FlextWebService:  # noqa: N802
    """Legacy alias for FlextWebService (Flask-specific naming)."""
    _deprecation_warning("FlaskService", "FlextWebService")
    return FlextWebService(*args, **kwargs)  # type: ignore[arg-type]


def FlaskApp(*args: object, **kwargs: object) -> object:  # noqa: N802
    """Legacy alias for create_app function."""
    _deprecation_warning("FlaskApp", "create_app")
    return create_app(*args, **kwargs)  # type: ignore[arg-type]


# Legacy exception aliases (more concise names that were probably used)
def WebError(message: str | None = None) -> FlextWebError:  # noqa: N802
    """Legacy alias for FlextWebError."""
    _deprecation_warning("WebError", "FlextWebError")
    return FlextWebError(message or "Legacy error")


def WebValidationError(message: str | None = None) -> FlextWebValidationError:  # noqa: N802
    """Legacy alias for FlextWebValidationError."""
    _deprecation_warning("WebValidationError", "FlextWebValidationError")
    return FlextWebValidationError(message or "Legacy validation error")


def WebConfigurationError(  # noqa: N802
    message: str | None = None,
) -> FlextWebConfigurationError:
    """Legacy alias for FlextWebConfigurationError."""
    _deprecation_warning("WebConfigurationError", "FlextWebConfigurationError")
    return FlextWebConfigurationError(message or "Legacy configuration error")


def WebConnectionError(message: str | None = None) -> FlextWebConnectionError:  # noqa: N802
    """Legacy alias for FlextWebConnectionError."""
    _deprecation_warning("WebConnectionError", "FlextWebConnectionError")
    return FlextWebConnectionError(message or "Legacy connection error")


def WebAuthenticationError(  # noqa: N802
    message: str | None = None,
) -> FlextWebAuthenticationError:
    """Legacy alias for FlextWebAuthenticationError."""
    _deprecation_warning("WebAuthenticationError", "FlextWebAuthenticationError")
    return FlextWebAuthenticationError(message or "Legacy authentication error")


def WebTemplateError(message: str | None = None) -> FlextWebTemplateError:  # noqa: N802
    """Legacy alias for FlextWebTemplateError."""
    _deprecation_warning("WebTemplateError", "FlextWebTemplateError")
    return FlextWebTemplateError(message or "Legacy template error")


def WebRoutingError(message: str | None = None) -> FlextWebRoutingError:  # noqa: N802
    """Legacy alias for FlextWebRoutingError."""
    _deprecation_warning("WebRoutingError", "FlextWebRoutingError")
    return FlextWebRoutingError(message or "Legacy routing error")


def WebSessionError(message: str | None = None) -> FlextWebSessionError:  # noqa: N802
    """Legacy alias for FlextWebSessionError."""
    _deprecation_warning("WebSessionError", "FlextWebSessionError")
    return FlextWebSessionError(message or "Legacy session error")


def WebMiddlewareError(message: str | None = None) -> FlextWebMiddlewareError:  # noqa: N802
    """Legacy alias for FlextWebMiddlewareError."""
    _deprecation_warning("WebMiddlewareError", "FlextWebMiddlewareError")
    return FlextWebMiddlewareError(message or "Legacy middleware error")


# Legacy function aliases
def get_web_config() -> object:
    """Legacy alias for get_web_settings."""
    _deprecation_warning("get_web_config", "get_web_settings")
    return get_web_settings()


def create_web_service(config: object = None) -> object:
    """Legacy alias for create_service."""
    _deprecation_warning("create_web_service", "create_service")
    return create_service(config)  # type: ignore[arg-type]


def create_flask_app(config: object = None) -> object:
    """Legacy alias for create_app."""
    _deprecation_warning("create_flask_app", "create_app")
    return create_app(config)  # type: ignore[arg-type]


def reset_config() -> None:
    """Legacy alias for reset_web_settings."""
    _deprecation_warning("reset_config", "reset_web_settings")
    reset_web_settings()


# Export legacy aliases for backward compatibility
__all__ = [
    "AppStatus",
    "FlaskApp",
    "FlaskService",
    "WebApp",
    "WebAppHandler",
    "WebAuthenticationError",
    # Legacy class aliases
    "WebConfig",
    "WebConfigurationError",
    "WebConnectionError",
    # Legacy exception aliases
    "WebError",
    "WebMiddlewareError",
    "WebRoutingError",
    "WebService",
    "WebSessionError",
    "WebTemplateError",
    "WebValidationError",
    "create_flask_app",
    "create_web_service",
    # Legacy function aliases
    "get_web_config",
    "reset_config",
]
