"""FLEXT Web Services - Consolidated web service system with enterprise patterns.

CONSOLIDAÇÃO COMPLETA seguindo flext-core architectural patterns:
- Apenas UMA classe FlextWebServices com toda funcionalidade
- Todas as outras classes antigas removidas completamente
- Arquitetura hierárquica seguindo padrão FLEXT estrito
- Python 3.13+ com Flask avançado sem compatibilidade legada

Architecture Overview:
    FlextWebServices - Single consolidated class containing:
        - Nested service classes for web operations (WebService, etc.)
        - Factory methods for creating service instances
        - Configuration methods for web service setup
        - Integration with FlextServices foundation patterns

Examples:
    Using consolidated FlextWebServices:
        service = FlextWebServices.WebService(config)
        registry = FlextWebServices.create_service_registry()
        result = FlextWebServices.create_web_service(config)

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flask import Flask, jsonify, render_template_string, request
from flask.typing import ResponseReturnValue
from flext_core import (
    FlextConstants,
    FlextResult,
    FlextTypes,
    FlextUtilities,
)

from flext_web.config import FlextWebConfigs
from flext_web.models import FlextWebModels
from flext_web.typings import FlextWebTypes


class FlextWebServices:
    """Consolidated FLEXT web service system providing all service functionality.

    This is the complete web service system for the FLEXT Web ecosystem, providing
    unified service patterns built on FlextServices foundation with web-specific
    implementations. All web service types are organized as nested classes within
    this single container for consistent configuration and easy access.

    Architecture Overview:
        The system is organized following Service-Oriented Architecture and flext-core patterns:

        - **Service Classes**: Web service implementations with Flask integration
        - **Service Registry**: Discovery and management of web services
        - **Service Configuration**: Environment-specific service setup
        - **Factory Methods**: Safe service creation returning FlextResult
        - **Integration Points**: Seamless flext-core service compatibility

    Design Patterns:
        - **Single Point of Truth**: All web services defined in one location
        - **Service Orchestration**: Integration with FlextServices patterns
        - **Type Safety**: Comprehensive generic type annotations and validation
        - **Railway Programming**: Service methods return FlextResult for error handling
        - **Dependency Injection**: Built-in service discovery and registration
        - **Flask Integration**: Native Flask application service hosting

    Usage Examples:
        Web service creation::

            # Create web service with configuration
            config = FlextWebConfigs.WebConfig(host="localhost", port=8080)
            service_result = FlextWebServices.create_web_service(config)

            # Run service
            if service_result.success:
                service = service_result.value
                service.run()

        Service management::

            # Create service registry
            registry_result = FlextWebServices.create_service_registry()

            # Register service
            registry = registry_result.value
            registry.register_web_service("main", service)

    Note:
        This consolidated approach follows flext-core architectural patterns,
        ensuring consistency with FlextServices while providing web-specific
        service functionality through Flask integration.

    """

    # =============================================================================
    # WEB SERVICE CLASSES
    # =============================================================================

    class WebService:
        """Primary web service implementation with Flask integration and application management.

        Enterprise-grade web service providing REST API endpoints, web dashboard,
        and comprehensive application lifecycle management. Built on Flask with
        FlextServices integration for consistent service patterns.

        Features:
            - **REST API**: Complete CRUD operations for web applications
            - **Web Dashboard**: HTML interface for application management
            - **State Management**: In-memory application registry with persistence support
            - **Health Monitoring**: Service health checks and status reporting
            - **Error Handling**: Comprehensive error handling with FlextResult patterns

        Endpoints:
            - GET /health: Service health check
            - GET /: Web dashboard interface
            - GET /api/v1/apps: List all applications
            - POST /api/v1/apps: Create new application
            - GET /api/v1/apps/<id>: Get application details
            - POST /api/v1/apps/<id>/start: Start application
            - POST /api/v1/apps/<id>/stop: Stop application

        Integration:
            - Built on Flask WSGI framework
            - Uses FlextWebModels for domain entities
            - Integrates with FlextResult for error handling
            - Compatible with FlextServices orchestration patterns
        """

        def __init__(self, config: FlextWebConfigs.WebConfig) -> None:
            """Initialize web service with configuration and Flask application."""
            self.config = config
            self.app = Flask(__name__)
            self.apps: dict[str, FlextWebModels.WebApp] = {}
            self.app_handler = FlextWebModels.WebAppHandler()

            # Configure Flask application
            self.app.config.update(
                {
                    "SECRET_KEY": config.secret_key,
                    "DEBUG": config.debug,
                }
            )

            # Register routes
            self._register_routes()

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
                health_data: FlextWebTypes.HealthResponse = {
                    "status": "healthy",
                    "service": "flext-web",
                    "version": "0.9.0",
                    "applications": len(self.apps),
                    "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
                }

                return jsonify(
                    {
                        "success": True,
                        "message": "Service is healthy",
                        "data": health_data,
                    }
                ), 200
            except Exception:
                return jsonify(
                    {
                        "success": False,
                        "message": "Service health check failed",
                        "data": {
                            "status": "unhealthy",
                            "error": "Internal error",
                        },
                    }
                ), 500

        def dashboard(self) -> ResponseReturnValue:
            """Web dashboard interface for application management."""
            try:
                app_count = len(self.apps)
                running_count = sum(1 for app in self.apps.values() if app.is_running)

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
                        "is_running": app.is_running,
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

        def create_app(self) -> ResponseReturnValue:
            """Create new application from JSON request."""
            try:
                if not request.is_json:
                    return jsonify(
                        {
                            "success": False,
                            "message": "Request must be JSON",
                        }
                    ), 400

                try:
                    data = request.get_json()
                except Exception:
                    return jsonify(
                        {
                            "success": False,
                            "message": "Invalid JSON in request body",
                        }
                    ), 400

                if not data:
                    return jsonify(
                        {
                            "success": False,
                            "message": "Request body is required",
                        }
                    ), 400

                # Extract and validate required fields with type checking
                name = data.get("name")
                host = data.get("host", "localhost")
                port = data.get("port")

                # Validate name field
                if not name:
                    return jsonify(
                        {
                            "success": False,
                            "message": "Application name is required",
                        }
                    ), 400

                if not isinstance(name, str):
                    return jsonify(
                        {
                            "success": False,
                            "message": "Application name must be a string",
                        }
                    ), 400

                # Validate host field
                if host is not None and not isinstance(host, str):
                    return jsonify(
                        {
                            "success": False,
                            "message": "Host must be a string",
                        }
                    ), 400

                # Validate and convert port field
                if not port:
                    port = 8000  # Use default port if not provided
                elif isinstance(port, str):
                    try:
                        port = int(port)
                    except ValueError:
                        return jsonify(
                            {
                                "success": False,
                                "message": "Port must be a valid integer",
                            }
                        ), 400
                elif not isinstance(port, int):
                    return jsonify(
                        {
                            "success": False,
                            "message": "Port must be an integer",
                        }
                    ), 400

                # Create application using handler
                # Ensure host has a default value if None after validation
                if host is None:
                    host = "localhost"
                create_result = self.app_handler.create(name, port, host)
                if create_result.is_failure:
                    return jsonify(
                        {
                            "success": False,
                            "message": "Application creation failed",
                            "error": create_result.error,
                        }
                    ), 400

                # Store application
                app = create_result.value
                self.apps[app.id] = app

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

            except Exception as e:
                return jsonify(
                    {
                        "success": False,
                        "message": "Internal error during application creation",
                        "error": str(e),
                    }
                ), 500

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
                            "is_running": app.is_running,
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
            """Start application by ID."""
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
                    if "already stopped" in (stop_result.error or ""):
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
            """Run the Flask web service."""
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

        Features:
            - **Service Registration**: Register web service instances
            - **Service Discovery**: Find services by name or type
            - **Health Monitoring**: Track service health and availability
            - **Load Balancing**: Support for multiple service instances

        Integration:
            - Built on FlextServices.ServiceRegistry patterns
            - Uses FlextResult for error handling
            - Compatible with FlextServices orchestration
        """

        def __init__(self) -> None:
            """Initialize web service registry."""
            self._services: dict[str, FlextWebServices.WebService] = {}
            self._health_status: dict[str, bool] = {}

        def register_web_service(
            self, name: str, service: FlextWebServices.WebService
        ) -> FlextResult[None]:
            """Register web service instance."""
            try:
                if name in self._services:
                    return FlextResult[None].fail(f"Service {name} already registered")

                self._services[name] = service
                self._health_status[name] = True
                return FlextResult[None].ok(None)

            except Exception as e:
                return FlextResult[None].fail(f"Service registration failed: {e}")

        def discover_web_service(
            self, name: str
        ) -> FlextResult[FlextWebServices.WebService]:
            """Discover web service by name."""
            try:
                if name not in self._services:
                    return FlextResult[FlextWebServices.WebService].fail(
                        f"Service {name} not found"
                    )

                service = self._services[name]
                return FlextResult[FlextWebServices.WebService].ok(service)

            except Exception as e:
                return FlextResult[FlextWebServices.WebService].fail(
                    f"Service discovery failed: {e}"
                )

        def list_web_services(self) -> FlextResult[list[str]]:
            """List all registered web service names."""
            try:
                service_names = list(self._services.keys())
                return FlextResult[list[str]].ok(service_names)
            except Exception as e:
                return FlextResult[list[str]].fail(f"Service listing failed: {e}")

    # =============================================================================
    # FACTORY METHODS AND UTILITIES
    # =============================================================================

    @classmethod
    def create_web_service(
        cls, config: FlextWebConfigs.WebConfig | None = None
    ) -> FlextResult[FlextWebServices.WebService]:
        """Create web service instance with configuration."""
        try:
            if config is None:
                # Import here to avoid circular dependency
                from flext_web.config import FlextWebConfigs

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
        cls,
        config: dict[str, object] | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Create complete web system services with configuration."""
        # Use config if needed for service creation, otherwise use defaults
        _ = config  # Acknowledge parameter
        try:
            services: dict[str, object] = {}

            # Create main web service
            web_service_result = cls.create_web_service()
            if web_service_result.is_failure:
                return FlextResult[dict[str, object]].fail(
                    f"Web service creation failed: {web_service_result.error}"
                )
            services["web_service"] = web_service_result.value

            # Create service registry
            registry_result = cls.create_service_registry()
            if registry_result.is_failure:
                return FlextResult[dict[str, object]].fail(
                    f"Registry creation failed: {registry_result.error}"
                )
            services["registry"] = registry_result.value

            # Register web service in registry
            registry = services["registry"]
            if not isinstance(registry, FlextWebServices.WebServiceRegistry):
                return FlextResult[dict[str, object]].fail("Invalid registry type")
            web_service = services["web_service"]
            if not isinstance(web_service, FlextWebServices.WebService):
                return FlextResult[dict[str, object]].fail("Invalid web service type")
            register_result = registry.register_web_service("main", web_service)
            if register_result.is_failure:
                return FlextResult[dict[str, object]].fail(
                    f"Service registration failed: {register_result.error}"
                )

            return FlextResult[dict[str, object]].ok(services)

        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"Web system services creation failed: {e}"
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


# FlextWebConfigs imported at top of file


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    "FlextWebServices",
]
