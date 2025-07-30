"""FlextWeb - Web Interface Library using Flask + flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Web interface library providing Flask integration with flext-core standardization.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from flask import Flask, jsonify, request
from flext_core import (
    FlextConfig,
    FlextEntity,
    FlextError,
    FlextHandlers,
    FlextResult,
    FlextTimestampMixin,
    FlextValidatableMixin,
    FlextValidationError,
    FlextValidators,
    get_logger,
)
from pydantic import Field
from pydantic_settings import BaseSettings

if TYPE_CHECKING:
    from flask.typing import ResponseReturnValue

__version__ = "0.9.0"
__author__ = "FLEXT Contributors"

logger = get_logger(__name__)


# =============================================================================
# DOMAIN MODELS - Using flext-core patterns
# =============================================================================


class FlextWebAppStatus(Enum):
    """Web application status enumeration."""

    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"


class FlextWebApp(FlextEntity, FlextTimestampMixin, FlextValidatableMixin):
    """Web application entity using flext-core composition."""

    name: str = Field(description="Application name")
    host: str = Field(default="localhost", description="Host address")
    port: int = Field(default=8000, ge=1, le=65535, description="Port number")
    status: FlextWebAppStatus = Field(
        default=FlextWebAppStatus.STOPPED,
        description="Application status",
    )

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate application using FlextValidators."""
        if not FlextValidators.is_non_empty_string(self.name):
            return FlextResult.fail("App name is required")
        if not (1 <= self.port <= 65535):
            return FlextResult.fail("Invalid port number")
        return FlextResult.ok(None)

    @property
    def is_running(self) -> bool:
        """Check if application is running."""
        return self.status == FlextWebAppStatus.RUNNING

    def start(self) -> FlextResult[FlextWebApp]:
        """Start application."""
        if self.status == FlextWebAppStatus.RUNNING:
            return FlextResult.fail("Application already running")
        if self.status == FlextWebAppStatus.STARTING:
            return FlextResult.fail("Application already starting")
        return FlextResult.ok(
            self.model_copy(update={"status": FlextWebAppStatus.RUNNING}),
        )

    def stop(self) -> FlextResult[FlextWebApp]:
        """Stop application."""
        if self.status == FlextWebAppStatus.STOPPED:
            return FlextResult.fail("Application already stopped")
        if self.status == FlextWebAppStatus.STOPPING:
            return FlextResult.fail("Application already stopping")
        return FlextResult.ok(
            self.model_copy(update={"status": FlextWebAppStatus.STOPPED}),
        )


# =============================================================================
# CONFIGURATION - Using FlextConfig patterns
# =============================================================================


class FlextWebConfig(BaseSettings, FlextConfig):
    """Web configuration using flext-core patterns."""

    model_config = {
        "env_prefix": "FLEXT_WEB_",
        "case_sensitive": False,
        "validate_assignment": True,
    }

    app_name: str = Field(default="FLEXT Web", description="Application name")
    version: str = Field(default="0.9.0", description="Application version")
    debug: bool = Field(default=True, description="Debug mode")

    # Server settings
    host: str = Field(default="localhost", description="Server host")
    port: int = Field(default=8080, ge=1, le=65535, description="Server port")

    # Security settings
    secret_key: str = Field(
        default="change-in-production-" + "x" * 32,
        min_length=32,
        description="Secret key for cryptographic operations",
    )

    def validate_config(self) -> FlextResult[None]:
        """Validate configuration using FlextValidators."""
        if not FlextValidators.is_non_empty_string(self.app_name):
            return FlextResult.fail("App name is required")
        if not FlextValidators.matches_pattern(self.version, r"^\d+\.\d+\.\d+$"):
            return FlextResult.fail("Invalid version format (use x.y.z)")
        if not FlextValidators.is_non_empty_string(self.host):
            return FlextResult.fail("Host is required")
        if not (1 <= self.port <= 65535):
            return FlextResult.fail("Port must be between 1 and 65535")
        # Security validation in production
        if not self.debug and "change-in-production" in self.secret_key:
            return FlextResult.fail("Secret key must be changed in production")
        return FlextResult.ok(None)

    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.debug

    def get_server_url(self) -> str:
        """Get complete server URL."""
        return f"http://{self.host}:{self.port}"


# =============================================================================
# HANDLERS - Using FlextHandlers patterns
# =============================================================================


