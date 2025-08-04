"""FLEXT Web Interface - Domain-Specific Exception Hierarchy.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Comprehensive exception hierarchy for web service operations extending flext-core
foundation patterns. Provides structured error handling with context information,
route tracking, and consistent error reporting across the web interface.

The exception hierarchy follows enterprise patterns with detailed context capture,
structured error codes, and integration with flext-core's logging and monitoring
systems. All exceptions maintain backward compatibility and provide comprehensive
debugging information for operational visibility.

Exception Categories:
    - FlextWebError: Base web service exception with route context
    - FlextWebValidationError: Input validation failures with field details
    - FlextWebAuthenticationError: Authentication and authorization failures
    - FlextWebConfigurationError: Configuration and setup errors
    - FlextWebConnectionError: Network and connectivity issues
    - FlextWebProcessingError: Business logic and processing failures
    - FlextWebTimeoutError: Operation timeout and performance issues
    - FlextWebTemplateError: Template rendering and UI errors
    - FlextWebRoutingError: URL routing and endpoint resolution
    - FlextWebSessionError: Session management and state issues
    - FlextWebMiddlewareError: Middleware processing failures

Integration:
    - Built on flext-core exception foundation patterns
    - Integrates with structured logging for operational visibility
    - Provides context information for debugging and monitoring
    - Compatible with Flask error handling and HTTP status mapping
    - Supports enterprise error reporting and alerting systems

Example:
    Basic exception usage with context:

    >>> try:
    ...     validate_user_input(data)
    ... except FlextWebValidationError as e:
    ...     logger.error("Validation failed", error=e, context=e.context)

Author: FLEXT Development Team
Version: 0.9.0
Status: Development (targeting 1.0.0 production release)

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
    """Base exception for all web service operations with route context tracking.

    Serves as the foundation exception for all FLEXT Web Interface operations,
    providing structured error handling with route context and comprehensive
    debugging information. Extends flext-core's FlextError with web-specific
    context including route information and HTTP-related metadata.

    The exception supports structured error reporting, integration with monitoring
    systems, and consistent error handling patterns across all web operations.
    All web-specific exceptions inherit from this base class.

    Attributes:
        message: Human-readable error description
        route: HTTP route where the error occurred (optional)
        context: Additional context information for debugging
        error_code: Structured error code for programmatic handling

    Integration:
        - Extends flext-core FlextError foundation patterns
        - Compatible with Flask error handling middleware
        - Integrates with structured logging systems
        - Supports monitoring and alerting integration

    Example:
        Creating web service error with route context:

        >>> error = FlextWebError(
        ...     "Service unavailable",
        ...     route="/api/v1/apps",
        ...     status_code=503,
        ...     retry_after=30,
        ... )
        >>> logger.error("Web service error", error=error)

    """

    def __init__(
        self,
        message: str = "Web service error",
        route: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize web service error with comprehensive context information.

        Creates a new web service error with structured context including route
        information and additional metadata for debugging and monitoring purposes.

        Args:
            message: Human-readable error description
            route: HTTP route where error occurred (e.g., "/api/v1/apps")
            **kwargs: Additional context information (status_code, method, etc.)

        Example:
            >>> error = FlextWebError(
            ...     "Database connection failed",
            ...     route="/api/v1/users",
            ...     method="POST",
            ...     status_code=500,
            ... )

        """
        context = kwargs.copy()
        if route is not None:
            context["route"] = route

        super().__init__(message, error_code="WEB_SERVICE_ERROR", context=context)


class FlextWebValidationError(FlextValidationError):
    """Web service input validation errors with detailed field information.

    Specialized validation exception for web interface operations providing
    detailed field-level validation information, form context, and structured
    error reporting. Extends flext-core's FlextValidationError with web-specific
    validation context including field names, values, and form information.

    The exception supports comprehensive validation error reporting with
    field-specific details, truncated values for security, and integration
    with form validation systems and client-side error display.

    Attributes:
        message: Human-readable validation error description
        field: Name of the field that failed validation (optional)
        value: Truncated field value for debugging (optional)
        form_name: Name of the form being validated (optional)
        validation_details: Structured validation information

    Integration:
        - Extends flext-core FlextValidationError patterns
        - Compatible with Flask-WTF and form validation
        - Integrates with client-side error display
        - Supports structured API error responses

    Example:
        Field validation error with context:

        >>> error = FlextWebValidationError(
        ...     "Email format is invalid",
        ...     field="email",
        ...     value="invalid-email",
        ...     form_name="user_registration",
        ... )
        >>> return {"error": error.message, "field": error.field}

    """

    def __init__(
        self,
        message: str = "Web validation failed",
        field: str | None = None,
        value: object = None,
        form_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize web validation error with comprehensive field context.

        Creates validation error with detailed field information and context
        for debugging and client-side error display. Values are truncated
        for security and logging safety.

        Args:
            message: Human-readable validation error description
            field: Name of field that failed validation
            value: Field value that failed (truncated to 100 chars)
            form_name: Name of form containing the field
            **kwargs: Additional context (route, method, etc.)

        Example:
            >>> error = FlextWebValidationError(
            ...     "Port must be between 1 and 65535",
            ...     field="port",
            ...     value=70000,
            ...     form_name="app_creation",
            ... )

        """
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

        route_obj = context.get("route")
        route_str = route_obj if isinstance(route_obj, str) else None
        filtered_context = {k: v for k, v in context.items() if k != "route"}
        super().__init__(
            f"Web auth: {message}",
            route=route_str,
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

        route_obj = context.get("route")
        route_str = route_obj if isinstance(route_obj, str) else None
        filtered_context = {k: v for k, v in context.items() if k != "route"}
        super().__init__(
            f"Web config: {message}",
            route=route_str,
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

        route_obj = context.get("route")
        route_str = route_obj if isinstance(route_obj, str) else None
        filtered_context = {k: v for k, v in context.items() if k != "route"}
        super().__init__(
            f"Web processing: {message}",
            route=route_str,
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

        route_obj = context.get("route")
        route_str = route_obj if isinstance(route_obj, str) else None
        filtered_context = {k: v for k, v in context.items() if k != "route"}
        super().__init__(
            f"Web timeout: {message}",
            route=route_str,
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


__all__: list[str] = [
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
