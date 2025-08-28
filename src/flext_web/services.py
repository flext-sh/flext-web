"""FLEXT Web Services - Consolidated service system extending flext-core patterns.

This module implements the consolidated service architecture following the
"one class per module" pattern, with FlextWebServices extending FlextServices
and containing all web-specific service functionality as nested classes and methods.
"""

from __future__ import annotations

from typing import cast

from flask import Flask, jsonify, request
from flask.typing import ResponseReturnValue
from flext_core import FlextDomainService, FlextLogger, FlextResult
from pydantic import ValidationError
from werkzeug.exceptions import BadRequest

from flext_web.config import FlextWebConfig
from flext_web.handlers import FlextWebAppHandler
from flext_web.models import FlextWebApp
from flext_web.protocols import AppManagerProtocol
from flext_web.typings import FlextWebTypes
from flext_web.utilities import FlextWebUtilities

# =============================================================================
# CONSOLIDATED SERVICES CLASS
# =============================================================================


class FlextWebServices(FlextDomainService[dict[str, object]]):
    """Consolidated web service system extending flext-core patterns.

    This class serves as the single point of access for all web-specific
    services while extending FlextDomainService from flext-core
    for proper architectural inheritance.

    All service functionality is accessible through this single class following the
    "one class per module" architectural requirement.
    """

    # =========================================================================
    # DEPENDENCY INVERSION ADAPTER
    # =========================================================================

    class _AppManagerAdapter:
        """Adapter to make FlextWebAppHandler compatible with AppManagerProtocol.

        Following SOLID principles, this adapter provides dependency inversion
        without modifying existing handler implementation.
        """

        def __init__(
            self, handler: FlextWebAppHandler, apps_store: dict[str, FlextWebApp]
        ) -> None:
            """Initialize adapter with handler and apps storage."""
            self._handler = handler
            self._apps = apps_store

        def create_app(
            self, name: str, port: int, host: str
        ) -> FlextResult[FlextWebApp]:
            """Create app via adapter - delegates to handler.create."""
            return self._handler.create(name=name, port=port, host=host)

        def start_app(self, app_id: str) -> FlextResult[FlextWebApp]:
            """Start app via adapter - delegates to handler.start."""
            if app_id not in self._apps:
                return FlextResult.fail(f"Application {app_id} not found")
            return self._handler.start(self._apps[app_id])

        def stop_app(self, app_id: str) -> FlextResult[FlextWebApp]:
            """Stop app via adapter - delegates to handler.stop."""
            if app_id not in self._apps:
                return FlextResult.fail(f"Application {app_id} not found")
            return self._handler.stop(self._apps[app_id])

        def list_apps(self) -> FlextResult[list[FlextWebApp]]:
            """List apps via adapter - accesses apps store."""
            return FlextResult.ok(list(self._apps.values()))

    # =========================================================================
    # NESTED SERVICE CLASSES
    # =========================================================================

    class WebService:
        """Flask-based web service providing REST API and dashboard with enterprise patterns.

        Comprehensive web service implementation providing both REST API endpoints
        and web dashboard functionality using Flask framework integration with
        flext-core patterns.
        """

        def __init__(
            self,
            config: FlextWebConfig,
            app_manager: AppManagerProtocol | None = None,
        ) -> None:
            """Initialize web service with configuration and dependency injection.

            Args:
                config: Web service configuration
                app_manager: Optional app manager protocol implementation.
                    If None, defaults to FlextWebAppHandler for backward compatibility.

            """
            self.config = config
            self.logger = FlextLogger(__name__)
            self.app = Flask(__name__)
            self.apps: dict[str, FlextWebApp] = {}

            # Dependency Inversion: depend on protocol, not concrete implementation
            if app_manager is not None:
                self.handler = app_manager
            else:
                # Create adapter for backward compatibility
                concrete_handler = FlextWebAppHandler()
                self.handler = FlextWebServices._AppManagerAdapter(
                    concrete_handler, self.apps
                )

            self._configure_flask()
            self._register_routes()

        def _configure_flask(self) -> None:
            """Configure Flask application with settings from config."""
            self.app.config["DEBUG"] = self.config.debug
            self.app.config["SECRET_KEY"] = self.config.secret_key

        def _register_routes(self) -> None:
            """Register all Flask routes."""
            # Health endpoints
            self.app.route("/health", methods=["GET"])(self.health)
            self.app.route("/", methods=["GET"])(self.dashboard)

            # API endpoints
            self.app.route("/api/v1/apps", methods=["GET"])(self.list_apps)
            self.app.route("/api/v1/apps", methods=["POST"])(self.create_app)
            self.app.route("/api/v1/apps/<app_id>", methods=["GET"])(self.get_app)
            self.app.route("/api/v1/apps/<app_id>/start", methods=["POST"])(
                self.start_app
            )
            self.app.route("/api/v1/apps/<app_id>/stop", methods=["POST"])(
                self.stop_app
            )

        def health(self) -> ResponseReturnValue:
            """Health check endpoint."""
            health_data: FlextWebTypes.HealthDataDict = {
                "status": "healthy",
                "service": "flext-web",
                "version": "0.9.0",
                "apps_count": len(self.apps),
            }

            return jsonify(
                {"success": True, "message": "Service is healthy", "data": health_data}
            )

        def dashboard(self) -> ResponseReturnValue:
            """Web dashboard endpoint."""
            apps_html = ""
            for app in self.apps.values():
                apps_html += f"""
                <div class="app-card">
                    <h3>{app.name}</h3>
                    <p>Host: {app.host}:{app.port}</p>
                    <p>Status: {app.status_value}</p>
                    <p>ID: {app.id!s}</p>
                </div>
                """

            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>FLEXT Web Dashboard</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .app-card {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; }}
                    h1 {{ color: #333; }}
                </style>
            </head>
            <body>
                <h1>FLEXT Web Dashboard</h1>
                <h2>Applications ({len(self.apps)})</h2>
                {apps_html or "<p>No applications registered</p>"}
            </body>
            </html>
            """

        def list_apps(self) -> ResponseReturnValue:
            """List all applications endpoint."""
            apps_data = [
                FlextWebTypes.AppDataDict(
                    name=app.name,
                    host=app.host,
                    port=app.port,
                    status=app.status_value,
                    id=str(app.id),
                )
                for app in self.apps.values()
            ]

            return jsonify(
                {
                    "success": True,
                    "message": f"Found {len(apps_data)} applications",
                    "data": {"apps": apps_data},
                }
            )

        def create_app(self) -> ResponseReturnValue:  # noqa: PLR0911
            """Create application endpoint using FlextWebUtilities for processing."""
            try:
                data = request.get_json()
                if not data:
                    # Use WebResultUtils for standardized error response
                    error_response = FlextWebUtilities.WebFactories.create_error_response(
                        "Request body is required", 400
                    )
                    return jsonify(error_response), 400

                # Extract and sanitize request data using WebProcessors
                app_info = FlextWebUtilities.WebProcessors.extract_app_info_from_request(data)

                name = app_info.get("name")
                if not name:
                    error_response = FlextWebUtilities.WebFactories.create_error_response(
                        "Application name is required", 400
                    )
                    return jsonify(error_response), 400

                # Validate using WebValidators
                if not FlextWebUtilities.WebValidators.validate_app_name(str(name)):
                    error_response = FlextWebUtilities.WebFactories.create_error_response(
                        f"Invalid application name: {name}", 400
                    )
                    return jsonify(error_response), 400

                # Generate app_id using WebFormatters
                app_id = FlextWebUtilities.WebFormatters.format_app_id(str(name))

                # Check for duplicates
                if app_id in self.apps:
                    message = FlextWebUtilities.WebFormatters.format_response_message(
                        "creation", str(name), success=False
                    ) + " - already exists"
                    error_response = FlextWebUtilities.WebFactories.create_error_response(
                        message, 400
                    )
                    return jsonify(error_response), 400

                # Extract port and host with defaults
                port = app_info.get("port", 8000)
                host = app_info.get("host", "localhost")

                # Validate port using WebValidators
                if not isinstance(port, int) or not FlextWebUtilities.WebValidators.validate_port_range(port):
                    error_response = FlextWebUtilities.WebFactories.create_error_response(
                        f"Invalid port: {port}. Must be between 1-65535", 400
                    )
                    return jsonify(error_response), 400

                # Validate host using WebValidators
                if not FlextWebUtilities.WebValidators.validate_host_format(str(host)):
                    error_response = FlextWebUtilities.WebFactories.create_error_response(
                        f"Invalid host format: {host}", 400
                    )
                    return jsonify(error_response), 400

                # Create application using validated data
                app = FlextWebApp(
                    id=app_id,
                    name=str(name),
                    host=str(host),
                    port=port,
                )

                # Domain validation
                validation_result = app.validate_domain_rules()
                if not validation_result.success:
                    error_response = FlextWebUtilities.WebFactories.create_error_response(
                        f"Domain validation failed: {validation_result.error}", 400
                    )
                    return jsonify(error_response), 400

                # Store the application
                self.apps[app_id] = app

                # Create response data
                app_data = FlextWebTypes.AppDataDict(
                    name=app.name,
                    host=app.host,
                    port=app.port,
                    status=app.status_value,
                    id=str(app.id),
                )

                # Create success response using WebResultUtils
                success_message = FlextWebUtilities.WebFormatters.format_response_message(
                    "created", str(name), success=True
                )
                success_response = FlextWebUtilities.WebResultUtils.create_api_response(
                    message=success_message,
                    success=True,
                    data=app_data
                )

                return jsonify(success_response), 201

            except BadRequest:
                # Use WebFactories for error response
                error_response = FlextWebUtilities.WebFactories.create_error_response(
                    "Invalid JSON in request body", 400
                )
                return jsonify(error_response), 400
            except ValidationError as e:
                error_response = FlextWebUtilities.WebFactories.create_error_response(
                    f"Validation error: {e}", 400
                )
                return jsonify(error_response), 400
            except Exception as e:
                self.logger.exception("Error creating application")
                error_response = FlextWebUtilities.WebFactories.create_error_response(
                    f"Internal error: {e}", 500
                )
                return jsonify(error_response), 500

        def get_app(self, app_id: str) -> ResponseReturnValue:
            """Get application endpoint."""
            if app_id not in self.apps:
                return jsonify(
                    {
                        "success": False,
                        "message": f"Application '{app_id}' not found",
                        "data": None,
                    }
                ), 404

            app = self.apps[app_id]
            app_data = FlextWebTypes.AppDataDict(
                name=app.name,
                host=app.host,
                port=app.port,
                status=app.status_value,
                id=str(app.id),
            )

            return jsonify(
                {
                    "success": True,
                    "message": f"Application '{app_id}' found",
                    "data": app_data,
                }
            )

        def start_app(self, app_id: str) -> ResponseReturnValue:
            """Start application endpoint using FlextWebUtilities."""
            if app_id not in self.apps:
                error_response = FlextWebUtilities.WebFactories.create_error_response(
                    f"Application '{app_id}' not found", 404
                )
                return jsonify(error_response), 404

            # Use handler to start the app
            result = self.handler.start_app(app_id)

            # Use WebResultUtils to handle FlextResult
            if result.success:
                updated_app = result.value
                self.apps[app_id] = updated_app

                app_data = FlextWebTypes.AppDataDict(
                    name=updated_app.name,
                    host=updated_app.host,
                    port=updated_app.port,
                    status=updated_app.status_value,
                    id=str(updated_app.id),
                )

                # Use WebFormatters for consistent messaging
                success_message = FlextWebUtilities.WebFormatters.format_response_message(
                    "started", app_id, success=True
                )
                success_response = FlextWebUtilities.WebResultUtils.create_api_response(
                    message=success_message,
                    success=True,
                    data=app_data
                )
                return jsonify(success_response)
            # Handle failure using WebResultUtils
            error_response = FlextWebUtilities.WebResultUtils.handle_flext_result(
                cast("FlextResult[object]", result)
            )
            return jsonify(error_response), 400

        def stop_app(self, app_id: str) -> ResponseReturnValue:
            """Stop application endpoint using FlextWebUtilities."""
            if app_id not in self.apps:
                error_response = FlextWebUtilities.WebFactories.create_error_response(
                    f"Application '{app_id}' not found", 404
                )
                return jsonify(error_response), 404

            # Use handler to stop the app
            result = self.handler.stop_app(app_id)

            # Use WebResultUtils to handle FlextResult
            if result.success:
                updated_app = result.value
                self.apps[app_id] = updated_app

                app_data = FlextWebTypes.AppDataDict(
                    name=updated_app.name,
                    host=updated_app.host,
                    port=updated_app.port,
                    status=updated_app.status_value,
                    id=str(updated_app.id),
                )

                # Use WebFormatters for consistent messaging
                success_message = FlextWebUtilities.WebFormatters.format_response_message(
                    "stopped", app_id, success=True
                )
                success_response = FlextWebUtilities.WebResultUtils.create_api_response(
                    message=success_message,
                    success=True,
                    data=app_data
                )
                return jsonify(success_response)
            # Handle failure using WebResultUtils
            error_response = FlextWebUtilities.WebResultUtils.handle_flext_result(
                cast("FlextResult[object]", result)
            )
            return jsonify(error_response), 400

        def run(
            self,
            host: str | None = None,
            port: int | None = None,
            *,
            debug: bool | None = None,
            **kwargs: object,
        ) -> None:
            """Run the Flask web service.

            Args:
                host: Optional host override
                port: Optional port override
                debug: Optional debug mode override
                **kwargs: Additional Flask run arguments

            """
            run_host = host or self.config.host
            run_port = port or self.config.port
            run_debug = debug if debug is not None else self.config.debug

            self.logger.info(f"Starting FLEXT Web Service on {run_host}:{run_port}")
            self.app.run(host=run_host, port=run_port, debug=run_debug, **kwargs)  # type: ignore[arg-type]

    # =========================================================================
    # SERVICE FACTORY METHODS
    # =========================================================================

    @classmethod
    def create_web_service(cls, config: FlextWebConfig) -> WebService:
        """Create web service instance.

        Args:
            config: Web service configuration

        Returns:
            Configured WebService instance

        """
        return cls.WebService(config)

    @classmethod
    def create_flask_app(cls, config: FlextWebConfig) -> Flask:
        """Create Flask application instance.

        Args:
            config: Web service configuration

        Returns:
            Configured Flask application

        """
        service = cls.create_web_service(config)
        return service.app


# =============================================================================
# BACKWARD COMPATIBILITY ALIASES
# =============================================================================

# Legacy aliases for existing code compatibility
FlextWebService = FlextWebServices.WebService


__all__ = [
    # Legacy compatibility exports
    "FlextWebService",
    "FlextWebServices",
]
