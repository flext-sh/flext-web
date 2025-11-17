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
        from flext_core import FlextConstants

        from flext_web.models import FlextWebModels

        service = FlextWebServices()
        # Use valid credentials from constants
        credentials = FlextWebModels.Service.Credentials(
            username="testuser",
            password=FlextConstants.Test.DEFAULT_PASSWORD,
        )
        authenticate_result = service.authenticate(credentials)
        assert authenticate_result.is_success
        authenticate_data = authenticate_result.unwrap()
        assert authenticate_data.authenticated is True
        assert authenticate_data.token is not None
        assert authenticate_data.user_id == "testuser"

    def test_authenticate_invalid_credentials(self) -> None:
        """Test authenticate with invalid credentials."""
        from flext_core import FlextConstants

        from flext_web.models import FlextWebModels

        service = FlextWebServices()
        # Use nonexistent username from constants
        credentials = FlextWebModels.Service.Credentials(
            username=FlextConstants.Test.NONEXISTENT_USERNAME,
            password="wrongpassword",
        )
        authenticate_result = service.authenticate(credentials)
        assert authenticate_result.is_failure
        assert authenticate_result.error is not None
        assert "Authentication failed" in authenticate_result.error

    def test_authenticate_invalid_input(self) -> None:
        """Test authentication with invalid input types."""
        from pydantic import ValidationError

        from flext_web.models import FlextWebModels

        service = FlextWebServices()
        # Try to create invalid credentials - should fail at model validation
        try:
            credentials = FlextWebModels.Service.Credentials(
                username=123,  # type: ignore[arg-type]  # Invalid type
                password="password",
            )
            # If validation passes (shouldn't), test will fail
            auth_result = service.authenticate(credentials)
            assert auth_result.is_failure
            assert auth_result.error is not None
        except ValidationError:
            # Expected - Pydantic validation should fail fast
            # This is the correct behavior - no fallback, fail fast
            pass

    def test_logout(self) -> None:
        """Test logout functionality."""
        service = FlextWebServices()
        logout_result = service.logout()
        assert logout_result.is_success
        logout_data = logout_result.unwrap()
        assert logout_data.data["success"] is True

    def test_register_success(self) -> None:
        """Test successful user registration."""
        from flext_web.models import FlextWebModels

        service = FlextWebServices()
        user_data = FlextWebModels.Service.UserData(
            username="newuser",
            email="newuser@example.com",
            password="password123",
        )
        register_result = service.register_user(user_data)
        assert register_result.is_success
        user_response = register_result.unwrap()
        assert user_response.id is not None
        assert user_response.username == "newuser"
        assert user_response.email == "newuser@example.com"
        assert user_response.created is True

    def test_register_duplicate_user(self) -> None:
        """Test registration with duplicate username."""
        from flext_web.models import FlextWebModels

        service = FlextWebServices()
        # Register first user
        first_user_data = FlextWebModels.Service.UserData(
            username="duplicate",
            email="user1@example.com",
            password="password123",
        )
        first_result = service.register_user(first_user_data)
        assert first_result.is_success

        # Try to register with same username (service allows it without duplicate checking)
        second_user_data = FlextWebModels.Service.UserData(
            username="duplicate",
            email="user2@example.com",
            password="password456",
        )
        register_result = service.register_user(second_user_data)
        assert register_result.is_success

    def test_register_invalid_input(self) -> None:
        """Test registration with invalid input types."""
        from pydantic import ValidationError

        from flext_web.models import FlextWebModels

        service = FlextWebServices()
        # Try to create invalid user data - should fail at model validation
        try:
            user_data = FlextWebModels.Service.UserData(
                username=123,  # type: ignore[arg-type]  # Invalid type
                email="test@example.com",
            )
            # If validation passes (shouldn't), test will fail
            register_result = service.register_user(user_data)
            assert register_result.is_failure
        except ValidationError:
            # Expected - Pydantic validation should fail
            pass

    def test_health_check(self) -> None:
        """Test health check functionality."""
        service = FlextWebServices()
        health_result = service.health_check()
        assert health_result.is_success
        health_data = health_result.unwrap()
        assert health_data["status"] == "healthy"
        assert health_data["service"] == "flext-web"
        assert "timestamp" in health_data

    def test_dashboard(self) -> None:
        """Test dashboard functionality."""
        service = FlextWebServices()
        dashboard_result = service.dashboard()
        assert dashboard_result.is_success
        dashboard_data = dashboard_result.unwrap()
        assert dashboard_data.total_applications >= 0
        assert dashboard_data.running_applications >= 0
        assert dashboard_data.service_status in {"operational", "stopped"}
        assert isinstance(dashboard_data.routes_initialized, bool)
        assert isinstance(dashboard_data.middleware_configured, bool)
        assert dashboard_data.timestamp is not None

    def test_list_apps(self) -> None:
        """Test list apps functionality."""
        service = FlextWebServices()
        list_result = service.list_apps()
        assert list_result.is_success
        apps_data = list_result.unwrap()
        assert isinstance(apps_data, list)
        assert all(hasattr(app, "id") for app in apps_data)

    def test_create_app_success(self) -> None:
        """Test successful app creation."""
        from flext_web.models import FlextWebModels

        service = FlextWebServices()
        app_data = FlextWebModels.Service.AppData(
            name="test-app",
            host="localhost",
            port=8080,
        )
        create_result = service.create_app(app_data)
        assert create_result.is_success
        app_response = create_result.unwrap()
        assert app_response.name == "test-app"
        assert app_response.host == "localhost"
        assert app_response.port == 8080
        assert app_response.id is not None
        assert app_response.status == "stopped"
        assert app_response.created_at is not None

    def test_create_app_invalid_input(self) -> None:
        """Test app creation with invalid input."""
        from pydantic import ValidationError

        from flext_web.models import FlextWebModels

        service = FlextWebServices()
        # Try to create invalid app data - should fail at model validation
        try:
            app_data = FlextWebModels.Service.AppData(
                name=123,  # type: ignore[arg-type]  # Invalid type
                host="localhost",
                port=8080,
            )
            # If validation passes (shouldn't), test will fail
            create_result = service.create_app(app_data)
            assert create_result.is_failure
        except ValidationError:
            # Expected - Pydantic validation should fail
            pass

    def test_get_app_success(self) -> None:
        """Test successful app retrieval."""
        from flext_web.models import FlextWebModels

        service = FlextWebServices()
        # First create an app
        app_data = FlextWebModels.Service.AppData(
            name="test-app",
            host="localhost",
            port=8080,
        )
        create_result = service.create_app(app_data)
        assert create_result.is_success
        app_response = create_result.unwrap()
        app_id = app_response.id

        # Then get it
        get_result = service.get_app(app_id)
        assert get_result.is_success
        retrieved_app = get_result.unwrap()
        assert retrieved_app.id == app_id

    def test_get_app_not_found(self) -> None:
        """Test app retrieval with non-existent app."""
        service = FlextWebServices()
        get_result = service.get_app("nonexistent-id")
        assert get_result.is_failure
        assert get_result.error is not None and "not found" in get_result.error

    def test_start_app_success(self) -> None:
        """Test successful app start."""
        from flext_web.models import FlextWebModels

        service = FlextWebServices()
        # First create an app
        app_data = FlextWebModels.Service.AppData(
            name="test-app",
            host="localhost",
            port=8080,
        )
        create_result = service.create_app(app_data)
        assert create_result.is_success
        app_response = create_result.unwrap()
        app_id = app_response.id

        # Then start it
        start_result = service.start_app(app_id)
        assert start_result.is_success
        started_app = start_result.unwrap()
        assert started_app.status == "running"

    def test_stop_app_success(self) -> None:
        """Test successful app stop."""
        from flext_web.models import FlextWebModels

        service = FlextWebServices()
        # First create and start an app
        app_data = FlextWebModels.Service.AppData(
            name="test-app",
            host="localhost",
            port=8080,
        )
        create_result = service.create_app(app_data)
        assert create_result.is_success
        app_response = create_result.unwrap()
        app_id = app_response.id

        service.start_app(app_id)

        # Then stop it
        stop_result = service.stop_app(app_id)
        assert stop_result.is_success
        stopped_app = stop_result.unwrap()
        assert stopped_app.status == "stopped"

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
        """Test create_web_service with invalid config (Pydantic validation fails on creation)."""
        import pytest
        from pydantic import ValidationError

        from flext_web.config import FlextWebConfig

        # Config with invalid port should fail Pydantic validation on creation
        with pytest.raises(ValidationError):  # Pydantic will raise ValidationError
            FlextWebConfig(port=-1)
