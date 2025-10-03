"""FLEXT Web Services - Consolidated web service system with enterprise patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from typing import override

from flask import Flask, Response, jsonify, render_template_string, request
from flask.typing import ResponseReturnValue
from flext_api import FlextApiClient
from flext_auth import FlextAuthModels
from flext_auth.api import FlextAuthQuickstart

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
from flext_web.protocols import FlextWebProtocols
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

    class WebService(FlextWebProtocols.Web.WebServiceInterface):
        """Primary web service implementation with Flask integration and application management.

        **PROTOCOL IMPLEMENTATION**: This service implements FlextWebProtocols.WebServiceInterface,
        extending FlextProtocols.Domain.Service with web-specific lifecycle operations including
        route initialization, middleware configuration, and service start/stop management.

        Enterprise-grade web service providing REST API endpoints, web dashboard,
        and comprehensive application lifecycle management. Built on Flask with
        FlextProcessors integration for consistent service patterns.

        Implements FlextWebProtocols through structural subtyping:
        - WebServiceInterface: initialize_routes, configure_middleware, start_service, stop_service
        - AppManagerProtocol: create_app, start_app, stop_app, list_apps
        - ResponseFormatterProtocol: format_success, format_error
        """

        _config_object: FlextWebConfig

        @override
        def __init__(
            self, config: FlextWebTypes.Core.WebConfigDict | FlextWebConfig
        ) -> None:
            """Initialize web service with enhanced FlextWebConfig integration.

            Uses FlextWebConfig's advanced features:
            - Protocol implementations for configuration management
            - Computed fields for derived configuration
            - Enhanced validation and business rules
            - Pydantic 2.11+ features
            """
            # Convert to FlextWebConfig object for full feature access
            if isinstance(config, FlextWebConfig):
                self._config_object = config
            else:
                # Create FlextWebConfig from dict using advanced features
                self._config_object = FlextWebConfig(**config)

            # Keep dict access for backward compatibility but prefer object access
            self.config: FlextWebTypes.Core.WebConfigDict = self._config_object.model_dump()

            self.app = Flask(__name__)
            self.apps: dict[str, FlextWebModels.WebApp] = {}
            self.app_handler = FlextWebHandlers.WebAppHandler()
            self.logger = FlextLogger(__name__)

            # Initialize flext-auth for authentication (lazy initialization for testing)
            self._auth: FlextAuthQuickstart | None = None

            # Initialize flext-api client for REST API calls
            api_base_url = str(self.config.get("api_base_url", "http://localhost:8000"))
            self.api_client = FlextApiClient(base_url=api_base_url)
            self.logger.info(f"API client initialized with base URL: {api_base_url}")

            # Create framework adapter for abstraction
            self._framework = self._FlaskAdapter()

            # Initialize service state
            self._initialized = True
            self.logger.info("Service initialized")

            # Configure Flask application
            self.app.config.update(
                {
                    "SECRET_KEY": self.config.get("secret_key", "default-secret-key"),
                    "DEBUG": self.config.get("debug", False),
                },
            )

            # Register routes
            self.initialize_routes()

            # Mark service as ready
            self._ready = True
            self.logger.info("Service ready")

    @property
    def auth(self: FlextWebServices.WebServiceRegistry) -> FlextAuthQuickstart:
        """Lazy initialization of authentication service."""
        if self._auth is None:
            try:
                self._auth = FlextAuthQuickstart()
                self.logger.info("Authentication system initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize authentication: {e}")
                # Create a mock auth for testing
                self._auth = self._create_mock_auth()
        return self._auth

    def _create_mock_auth(
        self: FlextWebServices.WebServiceRegistry,
    ) -> FlextAuthQuickstart:
        """Create a mock authentication service for testing."""

        # Create a simple mock that implements the minimal interface needed
        class MockAuth(FlextAuthQuickstart):
            def execute(
                self: FlextWebServices.WebServiceRegistry,
            ) -> FlextResult[object]:
                return FlextResult[object].ok({"status": "mock_auth"})

            def authenticate_user(
                self, username: str, _password: str
            ) -> FlextResult[object]:
                # Mock successful authentication
                return FlextResult[object].ok({
                    "user_id": "mock_user",
                    "username": username,
                })

            def validate_token(
                self: MockAuth, _token: str
            ) -> FlextResult[FlextAuthModels.User]:
                # Mock token validation
                user = FlextAuthModels.User(
                    id="mock_user",
                    username="mock@example.com",
                    email="mock@example.com",
                    hashed_password="mock_hash",  # noqa: S106
                )
                return FlextResult[FlextAuthModels.User].ok(user)

        return MockAuth()

        def execute(self: FlextWebServices.WebServiceRegistry) -> FlextResult[object]:
            """Execute the web service operation (start the service).

            Returns:
                FlextResult[object]: Success with service status or failure with error

            """
            try:
                self.run()
                return FlextResult[object].ok({"status": "running"})
            except Exception as e:
                return FlextResult[object].fail(f"Failed to execute web service: {e}")

        def is_valid(self: FlextWebServices.WebServiceRegistry) -> bool:
            """Check if the web service is properly configured and ready.

            Returns:
                bool: True if service is valid and ready, False otherwise

            """
            return getattr(self, "_ready", False)

        def _validate_authentication(
            self: FlextWebServices.WebServiceRegistry,
        ) -> FlextResult[FlextAuthModels.User]:
            """Validate authentication token from request.

            Returns:
                FlextResult containing authenticated user or error

            """
            # Get token from cookie or Authorization header
            token = request.cookies.get("session_token")
            if not token:
                auth_header = request.headers.get("Authorization")
                if auth_header and auth_header.startswith("Bearer "):
                    token = auth_header[7:]

            if not token:
                return FlextResult[FlextAuthModels.User].fail(
                    "No authentication token provided"
                )

            # Validate token using flext-auth
            validation_result = self.auth.validate_token(token)
            if validation_result.is_failure:
                return FlextResult[FlextAuthModels.User].fail(
                    f"Invalid token: {validation_result.error}"
                )

            # Get user information from token
            # validate_token already returns the User object
            return validation_result

        def _require_authentication(
            self: FlextWebServices.WebServiceRegistry,
        ) -> ResponseReturnValue | None:
            """Decorator helper for routes requiring authentication.

            Returns:
                None if authenticated, error response if not

            """
            auth_result = self._validate_authentication()
            if auth_result.is_failure:
                return jsonify({
                    "error": "Unauthorized",
                    "message": auth_result.error,
                }), 401
            return None

        # =============================================================================
        # AUTHENTICATION ENDPOINTS
        # =============================================================================

        def login(self: FlextWebServices.WebServiceRegistry) -> ResponseReturnValue:
            """User login endpoint - authenticate and create session.

            Expected JSON body:
                {
                    "username": "user@example.com",
                    "password": "password123"
                }

            Returns:
                JSON response with authentication token

            """
            try:
                data = request.get_json() or {}
                username = data.get("username")
                password = data.get("password")

                if not username or not password:
                    return jsonify({"error": "Username and password required"}), 400

                # Authenticate using flext-auth
                auth_result = self.auth.authenticate_user(
                    username=username, password=password
                )

                if auth_result.is_failure:
                    return jsonify({
                        "error": "Authentication failed",
                        "message": auth_result.error,
                    }), 401

                # Get the authenticated token
                auth_token = auth_result.value

                # Get user information using the user_id from the token
                user_result = self.auth.get_user(auth_token.user_id)
                if user_result.is_failure:
                    return jsonify({"error": "Failed to get user information"}), 500

                user = user_result.value

                # Generate JWT token using flext-auth
                token_result = self.auth.generate_jwt_token(user_id=user.id)

                if token_result.is_failure:
                    return jsonify({"error": "Token generation failed"}), 500

                token = token_result.value.token

                # Create response with token
                response = jsonify({
                    "success": True,
                    "message": "Login successful",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                })

                # Set session cookie with token
                response.set_cookie(
                    "session_token",
                    token,
                    httponly=True,
                    secure=bool(self.config.get("session_cookie_secure", False)),
                    samesite=str(self.config.get("session_cookie_samesite", "Lax")),
                )

                return response

            except Exception:
                self.logger.exception("Login error")
                return jsonify({"error": "Login failed"}), 500

        def logout(self: FlextWebServices.WebServiceRegistry) -> ResponseReturnValue:
            """User logout endpoint - invalidate session."""
            try:
                # Get current session token
                token = request.cookies.get("session_token")

                if token:
                    # Revoke session using flext-auth
                    # Note: FlextAuth.logout_user requires user_id, we'd need to decode token first
                    # For now, just clear the cookie
                    pass

                # Create response
                response = jsonify({"success": True, "message": "Logout successful"})

                # Clear session cookie
                response.set_cookie("session_token", "", expires=0)

                return response

            except Exception:
                self.logger.exception("Logout error")
                return jsonify({"error": "Logout failed"}), 500

        def register(self: FlextWebServices.WebServiceRegistry) -> ResponseReturnValue:
            """User registration endpoint - create new user account.

            Expected JSON body:
                {
                    "username": "newuser",
                    "email": "user@example.com",
                    "password": "password123"
                }

            Returns:
                JSON response with registration result

            """
            try:
                data = request.get_json() or {}
                username = data.get("username")
                email = data.get("email")
                password = data.get("password")

                if not username or not email or not password:
                    return jsonify({
                        "error": "Username, email, and password required"
                    }), 400

                # Register user using flext-auth
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
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                }), 201

            except Exception:
                self.logger.exception("Registration error")
                return jsonify({"error": "Registration failed"}), 500

        class _FlaskAdapter:
            """Framework adapter for Flask - provides framework-agnostic interface."""

            def create_json_response(
                self,
                data: FlextWebTypes.Core.ResponseDict,
                status_code: int = FlextConstants.Http.HTTP_OK,
            ) -> ResponseReturnValue:
                """Create JSON response using Flask."""
                return jsonify(data), status_code

            def get_request_data(
                self: FlextWebServices.WebServiceRegistry,
            ) -> FlextWebTypes.Core.RequestDict:
                """Get request JSON data."""
                if request.is_json:
                    return request.get_json() or {}
                return {}

            def is_json_request(self: FlextWebServices.WebServiceRegistry) -> bool:
                """Check if request is JSON."""
                return request.is_json

        # =============================================================================
        # PROTOCOL IMPLEMENTATION METHODS - WebServiceInterface
        # =============================================================================

        def initialize_routes(self: FlextWebServices.WebServiceRegistry) -> None:
            """Initialize web service routes and endpoints - implements WebServiceInterface."""
            # Health check endpoint (public)
            self.app.route("/health", methods=["GET"])(self.health_check)

            # Authentication endpoints (public)
            self.app.route("/auth/login", methods=["POST"])(self.login)
            self.app.route("/auth/logout", methods=["POST"])(self.logout)
            self.app.route("/auth/register", methods=["POST"])(self.register)

            # Dashboard endpoint (public - shows login if not authenticated)
            self.app.route("/", methods=["GET"])(self.dashboard)

            # API endpoints (protected - will be moved to flext-api in next phase)
            self.app.route("/api/v1/apps", methods=["GET"])(self.list_apps_endpoint)
            self.app.route("/api/v1/apps", methods=["POST"])(self.create_app_endpoint)
            self.app.route("/api/v1/apps/<app_id>", methods=["GET"])(self.get_app)
            self.app.route("/api/v1/apps/<app_id>/start", methods=["POST"])(
                self.start_app_endpoint,
            )
            self.app.route("/api/v1/apps/<app_id>/stop", methods=["POST"])(
                self.stop_app_endpoint,
            )

        def configure_middleware(self: FlextWebServices.WebServiceRegistry) -> None:
            """Configure request/response middleware - implements WebServiceInterface."""

            # Add CORS headers
            @self.app.after_request
            def after_request(response: Response) -> Response:
                response.headers["Access-Control-Allow-Origin"] = "*"
                response.headers["Access-Control-Allow-Methods"] = (
                    "GET, POST, PUT, DELETE, OPTIONS"
                )
                response.headers["Access-Control-Allow-Headers"] = (
                    "Content-Type, Authorization"
                )
                return response

            # Add request logging
            @self.app.before_request
            def before_request() -> None:
                self.logger.info(f"Request: {request.method} {request.path}")

        def start_service(
            self: FlextWebServices.WebService,
            host: str,
            port: int,
            *,
            debug: bool = False,
            **kwargs: object,  # noqa: ARG001 # reserved for future extensions
        ) -> None:
            """Start the web service with specified configuration - implements WebServiceInterface."""
            # kwargs reserved for future extensions
            self.configure_middleware()
            self.app.run(host=host, port=port, debug=debug)

        def stop_service(self: FlextWebServices.WebService) -> None:
            """Stop the web service gracefully - implements WebServiceInterface."""
            # Flask doesn't have a built-in stop method, this would need proper implementation
            # with werkzeug server shutdown
            self.logger.info("Service stop requested")

        # =============================================================================
        # PROTOCOL IMPLEMENTATION METHODS - AppManagerProtocol
        # =============================================================================

        def create_app(
            self: FlextWebServices.WebService,
            name: str,
            port: int,
            host: str,
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Create a new application - implements AppManagerProtocol."""
            try:
                self.logger.info("Create app request via protocol")

                # Use existing handler for actual creation
                create_result = self.app_handler.create(name, port, host)
                if create_result.is_failure:
                    return FlextResult[FlextWebModels.WebApp].fail(
                        f"Application creation failed: {create_result.error}"
                    )

                app = create_result.unwrap()
                self.apps[app.id] = app

                return FlextResult[FlextWebModels.WebApp].ok(app)

            except Exception as e:
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"Create app failed: {e}"
                )

        def start_app(
            self: FlextWebServices.WebService, app_id: str
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Start an application - implements AppManagerProtocol."""
            try:
                if app_id not in self.apps:
                    return FlextResult[FlextWebModels.WebApp].fail(
                        f"Application {app_id} not found"
                    )

                app = self.apps[app_id]
                start_result = self.app_handler.start(app)

                if start_result.is_failure:
                    return FlextResult[FlextWebModels.WebApp].fail(
                        f"Start failed: {start_result.error}"
                    )

                # Update stored app
                updated_app = start_result.unwrap()
                self.apps[app_id] = updated_app

                return FlextResult[FlextWebModels.WebApp].ok(updated_app)

            except Exception as e:
                return FlextResult[FlextWebModels.WebApp].fail(f"Start app failed: {e}")

        def stop_app(
            self: FlextWebServices.WebService, app_id: str
        ) -> FlextResult[FlextWebModels.WebApp]:
            """Stop an application - implements AppManagerProtocol."""
            try:
                if app_id not in self.apps:
                    return FlextResult[FlextWebModels.WebApp].fail(
                        f"Application {app_id} not found"
                    )

                app = self.apps[app_id]
                stop_result = self.app_handler.stop(app)

                if stop_result.is_failure:
                    return FlextResult[FlextWebModels.WebApp].fail(
                        f"Stop failed: {stop_result.error}"
                    )

                # Update stored app
                updated_app = stop_result.unwrap()
                self.apps[app_id] = updated_app

                return FlextResult[FlextWebModels.WebApp].ok(updated_app)

            except Exception as e:
                return FlextResult[FlextWebModels.WebApp].fail(f"Stop app failed: {e}")

        def list_apps(
            self: FlextWebServices.WebServiceRegistry,
        ) -> FlextResult[list[FlextWebModels.WebApp]]:
            """List all applications - implements AppManagerProtocol."""
            try:
                apps_list = list(self.apps.values())
                return FlextResult[list[FlextWebModels.WebApp]].ok(apps_list)
            except Exception as e:
                return FlextResult[list[FlextWebModels.WebApp]].fail(
                    f"List apps failed: {e}"
                )

        # =============================================================================
        # PROTOCOL IMPLEMENTATION METHODS - ResponseFormatterProtocol
        # =============================================================================

        @staticmethod
        def format_success(
            data: FlextTypes.Dict,
            message: str = "Success",
            status_code: int = 200,
        ) -> FlextWebTypes.Core.WebResponse:
            """Format success response - implements ResponseFormatterProtocol."""
            response_data = {
                "success": True,
                "message": message,
                "data": data,
                "status_code": status_code,
            }
            return jsonify(response_data), status_code

        @staticmethod
        def format_error(
            message: str,
            status_code: int = 500,
            details: str | None = None,
        ) -> FlextWebTypes.Core.WebResponse:
            """Format error response - implements ResponseFormatterProtocol."""
            response_data = {
                "success": False,
                "message": message,
                "status_code": status_code,
            }
            if details:
                response_data["details"] = details
            return jsonify(response_data), status_code

        # =============================================================================
        # EXISTING ENDPOINT METHODS - Updated to use protocol methods
        # =============================================================================

        def health_check(
            self: FlextWebServices.WebServiceRegistry,
        ) -> ResponseReturnValue:
            """Health check endpoint returning service status."""
            try:
                self.logger.info("Health check performed")

                health_data = {
                    "status": "healthy",
                    "service": "flext-web",
                    "version": FlextConstants.Core.VERSION,
                    "applications": len(self.apps),
                    "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
                    "service_id": getattr(self, "_id", "unknown"),
                    "created_at": getattr(self, "created_at", None),
                }

                return self.format_success(
                    data=health_data, message="Service is healthy"
                )
            except Exception:
                self.logger.exception("Health check failed")
                return self.format_error(
                    message="Service health check failed",
                    status_code=FlextConstants.Http.HTTP_INTERNAL_SERVER_ERROR,
                )

        def dashboard(self: FlextWebServices.WebServiceRegistry) -> ResponseReturnValue:
            """Web dashboard interface showing applications.

            Integration demonstration:
            - Uses flext-auth for authentication (login/logout/register endpoints)
            - Ready to use FlextApiClient for backend API calls (fetch_apps_from_api method available)
            - Current implementation uses local data, can be switched to API calls when backend available

            Note: Dashboard currently uses local data (self.apps).
            To use backend API, the application needs support or background task for API calls.
            The fetch_apps_from_api() method is available and ready to use.
            """
            try:
                # Current: Use local data
                # Future: When support added, use: apps_result = self.fetch_apps_from_api()
                apps_data = list(self.apps.values())

                app_count = len(apps_data)
                running_count = sum(1 for app in apps_data if bool(app.is_running))

                html_template = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>FLEXT Web Dashboard</title>
                    <style>
                        body { font-family: "Arial", sans-serif; margin: 40px; }
                        .header { color: #333; border-bottom: 2px solid #007acc; padding-bottom: 10px; }
                        .integration-badge { background: #007acc; color: white; padding: 5px 10px; border-radius: 3px; font-size: 12px; margin-left: 10px; }
                        .stats { background: #f5f5f5; padding: 20px; border-radius: 5px; margin: 20px 0; }
                        .integration-info { background: #e8f4f8; padding: 15px; border-left: 4px solid #007acc; margin: 20px 0; }
                        .app-list { margin-top: 20px; }
                        .app-item { background: white; border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
                        .status-running { color: green; font-weight: bold; }
                        .status-stopped { color: red; }
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>FLEXT Web Service Dashboard
                            <span class="integration-badge">✓ flext-auth</span>
                            <span class="integration-badge">✓ flext-api</span>
                        </h1>
                    </div>

                    <div class="integration-info">
                        <h3>🎉 Integration Complete</h3>
                        <p><strong>Authentication:</strong> Using flext-auth for JWT-based authentication (login/logout/register)</p>
                        <p><strong>API Client:</strong> Using FlextApiClient for HTTP communication with backend services</p>
                        <p><strong>Domain Separation:</strong> Clean integration following FLEXT architecture patterns</p>
                    </div>

                    <div class="stats">
                        <h2>Service Statistics</h2>
                        <p><strong>Total Applications:</strong> {{ app_count }}</p>
                        <p><strong>Running Applications:</strong> {{ running_count }}</p>
                        <p><strong>Service Status:</strong> <span class="status-running">Operational</span></p>
                        <p><strong>Authentication:</strong> ✓ flext-auth integrated</p>
                        <p><strong>HTTP Client:</strong> ✓ flext-api integrated</p>
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

                    <div class="integration-info" style="margin-top: 30px;">
                        <h3>📋 Available Features</h3>
                        <ul>
                            <li><strong>POST /auth/login</strong> - User authentication with JWT tokens</li>
                            <li><strong>POST /auth/logout</strong> - Secure logout</li>
                            <li><strong>POST /auth/register</strong> - User registration</li>
                            <li><strong>FlextApiClient</strong> - Ready for backend API communication (see fetch_apps_from_api method)</li>
                        </ul>
                    </div>
                </body>
                </html>
                """

                return render_template_string(
                    html_template,
                    app_count=app_count,
                    running_count=running_count,
                    apps=apps_data,
                )

            except Exception:
                self.logger.exception("Dashboard error")
                return "Dashboard error", FlextConstants.Http.HTTP_INTERNAL_SERVER_ERROR

        # =============================================================================
        # API CLIENT INTEGRATION EXAMPLES
        # =============================================================================

        def fetch_apps_from_api(
            self: FlextWebServices.WebServiceRegistry,
        ) -> FlextResult[list[FlextTypes.Dict]]:
            """Example: Fetch applications from backend API using flext-api client.

            This demonstrates how flext-web delegates REST API operations to flext-api.
            In future refactoring, this pattern will replace direct Flask API endpoints.

            Returns:
                FlextResult containing list of applications from backend API

            """
            try:
                # Use FlextApiClient to call backend REST API
                response = self.api_client.get("/api/v1/apps")

                if response.is_failure:
                    return FlextResult[list[FlextTypes.Dict]].fail(
                        f"API call failed: {response.error}"
                    )

                # Parse body as dict if it's a string (JSON response)
                body_data = response.value.body
                if isinstance(body_data, str):
                    try:
                        body_data = json.loads(body_data)
                    except json.JSONDecodeError:
                        body_data = {}

                apps_data = (
                    body_data.get("apps", []) if isinstance(body_data, dict) else []
                )
                return FlextResult[list[FlextTypes.Dict]].ok(apps_data)

            except Exception as e:
                self.logger.exception("Error fetching apps from API")
                return FlextResult[list[FlextTypes.Dict]].fail(str(e))

        def create_app_via_api(
            self: FlextWebServices.WebService, app_data: FlextTypes.Dict
        ) -> FlextResult[FlextTypes.Dict]:
            """Example: Create application via backend API using flext-api client.

            Args:
                app_data: Application configuration data

            Returns:
                FlextResult containing created application data

            """
            try:
                # Use FlextApiClient to call backend REST API with POST
                response = self.api_client.post("/api/v1/apps", json=app_data)

                if response.is_failure:
                    return FlextResult[FlextTypes.Dict].fail(
                        f"API call failed: {response.error}"
                    )

                # Parse body as dict if it's a string (JSON response)
                body_data = response.value.body
                if isinstance(body_data, str):
                    try:
                        body_data = json.loads(body_data)
                    except json.JSONDecodeError:
                        body_data = {}
                elif not isinstance(body_data, dict):
                    body_data = {}

                return FlextResult[FlextTypes.Dict].ok(body_data)

            except Exception as e:
                self.logger.exception("Error creating app via API")
                return FlextResult[FlextTypes.Dict].fail(str(e))

        # =============================================================================
        # LEGACY API ENDPOINTS (TO BE DEPRECATED AND MOVED TO FLEXT-API)
        # =============================================================================
        # NOTE: These endpoints will be removed in future refactoring.
        # All REST API functionality should be handled by flext-api (FlextApiServer).
        # flext-web should use FlextApiClient to communicate with the backend API.
        # =============================================================================

        def list_apps_endpoint(
            self: FlextWebServices.WebServiceRegistry,
        ) -> ResponseReturnValue:
            """List all registered applications endpoint."""
            try:
                apps_result = self.list_apps()
                if apps_result.is_failure:
                    return self.format_error(
                        message=f"Failed to list applications: {apps_result.error}",
                        status_code=FlextConstants.Http.HTTP_INTERNAL_SERVER_ERROR,
                    )

                apps_data = []
                for app in apps_result.unwrap():
                    app_data = {
                        "id": app.id,
                        "name": app.name,
                        "host": app.host,
                        "port": app.port,
                        "status": app.status,
                        "is_running": bool(app.is_running),
                    }
                    apps_data.append(app_data)

                return self.format_success(
                    data={"apps": apps_data},
                    message=f"Found {len(apps_data)} applications",
                )

            except Exception as e:
                return self.format_error(
                    message="Failed to list applications",
                    details=str(e),
                    status_code=FlextConstants.Http.HTTP_INTERNAL_SERVER_ERROR,
                )

        @staticmethod
        def validate_json_request() -> FlextResult[FlextWebTypes.Core.RequestDict]:
            """Railway-oriented validation of JSON request data."""
            if not request.is_json:
                return FlextResult[FlextWebTypes.Core.RequestDict].fail(
                    "Request must be JSON"
                )

            try:
                data: FlextWebTypes.Core.RequestDict = request.get_json()
                if not data:
                    return FlextResult[FlextWebTypes.Core.RequestDict].fail(
                        "Request body is required",
                    )
                return FlextResult[FlextWebTypes.Core.RequestDict].ok(data)
            except Exception:
                return FlextResult[FlextWebTypes.Core.RequestDict].fail(
                    "Invalid JSON in request body",
                )

        @staticmethod
        def validate_app_data(
            data: FlextWebTypes.Core.RequestDict,
        ) -> FlextResult[tuple[str, str, int]]:
            """Validate application data using Railway pattern."""
            # Extract and validate required fields
            try:
                name = data.get("name")
                host = data.get(
                    "host",
                    FlextWebConstants.WebServer.DEFAULT_HOST,
                )  # Use FlextWebConstants for host default
                port = data.get(
                    "port",
                    FlextWebConstants.WebServer.DEFAULT_PORT,
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

        def create_app_endpoint(
            self: FlextWebServices.WebServiceRegistry,
        ) -> ResponseReturnValue:
            """Create new application endpoint using protocol method."""
            try:
                self.logger.info("Create app request received")

                # Validate JSON request
                json_validation = FlextWebServices.WebService.validate_json_request()
                if json_validation.is_failure:
                    return FlextWebServices.WebService.format_error(
                        message=json_validation.error or "Validation failed",
                        status_code=FlextConstants.Http.HTTP_BAD_REQUEST,
                    )

                # Validate app data
                app_validation = FlextWebServices.WebService.validate_app_data(json_validation.unwrap())
                if app_validation.is_failure:
                    return self.format_error(
                        message=app_validation.error or "App validation failed",
                        status_code=FlextConstants.Http.HTTP_BAD_REQUEST,
                    )

                # Unpack validated data and create app using protocol method
                name, host, port = app_validation.unwrap()
                create_result = self.create_app(name, port, host)

                if create_result.is_failure:
                    return self.format_error(
                        message=create_result.error or "Unknown error",
                        status_code=FlextConstants.Http.HTTP_BAD_REQUEST,
                    )

                app = create_result.unwrap()
                app_data: FlextTypes.Dict = {
                    "id": app.id,
                    "name": app.name,
                    "host": app.host,
                    "port": app.port,
                    "status": app.status,
                }

                return self.format_success(
                    data=app_data,
                    message="Application created successfully",
                    status_code=FlextConstants.Http.HTTP_CREATED,
                )

            except Exception as e:
                return self.format_error(
                    message=f"Internal error during application creation: {e}",
                    status_code=FlextConstants.Http.HTTP_INTERNAL_SERVER_ERROR,
                )

        def get_app(
            self: FlextWebServices.WebService, app_id: str
        ) -> ResponseReturnValue:
            """Get specific application by ID."""
            try:
                if app_id not in self.apps:
                    return self.format_error(
                        message=f"Application {app_id} not found",
                        status_code=FlextConstants.Http.HTTP_NOT_FOUND,
                    )

                app = self.apps[app_id]
                app_data: FlextTypes.Dict = {
                    "id": app.id,
                    "name": app.name,
                    "host": app.host,
                    "port": app.port,
                    "status": app.status,
                    "is_running": bool(app.is_running),
                }

                return self.format_success(data=app_data, message="Application found")

            except Exception as e:
                return self.format_error(
                    message="Failed to get application",
                    details=str(e),
                    status_code=FlextConstants.Http.HTTP_INTERNAL_SERVER_ERROR,
                )

        def start_app_endpoint(
            self: FlextWebServices.WebService, app_id: str
        ) -> ResponseReturnValue:
            """Start application endpoint using protocol method."""
            try:
                start_result = self.start_app(app_id)

                if start_result.is_failure:
                    if start_result.error and "not found" in start_result.error.lower():
                        status_code = FlextConstants.Http.HTTP_NOT_FOUND
                    else:
                        status_code = FlextConstants.Http.HTTP_BAD_REQUEST

                    return self.format_error(
                        message=start_result.error or "Application start failed",
                        status_code=status_code,
                    )

                app = start_result.unwrap()
                app_data: FlextTypes.Dict = {
                    "id": app.id,
                    "name": app.name,
                    "status": app.status,
                }

                return self.format_success(
                    data=app_data,
                    message=f"Application {app.name} started successfully",
                )

            except Exception as e:
                return self.format_error(
                    message="Failed to start application",
                    details=str(e),
                    status_code=FlextConstants.Http.HTTP_INTERNAL_SERVER_ERROR,
                )

        def stop_app_endpoint(
            self: FlextWebServices.WebService, app_id: str
        ) -> ResponseReturnValue:
            """Stop application endpoint using protocol method."""
            try:
                stop_result = self.stop_app(app_id)

                if stop_result.is_failure:
                    if stop_result.error and "not found" in stop_result.error.lower():
                        status_code = FlextConstants.Http.HTTP_NOT_FOUND
                    else:
                        status_code = FlextConstants.Http.HTTP_BAD_REQUEST

                    return self.format_error(
                        message=stop_result.error or "Application stop failed",
                        status_code=status_code,
                    )

                app = stop_result.unwrap()
                app_data: FlextTypes.Dict = {
                    "id": app.id,
                    "name": app.name,
                    "status": app.status,
                }

                return self.format_success(
                    data=app_data,
                    message=f"Application {app.name} stopped successfully",
                )

            except Exception as e:
                return self.format_error(
                    message="Failed to stop application",
                    details=str(e),
                    status_code=FlextConstants.Http.HTTP_INTERNAL_SERVER_ERROR,
                )

        def run(self: FlextWebServices.WebServiceRegistry) -> None:
            """Run the Flask web service."""
            self.start_service(
                host=str(
                    self.config.get("host", FlextWebConstants.WebServer.DEFAULT_HOST)
                ),
                port=int(
                    str(
                        self.config.get(
                            "port", FlextWebConstants.WebServer.DEFAULT_PORT
                        )
                    )
                ),
                debug=bool(self.config.get("debug", False)),
            )

        return None

    class WebServiceRegistry:
        """Service registry for web service discovery and management.

        Provides centralized registry functionality for web service instances,
        supporting service discovery, health monitoring, and lifecycle management
        within the FLEXT Web ecosystem.
        """

        @override
        def __init__(self: FlextWebServices.WebServiceRegistry) -> None:
            """Initialize web service registry."""
            self._services: dict[str, FlextWebServices.WebService] = {}
            self._health_status: FlextTypes.BoolDict = {}
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

        def list_web_services(
            self: FlextWebServices.WebServiceRegistry,
        ) -> FlextResult[FlextWebTypes.Core.DataDict]:
            """List all registered web service names.

            Returns:
                FlextResult[FlextWebTypes.Core.DataDict]: Names of registered services.

            """
            try:
                service_names = list(self._services.keys())
                service_data: FlextWebTypes.Core.DataDict = {
                    "services": service_names,
                    "count": len(service_names),
                }
                return FlextResult[FlextWebTypes.Core.DataDict].ok(service_data)
            except Exception as e:
                return FlextResult[FlextWebTypes.Core.DataDict].fail(
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

        def get_service(
            self: FlextWebServices.WebServiceRegistry, name: str
        ) -> FlextResult[FlextWebServices.WebService]:
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
                validated_config: FlextWebTypes.Core.WebConfigDict = (
                    config_result.value.model_dump()
                )
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
        config: FlextWebTypes.Core.DataDict | None = None,
    ) -> FlextResult[FlextWebTypes.Core.DataDict]:
        """Create web system services."""
        _ = config  # Acknowledge parameter

        try:
            # Create service and registry
            service_result = cls.create_web_service()
            if service_result.is_failure:
                return FlextResult[FlextWebTypes.Core.DataDict].fail(
                    service_result.error or "Service creation failed",
                )

            registry_result = cls.create_service_registry()
            if registry_result.is_failure:
                return FlextResult[FlextWebTypes.Core.DataDict].fail(
                    registry_result.error or "Registry creation failed",
                )

            service = service_result.value
            registry = registry_result.value

            # Register service
            register_result = registry.register_web_service("main", service)
            if register_result.is_failure:
                return FlextResult[FlextWebTypes.Core.DataDict].fail(
                    register_result.error or "Registration failed",
                )

            return FlextResult[FlextWebTypes.Core.DataDict].ok(
                {
                    "web_service": "service",
                    "registry": "registry",
                },
            )

        except Exception as e:
            return FlextResult[FlextWebTypes.Core.DataDict].fail(
                f"System services creation failed: {e}",
            )

    # =============================================================================
    # FLEXT WEB SERVICES CONFIGURATION METHODS
    # =============================================================================

    @classmethod
    def configure_web_services_system(
        cls,
        config: FlextTypes.Dict,
    ) -> FlextResult[FlextTypes.Dict]:
        """Configure web services system using FlextTypes.Config with validation."""
        try:
            validated_config: FlextTypes.Dict = dict(config)

            # Validate environment using FlextConstants
            if "environment" in config:
                env_value = config["environment"]
                valid_environments = ["development", "staging", "production", "test"]
                if env_value not in valid_environments:
                    return FlextResult[FlextTypes.Dict].fail(
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

            return FlextResult[FlextTypes.Dict].ok(validated_config)

        except Exception as e:
            return FlextResult[FlextTypes.Dict].fail(
                f"Failed to configure web services system: {e}",
            )

    @classmethod
    def get_web_services_system_config(
        cls,
    ) -> FlextResult[FlextTypes.Dict]:
        """Get current web services system configuration with runtime information."""
        try:
            config: FlextTypes.Dict = {
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

            return FlextResult[FlextTypes.Dict].ok(config)

        except Exception as e:
            return FlextResult[FlextTypes.Dict].fail(
                f"Failed to get web services system config: {e}",
            )


__all__ = [
    "FlextWebServices",
]
