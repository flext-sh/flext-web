"""FLEXT Web Exceptions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_core import FlextExceptions


class FlextWebExceptions(FlextExceptions):
    """Consolidated web exception system extending flext-core patterns.

    This class serves as the single point of access for all web-specific
    exceptions, consolidating functionality while extending FlextExceptions
    from flext-core for proper architectural inheritance.

    All exceptions are accessible as nested classes for direct instantiation.
    """

    # =========================================================================
    # BASE EXCEPTION CLASSES
    # =========================================================================

    class WebError(FlextExceptions.BaseError):
        """Base exception for all FLEXT Web Interface operations.

        Accepts arbitrary keyword details and stores them as context.
        """

        @override
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

        @override
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

    class WebTemplateError(WebError):
        """Web template processing errors."""

        @override
        def __init__(
            self,
            message: str = "Web template error",
            template_name: str | None = None,
        ) -> None:
            """Initialize web template error."""
            super().__init__(message)
            self.template_name = template_name

    class WebRoutingError(WebError):
        """Web routing errors."""

        @override
        def __init__(
            self,
            message: str = "Web routing error",
            endpoint: str | None = None,
            method: str | None = None,
        ) -> None:
            """Initialize web routing error."""
            super().__init__(message)
            """Initialize web routing error."""
            self.endpoint = endpoint
            self.method = method

    class WebSessionError(WebError):
        """Web session management errors."""

        @override
        def __init__(
            self,
            message: str = "Web session error",
            session_id: str | None = None,
        ) -> None:
            """Initialize web session error."""
            super().__init__(message)
            self.session_id = session_id

    class WebMiddlewareError(WebError):
        """Web middleware processing errors."""

        @override
        def __init__(
            self,
            message: str = "Web middleware error",
            middleware_name: str | None = None,
        ) -> None:
            """Initialize middleware error."""
            super().__init__(message, operation=middleware_name)


__all__ = [
    # Main consolidated class
    "FlextWebExceptions",
]
