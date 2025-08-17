"""FLEXT Web Interface - Domain-Specific Exception Hierarchy.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Web service exception hierarchy built on FLEXT ecosystem error handling patterns
with specialized exceptions for routing, templates, sessions, middleware,
and web-specific operations.

This module provides a comprehensive exception hierarchy for the FLEXT Web Interface,
extending the base FlextError pattern with domain-specific exceptions that capture
web service context and provide meaningful error messages for debugging and monitoring.

Exception Architecture:
    FlextWebError: Base exception for all web service operations
    FlextWebValidationError: Configuration and input validation errors
    FlextWebConnectionError: Network and connection-related errors
    FlextWebProcessingError: Data processing and business logic errors
    FlextWebAuthenticationError: Authentication and authorization failures
    FlextWebTimeoutError: Operation timeout errors

Domain-specific exceptions:
    FlextWebTemplateError: Template processing and rendering errors
    FlextWebRoutingError: URL routing and endpoint resolution errors
    FlextWebSessionError: Session management and state errors
    FlextWebMiddlewareError: Middleware processing and pipeline errors
"""

from __future__ import annotations

from flext_core import FlextError

# =============================================================================
# BASE EXCEPTION HIERARCHY
# =============================================================================


class FlextWebError(FlextError):
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


class FlextWebValidationError(FlextWebError):
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


class FlextWebConfigurationError(FlextWebError):
    """Web service configuration errors."""


class FlextWebConnectionError(FlextWebError):
    """Web service network and connection errors."""


class FlextWebProcessingError(FlextWebError):
    """Web service data processing and business logic errors."""


class FlextWebAuthenticationError(FlextWebError):
    """Web service authentication and authorization errors."""


class FlextWebTimeoutError(FlextWebError):
    """Web service operation timeout errors."""


# =============================================================================
# DOMAIN-SPECIFIC EXCEPTIONS
# =============================================================================


class FlextWebTemplateError(FlextWebError):
    """Web service template processing and rendering errors."""

    def __init__(
      self,
      message: str = "Web template error",
      template_name: str | None = None,
      template_error: str | None = None,
    ) -> None:
      """Initialize web template error with context."""
      full_message = f"Web template: {message}"
      if template_name:
          full_message += f" (template: {template_name})"
      if template_error:
          full_message += f" - {template_error}"
      super().__init__(full_message)


class FlextWebRoutingError(FlextWebError):
    """Web service URL routing and endpoint resolution errors."""

    def __init__(
      self,
      message: str = "Web routing error",
      route: str | None = None,
      method: str | None = None,
    ) -> None:
      """Initialize web routing error with context."""
      full_message = f"Web routing: {message}"
      if route:
          full_message += f" (route: {route})"
      if method:
          full_message += f" [method: {method}]"
      super().__init__(full_message)


class FlextWebSessionError(FlextWebError):
    """Web service session management and state errors."""

    def __init__(
      self,
      message: str = "Web session error",
      session_id: str | None = None,
      session_state: str | None = None,
    ) -> None:
      """Initialize web session error with context."""
      full_message = f"Web session: {message}"
      if session_id:
          full_message += f" (session: {session_id})"
      if session_state:
          full_message += f" [state: {session_state}]"
      super().__init__(full_message)


class FlextWebMiddlewareError(FlextWebError):
    """Web service middleware processing and pipeline errors."""

    def __init__(
      self,
      message: str = "Web middleware error",
      middleware_name: str | None = None,
      stage: str | None = None,
    ) -> None:
      """Initialize web middleware error with context."""
      full_message = f"Web middleware: {message}"
      if middleware_name:
          full_message += f" (middleware: {middleware_name})"
      if stage:
          full_message += f" [stage: {stage}]"
      super().__init__(full_message)


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
