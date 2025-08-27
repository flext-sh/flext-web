"""FLEXT Web Interface - Consolidated Exception System.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

This module implements the consolidated exception architecture following the
"one class per module" pattern, with FlextWebExceptions extending FlextExceptions
and containing all web-specific exceptions as nested classes with aliases.
"""

from __future__ import annotations

from flext_core import FlextExceptions

# =============================================================================
# CONSOLIDATED EXCEPTION CLASS
# =============================================================================


class FlextWebExceptions(FlextExceptions):
    """Consolidated web exception system extending flext-core patterns.

    This class serves as the single point of access for all web-specific
    exceptions, consolidating functionality while extending FlextExceptions
    from flext-core for proper architectural inheritance.

    All exceptions are accessible as nested classes and through aliases
    for backward compatibility. The class provides factory methods for
    common exception creation patterns.
    """

    # =========================================================================
    # BASE EXCEPTION CLASSES
    # =========================================================================

    class WebError(FlextExceptions):
        """Base exception for all FLEXT Web Interface operations.

        Accepts arbitrary keyword details and stores them as context.
        """

        def __init__(
            self,
            message: str,
            route: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize web error with context."""
            context = dict(kwargs)
            if route is not None:
                context["route"] = route
            super().__init__(message, context=context)

    class WebValidationError(WebError):
        """Web service configuration and input validation errors."""

        def __init__(
            self,
            message: str = "Web validation error",
            field: str | None = None,
            value: str | None = None,
        ) -> None:
            """Initialize web validation error with context."""
            full_message = f"Web validation: {message}"
            if field:
                full_message += f" (field: {field})"
            if value:
                full_message += f" [value: {value}]"
            super().__init__(full_message)

    class WebConfigurationError(WebError):
        """Web service configuration errors."""

    class WebConnectionError(WebError):
        """Web service network and connection errors."""

    class WebProcessingError(WebError):
        """Web service data processing and business logic errors."""

    class WebAuthenticationError(WebError):
        """Web service authentication and authorization errors."""

    class WebTimeoutError(WebError):
        """Web service operation timeout errors."""

    # =========================================================================
    # DOMAIN-SPECIFIC EXCEPTIONS
    # =========================================================================

    class WebTemplateError(WebError):
        """Web service template processing and rendering errors."""

        def __init__(
            self,
            message: str = "Web template error",
            template_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize web template error with context."""
            full_message = f"Template error: {message}"
            if template_name:
                full_message += f" (template: {template_name})"
            route_value = kwargs.get("route")
            super().__init__(
                full_message,
                route=route_value if isinstance(route_value, str) else None,
                **{k: v for k, v in kwargs.items() if k != "route"},
            )

    class WebRoutingError(WebError):
        """Web service URL routing and endpoint resolution errors."""

        def __init__(
            self,
            message: str = "Web routing error",
            endpoint: str | None = None,
            method: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize web routing error with context."""
            full_message = f"Routing error: {message}"
            if endpoint:
                full_message += f" (endpoint: {endpoint})"
            if method:
                full_message += f" [{method}]"
            route_value = kwargs.get("route")
            super().__init__(
                full_message,
                route=route_value if isinstance(route_value, str) else None,
                **{k: v for k, v in kwargs.items() if k != "route"},
            )

    class WebSessionError(WebError):
        """Web service session management and state errors."""

        def __init__(
            self,
            message: str = "Web session error",
            session_id: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize web session error with context."""
            full_message = f"Session error: {message}"
            if session_id:
                full_message += f" (session: {session_id})"
            route_value = kwargs.get("route")
            super().__init__(
                full_message,
                route=route_value if isinstance(route_value, str) else None,
                **{k: v for k, v in kwargs.items() if k != "route"},
            )

    class WebMiddlewareError(WebError):
        """Web service middleware processing and pipeline errors."""

        def __init__(
            self,
            message: str = "Web middleware error",
            middleware_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize web middleware error with context."""
            full_message = f"Middleware error: {message}"
            if middleware_name:
                full_message += f" (middleware: {middleware_name})"
            route_value = kwargs.get("route")
            super().__init__(
                full_message,
                route=route_value if isinstance(route_value, str) else None,
                **{k: v for k, v in kwargs.items() if k != "route"},
            )

    # =========================================================================
    # FACTORY METHODS
    # =========================================================================

    @classmethod
    def create_web_error(
        cls,
        message: str,
        route: str | None = None,
        **kwargs: object,
    ) -> WebError:
        """Create base web error instance."""
        return cls.WebError(message, route=route, **kwargs)

    @classmethod
    def create_validation_error(
        cls,
        message: str = "Web validation error",
        field: str | None = None,
        value: str | None = None,
    ) -> WebValidationError:
        """Create web validation error instance."""
        return cls.WebValidationError(message, field=field, value=value)

    @classmethod
    def create_template_error(
        cls,
        message: str = "Web template error",
        template_name: str | None = None,
        **kwargs: object,
    ) -> WebTemplateError:
        """Create web template error instance."""
        return cls.WebTemplateError(message, template_name=template_name, **kwargs)

    @classmethod
    def create_routing_error(
        cls,
        message: str = "Web routing error",
        endpoint: str | None = None,
        method: str | None = None,
        **kwargs: object,
    ) -> WebRoutingError:
        """Create web routing error instance."""
        return cls.WebRoutingError(message, endpoint=endpoint, method=method, **kwargs)


# =============================================================================
# BACKWARD COMPATIBILITY ALIASES
# =============================================================================

# Legacy aliases for existing code compatibility
FlextWebError = FlextWebExceptions.WebError
FlextWebValidationError = FlextWebExceptions.WebValidationError
FlextWebConfigurationError = FlextWebExceptions.WebConfigurationError
FlextWebConnectionError = FlextWebExceptions.WebConnectionError
FlextWebProcessingError = FlextWebExceptions.WebProcessingError
FlextWebAuthenticationError = FlextWebExceptions.WebAuthenticationError
FlextWebTimeoutError = FlextWebExceptions.WebTimeoutError
FlextWebTemplateError = FlextWebExceptions.WebTemplateError
FlextWebRoutingError = FlextWebExceptions.WebRoutingError
FlextWebSessionError = FlextWebExceptions.WebSessionError
FlextWebMiddlewareError = FlextWebExceptions.WebMiddlewareError


__all__ = [
    "FlextWebAuthenticationError",
    "FlextWebConfigurationError",
    "FlextWebConnectionError",
    # Legacy compatibility exports
    "FlextWebError",
    "FlextWebExceptions",
    "FlextWebMiddlewareError",
    "FlextWebProcessingError",
    "FlextWebRoutingError",
    "FlextWebSessionError",
    "FlextWebTemplateError",
    "FlextWebTimeoutError",
    "FlextWebValidationError",
]
