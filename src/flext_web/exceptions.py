"""Web service exception hierarchy using flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Domain-specific exceptions for web service operations inheriting from flext-core.
"""

from __future__ import annotations

from flext_core.exceptions import (
    FlextAuthenticationError,
    FlextConfigurationError,
    FlextConnectionError,
    FlextError,
    FlextProcessingError,
    FlextTimeoutError,
    FlextValidationError,
)


class FlextWebError(FlextError):
    """Base exception for web service operations."""

    def __init__(
        self,
        message: str = "Web service error",
        route: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize web service error with context."""
        context = kwargs.copy()
        if route is not None:
            context["route"] = route

        super().__init__(message, error_code="WEB_SERVICE_ERROR", context=context)


class FlextWebValidationError(FlextValidationError):
    """Web service validation errors."""

    def __init__(
        self,
        message: str = "Web validation failed",
        field: str | None = None,
        value: object = None,
        form_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize web validation error with context."""
        validation_details = {}
        if field is not None:
            validation_details["field"] = field
        if value is not None:
            validation_details["value"] = str(value)[:100]  # Truncate long values

        context = kwargs.copy()
        if form_name is not None:
            context["form_name"] = form_name

        super().__init__(
            f"Web validation: {message}",
            validation_details=(
                validation_details
                if validation_details is None
                else dict(validation_details)
            ),
            context=context,
        )


class FlextWebAuthenticationError(FlextAuthenticationError):
    """Web service authentication errors."""

    def __init__(
        self,
        message: str = "Web authentication failed",
        auth_method: str | None = None,
        route: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize web authentication error with context."""
        context = kwargs.copy()
        if auth_method is not None:
            context["auth_method"] = auth_method
        if route is not None:
            context["route"] = route

        route = context.get("route")
        filtered_context = {k: v for k, v in context.items() if k != "route"}
        super().__init__(
            f"Web auth: {message}",
            route=route if isinstance(route, str) else None,
            **filtered_context,
        )


class FlextWebConfigurationError(FlextConfigurationError):
    """Web service configuration errors."""

    def __init__(
        self,
        message: str = "Web configuration error",
        config_key: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize web configuration error with context."""
        context = kwargs.copy()
        if config_key is not None:
            context["config_key"] = config_key

        route = context.get("route")
        filtered_context = {k: v for k, v in context.items() if k != "route"}
        super().__init__(
            f"Web config: {message}",
            route=route if isinstance(route, str) else None,
            **filtered_context,
        )


class FlextWebConnectionError(FlextConnectionError):
    """Web service connection errors."""

    def __init__(
        self,
        message: str = "Web connection failed",
        host: str | None = None,
        port: int | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize web connection error with context."""
        context = kwargs.copy()
        if host is not None:
            context["host"] = host
        if port is not None:
            context["port"] = port

        route = context.get("route")
        filtered_context = {k: v for k, v in context.items() if k != "route"}
        super().__init__(
            f"Web connection: {message}",
            route=route if isinstance(route, str) else None,
            **filtered_context,
        )


class FlextWebProcessingError(FlextProcessingError):
    """Web service processing errors."""

    def __init__(
        self,
        message: str = "Web processing failed",
        handler: str | None = None,
        route: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize web processing error with context."""
        context = kwargs.copy()
        if handler is not None:
            context["handler"] = handler
        if route is not None:
            context["route"] = route

        route = context.get("route")
        filtered_context = {k: v for k, v in context.items() if k != "route"}
        super().__init__(
            f"Web processing: {message}",
            route=route if isinstance(route, str) else None,
            **filtered_context,
        )


class FlextWebTimeoutError(FlextTimeoutError):
    """Web service timeout errors."""

    def __init__(
        self,
        message: str = "Web operation timed out",
        route: str | None = None,
        timeout_seconds: float | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize web timeout error with context."""
        context = kwargs.copy()
        if route is not None:
            context["route"] = route
        if timeout_seconds is not None:
            context["timeout_seconds"] = timeout_seconds

        route = context.get("route")
        filtered_context = {k: v for k, v in context.items() if k != "route"}
        super().__init__(
            f"Web timeout: {message}",
            route=route if isinstance(route, str) else None,
            **filtered_context,
        )


class FlextWebTemplateError(FlextWebError):
    """Web service template errors."""

    def __init__(
        self,
        message: str = "Web template error",
        template_name: str | None = None,
        template_error: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize web template error with context."""
        context = kwargs.copy()
        if template_name is not None:
            context["template_name"] = template_name
        if template_error is not None:
            context["template_error"] = template_error

        route = context.get("route")
        filtered_context = {k: v for k, v in context.items() if k != "route"}
        super().__init__(
            f"Web template: {message}",
            route=route if isinstance(route, str) else None,
            **filtered_context,
        )


class FlextWebRoutingError(FlextWebError):
    """Web service routing errors."""

    def __init__(
        self,
        message: str = "Web routing error",
        route: str | None = None,
        method: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize web routing error with context."""
        context = kwargs.copy()
        if method is not None:
            context["method"] = method

        super().__init__(f"Web routing: {message}", route=route, **context)


class FlextWebSessionError(FlextWebError):
    """Web service session errors."""

    def __init__(
        self,
        message: str = "Web session error",
        session_id: str | None = None,
        session_state: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize web session error with context."""
        context = kwargs.copy()
        if session_id is not None:
            context["session_id"] = session_id
        if session_state is not None:
            context["session_state"] = session_state

        route = context.get("route")
        filtered_context = {k: v for k, v in context.items() if k != "route"}
        super().__init__(
            f"Web session: {message}",
            route=route if isinstance(route, str) else None,
            **filtered_context,
        )


class FlextWebMiddlewareError(FlextWebError):
    """Web service middleware errors."""

    def __init__(
        self,
        message: str = "Web middleware error",
        middleware_name: str | None = None,
        stage: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize web middleware error with context."""
        context = kwargs.copy()
        if middleware_name is not None:
            context["middleware_name"] = middleware_name
        if stage is not None:
            context["stage"] = stage

        route = context.get("route")
        filtered_context = {k: v for k, v in context.items() if k != "route"}
        super().__init__(
            f"Web middleware: {message}",
            route=route if isinstance(route, str) else None,
            **filtered_context,
        )


__all__ = [
    "FlextWebAuthenticationError",
    "FlextWebConfigurationError",
    "FlextWebConnectionError",
    "FlextWebError",
    "FlextWebMiddlewareError",
    "FlextWebProcessingError",
    "FlextWebRoutingError",
    "FlextWebSessionError",
    "FlextWebTemplateError",
    "FlextWebTimeoutError",
    "FlextWebValidationError",
]
