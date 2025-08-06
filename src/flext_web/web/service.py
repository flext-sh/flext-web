"""FLEXT Web Service - Flask-based web service with REST API and dashboard.

This module implements the Flask-based web service for the FLEXT Web Interface,
providing REST API endpoints and web dashboard functionality with Clean Architecture
patterns and enterprise-grade reliability.

Key Components:
    - FlextWebService: Flask service with route registration and API endpoints

Integration:
    - Built on Flask web framework with enterprise patterns
    - Uses FlextWebAppHandler for CQRS application operations
    - Integrates with FlextWebConfig for configuration management
    - Compatible with reverse proxy and load balancer deployment
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask import Flask, jsonify, request
from flext_core import get_logger

from flext_web.config import FlextWebConfig
from flext_web.domain import FlextWebApp, FlextWebAppHandler

if TYPE_CHECKING:
    from flask.typing import ResponseReturnValue


class FlextWebService:
    """Flask-based web service providing REST API and dashboard with enterprise patterns.

    Comprehensive web service implementation providing both REST API endpoints
    and web dashboard functionality using Flask framework integration with
    flext-core patterns. The service implements Clean Architecture with proper
    separation between presentation, application, and domain concerns.

    The service provides complete application lifecycle management through
    RESTful endpoints, comprehensive health monitoring, and an integrated
    web dashboard for operational visibility. All operations follow
    railway-oriented programming patterns with structured error handling.

    Features:
        - RESTful API endpoints for application management
        - Web dashboard with real-time application status
        - Health check endpoints for monitoring integration
        - Structured JSON responses with consistent error handling
        - Integration with CQRS handlers for business logic
        - Flask integration with enterprise configuration patterns

    Architecture:
        - Presentation Layer: Flask routes and response formatting
        - Application Layer: CQRS handlers and business operations
        - Domain Layer: Application entities and business rules
        - Infrastructure Layer: HTTP framework and external integrations

    API Endpoints:
        GET /health - Service health check with system metrics
        GET / - Web dashboard with application overview
        GET /api/v1/apps - List all managed applications
        POST /api/v1/apps - Create new application
        GET /api/v1/apps/<id> - Get application details
        POST /api/v1/apps/<id>/start - Start application
        POST /api/v1/apps/<id>/stop - Stop application

    Integration:
        - Built on Flask web framework with enterprise patterns
        - Uses FlextWebAppHandler for CQRS application operations
        - Integrates with FlextWebConfig for configuration management
        - Compatible with reverse proxy and load balancer deployment
        - Supports monitoring and observability integration

    Example:
        Basic service setup and startup:

        >>> config = FlextWebConfig(host="localhost", port=8080)
        >>> service = FlextWebService(config)
        >>> service.run()  # Starts Flask development server

        Production deployment with custom configuration:

        >>> config = FlextWebConfig(host="0.0.0.0", port=8080, debug=False)
        >>> service = FlextWebService(config)
        >>> service.run(host=config.host, port=config.port, debug=False)

    """

    def __init__(self, config: FlextWebConfig | None = None) -> None:
        self.config = config or FlextWebConfig()
        self.app = Flask(__name__)
        self.app.secret_key = self.config.secret_key
        self.handler = FlextWebAppHandler()
        self.apps: dict[str, FlextWebApp] = {}
        self.logger = get_logger(__name__)
        self._register_routes()

    def _register_routes(self) -> None:
        """Register Flask routes."""
        self.app.route("/health")(self.health_check)
        self.app.route("/api/v1/apps", methods=["GET"])(self.list_apps)
        self.app.route("/api/v1/apps", methods=["POST"])(self.create_app)
        self.app.route("/api/v1/apps/<app_id>", methods=["GET"])(self.get_app)
        self.app.route("/api/v1/apps/<app_id>/start", methods=["POST"])(self.start_app)
        self.app.route("/api/v1/apps/<app_id>/stop", methods=["POST"])(self.stop_app)
        self.app.route("/")(self.dashboard)

    def _create_response(
        self,
        *,
        success: bool,
        message: str,
        data: dict[str, object] | None = None,
        status: int = 200,
    ) -> ResponseReturnValue:
        """Create standardized response."""
        response = jsonify(
            {
                "success": success,
                "message": message,
                "data": data,
            },
        )
        response.status_code = status
        return response

    def health_check(self) -> ResponseReturnValue:
        """Health check endpoint."""
        return self._create_response(
            success=True,
            message="FLEXT Web Service is healthy",
            data={
                "status": "healthy",
                "version": self.config.version,
                "apps_count": len(self.apps),
                "config": self.config.app_name,
            },
        )

    def list_apps(self) -> ResponseReturnValue:
        """List all applications."""
        apps_data = [
            {
                "id": app.id,
                "name": app.name,
                "port": app.port,
                "host": app.host,
                "is_running": app.is_running,
                "status": app.status.value,
            }
            for app in self.apps.values()
        ]
        return self._create_response(
            success=True,
            message="Applications retrieved successfully",
            data={"apps": apps_data},
        )

    def create_app(self) -> ResponseReturnValue:
        """Create new application using handler."""
        data = request.get_json()

        if not data or not data.get("name"):
            return self._create_response(
                success=False, message="App name is required", status=400,
            )

        name = data["name"]
        port = data.get("port", 8000)
        host = data.get("host", "localhost")

        app_result = self.handler.create(name, port, host)

        if app_result.success:
            app = app_result.data
            if app is not None:
                self.apps[app.id] = app

                app_data = {
                    "id": app.id,
                    "name": app.name,
                    "port": app.port,
                    "host": app.host,
                    "is_running": app.is_running,
                    "status": app.status.value,
                }
                return self._create_response(
                    success=True,
                    message="Application created successfully",
                    data=app_data,
                )

        return self._create_response(
            success=False,
            message=f"Failed to create app: {app_result.error}",
            status=400,
        )

    def get_app(self, app_id: str) -> ResponseReturnValue:
        """Get application information."""
        app = self.apps.get(app_id)
        if not app:
            return self._create_response(
                success=False, message="Application not found", status=404,
            )

        app_data = {
            "id": app.id,
            "name": app.name,
            "port": app.port,
            "host": app.host,
            "is_running": app.is_running,
            "status": app.status.value,
        }
        return self._create_response(
            success=True,
            message="Application retrieved successfully",
            data=app_data,
        )

    def start_app(self, app_id: str) -> ResponseReturnValue:
        """Start application using handler."""
        app = self.apps.get(app_id)
        if not app:
            return self._create_response(
                success=False, message="Application not found", status=404,
            )

        start_result = self.handler.start(app)

        if start_result.success:
            started_app = start_result.data
            if started_app is not None:
                self.apps[app_id] = started_app

                app_data = {
                    "id": started_app.id,
                    "name": started_app.name,
                    "is_running": started_app.is_running,
                    "status": started_app.status.value,
                }
                return self._create_response(
                    success=True,
                    message="Application started successfully",
                    data=app_data,
                )

        return self._create_response(
            success=False,
            message=f"Failed to start app: {start_result.error}",
            status=400,
        )

    def stop_app(self, app_id: str) -> ResponseReturnValue:
        """Stop application using handler."""
        app = self.apps.get(app_id)
        if not app:
            return self._create_response(
                success=False, message="Application not found", status=404,
            )

        stop_result = self.handler.stop(app)

        if stop_result.success:
            stopped_app = stop_result.data
            if stopped_app is not None:
                self.apps[app_id] = stopped_app

                app_data = {
                    "id": stopped_app.id,
                    "name": stopped_app.name,
                    "is_running": stopped_app.is_running,
                    "status": stopped_app.status.value,
                }
                return self._create_response(
                    success=True,
                    message="Application stopped successfully",
                    data=app_data,
                )

        return self._create_response(
            success=False,
            message=f"Failed to stop app: {stop_result.error}",
            status=400,
        )

    def dashboard(self) -> str:
        """Serve dashboard."""
        apps_count = len(self.apps)
        running_count = sum(1 for app in self.apps.values() if app.is_running)

        return f"""<!DOCTYPE html>
