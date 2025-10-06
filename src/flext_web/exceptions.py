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

        Accepts arbitrary keyword details and stores them as context using helpers.
        """

        @staticmethod
        def _extract_common_kwargs(
            kwargs: dict[str, object],
        ) -> tuple[dict[str, object], str | None, str | None]:
            """Extract common parameters from kwargs.

            Args:
                kwargs: Keyword arguments

            Returns:
                Tuple of (base_context, correlation_id, error_code)

            """
            # Extract known parameters
            base_context_raw = kwargs.get("context", {})
            base_context = (
                base_context_raw if isinstance(base_context_raw, dict) else {}
            )
            correlation_id = kwargs.get("correlation_id")
            error_code = kwargs.get("error_code")

            # Ensure proper types for return
            if correlation_id is not None and not isinstance(correlation_id, str):
                correlation_id = str(correlation_id)
            if error_code is not None and not isinstance(error_code, str):
                error_code = str(error_code)

            # Remove extracted parameters from kwargs to avoid duplication
            filtered_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k not in {"context", "correlation_id", "error_code"}
            }

            # Merge filtered kwargs into base_context if it's a dict
            if isinstance(base_context, dict):
                base_context.update(filtered_kwargs)
            else:
                base_context = filtered_kwargs

            return base_context, correlation_id, error_code

        @staticmethod
        def _build_context(
            base_context: dict[str, object], **additional_fields: object
        ) -> dict[str, object]:
            """Build complete context dictionary.

            Args:
                base_context: Base context dictionary
                **additional_fields: Additional fields to include

            Returns:
                Complete context dictionary

            """
            context = dict(base_context)
            context.update(additional_fields)
            return context

        @override
        def __init__(
            self,
            message: str,
            *,
            route: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize web error with context using helpers.

            Args:
                message: Error message
                route: Web route that triggered the error
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with web-specific fields
            context = self._build_context(
                base_context,
                route=route,
            )

            # Call parent with complete error information
            super().__init__(
                message,
                error_code=error_code or "WEB_ERROR",
                correlation_id=correlation_id,
                **context,
            )

    class WebValidationError(WebError):
        """Web service configuration and input validation errors."""

        @override
        def __init__(
            self,
            message: str = "Web validation error",
            *,
            field: str | None = None,
            value: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize web validation error with context using helpers.

            Args:
                message: Error message
                field: Field name that failed validation
                value: Invalid value
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Build full message with field context
            full_message = f"Web validation: {message}"
            if field:
                full_message += f" (field: {field})"
            if value:
                full_message += f" [value: {value}]"

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with validation-specific fields
            context = self._build_context(
                base_context,
                field=field,
                value=value,
            )

            # Call parent with complete error information
            super().__init__(
                full_message,
                error_code=error_code or "WEB_VALIDATION_ERROR",
                correlation_id=correlation_id,
                **context,
            )

    class WebConfigurationError(WebError):
        """Web service configuration errors."""

        @override
        def __init__(self, message: str, **kwargs: object) -> None:
            """Initialize configuration error using helpers.

            Args:
                message: Error message
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context
            context = self._build_context(base_context)

            # Call parent with complete error information
            super().__init__(
                message,
                error_code=error_code or "WEB_CONFIG_ERROR",
                context=str(context),
                correlation_id=correlation_id,
            )

    class WebConnectionError(WebError):
        """Web service network and connection errors."""

        @override
        def __init__(self, message: str, **kwargs: object) -> None:
            """Initialize connection error using helpers.

            Args:
                message: Error message
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context
            context = self._build_context(base_context)

            # Call parent with complete error information
            super().__init__(
                message,
                error_code=error_code or "WEB_CONNECTION_ERROR",
                context=str(context),
                correlation_id=correlation_id,
            )

    class WebProcessingError(WebError):
        """Web service data processing and business logic errors."""

        @override
        def __init__(self, message: str, **kwargs: object) -> None:
            """Initialize processing error using helpers.

            Args:
                message: Error message
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context
            context = self._build_context(base_context)

            # Call parent with complete error information
            super().__init__(
                message,
                error_code=error_code or "WEB_PROCESSING_ERROR",
                context=str(context),
                correlation_id=correlation_id,
            )

    class WebAuthenticationError(WebError):
        """Web service authentication and authorization errors."""

        @override
        def __init__(self, message: str, **kwargs: object) -> None:
            """Initialize authentication error using helpers.

            Args:
                message: Error message
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context
            context = self._build_context(base_context)

            # Call parent with complete error information
            super().__init__(
                message,
                code=error_code or "WEB_AUTH_ERROR",
                context=str(context),
                correlation_id=correlation_id,
            )

    class WebTimeoutError(WebError):
        """Web service operation timeout errors."""

        @override
        def __init__(self, message: str, **kwargs: object) -> None:
            """Initialize timeout error using helpers.

            Args:
                message: Error message
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context
            context = self._build_context(base_context)

            # Call parent with complete error information
            super().__init__(
                message,
                code=error_code or "WEB_TIMEOUT_ERROR",
                context=str(context),
                correlation_id=correlation_id,
            )

    class WebTemplateError(WebError):
        """Web template processing errors."""

        @override
        def __init__(
            self,
            message: str = "Web template error",
            *,
            template_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize web template error using helpers.

            Args:
                message: Error message
                template_name: Name of the template that failed
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store template_name before extracting common kwargs
            self.template_name = template_name

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with template-specific fields
            context = self._build_context(
                base_context,
                template_name=template_name,
            )

            # Call parent with complete error information
            super().__init__(
                message,
                code=error_code or "WEB_TEMPLATE_ERROR",
                context=str(context),
                correlation_id=correlation_id,
            )

    class WebRoutingError(WebError):
        """Web routing errors."""

        @override
        def __init__(
            self,
            message: str = "Web routing error",
            *,
            endpoint: str | None = None,
            method: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize web routing error using helpers.

            Args:
                message: Error message
                endpoint: Endpoint that failed routing
                method: HTTP method used
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store routing-specific attributes before extracting common kwargs
            self.endpoint = endpoint
            self.method = method

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with routing-specific fields
            context = self._build_context(
                base_context,
                endpoint=endpoint,
                method=method,
            )

            # Call parent with complete error information
            super().__init__(
                message,
                code=error_code or "WEB_ROUTING_ERROR",
                context=str(context),
                correlation_id=correlation_id,
            )

    class WebSessionError(WebError):
        """Web session management errors."""

        @override
        def __init__(
            self,
            message: str = "Web session error",
            *,
            session_id: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize web session error using helpers.

            Args:
                message: Error message
                session_id: Session identifier
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store session_id before extracting common kwargs
            self.session_id = session_id

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with session-specific fields
            context = self._build_context(
                base_context,
                session_id=session_id,
            )

            # Call parent with complete error information
            super().__init__(
                message,
                error_code=error_code or "WEB_SESSION_ERROR",
                correlation_id=correlation_id,
                **context,
            )

    class WebMiddlewareError(WebError):
        """Web middleware processing errors."""

        @override
        def __init__(
            self,
            message: str = "Web middleware error",
            *,
            middleware_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize middleware error using helpers.

            Args:
                message: Error message
                middleware_name: Name of the middleware that failed
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with middleware-specific fields
            context = self._build_context(
                base_context,
                operation=middleware_name,
            )

            # Call parent with complete error information
            super().__init__(
                message,
                code=error_code or "WEB_MIDDLEWARE_ERROR",
                context=str(context),
                correlation_id=correlation_id,
            )


__all__ = [
    # Main consolidated class
    "FlextWebExceptions",
]
