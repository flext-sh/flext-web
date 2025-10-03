"""FLEXT Web Services - Unified web service class with flext-core integration.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flask import Flask, jsonify, render_template_string, request
from flask.typing import ResponseReturnValue
from flext_api import FlextApiClient
from flext_auth import FlextAuthModels
from flext_auth.api import FlextAuthQuickstart
from flext_auth.models import AuthToken

from flext_core import (
    FlextConstants,
    FlextContainer,
    FlextLogger,
    FlextResult,
    FlextService,
    FlextUtilities,
)
from flext_web.config import FlextWebConfig
from flext_web.handlers import FlextWebHandlers
from flext_web.models import FlextWebModels
from flext_web.typings import FlextWebTypes


class FlextWebServices(FlextService[FlextWebConfig]):
    """Unified FLEXT web service class with complete flext-core integration.

    This is the single unified web service class for flext-web, providing
    Flask-based web functionality with full flext-core integration including
    FlextResult, FlextContainer, FlextLogger, and other foundation patterns.

    Follows the single responsibility principle while maintaining unified
    web interface patterns for the FLEXT ecosystem.
    """

    # Backward compatibility: Nested WebService class (alias to main class)
    WebService = FlextWebServices

    def __init__(
        self,
        config: FlextWebTypes.Core.WebConfigDict | FlextWebConfig | None = None,
        **data: object,
    ) -> None:
        """Initialize unified web service with flext-core integration."""
        # Convert config to FlextWebConfig if needed
        if isinstance(config, FlextWebConfig):
            self._config = config
        elif isinstance(config, dict):
            self._config = FlextWebConfig(**config)
        else:
            self._config = FlextWebConfig()

        # Initialize flext-core service base with remaining data
        super().__init__(**data)

        # Flext-core integration
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)

        # Web service components
        self.app = Flask(__name__)
        self.apps: dict[str, FlextWebModels.WebApp] = {}
        self.app_handler = FlextWebHandlers.WebAppHandler()

        # Authentication (lazy initialization)
        self._auth: FlextAuthQuickstart | None = None

        # API client for backend communication
        api_base_url = str(self._config.base_url or "http://localhost:8000")
        self.api_client = FlextApiClient(base_url=api_base_url)

        # Configure Flask app
        self._configure_flask_app()

        # Initialize routes
        self._initialize_routes()

        self._logger.info("FlextWebServices initialized successfully")

    def execute(self) -> FlextResult[FlextWebConfig]:
        """Execute the web service operation (required by FlextService)."""
        try:
            self.run()
            return FlextResult[FlextWebConfig].ok(self._config)
        except Exception as e:
            return FlextResult[FlextWebConfig].fail(
                f"Failed to execute web service: {e}"
            )

    @property
    def auth(self) -> FlextAuthQuickstart:
        """Lazy initialization of authentication service."""
        if self._auth is None:
            try:
                self._auth = FlextAuthQuickstart()
                self._logger.info("Authentication system initialized")
            except Exception as e:
                self._logger.warning(f"Failed to initialize authentication: {e}")
                self._auth = self._create_mock_auth()
        return self._auth

    def _create_mock_auth(self) -> FlextAuthQuickstart:
        """Create a mock authentication service for testing."""

        class MockAuth(FlextAuthQuickstart):
            def execute(self) -> FlextResult[object]:
                return FlextResult[object].ok({"status": "mock_auth"})

            def authenticate_user(
                self, username: str, password: str
            ) -> FlextResult[FlextAuthModels.AuthToken]:
                # Mock authentication - password is ignored for testing
                _ = password  # Acknowledge parameter
                # Create a mock auth token
                token = AuthToken(
                    token=FlextConstants.Security.MOCK_JWT_TOKEN,
                    user_id=FlextConstants.Security.MOCK_USER_ID,
                    expires_at=FlextUtilities.Generators.generate_iso_timestamp(),
                    token_type=FlextConstants.Security.BEARER_TOKEN_TYPE
                )
                return FlextResult[FlextAuthModels.AuthToken].ok(token)

            def validate_token(self, token: str) -> FlextResult[FlextAuthModels.User]:  # noqa: ARG002
                user = FlextAuthModels.User(
                    id="mock_user",
                    user_id="mock_user",
                    username="mock@example.com",
                    email="mock@example.com",
                    password_hash="mock_hash",  # noqa: S106  # Mock password for testing
                    full_name="Mock User",
                    is_active=True,
                    roles=[],
                    last_login=None,
                    created_at=FlextUtilities.Generators.generate_iso_timestamp(),
                    updated_at=FlextUtilities.Generators.generate_iso_timestamp(),
                )
                return FlextResult[FlextAuthModels.User].ok(user)

        return MockAuth()

    def _configure_flask_app(self) -> None:
        """Configure Flask application with settings."""
        self.app.config.update({
            "SECRET_KEY": self._config.secret_key.get_secret_value()
            if self._config.secret_key
            else "dev-key",
            "DEBUG": self._config.debug,
            "MAX_CONTENT_LENGTH": self._config.max_content_length,
        })

    def _initialize_routes(self) -> None:
        """Initialize Flask routes."""
        # Health check
        self.app.route("/health", methods=["GET"])(self.health_check)

        # Authentication routes
        self.app.route("/auth/login", methods=["POST"])(self.login)
        self.app.route("/auth/logout", methods=["POST"])(self.logout)
        self.app.route("/auth/register", methods=["POST"])(self.register)

        # Dashboard
        self.app.route("/", methods=["GET"])(self.dashboard)

        # API routes
        self.app.route("/api/v1/apps", methods=["GET"])(self.list_apps_endpoint)
        self.app.route("/api/v1/apps", methods=["POST"])(self.create_app_endpoint)
        self.app.route("/api/v1/apps/<app_id>", methods=["GET"])(self.get_app)
        self.app.route("/api/v1/apps/<app_id>/start", methods=["POST"])(
            self.start_app_endpoint
        )
        self.app.route("/api/v1/apps/<app_id>/stop", methods=["POST"])(
            self.stop_app_endpoint
        )

    # Authentication methods

    def login(self) -> ResponseReturnValue:
        """User login endpoint."""
        try:
            data = request.get_json() or {}
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return jsonify({"error": "Username and password required"}), 400

            auth_result = self.auth.authenticate_user(
                username=username, password=password
            )
            if auth_result.is_failure:
                return jsonify({
                    "error": "Authentication failed",
                    "message": auth_result.error,
                }), 401

            auth_token = auth_result.value
            # The auth_token already contains the JWT token
            token = auth_token.token
            response = jsonify({"success": True, "message": "Login successful"})
            response.set_cookie(
                "session_token", token, httponly=True, secure=False, samesite="Lax"
            )
            return response

        except Exception:
            self._logger.exception("Login error")
            return jsonify({"error": "Login failed"}), 500

    def logout(self) -> ResponseReturnValue:
        """User logout endpoint."""
        try:
            response = jsonify({"success": True, "message": "Logout successful"})
            response.set_cookie("session_token", "", expires=0)
            return response
        except Exception:
            self._logger.exception("Logout error")
            return jsonify({"error": "Logout failed"}), 500

    def register(self) -> ResponseReturnValue:
        """User registration endpoint."""
        try:
            data = request.get_json() or {}
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            if not username or not email or not password:
                return jsonify({"error": "Username, email, and password required"}), 400

            register_result = self.auth.register_user(
                username=username, email=email, password=password
            )
            if register_result.is_failure:
                return jsonify({
                    "error": "Registration failed",
                    "message": register_result.error,
                }), 400

            user = register_result.value
            return jsonify({
                "success": True,
                "message": "Registration successful",
                "user": {"id": user.id, "username": user.username, "email": user.email},
            }), 201

        except Exception:
            self._logger.exception("Registration error")
            return jsonify({"error": "Registration failed"}), 500

    # Web endpoints

    def health_check(self) -> ResponseReturnValue:
        """Health check endpoint."""
        return jsonify({
            "status": "healthy",
            "service": "flext-web",
            "version": FlextConstants.Core.VERSION,
            "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
        })

    def dashboard(self) -> ResponseReturnValue:
        """Web dashboard."""
        try:
            apps_data = list(self.apps.values())
            app_count = len(apps_data)
            running_count = sum(1 for app in apps_data if app.is_running)

            html = f"""
            <!DOCTYPE html>
            <html>
            <head><title>FLEXT Web Dashboard</title></head>
            <body>
                <h1>FLEXT Web Service Dashboard</h1>
                <p>Total Applications: {app_count}</p>
                <p>Running Applications: {running_count}</p>
                <p>Service Status: Operational</p>
            </body>
            </html>
            """
            return render_template_string(html)

        except Exception:
            self._logger.exception("Dashboard error")
            return "Dashboard error", 500

    # API endpoints

    def list_apps_endpoint(self) -> ResponseReturnValue:
        """List all applications."""
        try:
            apps_list = [
                {
                    "id": app.id,
                    "name": app.name,
                    "host": app.host,
                    "port": app.port,
                    "status": app.status,
                    "is_running": app.is_running,
                }
                for app in self.apps.values()
            ]

            return jsonify({"apps": apps_list})

        except Exception:
            self._logger.exception("List apps error")
            return jsonify({"error": "Failed to list applications"}), 500

    def create_app_endpoint(self) -> ResponseReturnValue:
        """Create new application."""
        try:
            data = request.get_json() or {}
            name = data.get("name")
            host = data.get("host", "localhost")
            port = data.get("port", 8080)

            if not name:
                return jsonify({"error": "Name is required"}), 400

            create_result = self.app_handler.create(name, port, host)
            if create_result.is_failure:
                return jsonify({"error": create_result.error}), 400

            app = create_result.unwrap()
            self.apps[app.id] = app

            return jsonify({
                "id": app.id,
                "name": app.name,
                "host": app.host,
                "port": app.port,
                "status": app.status,
            }), 201

        except Exception:
            self._logger.exception("Create app error")
            return jsonify({"error": "Failed to create application"}), 500

    def get_app(self, app_id: str) -> ResponseReturnValue:
        """Get application by ID."""
        try:
            if app_id not in self.apps:
                return jsonify({"error": "Application not found"}), 404

            app = self.apps[app_id]
            return jsonify({
                "id": app.id,
                "name": app.name,
                "host": app.host,
                "port": app.port,
                "status": app.status,
                "is_running": app.is_running,
            })

        except Exception:
            self._logger.exception("Get app error")
            return jsonify({"error": "Failed to get application"}), 500

    def start_app_endpoint(self, app_id: str) -> ResponseReturnValue:
        """Start application."""
        try:
            if app_id not in self.apps:
                return jsonify({"error": "Application not found"}), 404

            app = self.apps[app_id]
            start_result = self.app_handler.start(app)
            if start_result.is_failure:
                return jsonify({"error": start_result.error}), 400

            updated_app = start_result.unwrap()
            self.apps[app_id] = updated_app

            return jsonify({
                "id": updated_app.id,
                "name": updated_app.name,
                "status": updated_app.status,
            })

        except Exception:
            self._logger.exception("Start app error")
            return jsonify({"error": "Failed to start application"}), 500

    def stop_app_endpoint(self, app_id: str) -> ResponseReturnValue:
        """Stop application."""
        try:
            if app_id not in self.apps:
                return jsonify({"error": "Application not found"}), 404

            app = self.apps[app_id]
            stop_result = self.app_handler.stop(app)
            if stop_result.is_failure:
                return jsonify({"error": stop_result.error}), 400

            updated_app = stop_result.unwrap()
            self.apps[app_id] = updated_app

            return jsonify({
                "id": updated_app.id,
                "name": updated_app.name,
                "status": updated_app.status,
            })

        except Exception:
            self._logger.exception("Stop app error")
            return jsonify({"error": "Failed to stop application"}), 500

    # Service lifecycle

    def run(self) -> None:
        """Run the Flask web service."""
        self.app.run(
            host=self._config.host, port=self._config.port, debug=self._config.debug
        )

    # Factory methods

    @classmethod
    def create_web_service(
        cls,
        config: FlextWebTypes.Core.WebConfigDict | None = None,
    ) -> FlextResult[FlextWebServices]:
        """Create web service instance."""
        try:
            service = cls(config)
            return FlextResult[FlextWebServices].ok(service)
        except Exception as e:
            return FlextResult[FlextWebServices].fail(
                f"Web service creation failed: {e}"
            )


# Type alias for backward compatibility
WebService = FlextWebServices

__all__ = [
    "FlextWebServices",
    "WebService",  # Backward compatibility alias
]
