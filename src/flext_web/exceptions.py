"""FLEXT Web Exceptions - Domain-specific exception hierarchy.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextCore


class FlextWebExceptions(FlextCore.Exceptions):
    """Web-specific exception hierarchy extending flext-core patterns.

    Provides domain-specific exceptions for web operations while maintaining
    compatibility with the flext-core exception hierarchy.

    **Pattern**: All web exceptions extend from appropriate flext-core base classes
    to ensure consistent error handling and logging across the ecosystem.
    """

    class WebError(FlextCore.Exceptions.BaseError):
        """Base web error for general web operation failures.

        Use this for web-specific errors that don't fit other categories.
        """

        def __init__(
            self,
            message: str,
            route: str | None = None,
            status_code: int | None = None,
            error_code: str = "WEB_ERROR",
        ) -> None:
            """Initialize web error with optional route and status information."""
            super().__init__(message, error_code=error_code)
            self.route = route
            self.status_code = status_code

        def __str__(self) -> str:
            """String representation including route if available."""
            base_msg = super().__str__()
            if self.route:
                return f"{base_msg} (route: {self.route})"
            return base_msg

    class WebConfigError(FlextCore.Exceptions.ConfigurationError):
        """Web configuration error for invalid web settings."""

        def __init__(self, message: str, config_key: str | None = None) -> None:
            """Initialize web config error with optional config key."""
            super().__init__(message, config_key=config_key)
            self.config_key = config_key

    class WebRequestError(FlextCore.Exceptions.ValidationError):
        """Web request validation error for malformed HTTP requests."""

        def __init__(
            self,
            message: str,
            request_id: str | None = None,
            validation_errors: dict | None = None,
        ) -> None:
            """Initialize web request error with request context."""
            super().__init__(message)
            self.request_id = request_id
            self.validation_errors = validation_errors or {}

    class WebResponseError(FlextCore.Exceptions.OperationError):
        """Web response error for issues with HTTP response generation."""

        def __init__(
            self,
            message: str,
            response_id: str | None = None,
            status_code: int | None = None,
        ) -> None:
            """Initialize web response error with response context."""
            super().__init__(message)
            self.response_id = response_id
            self.status_code = status_code

    class WebAuthError(FlextCore.Exceptions.AuthorizationError):
        """Web authentication/authorization error."""

        def __init__(
            self,
            message: str,
            user_id: str | None = None,
            required_permission: str | None = None,
        ) -> None:
            """Initialize web auth error with user and permission context."""
            super().__init__(message, user_id=user_id, permission=required_permission)
            self.user_id = user_id
            self.required_permission = required_permission

    class WebServiceError(FlextCore.Exceptions.OperationError):
        """Web service operational error."""

        def __init__(
            self,
            message: str,
            service_name: str | None = None,
            operation: str | None = None,
        ) -> None:
            """Initialize web service error with service context."""
            super().__init__(message, operation=service_name)
            self.operation = operation


__all__ = [
    "FlextWebExceptions",
]
