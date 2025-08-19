"""FLEXT Web Handlers - CQRS handlers and command processors.

This module provides specialized handlers for web-specific operations,
extending the base handler patterns from flext-core with web domain
requirements.

Handlers follow CQRS (Command Query Responsibility Segregation) patterns
for clean separation between commands and queries, with comprehensive
error handling and validation.

Key Components:
    - Base web handlers extending flext-core patterns
    - Specialized handlers for web operations
    - Command and query separation
    - Integration with Flask request/response cycles
"""

from __future__ import annotations

from flask import jsonify
from flask.typing import ResponseReturnValue
from flext_core import FlextHandlers, FlextResult

from flext_web.models import FlextWebApp, FlextWebAppHandler
from flext_web.type_aliases import ErrorDetails, ResponseData


class WebHandlers(FlextHandlers):
    """Web-specific handlers extending flext-core handler patterns.

    Provides specialized handling for web operations with Flask integration,
    request validation, and response formatting following enterprise patterns.
    """

    @staticmethod
    def handle_health_check() -> FlextResult[dict[str, ResponseData]]:
        """Handle health check requests with system status.

        Returns:
            FlextResult containing health status information.

        """
        return FlextResult[dict[str, ResponseData]].ok({
            "status": "healthy",
            "service": "flext-web",
            "version": "0.9.0"
        })

    @staticmethod
    def handle_app_creation(name: str, port: int = 8000, host: str = "localhost") -> FlextResult[FlextWebApp]:
        """Handle application creation with validation.

        Args:
            name: Application name
            port: Application port
            host: Application host

        Returns:
            FlextResult containing created application or error.

        """
        handler = FlextWebAppHandler()
        return handler.create(name, port, host)

    @staticmethod
    def handle_app_start(app: FlextWebApp) -> FlextResult[FlextWebApp]:
        """Handle application start with validation.

        Args:
            app: Application to start

        Returns:
            FlextResult containing updated application or error.

        """
        handler = FlextWebAppHandler()
        return handler.start(app)

    @staticmethod
    def handle_app_stop(app: FlextWebApp) -> FlextResult[FlextWebApp]:
        """Handle application stop with validation.

        Args:
            app: Application to stop

        Returns:
            FlextResult containing updated application or error.

        """
        handler = FlextWebAppHandler()
        return handler.stop(app)


class WebResponseHandler:
    """Handler for formatting HTTP responses.

    Provides consistent response formatting across all web endpoints
    with proper error handling and JSON serialization.
    """

    @staticmethod
    def create_json_response(
        message: str,
        *,
        success: bool,
        data: ResponseData = None,
        status_code: int = 200
    ) -> ResponseReturnValue:
        """Create standardized JSON response.

        Args:
            success: Whether the operation was successful
            message: Human-readable message
            data: Optional data payload
            status_code: HTTP status code

        Returns:
            Flask JSON response with standardized format.

        """
        response_data = {
            "success": success,
            "message": message,
            "data": data
        }

        response = jsonify(response_data)
        response.status_code = status_code
        return response

    @staticmethod
    def create_error_response(
        message: str,
        status_code: int = 500,
        error_details: ErrorDetails = None
    ) -> ResponseReturnValue:
        """Create standardized error response.

        Args:
            message: Error message
            status_code: HTTP status code
            error_details: Optional error details

        Returns:
            Flask JSON error response.

        """
        return WebResponseHandler.create_json_response(
            message,
            success=False,
            data=error_details,
            status_code=status_code
        )

    @staticmethod
    def create_success_response(
        message: str,
        data: ResponseData = None,
        status_code: int = 200
    ) -> ResponseReturnValue:
        """Create standardized success response.

        Args:
            message: Success message
            data: Optional data payload
            status_code: HTTP status code

        Returns:
            Flask JSON success response.

        """
        return WebResponseHandler.create_json_response(
            message,
            success=True,
            data=data,
            status_code=status_code
        )