<html>
<head>
    <title>{self.config.app_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }}
        .header {{ color: #333; border-bottom: 2px solid #007bff; padding-bottom: 20px; }}
        .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat {{ background: #007bff; color: white; padding: 15px; border-radius: 5px; flex: 1; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{self.config.app_name}</h1>
            <p>Enterprise Web Interface v{self.config.version}</p>
        </div>
        <div class="stats">
            <div class="stat">
                <h3>{apps_count}</h3>
                <p>Total Apps</p>
            </div>
            <div class="stat">
                <h3>{running_count}</h3>
                <p>Running Apps</p>
            </div>
        </div>
        <h2>Features</h2>
        <ul>
            <li>✓ Flask-based web interface</li>
            <li>✓ flext-core standardization</li>
            <li>✓ Enterprise patterns</li>
            <li>✓ Type-safe operations</li>
        </ul>
    </div>
</body>
</html>"""

    def run(
        self,
        host: str | None = None,
        port: int | None = None,
        *,
        debug: bool | None = None,
    ) -> None:
        """Run the web service."""
        run_host = host or self.config.host
        run_port = port or self.config.port
        run_debug = debug if debug is not None else self.config.debug

        self.logger.info(
            "Starting %s on %s:%d", self.config.app_name, run_host, run_port,
        )
        self.app.run(host=run_host, port=run_port, debug=run_debug)
