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
        assert hasattr(service, "_web_logger")
        assert hasattr(service, "_web_bus")
        assert hasattr(service, "_dispatcher")
        assert hasattr(service, "_processors")
        assert hasattr(service, "_registry")
        assert hasattr(service, "apps")
        assert hasattr(service, "app_handler")

    def test_initialization_with_config(self) -> None:
        """Test FlextWebServices initialization with config."""
        config = FlextWebConfig(host="localhost", port=8080)
        service = FlextWebServices(config=config)
        assert service is not None
        assert service._web_config == config

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
        service.start_service("localhost", 8080, debug=True)
        assert service._service_running is True

    def test_stop_service(self) -> None:
        """Test service stop."""
        service = FlextWebServices()
        service._service_running = True
        service.stop_service()
        assert service._service_running is False

    def test_auth_property_lazy_initialization(self) -> None:
        """Test auth property lazy initialization."""
        service = FlextWebServices()
        auth = service.auth
        assert auth is not None
        assert isinstance(auth, FlextWebServices.MockAuth)

    def test_login_success(self) -> None:
        """Test successful login."""
        service = FlextWebServices()
        # First register a user
        register_result = service.register({
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        })
        assert register_result.is_success

        # Then login
        login_result = service.login({
            "username": "testuser",
            "password": "password123",
        })
        assert login_result.is_success
        login_data = login_result.unwrap()
        assert "success" in login_data
        assert login_data["success"] is True

    def test_login_invalid_credentials(self) -> None:
        """Test login with invalid credentials."""
        service = FlextWebServices()
        login_result = service.login({
            "username": "nonexistent",
            "password": "wrongpassword",
        })
        assert login_result.is_failure
        assert "Authentication failed" in login_result.error

    def test_login_invalid_input(self) -> None:
        """Test login with invalid input types."""
        service = FlextWebServices()
        login_result = service.login({
            "username": 123,  # Invalid type
            "password": "password",
        })
        assert login_result.is_failure
        assert "must be strings" in login_result.error

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
        register_result = service.register({
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
        })
        assert register_result.is_success
        user_data = register_result.unwrap()
        assert user_data["success"] is True
        assert user_data["user"]["username"] == "newuser"

    def test_register_duplicate_user(self) -> None:
        """Test registration with duplicate username."""
        service = FlextWebServices()
        # Register first user
        service.register({
            "username": "duplicate",
            "email": "user1@example.com",
            "password": "password123",
        })

        # Try to register with same username
        register_result = service.register({
            "username": "duplicate",
            "email": "user2@example.com",
            "password": "password456",
        })
        assert register_result.is_failure
        assert "Registration failed" in register_result.error

    def test_register_invalid_input(self) -> None:
        """Test registration with invalid input types."""
        service = FlextWebServices()
        register_result = service.register({
            "username": 123,  # Invalid type
            "email": "test@example.com",
            "password": "password",
        })
        assert register_result.is_failure
        assert "must be strings" in register_result.error

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
        assert "must be a string" in create_result.error

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
        assert "not found" in get_result.error

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
        """Test create_web_service with invalid config type."""
        result = FlextWebServices.create_web_service("invalid_config")
        assert result.is_failure
        assert "must be a dictionary" in result.error

    def test_create_web_application(self) -> None:
        """Test create_web_application method."""
        service = FlextWebServices()
        web_config = {"name": "test-app", "host": "localhost", "port": 8080}
        result = service.create_web_application(web_config)
        assert result.is_success
        app_info = result.unwrap()
        assert app_info["name"] == "test-app"
        assert app_info["host"] == "localhost"
        assert app_info["port"] == 8080

    def test_create_web_application_empty_config(self) -> None:
        """Test create_web_application with empty config."""
        service = FlextWebServices()
        result = service.create_web_application({})
        assert result.is_failure
        assert "cannot be empty" in result.error

    def test_create_web_application_invalid_config_type(self) -> None:
        """Test create_web_application with invalid config type."""
        service = FlextWebServices()
        result = service.create_web_application("invalid_config")
        assert result.is_failure
        assert "Expected dict" in result.error

    def test_mock_auth_initialization(self) -> None:
        """Test MockAuth initialization."""
        auth = FlextWebServices.MockAuth()
        assert auth is not None
        assert hasattr(auth, "_users")
        assert hasattr(auth, "_tokens")

    def test_mock_auth_authenticate_user_success(self) -> None:
        """Test MockAuth successful user authentication."""
        auth = FlextWebServices.MockAuth()
        # First register a user
        auth.register_user("testuser", "test@example.com", "password123")

        # Then authenticate
        result = auth.authenticate_user("testuser", "password123")
        assert result.is_success
        auth_data = result.unwrap()
        assert "token" in auth_data
        assert "user_id" in auth_data
        assert "username" in auth_data

    def test_mock_auth_authenticate_user_invalid_credentials(self) -> None:
        """Test MockAuth authentication with invalid credentials."""
        auth = FlextWebServices.MockAuth()
        result = auth.authenticate_user("nonexistent", "wrongpassword")
        assert result.is_failure
        assert "Invalid credentials" in result.error

    def test_mock_auth_register_user_success(self) -> None:
        """Test MockAuth successful user registration."""
        auth = FlextWebServices.MockAuth()
        result = auth.register_user("newuser", "newuser@example.com", "password123")
        assert result.is_success
        user_data = result.unwrap()
        assert user_data["username"] == "newuser"
        assert user_data["email"] == "newuser@example.com"

    def test_mock_auth_register_user_duplicate(self) -> None:
        """Test MockAuth registration with duplicate username."""
        auth = FlextWebServices.MockAuth()
        # Register first user
        auth.register_user("duplicate", "user1@example.com", "password123")

        # Try to register with same username
        result = auth.register_user("duplicate", "user2@example.com", "password456")
        assert result.is_failure
        assert "already exists" in result.error
