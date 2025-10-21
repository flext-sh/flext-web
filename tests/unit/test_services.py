"""Unit tests for flext_web.services module.

Tests the web services functionality following flext standards.
"""

from flext_web.config import FlextWebConfig
from flext_web.services import FlextWebServices


class TestFlextWebService:
    """Test suite for FlextWebServices class."""

    def test_initialization_without_config(self) -> None:
        """Test FlextWebServices initialization without config."""
        service = FlextWebServices()
        assert service is not None
        assert hasattr(service, "_container")
        assert hasattr(service, "_logger")
        assert hasattr(service, "_config")
        assert service._config is None

    def test_initialization_with_config(self) -> None:
        """Test FlextWebServices initialization with config."""
        config = FlextWebConfig(host="localhost", port=8080)
        service = FlextWebServices(config=config)
        assert service is not None
        assert service._config == config

    def test_initialize_routes(self) -> None:
        """Test routes initialization."""
        service = FlextWebServices()
        service.initialize_routes()
        assert service._routes_initialized is True

    def test_configure_middleware(self) -> None:
        """Test middleware configuration."""
        service = FlextWebServices()
        service.configure_middleware()
        assert service._middleware_configured is True

    def test_start_service(self) -> None:
        """Test service start."""
        service = FlextWebServices()
        service.start_service("localhost", 8080, _debug=True)
        assert service._service_running is True

    def test_stop_service(self) -> None:
        """Test service stop."""
        service = FlextWebServices()
        service._service_running = True
        service.stop_service()
        assert service._service_running is False

    def test_auth_property_lazy_initialization(self) -> None:
        """Test auth service access."""
        service = FlextWebServices()
        # Service has auth operations available through authenticate method
        assert hasattr(service, "authenticate")

    def test_authenticate_success(self) -> None:
        """Test successful authenticate."""
        service = FlextWebServices()
        # First register a user
        register_result = service.register({
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        })
        assert register_result.is_success

        # Then authenticate
        authenticate_result = service.authenticate({
            "username": "testuser",
            "password": "password123",
        })
        assert authenticate_result.is_success
        authenticate_data = authenticate_result.unwrap()
        assert "authenticated" in authenticate_data
        assert authenticate_data["authenticated"] is True

    def test_authenticate_invalid_credentials(self) -> None:
        """Test authenticate with invalid credentials."""
        service = FlextWebServices()
        authenticate_result = service.authenticate({
            "username": "nonexistent",
            "password": "wrongpassword",
        })
        assert authenticate_result.is_failure
        assert authenticate_result.error is not None
        assert "Authentication failed" in authenticate_result.error

    def test_authenticate_invalid_input(self) -> None:
        """Test authentication with invalid input types."""
        service = FlextWebServices()
        auth_result = service.authenticate({
            "username": 123,  # Invalid type
            "password": "password",
        })
        assert auth_result.is_failure
        assert auth_result.error is not None
        assert "Invalid credentials format" in auth_result.error

    def test_logout(self) -> None:
        """Test logout functionality."""
        service = FlextWebServices()
        logout_result = service.logout()
        assert logout_result.is_success
        logout_data = logout_result.unwrap()
        assert logout_data["success"] is True

    def test_register_success(self) -> None:
        """Test successful user registration."""
        service = FlextWebServices()
        register_result = service.register_user({
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
        })
        assert register_result.is_success
        user_data = register_result.unwrap()
        assert user_data["id"] is not None
        assert user_data["username"] == "newuser"

    def test_register_duplicate_user(self) -> None:
        """Test registration with duplicate username."""
        service = FlextWebServices()
        # Register first user
        first_result = service.register_user({
            "username": "duplicate",
            "email": "user1@example.com",
            "password": "password123",
        })
        assert first_result.is_success

        # Try to register with same username (service allows it without duplicate checking)
        register_result = service.register_user({
            "username": "duplicate",
            "email": "user2@example.com",
            "password": "password456",
        })
        assert register_result.is_success

    def test_register_invalid_input(self) -> None:
        """Test registration with invalid input types."""
        service = FlextWebServices()
        register_result = service.register_user({
            "username": 123,  # Invalid type
            "email": "test@example.com",
            "password": "password",
        })
        assert register_result.is_failure
        assert register_result.error is not None
        assert "Invalid user data format" in register_result.error

    def test_health_check(self) -> None:
        """Test health check functionality."""
        service = FlextWebServices()
        health_result = service.health_check()
        assert health_result.is_success
        health_data = health_result.unwrap()
        assert health_data["status"] == "healthy"
        assert health_data["service"] == "flext-web"

    def test_dashboard(self) -> None:
        """Test dashboard functionality."""
        service = FlextWebServices()
        dashboard_result = service.dashboard()
        assert dashboard_result.is_success
        dashboard_data = dashboard_result.unwrap()
        assert "total_applications" in dashboard_data
        assert "running_applications" in dashboard_data
        assert "service_status" in dashboard_data

    def test_list_apps(self) -> None:
        """Test list apps functionality."""
        service = FlextWebServices()
        list_result = service.list_apps()
        assert list_result.is_success
        apps_data = list_result.unwrap()
        assert "apps" in apps_data
        assert isinstance(apps_data["apps"], list)

    def test_create_app_success(self) -> None:
        """Test successful app creation."""
        service = FlextWebServices()
        create_result = service.create_app({
            "name": "test-app",
            "host": "localhost",
            "port": 8080,
        })
        assert create_result.is_success
        app_data = create_result.unwrap()
        assert app_data["name"] == "test-app"
        assert app_data["host"] == "localhost"
        assert app_data["port"] == 8080

    def test_create_app_invalid_input(self) -> None:
        """Test app creation with invalid input."""
        service = FlextWebServices()
        create_result = service.create_app({
            "name": 123,  # Invalid type
            "host": "localhost",
            "port": 8080,
        })
        assert create_result.is_failure
        assert (
            create_result.error is not None
            and "must be a string" in create_result.error
        )

    def test_get_app_success(self) -> None:
        """Test successful app retrieval."""
        service = FlextWebServices()
        # First create an app
        create_result = service.create_app({
            "name": "test-app",
            "host": "localhost",
            "port": 8080,
        })
        assert create_result.is_success
        app_data = create_result.unwrap()
        app_id = app_data["id"]

        # Then get it
        get_result = service.get_app(app_id)
        assert get_result.is_success
        retrieved_app = get_result.unwrap()
        assert retrieved_app["id"] == app_id

    def test_get_app_not_found(self) -> None:
        """Test app retrieval with non-existent app."""
        service = FlextWebServices()
        get_result = service.get_app("nonexistent-id")
        assert get_result.is_failure
        assert get_result.error is not None and "not found" in get_result.error

    def test_start_app_success(self) -> None:
        """Test successful app start."""
        service = FlextWebServices()
        # First create an app
        create_result = service.create_app({
            "name": "test-app",
            "host": "localhost",
            "port": 8080,
        })
        assert create_result.is_success
        app_data = create_result.unwrap()
        app_id = app_data["id"]

        # Then start it
        start_result = service.start_app(app_id)
        assert start_result.is_success
        started_app = start_result.unwrap()
        assert started_app["status"] == "running"

    def test_stop_app_success(self) -> None:
        """Test successful app stop."""
        service = FlextWebServices()
        # First create and start an app
        create_result = service.create_app({
            "name": "test-app",
            "host": "localhost",
            "port": 8080,
        })
        assert create_result.is_success
        app_data = create_result.unwrap()
        app_id = app_data["id"]

        service.start_app(app_id)

        # Then stop it
        stop_result = service.stop_app(app_id)
        assert stop_result.is_success
        stopped_app = stop_result.unwrap()
        assert stopped_app["status"] == "stopped"

    def test_create_web_service_class_method(self) -> None:
        """Test create_web_service class method."""
        result = FlextWebServices.create_web_service()
        assert result.is_success
        service = result.unwrap()
        assert isinstance(service, FlextWebServices)

    def test_create_web_service_with_config(self) -> None:
        """Test create_web_service with config."""
        config = {"host": "localhost", "port": 8080}
        result = FlextWebServices.create_web_service(config)
        assert result.is_success
        service = result.unwrap()
        assert isinstance(service, FlextWebServices)

    def test_create_web_service_invalid_config(self) -> None:
        """Test create_web_service with invalid config dict (extra fields)."""
        result = FlextWebServices.create_web_service({"invalid": "config"})
        assert result.is_failure
        assert result.error is not None and (
            "Extra inputs are not permitted" in result.error
            or "extra" in result.error.lower()
        )
