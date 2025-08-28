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
from flext_web.handlers import FlextWebAppHandler
from flext_web.models import (
    FlextWebApp,
    FlextWebAppStatus,
)
from flext_web.services import FlextWebService


def deprecation_warning(old_name: str, new_name: str) -> None:
    """Issue a deprecation warning for legacy imports."""
    warnings.warn(
        f"{old_name} is deprecated, use {new_name} instead",
        DeprecationWarning,
        stacklevel=3,
    )


# Legacy aliases for main web service classes - commonly used names
# ruff: noqa: N802
def WebConfig(**kwargs: object) -> FlextWebConfig:
    """Legacy alias for FlextWebConfig."""
    deprecation_warning("WebConfig", "FlextWebConfig")
    # Legacy function: type: ignore needed for backward compatibility with generic kwargs
    return FlextWebConfig(**kwargs)


def WebService(config: object = None) -> FlextWebService:
    """Legacy alias for FlextWebService."""
    deprecation_warning("WebService", "FlextWebService")
    if config is None:
        config = get_web_settings()
    # Legacy function: type: ignore needed for backward compatibility with generic config
    return FlextWebService(config)


def WebApp(
    name: str, port: int = 8000, host: str = "localhost", **kwargs: object
) -> FlextWebApp:
    """Legacy alias for FlextWebApp."""
    deprecation_warning("WebApp", "FlextWebApp")
    # Legacy function: type: ignore needed for backward compatibility with generic kwargs
    return FlextWebApp(name=name, port=port, host=host, **kwargs)


def WebAppHandler(*args: object, **kwargs: object) -> FlextWebAppHandler:
    """Legacy alias for FlextWebAppHandler."""
    deprecation_warning("WebAppHandler", "FlextWebAppHandler")
    return FlextWebAppHandler(*args, **kwargs)


def AppStatus(*args: object, **kwargs: object) -> FlextWebAppStatus:
    """Legacy alias for FlextWebAppStatus."""
    deprecation_warning("AppStatus", "FlextWebAppStatus")
    return FlextWebAppStatus(*args, **kwargs)


# Legacy aliases for Flask-specific names that might have been used
def FlaskService(*args: object, **kwargs: object) -> FlextWebService:
    """Legacy alias for FlextWebService (Flask-specific naming)."""
    deprecation_warning("FlaskService", "FlextWebService")
    return FlextWebService(*args, **kwargs)


def FlaskApp(*args: object, **kwargs: object) -> object:
    """Legacy alias for create_app function."""
    deprecation_warning("FlaskApp", "create_app")
    return create_app(*args, **kwargs)


# Legacy exception aliases (more concise names that were probably used)
def WebError(message: str | None = None) -> FlextWebError:
    """Legacy alias for FlextWebError."""
    deprecation_warning("WebError", "FlextWebError")
    return FlextWebError(message or "Legacy error")


def WebValidationError(message: str | None = None) -> FlextWebValidationError:
    """Legacy alias for FlextWebValidationError."""
    deprecation_warning("WebValidationError", "FlextWebValidationError")
    return FlextWebValidationError(message or "Legacy validation error")


def WebConfigurationError(
    message: str | None = None,
) -> FlextWebConfigurationError:
    """Legacy alias for FlextWebConfigurationError."""
    deprecation_warning("WebConfigurationError", "FlextWebConfigurationError")
    return FlextWebConfigurationError(message or "Legacy configuration error")


def WebConnectionError(message: str | None = None) -> FlextWebConnectionError:
    """Legacy alias for FlextWebConnectionError."""
    deprecation_warning("WebConnectionError", "FlextWebConnectionError")
    return FlextWebConnectionError(message or "Legacy connection error")


def WebAuthenticationError(
    message: str | None = None,
) -> FlextWebAuthenticationError:
    """Legacy alias for FlextWebAuthenticationError."""
    deprecation_warning("WebAuthenticationError", "FlextWebAuthenticationError")
    return FlextWebAuthenticationError(message or "Legacy authentication error")


def WebTemplateError(message: str | None = None) -> FlextWebTemplateError:
    """Legacy alias for FlextWebTemplateError."""
    deprecation_warning("WebTemplateError", "FlextWebTemplateError")
    return FlextWebTemplateError(message or "Legacy template error")


def WebRoutingError(message: str | None = None) -> FlextWebRoutingError:
    """Legacy alias for FlextWebRoutingError."""
    deprecation_warning("WebRoutingError", "FlextWebRoutingError")
    return FlextWebRoutingError(message or "Legacy routing error")


def WebSessionError(message: str | None = None) -> FlextWebSessionError:
    """Legacy alias for FlextWebSessionError."""
    deprecation_warning("WebSessionError", "FlextWebSessionError")
    return FlextWebSessionError(message or "Legacy session error")


def WebMiddlewareError(message: str | None = None) -> FlextWebMiddlewareError:
    """Legacy alias for FlextWebMiddlewareError."""
    deprecation_warning("WebMiddlewareError", "FlextWebMiddlewareError")
    return FlextWebMiddlewareError(message or "Legacy middleware error")


# Legacy function aliases
def get_web_config() -> object:
    """Legacy alias for get_web_settings."""
    deprecation_warning("get_web_config", "get_web_settings")
    return get_web_settings()


def create_web_service(config: object = None) -> object:
    """Legacy alias for create_service."""
    deprecation_warning("create_web_service", "create_service")
    return create_service(config)


def create_flask_app(config: object = None) -> object:
    """Legacy alias for create_app."""
    deprecation_warning("create_flask_app", "create_app")
    return create_app(config)


def reset_config() -> None:
    """Legacy alias for reset_web_settings."""
    deprecation_warning("reset_config", "reset_web_settings")
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
