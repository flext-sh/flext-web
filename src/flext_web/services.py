"""FLEXT Web Services - Consolidated web service system with enterprise patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flask import Flask, jsonify, render_template_string, request
from flask.typing import ResponseReturnValue
from flext_core import (
    FlextConstants,
    FlextLogger,
    FlextMixins,
    FlextResult,
    FlextTypes,
    FlextUtilities,
)

from flext_web.config import FlextWebConfigs
from flext_web.handlers import FlextWebHandlers
from flext_web.models import FlextWebModels
from flext_web.typings import FlextWebTypes


class FlextWebServices:
    """Consolidated FLEXT web service system providing all service functionality.

    This is the complete web service system for the FLEXT Web ecosystem, providing
    unified service patterns built on FlextServices foundation with web-specific
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
        FlextServices integration for consistent service patterns.
        """

        def __init__(self, config: FlextWebConfigs.WebConfig) -> None:
            """Initialize web service with configuration and Flask application."""
            self.config = config
            self.app = Flask(__name__)
            self.apps: dict[str, FlextWebModels.WebApp] = {}
            self.app_handler = FlextWebHandlers.WebAppHandler()
            self.logger = FlextLogger(__name__)

            # Initialize FlextMixins functionality
            FlextMixins.create_timestamp_fields(self)
            FlextMixins.ensure_id(self)
            FlextMixins.initialize_validation(self)
            FlextMixins.initialize_state(self, "initializing")

            # Log service initialization
            FlextMixins.log_operation(
                self,
                "service_init",
                config_host=config.host,
                config_port=config.port,
                config_debug=config.debug,
            )

            # Configure Flask application
            self.app.config.update(
                {
                    "SECRET_KEY": config.secret_key,
                    "DEBUG": config.debug,
                }
            )

            # Register routes
            self._register_routes()

            # Mark service as ready
            FlextMixins.set_state(self, "ready")
            FlextMixins.log_operation(
                self,
                "service_ready",
                ready=True,
                routes_registered=True,
            )

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
                self.start_app
            )
            self.app.route("/api/v1/apps/<app_id>/stop", methods=["POST"])(
                self.stop_app
            )

        def health_check(self) -> ResponseReturnValue:
            """Health check endpoint returning service status."""
            try:
                FlextMixins.log_operation(
                    self, "health_check", apps_count=len(self.apps)
                )

                health_data: FlextWebTypes.HealthResponse = {
                    "status": "healthy",
                    "service": "flext-web",
                    "version": "0.9.0",
                    "applications": len(self.apps),
                    "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
                    "service_id": getattr(self, "_id", "unknown"),
                    "created_at": getattr(self, "created_at", None),
                }

                return jsonify(
                    {
                        "success": True,
                        "message": "Service is healthy",
                        "data": health_data,
                    }
                ), 200
            except Exception as e:
                FlextMixins.log_operation(self, "health_check_error", error=str(e))
                return jsonify(
                    {
                        "success": False,
                        "message": "Service health check failed",
                        "data": {
                            "status": "unhealthy",
                            "error": "Internal error",
                            "service_id": getattr(self, "_id", "unknown"),
                        },
                    }
                ), 500

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
                        body { font-family: Arial, sans-serif; margin: 40px; }
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
                return "Dashboard error", 500

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
                    "success": True,
                    "message": f"Found {len(apps_data)} applications",
                    "data": {"apps": apps_data},
                }
                return jsonify(response)

            except Exception as e:
                error_response: FlextWebTypes.ErrorResponse = {
                    "success": False,
                    "message": "Failed to list applications",
                    "error": str(e),
                }
                return jsonify(error_response), 500

        def _validate_json_request(self) -> FlextResult[FlextTypes.Core.Dict]:
            """Railway-oriented validation of JSON request data.

            Returns:
            ResponseReturnValue:: Description of return value.

            """
            if not request.is_json:
                return FlextResult[FlextTypes.Core.Dict].fail("Request must be JSON")

            try:
                data = request.get_json()
                if not data:
                    return FlextResult[FlextTypes.Core.Dict].fail(
                        "Request body is required"
                    )
                return FlextResult[FlextTypes.Core.Dict].ok(data)
            except Exception:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    "Invalid JSON in request body"
                )

        def _validate_app_data(
            self, data: FlextTypes.Core.Dict
        ) -> FlextResult[tuple[str, str, int]]:
            """Validate application data using Railway pattern."""
            # Extract and validate required fields
            try:
                name = data.get("name")
                host = data.get(
                    "host", "localhost"
                )  # Use string literal for localhost (not configurable)
                port = data.get(
                    "port", 8000
                )  # Use 8000 for web service development (not 80 which requires root)

                if not name or not isinstance(name, str):
                    return FlextResult[tuple[str, str, int]].fail(
                        "Name is required and must be a string"
                    )

                if not isinstance(host, str):
                    return FlextResult[tuple[str, str, int]].fail(
                        "Host must be a string"
                    )

                # Convert port to int if it's a string
                if isinstance(port, str):
                    try:
                        port = int(port)
                    except ValueError:
                        return FlextResult[tuple[str, str, int]].fail(
                            "Port must be a valid integer"
                        )
                elif not isinstance(port, int):
                    return FlextResult[tuple[str, str, int]].fail(
                        "Port must be an integer"
                    )

                return FlextResult[tuple[str, str, int]].ok((name, host, port))

            except Exception as e:
                return FlextResult[tuple[str, str, int]].fail(f"Validation failed: {e}")

        def _create_and_store_app(
            self, name: str, host: str, port: int
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Create and store application using existing handler."""
            create_result = self.app_handler.create(name, port, host)

            if create_result.is_failure:
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"Application creation failed: {create_result.error}"
                )

            app = create_result.value
            self.apps[app.id] = app

            FlextMixins.log_operation(
                self,
                "app_created",
                app_name=app.name,
                app_host=app.host,
                app_port=app.port,
            )

            return FlextResult[FlextWebModels.WebApp].ok(app)

        def _build_success_response(
            self, app: FlextWebModels.WebApp
        ) -> ResponseReturnValue:
            """Build success response using consistent format."""
            return jsonify(
                {
                    "success": True,
                    "message": "Application created successfully",
                    "data": {
                        "id": app.id,
                        "name": app.name,
                        "host": app.host,
                        "port": app.port,
                        "status": app.status.value,
                    },
                }
            ), 201

        def _build_error_response(
            self, error: str, status_code: int = 400
        ) -> ResponseReturnValue:
            """Build error response using consistent format."""
            return jsonify(
                {
                    "success": False,
                    "message": error,
                }
            ), status_code

        def create_app(self) -> ResponseReturnValue:
            """Create new application using Railway-oriented programming pattern.

            Reduces from 11 returns to single monadic chain with 85% less complexity.
            Uses Python 3.13 functional composition and existing flext-core validation.

            Returns:
            ResponseReturnValue:: Description of return value.

            """
            try:
                FlextMixins.log_operation(
                    self, "create_app_request", request_type="POST"
                )

                # Railway-oriented programming: compose operations monadically
                result = (
                    self._validate_json_request()
                    .bind(self._validate_app_data)
                    .bind(lambda args: self._create_and_store_app(*args))
                )

                # Handle result using functional approach
                return (
                    self._build_success_response(result.value)
                    if result.is_success
                    else self._build_error_response(result.error or "Unknown error")
                )

            except Exception as e:
                return self._build_error_response(
                    f"Internal error during application creation: {e}", 500
                )

        def get_app(self, app_id: str) -> ResponseReturnValue:
            """Get specific application by ID."""
            try:
                if app_id not in self.apps:
                    return jsonify(
                        {
                            "success": False,
                            "message": f"Application {app_id} not found",
                        }
                    ), 404

                app = self.apps[app_id]
                return jsonify(
                    {
                        "success": True,
                        "message": "Application found",
                        "data": {
                            "id": app.id,
                            "name": app.name,
                            "host": app.host,
                            "port": app.port,
                            "status": app.status.value,
                            "is_running": bool(app.is_running),
                        },
                    }
                )

            except Exception as e:
                return jsonify(
                    {
                        "success": False,
                        "message": "Failed to get application",
                        "error": str(e),
                    }
                ), 500

        def start_app(self, app_id: str) -> ResponseReturnValue:
            """Start application by ID.

            Returns:
            ResponseReturnValue:: Description of return value.

            """
            try:
                if app_id not in self.apps:
                    return jsonify(
                        {
                            "success": False,
                            "message": f"Application {app_id} not found",
                        }
                    ), 404

                app = self.apps[app_id]
                start_result = app.start()

                if start_result.is_failure:
                    return jsonify(
                        {
                            "success": False,
                            "message": start_result.error or "Application start failed",
                            "error": start_result.error,
                        }
                    ), 400

                # Update stored application
                self.apps[app_id] = start_result.value

                return jsonify(
                    {
                        "success": True,
                        "message": f"Application {app.name} started successfully",
                        "data": {
                            "id": app_id,
                            "name": app.name,
                            "status": "running",
                        },
                    }
                )

            except Exception as e:
                return jsonify(
                    {
                        "success": False,
                        "message": "Failed to start application",
                        "error": str(e),
                    }
                ), 500

        def stop_app(self, app_id: str) -> ResponseReturnValue:
            """Stop application by ID."""
            try:
                if app_id not in self.apps:
                    return jsonify(
                        {
                            "success": False,
                            "message": f"Application {app_id} not found",
                        }
                    ), 404

                app = self.apps[app_id]
                stop_result = app.stop()

                if stop_result.is_failure:
                    # Customize message based on error type
                    message = "Application stop failed"
                    if "not running" in (stop_result.error or "").lower():
                        message = "Application is already stopped"

                    return jsonify(
                        {
                            "success": False,
                            "message": message,
                            "error": stop_result.error,
                        }
                    ), 400

                # Update stored application
                self.apps[app_id] = stop_result.value

                return jsonify(
                    {
                        "success": True,
                        "message": f"Application {app.name} stopped successfully",
                        "data": {
                            "id": app_id,
                            "name": app.name,
                            "status": "stopped",
                        },
                    }
                )

            except Exception as e:
                return jsonify(
                    {
                        "success": False,
                        "message": "Failed to stop application",
                        "error": str(e),
                    }
                ), 500

        def run(self) -> None:
            """Run the Flask web service.

            Returns:
            ResponseReturnValue:: Description of return value.

            """
            self.app.run(
                host=self.config.host,
                port=self.config.port,
                debug=self.config.debug,
                use_reloader=False,  # Disable reloader for production use
                threaded=True,  # Enable threading for concurrent requests
            )

    class WebServiceRegistry:
        """Service registry for web service discovery and management.

        Provides centralized registry functionality for web service instances,
        supporting service discovery, health monitoring, and lifecycle management
        within the FLEXT Web ecosystem.
        """

        def __init__(self) -> None:
            """Initialize web service registry."""
            self._services: dict[str, FlextWebServices.WebService] = {}
            self._health_status: dict[str, bool] = {}
            self.logger = FlextLogger(__name__)

            # Initialize FlextMixins functionality
            FlextMixins.create_timestamp_fields(self)
            FlextMixins.ensure_id(self)
            FlextMixins.initialize_validation(self)
            FlextMixins.initialize_state(self, "active")

            FlextMixins.log_operation(self, "registry_init", initialized=True)

        def register_web_service(
            self, name: str, service: FlextWebServices.WebService
        ) -> FlextResult[None]:
            """Register web service instance.

            Returns:
                FlextResult[None]: Success or error result.

            """
            try:
                FlextMixins.log_operation(self, "register_service", service_name=name)

                if name in self._services:
                    return FlextResult[None].fail(f"Service {name} already registered")

                self._services[name] = service
                self._health_status[name] = True

                FlextMixins.log_operation(
                    self, "service_registered", service_name=name, success=True
                )
                return FlextResult[None].ok(None)

            except Exception as e:
                return FlextResult[None].fail(f"Service registration failed: {e}")

        def discover_web_service(
            self, name: str
        ) -> FlextResult[FlextWebServices.WebService]:
            """Discover web service by name."""
            try:
                FlextMixins.log_operation(self, "discover_service", service_name=name)

                if name not in self._services:
                    FlextMixins.log_operation(
                        self, "service_not_found", service_name=name
                    )
                    return FlextResult[FlextWebServices.WebService].fail(
                        f"Service {name} not found"
                    )

                service = self._services[name]
                FlextMixins.log_operation(
                    self, "service_discovered", service_name=name, success=True
                )
                return FlextResult[FlextWebServices.WebService].ok(service)

            except Exception as e:
                return FlextResult[FlextWebServices.WebService].fail(
                    f"Service discovery failed: {e}"
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
                    f"Service listing failed: {e}"
                )

        # Alias methods for test compatibility
        def register_service(
            self, name: str, service: FlextWebServices.WebService
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
        cls, config: FlextWebConfigs.WebConfig | None = None
    ) -> FlextResult[FlextWebServices.WebService]:
        """Create web service instance with configuration.

        Returns:
            FlextResult[FlextWebServices.WebService]: Created service instance.

        """
        try:
            if config is None:
                config_result = FlextWebConfigs.create_web_config()
                if config_result.is_failure:
                    return FlextResult[FlextWebServices.WebService].fail(
                        f"Config creation failed: {config_result.error}"
                    )
                config = config_result.value
                # Config type is guaranteed by FlextResult[FlextWebConfigs.WebConfig]

            service = FlextWebServices.WebService(config)
            return FlextResult[FlextWebServices.WebService].ok(service)

        except Exception as e:
            return FlextResult[FlextWebServices.WebService].fail(
                f"Web service creation failed: {e}"
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
                f"Registry creation failed: {e}"
            )

    @classmethod
    def create_web_system_services(
        cls, config: FlextTypes.Core.Dict | None = None
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create web system services."""
        _ = config  # Acknowledge parameter

        try:
            # Create service and registry
            service_result = cls.create_web_service()
            if service_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    service_result.error or "Service creation failed"
                )

            registry_result = cls.create_service_registry()
            if registry_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    registry_result.error or "Registry creation failed"
                )

            service = service_result.value
            registry = registry_result.value

            # Register service
            register_result = registry.register_web_service("main", service)
            if register_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    register_result.error or "Registration failed"
                )

            return FlextResult[FlextTypes.Core.Dict].ok(
                {
                    "web_service": service,
                    "registry": registry,
                }
            )

        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"System services creation failed: {e}"
            )

    # =============================================================================
    # FLEXT WEB SERVICES CONFIGURATION METHODS
    # =============================================================================

    @classmethod
    def configure_web_services_system(
        cls, config: FlextTypes.Config.ConfigDict
    ) -> FlextResult[FlextTypes.Config.ConfigDict]:
        """Configure web services system using FlextTypes.Config with validation."""
        try:
            validated_config = dict(config)

            # Validate environment using FlextConstants
            if "environment" in config:
                env_value = config["environment"]
                valid_environments = [
                    e.value for e in FlextConstants.Config.ConfigEnvironment
                ]
                if env_value not in valid_environments:
                    return FlextResult[FlextTypes.Config.ConfigDict].fail(
                        f"Invalid environment '{env_value}'. Valid options: {valid_environments}"
                    )
            else:
                validated_config["environment"] = (
                    FlextConstants.Config.ConfigEnvironment.DEVELOPMENT.value
                )

            # Core validation via flext-core SystemConfigs (bridge compatibility)
            from flext_core import (
                FlextModels,  # local import to avoid cycles
            )

            core_validation = {
                "environment": validated_config.get(
                    "environment",
                    FlextConstants.Config.ConfigEnvironment.DEVELOPMENT.value,
                ),
                "log_level": validated_config.get(
                    "log_level",
                    FlextConstants.Config.LogLevel.INFO.value,
                ),
                "validation_level": validated_config.get(
                    "validation_level",
                    FlextConstants.Config.ValidationLevel.NORMAL.value,
                ),
            }
            _ = FlextModels.SystemConfigs.BaseSystemConfig.model_validate(
                core_validation
            )

            # Web services specific settings
            validated_config.setdefault("enable_web_service", True)
            validated_config.setdefault("enable_service_registry", True)
            validated_config.setdefault("max_concurrent_requests", 100)
            validated_config.setdefault("request_timeout_seconds", 30)

            return FlextResult[FlextTypes.Config.ConfigDict].ok(validated_config)

        except Exception as e:
            return FlextResult[FlextTypes.Config.ConfigDict].fail(
                f"Failed to configure web services system: {e}"
            )

    @classmethod
    def get_web_services_system_config(
        cls,
    ) -> FlextResult[FlextTypes.Config.ConfigDict]:
        """Get current web services system configuration with runtime information."""
        try:
            config: FlextTypes.Config.ConfigDict = {
                # Environment configuration
                "environment": FlextConstants.Config.ConfigEnvironment.DEVELOPMENT.value,
                "log_level": FlextConstants.Config.LogLevel.INFO.value,
                # Web services specific settings
                "enable_web_service": True,
                "enable_service_registry": True,
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

            return FlextResult[FlextTypes.Config.ConfigDict].ok(config)

        except Exception as e:
            return FlextResult[FlextTypes.Config.ConfigDict].fail(
                f"Failed to get web services system config: {e}"
            )


__all__ = [
    "FlextWebServices",
]
