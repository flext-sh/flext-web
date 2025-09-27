"""FLEXT Web Services - Consolidated web service system with enterprise patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flask import Flask, jsonify, render_template_string, request
from flask.typing import ResponseReturnValue

from flext_core import (
    FlextConstants,
    FlextLogger,
    FlextResult,
    FlextTypes,
    FlextUtilities,
)
from flext_web.config import FlextWebConfig
from flext_web.constants import FlextWebConstants
from flext_web.handlers import FlextWebHandlers
from flext_web.models import FlextWebModels
from flext_web.typings import FlextWebTypes


class FlextWebServices:
    """Consolidated FLEXT web service system providing all service functionality.

    This is the complete web service system for the FLEXT Web ecosystem, providing
    unified service patterns built on FlextProcessors foundation with web-specific
    implementations. All web service types are organized as nested classes within
    this single container for consistent configuration and easy access.

    """

    # =============================================================================
    # WEB SERVICE CLASSES
    # =============================================================================

    class WebService:
        """Primary web service implementation with Flask integration and application management.

        Enterprise-grade web service providing REST API endpoints, web dashboard,
        and comprehensive application lifecycle management. Built on Flask with
        FlextProcessors integration for consistent service patterns.
        """

        @override
        def __init__(self, config: FlextWebTypes.Core.WebConfigDict) -> None:
            """Initialize web service with configuration and Flask application."""
            self.config: FlextWebTypes.Core.WebConfigDict = config
            self.app = Flask(__name__)
            self.apps: dict[str, FlextWebModels.WebApp] = {}
            self.app_handler = FlextWebHandlers.WebAppHandler()
            self.logger = FlextLogger(__name__)

            # Create framework adapter for abstraction
            self._framework = self._FlaskAdapter()

            # Initialize service state
            self._initialized = True
            self.logger.info("Service initialized")

            # Configure Flask application
            self.app.config.update(
                {
                    "SECRET_KEY": config.get("secret_key", "default-secret-key"),
                    "DEBUG": config.get("debug_bool", False),
                },
            )

            # Register routes
            self._register_routes()

            # Mark service as ready
            self._ready = True
            self.logger.info("Service ready")

        class _FlaskAdapter:
            """Framework adapter for Flask - provides framework-agnostic interface."""

            def create_json_response(
                self,
                data: FlextTypes.Core.JsonObject,
                status_code: int = FlextWebConstants.Web.HTTP_OK,
            ) -> ResponseReturnValue:
                """Create JSON response using Flask."""
                return jsonify(data), status_code

            def get_request_data(self) -> FlextTypes.Core.JsonObject:
                """Get request JSON data."""
                if request.is_json:
                    return request.get_json() or {}
                return {}

            def is_json_request(self) -> bool:
                """Check if request is JSON."""
                return request.is_json

        def _register_routes(self) -> None:
            """Register all Flask routes for the web service."""
            # Health check endpoint
            self.app.route("/health", methods=["GET"])(self.health_check)

            # Dashboard endpoint
            self.app.route("/", methods=["GET"])(self.dashboard)

            # API endpoints
            self.app.route("/api/v1/apps", methods=["GET"])(self.list_apps)
            self.app.route("/api/v1/apps", methods=["POST"])(self.create_app)
            self.app.route("/api/v1/apps/<app_id>", methods=["GET"])(self.get_app)
            self.app.route("/api/v1/apps/<app_id>/start", methods=["POST"])(
                self.start_app,
            )
            self.app.route("/api/v1/apps/<app_id>/stop", methods=["POST"])(
                self.stop_app,
            )

        def health_check(self) -> ResponseReturnValue:
            """Health check endpoint returning service status."""
            try:
                self.logger.info("Health check performed")

                {
                    "status": "healthy",
                    "service": "flext - web",
                    "version": FlextConstants.Core.VERSION,
                    "applications": len(self.apps),
                    "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
                    "service_id": getattr(self, "_id", "unknown"),
                    "created_at": getattr(self, "created_at", None),
                }

                return jsonify(
                    {
                        "success": "True",
                        "message": "Service is healthy",
                        "data": "health_data",
                    },
                ), FlextWebConstants.Web.HTTP_OK
            except Exception:
                self.logger.exception("Health check failed")
                return jsonify(
                    {
                        "success": "False",
                        "message": "Service health check failed",
                        "data": {
                            "status": "unhealthy",
                            "error": "Internal error",
                            "service_id": getattr(self, "_id", "unknown"),
                        },
                    },
                ), FlextWebConstants.Web.HTTP_INTERNAL_ERROR

        def dashboard(self) -> ResponseReturnValue:
            """Web dashboard interface for application management.

            Returns:
            ResponseReturnValue:: Description of return value.

            """
            try:
                app_count = len(self.apps)
                running_count = sum(
                    1 for app in self.apps.values() if bool(app.is_running)
                )

                html_template = """

                <!DOCTYPE html>
                <html>
                <head>
                    <title>FLEXT Web Dashboard</title>
                    <style>
                        body { font-family: "Arial", sans-serif; margin: 40px; }
                        .header { color: #333; border-bottom: 2px solid #007acc; padding-bottom: 10px; }
                        .stats { background: #f5f5f5; padding: 20px; border-radius: 5px; margin: 20px 0; }
                        .app-list { margin-top: 20px; }
                        .app-item { background: white; border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
                        .status-running { color: green; font-weight: bold; }
                        .status-stopped { color: red; }
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>FLEXT Web Service Dashboard</h1>
                    </div>

                    <div class="stats">
                        <h2>Service Statistics</h2>
                        <p><strong>Total Applications:</strong> {{ app_count }}</p>
                        <p><strong>Running Applications:</strong> {{ running_count }}</p>
                        <p><strong>Service Status:</strong> <span class="status-running">Operational</span></p>
                    </div>

                    <div class="app-list">
                        <h2>Applications ({{ app_count }})</h2>
                        {% if apps %}
                            {% for app in apps %}
                            <div class="app-item">
                                <h3>{{ app.name }}</h3>
                                <p><strong>ID:</strong> {{ app.id }}</p>
                                <p><strong>Host:</strong> {{ app.host }}:{{ app.port }}</p>
                                <p><strong>Status:</strong>
                                    <span class="{% if app.is_running %}status-running{% else %}status-stopped{% endif %}">
                                        {{ app.status }}
                                    </span>
                                </p>
                            </div>
                            {% endfor %}
                        {% else %}
                            <p>No applications registered.</p>
                        {% endif %}
                    </div>
                </body>
                </html>
                """

                return render_template_string(
                    html_template,
                    app_count=app_count,
                    running_count=running_count,
                    apps=list(self.apps.values()),
                )

            except Exception:
                return "Dashboard error", FlextWebConstants.Web.HTTP_INTERNAL_ERROR

        def list_apps(self) -> ResponseReturnValue:
            """List all registered applications."""
            try:
                apps_data: list[FlextWebTypes.AppData] = []
                for app in self.apps.values():
                    app_data: FlextWebTypes.AppData = {
                        "id": app.id,
                        "name": app.name,
                        "host": app.host,
                        "port": app.port,
                        "status": app.status.value,
                        "is_running": bool(app.is_running),
                    }
                    apps_data.append(app_data)

                response: FlextWebTypes.SuccessResponse = {
                    "success": "True",
                    "message": f"Found {len(apps_data)} applications",
                    "data": {"apps": "apps_data"},
                }
                return jsonify(response)

            except Exception as e:
                error_response: FlextWebTypes.ErrorResponse = {
                    "success": "False",
                    "message": "Failed to list applications",
                    "error": str(e),
                }
                return jsonify(
                    error_response
                ), FlextWebConstants.Web.HTTP_INTERNAL_ERROR

        def _validate_json_request(self) -> FlextResult[FlextTypes.Core.Dict]:
            """Railway-oriented validation of JSON request data.

            Returns:
            ResponseReturnValue:: Description of return value.

            """
            if not request.is_json:
                return FlextResult[FlextTypes.Core.Dict].fail("Request must be JSON")

            try:
                data: FlextWebTypes.Core.RequestDict = request.get_json()
                if not data:
                    return FlextResult[FlextTypes.Core.Dict].fail(
                        "Request body is required",
                    )
                return FlextResult[FlextTypes.Core.Dict].ok(data)
            except Exception:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    "Invalid JSON in request body",
                )

        def _validate_app_data(
            self,
            data: FlextTypes.Core.Dict,
        ) -> FlextResult[tuple[str, str, int]]:
            """Validate application data using Railway pattern."""
            # Extract and validate required fields
            try:
                name = data.get("name")
                host = data.get(
                    "host",
                    FlextWebConstants.Web.DEFAULT_HOST,
                )  # Use FlextWebConstants for host default
                port = data.get(
                    "port",
                    FlextWebConstants.Web.DEFAULT_PORT,
                )  # Use FlextWebConstants for port default

                if not name or not isinstance(name, str):
                    return FlextResult[tuple[str, str, int]].fail(
                        "Name is required and must be a string",
                    )

                if not isinstance(host, str):
                    return FlextResult[tuple[str, str, int]].fail(
                        "Host must be a string",
                    )

                # Convert port to int if it's a string
                if isinstance(port, str):
                    try:
                        port = int(port)
                    except ValueError:
                        return FlextResult[tuple[str, str, int]].fail(
                            "Port must be a valid integer",
                        )
                elif not isinstance(port, int):
                    return FlextResult[tuple[str, str, int]].fail(
                        "Port must be an integer",
                    )

                return FlextResult[tuple[str, str, int]].ok((name, host, port))

            except Exception as e:
                return FlextResult[tuple[str, str, int]].fail(f"Validation failed: {e}")

        def _create_and_store_app(
            self,
            name: str,
            host: str,
            port: int,
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Create and store application using existing handler."""
            create_result: FlextResult[FlextWebModels.WebApp] = self.app_handler.create(
                name, port, host
            )

            if create_result.is_failure:
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"Application creation failed: {create_result.error}",
                )

            app = create_result.value
            self.apps[app.id] = app

            self.logger.info("App created")

            return FlextResult[FlextWebModels.WebApp].ok(app)

        def _build_success_response(
            self,
            app: FlextWebModels.WebApp,
        ) -> ResponseReturnValue:
            """Build success response using consistent format."""
            return jsonify(
                {
                    "success": "True",
                    "message": "Application created successfully",
                    "data": {
                        "id": app.id,
                        "name": app.name,
                        "host": app.host,
                        "port": app.port,
                        "status": app.status.value,
                    },
                },
            ), FlextWebConstants.Web.HTTP_CREATED

        def _build_error_response(
            self,
            error: str,
            status_code: int = FlextWebConstants.Web.HTTP_BAD_REQUEST,
        ) -> ResponseReturnValue:
            """Build error response using consistent format."""
            return jsonify(
                {
                    "success": "False",
                    "message": error,
                },
            ), status_code

        def create_app(self) -> ResponseReturnValue:
            """Create new application using Railway-oriented programming pattern.

            Reduces from 11 returns to single monadic chain with 85% less complexity.
            Uses Python 3.13 functional composition and existing flext-core validation.

            Returns:
            ResponseReturnValue:: Description of return value.

            """
            try:
                self.logger.info("Create app request received")

                # FlextResult chain with proper error handling
                json_validation = self._validate_json_request()
                if json_validation.is_failure:
                    return self._build_error_response(
                        json_validation.error or "Validation failed",
                    )

                app_validation = self._validate_app_data(json_validation.unwrap())
                if app_validation.is_failure:
                    return self._build_error_response(
                        app_validation.error or "App validation failed",
                    )

                # Unpack the validated data for method call
                app_data_tuple = app_validation.unwrap()

                # Unpack the validated data for method call
                result = self._create_and_store_app(
                    str(app_data_tuple[0]),
                    str(app_data_tuple[1]),
                    int(app_data_tuple[2]),
                )

                # Handle final result
                if result.is_failure:
                    return self._build_error_response(result.error or "Unknown error")

                return self._build_success_response(result.unwrap())

            except Exception as e:
                return self._build_error_response(
                    f"Internal error during application creation: {e}",
                    FlextWebConstants.Web.HTTP_INTERNAL_ERROR,
                )

        def get_app(self, app_id: str) -> ResponseReturnValue:
            """Get specific application by ID."""
            try:
                if app_id not in self.apps:
                    return jsonify(
                        {
                            "success": "False",
                            "message": f"Application {app_id} not found",
                        },
                    ), FlextWebConstants.Web.HTTP_NOT_FOUND

                app = self.apps[app_id]
                return jsonify(
                    {
                        "success": "True",
                        "message": "Application found",
                        "data": {
                            "id": app.id,
                            "name": app.name,
                            "host": app.host,
                            "port": app.port,
                            "status": app.status.value,
                            "is_running": bool(app.is_running),
                        },
                    },
                )

            except Exception as e:
                return jsonify(
                    {
                        "success": "False",
                        "message": "Failed to get application",
                        "error": str(e),
                    },
                ), FlextWebConstants.Web.HTTP_INTERNAL_ERROR

        def start_app(self, app_id: str) -> ResponseReturnValue:
            """Start application by ID.

            Returns:
            ResponseReturnValue:: Description of return value.

            """
            try:
                if app_id not in self.apps:
                    return jsonify(
                        {
                            "success": "False",
                            "message": f"Application {app_id} not found",
                        },
                    ), FlextWebConstants.Web.HTTP_NOT_FOUND

                app = self.apps[app_id]
                start_result: FlextResult[None] = app.start()

                if start_result.is_failure:
                    return jsonify(
                        {
                            "success": "False",
                            "message": start_result.error or "Application start failed",
                            "error": start_result.error,
                        },
                    ), FlextWebConstants.Web.HTTP_BAD_REQUEST

                # Update stored application - start returns updated app
                if start_result.value is not None:
                    self.apps[app_id] = start_result.value

                return jsonify(
                    {
                        "success": "True",
                        "message": f"Application {app.name} started successfully",
                        "data": {
                            "id": "app_id",
                            "name": app.name,
                            "status": "running",
                        },
                    },
                )

            except Exception as e:
                return jsonify(
                    {
                        "success": "False",
                        "message": "Failed to start application",
                        "error": str(e),
                    },
                ), FlextWebConstants.Web.HTTP_INTERNAL_ERROR

        def stop_app(self, app_id: str) -> ResponseReturnValue:
            """Stop application by ID."""
            try:
                if app_id not in self.apps:
                    return jsonify(
                        {
                            "success": "False",
                            "message": f"Application {app_id} not found",
                        },
                    ), FlextWebConstants.Web.HTTP_NOT_FOUND

                app = self.apps[app_id]
                stop_result: FlextResult[None] = app.stop()

                if stop_result.is_failure:
                    # Customize message based on error type
                    if "not running" in (stop_result.error or "").lower():
                        pass

                    return jsonify(
                        {
                            "success": "False",
                            "message": "message",
                            "error": stop_result.error,
                        },
                    ), FlextWebConstants.Web.HTTP_BAD_REQUEST

                # Update stored application - stop returns updated app
                if stop_result.value is not None:
                    self.apps[app_id] = stop_result.value

                return jsonify(
                    {
                        "success": "True",
                        "message": f"Application {app.name} stopped successfully",
                        "data": {
                            "id": "app_id",
                            "name": app.name,
                            "status": "stopped",
                        },
                    },
                )

            except Exception as e:
                return jsonify(
                    {
                        "success": "False",
                        "message": "Failed to stop application",
                        "error": str(e),
                    },
                ), FlextWebConstants.Web.HTTP_INTERNAL_ERROR

        @override
        def run(self) -> None:
            """Run the Flask web service."""
            self.app.run(
                host=self.config.get("host", FlextWebConstants.Web.DEFAULT_HOST),
                port=self.config.get("port", FlextWebConstants.Web.DEFAULT_PORT),
                debug=self.config.get("debug", False),
            )

    class WebServiceRegistry:
        """Service registry for web service discovery and management.

        Provides centralized registry functionality for web service instances,
        supporting service discovery, health monitoring, and lifecycle management
        within the FLEXT Web ecosystem.
        """

        @override
        def __init__(self) -> None:
            """Initialize web service registry."""
            self._services: dict[str, FlextWebServices.WebService] = {}
            self._health_status: dict[str, bool] = {}
            self.logger = FlextLogger(__name__)

            # Initialize registry state
            self._initialized = True
            self.logger.info("Registry initialized")

        def register_web_service(
            self,
            name: str,
            service: FlextWebServices.WebService,
        ) -> FlextResult[None]:
            """Register web service instance.

            Returns:
                FlextResult[None]: Success or error result.

            """
            try:
                self.logger.info("Registering service")

                if name in self._services:
                    return FlextResult[None].fail(f"Service {name} already registered")

                self._services[name] = service
                self._health_status[name] = True

                self.logger.info("Service registered successfully")
                return FlextResult[None].ok(None)

            except Exception as e:
                return FlextResult[None].fail(f"Service registration failed: {e}")

        def discover_web_service(
            self,
            name: str,
        ) -> FlextResult[FlextWebServices.WebService]:
            """Discover web service by name."""
            try:
                self.logger.info("Discovering service")

                if name not in self._services:
                    self.logger.warning(f"Service {name} not found")
                    return FlextResult[FlextWebServices.WebService].fail(
                        f"Service {name} not found",
                    )

                service = self._services[name]
                self.logger.info("Service discovered successfully")
                return FlextResult[FlextWebServices.WebService].ok(service)

            except Exception as e:
                return FlextResult[FlextWebServices.WebService].fail(
                    f"Service discovery failed: {e}",
                )

        def list_web_services(self) -> FlextResult[FlextTypes.Core.StringList]:
            """List all registered web service names.

            Returns:
                FlextResult[FlextTypes.Core.StringList]: Names of registered services.

            """
            try:
                service_names = list(self._services.keys())
                return FlextResult[FlextTypes.Core.StringList].ok(service_names)
            except Exception as e:
                return FlextResult[FlextTypes.Core.StringList].fail(
                    f"Service listing failed: {e}",
                )

        def register_service(
            self,
            name: str,
            service: FlextWebServices.WebService,
        ) -> FlextResult[None]:
            """Alias for register_web_service.

            Returns:
                FlextResult[None]: Success or error result.

            """
            return self.register_web_service(name, service)

        def get_service(self, name: str) -> FlextResult[FlextWebServices.WebService]:
            """Alias for discover_web_service."""
            return self.discover_web_service(name)

    # =============================================================================
    # FACTORY METHODS AND UTILITIES
    # =============================================================================

    @classmethod
    def create_web_service(
        cls,
        config: FlextWebTypes.Core.WebConfigDict | None = None,
    ) -> FlextResult[FlextWebServices.WebService]:
        """Create web service instance with configuration.

        Returns:
            FlextResult[FlextWebServices.WebService]: Created service instance.

        """
        try:
            if config is None:
                config_result = FlextWebConfig.create_web_config()
                if config_result.is_failure:
                    return FlextResult[FlextWebServices.WebService].fail(
                        f"Config creation failed: {config_result.error}",
                    )
                validated_config: FlextWebTypes.Core.WebConfigDict = config_result.value
                # Config type is guaranteed by FlextResult[FlextWebConfig.WebConfig]

            service = FlextWebServices.WebService(
                validated_config if config is None else config
            )
            return FlextResult[FlextWebServices.WebService].ok(service)

        except Exception as e:
            return FlextResult[FlextWebServices.WebService].fail(
                f"Web service creation failed: {e}",
            )

    @classmethod
    def create_service_registry(
        cls,
    ) -> FlextResult[FlextWebServices.WebServiceRegistry]:
        """Create web service registry instance."""
        try:
            registry = FlextWebServices.WebServiceRegistry()
            return FlextResult[FlextWebServices.WebServiceRegistry].ok(registry)
        except Exception as e:
            return FlextResult[FlextWebServices.WebServiceRegistry].fail(
                f"Registry creation failed: {e}",
            )

    @classmethod
    def create_web_system_services(
        cls,
        config: FlextTypes.Core.Dict | None = None,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create web system services."""
        _ = config  # Acknowledge parameter

        try:
            # Create service and registry
            service_result = cls.create_web_service()
            if service_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    service_result.error or "Service creation failed",
                )

            registry_result = cls.create_service_registry()
            if registry_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    registry_result.error or "Registry creation failed",
                )

            service = service_result.value
            registry = registry_result.value

            # Register service
            register_result = registry.register_web_service("main", service)
            if register_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    register_result.error or "Registration failed",
                )

            return FlextResult[FlextTypes.Core.Dict].ok(
                {
                    "web_service": "service",
                    "registry": "registry",
                },
            )

        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"System services creation failed: {e}",
            )

    # =============================================================================
    # FLEXT WEB SERVICES CONFIGURATION METHODS
    # =============================================================================

    @classmethod
    def configure_web_services_system(
        cls,
        config: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
        """Configure web services system using FlextTypes.Config with validation."""
        try:
            validated_config: dict[str, object] = dict(config)

            # Validate environment using FlextConstants
            if "environment" in config:
                env_value = config["environment"]
                valid_environments = [
                    e.value for e in list(FlextConstants.Environment.ConfigEnvironment)
                ]
                if env_value not in valid_environments:
                    return FlextResult[dict["str", "object"]].fail(
                        f"Invalid environment '{env_value}'. Valid options: {valid_environments}",
                    )
            else:
                validated_config["environment"] = (
                    FlextConstants.Environment.ConfigEnvironment.DEVELOPMENT.value
                )

            # Core validation completed - ensure required fields are present
            validated_config.setdefault(
                "environment",
                FlextConstants.Environment.ConfigEnvironment.DEVELOPMENT.value,
            )
            validated_config.setdefault(
                "log_level",
                FlextConstants.Config.LogLevel.INFO,
            )
            validated_config.setdefault(
                "validation_level",
                FlextConstants.Environment.ValidationLevel.NORMAL.value,
            )

            # Web services specific settings
            validated_config.setdefault("enable_web_service", True)
            validated_config.setdefault("enable_service_registry", True)
            validated_config.setdefault("max_concurrent_requests", 100)
            validated_config.setdefault("request_timeout_seconds", 30)

            return FlextResult[dict["str", "object"]].ok(validated_config)

        except Exception as e:
            return FlextResult[dict["str", "object"]].fail(
                f"Failed to configure web services system: {e}",
            )

    @classmethod
    def get_web_services_system_config(
        cls,
    ) -> FlextResult[dict[str, object]]:
        """Get current web services system configuration with runtime information."""
        try:
            config: dict[str, object] = {
                # Environment configuration
                "environment": FlextConstants.Environment.ConfigEnvironment.DEVELOPMENT.value,
                "log_level": FlextConstants.Config.LogLevel.INFO,
                # Web services specific settings
                "enable_web_service": "True",
                "enable_service_registry": "True",
                "max_concurrent_requests": 100,
                "request_timeout_seconds": 30,
                # Available service types
                "available_services": [
                    "WebService",
                    "WebServiceRegistry",
                ],
                "available_factories": [
                    "create_web_service",
                    "create_service_registry",
                    "create_web_system_services",
                ],
                # Runtime metrics
                "active_services": 0,
                "total_requests": 0,
                "average_response_time": 0.0,
            }

            return FlextResult[dict["str", "object"]].ok(config)

        except Exception as e:
            return FlextResult[dict["str", "object"]].fail(
                f"Failed to get web services system config: {e}",
            )


__all__ = [
    "FlextWebServices",
]