class FlextWebAppHandler(FlextHandlers.Handler[FlextWebApp, FlextWebApp]):
    """Web application handler using flext-core patterns."""

    def create(
        self,
        name: str,
        port: int = 8000,
        host: str = "localhost",
    ) -> FlextResult[FlextWebApp]:
        """Create WebApp with validation."""
        try:
            app = FlextWebApp(id=f"app_{name}", name=name, port=port, host=host)
            validation = app.validate_domain_rules()

            if not validation.is_success:
                return FlextResult.fail(validation.error or "Validation failed")

            return FlextResult.ok(app)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to create app: {e}")

    def start(self, app: FlextWebApp) -> FlextResult[FlextWebApp]:
        """Start WebApp with validation."""
        validation = app.validate_domain_rules()
        if not validation.is_success:
            return FlextResult.fail(validation.error or "Validation failed")
        return app.start()

    def stop(self, app: FlextWebApp) -> FlextResult[FlextWebApp]:
        """Stop WebApp."""
        return app.stop()


# =============================================================================
# WEB SERVICE - Flask integration with flext-core patterns
# =============================================================================


class FlextWebService:
    """Web service providing Flask integration with flext-core patterns."""

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
            True,
            "FLEXT Web Service is healthy",
            {
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
            True,
            "Applications retrieved successfully",
            {"apps": apps_data},
        )

    def create_app(self) -> ResponseReturnValue:
        """Create new application using handler."""
        data = request.get_json()

        if not data or not data.get("name"):
            return self._create_response(False, "App name is required", status=400)

        name = data["name"]
        port = data.get("port", 8000)
        host = data.get("host", "localhost")

        app_result = self.handler.create(name, port, host)

        if app_result.is_success:
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
                    True,
                    "Application created successfully",
                    app_data,
                )

        return self._create_response(
            False,
            f"Failed to create app: {app_result.error}",
            status=400,
        )

    def get_app(self, app_id: str) -> ResponseReturnValue:
        """Get application information."""
        app = self.apps.get(app_id)
        if not app:
            return self._create_response(False, "Application not found", status=404)

        app_data = {
            "id": app.id,
            "name": app.name,
            "port": app.port,
            "host": app.host,
            "is_running": app.is_running,
            "status": app.status.value,
        }
        return self._create_response(
            True,
            "Application retrieved successfully",
            app_data,
        )

    def start_app(self, app_id: str) -> ResponseReturnValue:
        """Start application using handler."""
        app = self.apps.get(app_id)
        if not app:
            return self._create_response(False, "Application not found", status=404)

        start_result = self.handler.start(app)

        if start_result.is_success:
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
                    True,
                    "Application started successfully",
                    app_data,
                )

        return self._create_response(
            False,
            f"Failed to start app: {start_result.error}",
            status=400,
        )

    def stop_app(self, app_id: str) -> ResponseReturnValue:
        """Stop application using handler."""
        app = self.apps.get(app_id)
        if not app:
            return self._create_response(False, "Application not found", status=404)

        stop_result = self.handler.stop(app)

        if stop_result.is_success:
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
                    True,
                    "Application stopped successfully",
                    app_data,
                )

        return self._create_response(
            False,
            f"Failed to stop app: {stop_result.error}",
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
        debug: bool | None = None,
    ) -> None:
        """Run the web service."""
        run_host = host or self.config.host
        run_port = port or self.config.port
        run_debug = debug if debug is not None else self.config.debug

        self.logger.info(f"Starting {self.config.app_name} on {run_host}:{run_port}")
        self.app.run(host=run_host, port=run_port, debug=run_debug)


# =============================================================================
# FACTORY FUNCTIONS - Configuration management
# =============================================================================


_config_instance: FlextWebConfig | None = None


def get_web_settings() -> FlextWebConfig:
    """Get web configuration singleton."""
    global _config_instance

    if _config_instance is None:
        _config_instance = FlextWebConfig()

        # Validate configuration
        validation_result = _config_instance.validate_config()
        if not validation_result.is_success:
            msg = f"Configuration validation failed: {validation_result.error}"
            raise ValueError(msg)

    return _config_instance


def reset_web_settings() -> None:
    """Reset configuration singleton (useful for testing)."""
    global _config_instance
    _config_instance = None


def create_service(config: FlextWebConfig | None = None) -> FlextWebService:
    """Create web service instance."""
    return FlextWebService(config or get_web_settings())


def create_app(config: FlextWebConfig | None = None) -> Flask:
    """Create Flask app instance."""
    service = create_service(config)
    return service.app


# =============================================================================
# EXCEPTIONS - Using flext-core patterns
# =============================================================================


class FlextWebError(FlextError):
    """Web error using flext-core."""


class FlextWebValidationError(FlextValidationError):
    """Web validation error using flext-core."""


# =============================================================================
# EXPORTS - Clean API
# =============================================================================


__all__ = [
    "FlextWebApp",
    "FlextWebAppHandler",
    "FlextWebAppStatus",
    "FlextWebConfig",
    "FlextWebError",
    "FlextWebService",
    "FlextWebValidationError",
    "__version__",
    "create_app",
    "create_service",
    "get_web_settings",
    "reset_web_settings",
]
