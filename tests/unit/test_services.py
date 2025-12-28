"""Unit tests for flext_web.services module.

Tests the web services functionality following flext standards.
"""

from __future__ import annotations

import pytest
from flext_core import FlextConstants
from pydantic import ValidationError

from flext_web.constants import FlextWebConstants
from flext_web.models import FlextWebModels
from flext_web.services import FlextWebServices
from flext_web.settings import FlextWebSettings


class TestFlextWebService:
    """Test suite for FlextWebServices class."""

    def test_initialization_without_config(self) -> None:
        """Test FlextWebServices initialization without config."""
        service = FlextWebServices()
        assert service is not None
        assert hasattr(service, "_container")
        assert hasattr(service, "_logger")
        assert hasattr(service, "_config")
        # Config should use Constants defaults when None is passed
        assert service._config is not None
        assert service._config.host == FlextWebConstants.WebDefaults.HOST
        assert service._config.port == FlextWebConstants.WebDefaults.PORT

    def test_initialization_with_config(self) -> None:
        """Test FlextWebServices initialization with config."""
        config = FlextWebSettings(host="localhost", port=8080)
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
        # Use valid credentials from constants
        credentials = FlextWebModels.Service.Credentials(
            username="testuser",
            password=FlextConstants.Test.DEFAULT_PASSWORD,
        )
        authenticate_result = service.authenticate(credentials)
        assert authenticate_result.is_success, "Authentication should succeed"
        authenticate_data = authenticate_result.value
        assert authenticate_data.authenticated is True
        assert authenticate_data.token is not None
        assert authenticate_data.user_id == "testuser"

    def test_authenticate_invalid_credentials(self) -> None:
        """Test authenticate with invalid credentials."""
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

    def test_authenticate_wrong_password(self) -> None:
        """Test authenticate with wrong password."""
        service = FlextWebServices()
        # Use valid username but wrong password
        credentials = FlextWebModels.Service.Credentials(
            username="testuser",
            password="wrongpassword",
        )
        authenticate_result = service.authenticate(credentials)
        assert authenticate_result.is_failure
        assert authenticate_result.error is not None
        assert "Authentication failed" in authenticate_result.error

    def test_authenticate_invalid_input(self) -> None:
        """Test authentication with invalid input types."""
        service = FlextWebServices()
        # Try to create invalid credentials - should fail at model validation
        try:
            credentials = FlextWebModels.Service.Credentials(
                username=123,
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
        logout_data = logout_result.value
        assert logout_data.data["success"] is True

    def test_register_success(self) -> None:
        """Test successful user registration."""
        service = FlextWebServices()
        user_data = FlextWebModels.Service.UserData(
            username="newuser",
            email="newuser@example.com",
            password="password123",
        )
        register_result = service.register_user(user_data)
        assert register_result.is_success
        user_response = register_result.value
        assert user_response.id is not None
        assert user_response.username == "newuser"
        assert user_response.email == "newuser@example.com"
        assert user_response.created is True

    def test_register_duplicate_user(self) -> None:
        """Test registration with duplicate username."""
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
        service = FlextWebServices()
        # Try to create invalid user data - should fail at model validation
        try:
            user_data = FlextWebModels.Service.UserData(
                username=123,
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
        health_data = health_result.value
        assert health_data["status"] == "healthy"
        assert health_data["service"] == "flext-web"
        assert "timestamp" in health_data

    def test_dashboard(self) -> None:
        """Test dashboard functionality."""
        service = FlextWebServices()
        dashboard_result = service.dashboard()
        assert dashboard_result.is_success
        dashboard_data = dashboard_result.value
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
        apps_data = list_result.value
        assert isinstance(apps_data, list)
        assert all(hasattr(app, "id") for app in apps_data)

    def test_create_app_success(self) -> None:
        """Test successful app creation."""
        service = FlextWebServices()
        app_data = FlextWebModels.Service.AppData(
            name="test-app",
            host="localhost",
            port=8080,
        )
        create_result = service.create_app(app_data)
        assert create_result.is_success
        app_response = create_result.value
        assert app_response.name == "test-app"
        assert app_response.host == "localhost"
        assert app_response.port == 8080
        assert app_response.id is not None
        assert app_response.status == "stopped"
        assert app_response.created_at is not None

    def test_create_app_invalid_input(self) -> None:
        """Test app creation with invalid input."""
        service = FlextWebServices()
        # Try to create invalid app data - should fail at model validation
        try:
            app_data = FlextWebModels.Service.AppData(
                name=123,
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
        service = FlextWebServices()
        # First create an app
        app_data = FlextWebModels.Service.AppData(
            name="test-app",
            host="localhost",
            port=8080,
        )
        create_result = service.create_app(app_data)
        assert create_result.is_success
        app_response = create_result.value
        app_id = app_response.id

        # Then get it
        get_result = service.get_app(app_id)
        assert get_result.is_success
        retrieved_app = get_result.value
        assert retrieved_app.id == app_id

    def test_get_app_not_found(self) -> None:
        """Test app retrieval with non-existent app."""
        service = FlextWebServices()
        get_result = service.get_app("nonexistent-id")
        assert get_result.is_failure
        assert get_result.error is not None
        assert "not found" in get_result.error

    def test_get_app_invalid_id(self) -> None:
        """Test app retrieval with invalid ID."""
        service = FlextWebServices()
        # Test with non-string ID - use actual invalid type
        invalid_id: object = 123
        get_result = service.get_app(invalid_id)  # type: ignore[arg-type]
        assert get_result.is_failure
        assert get_result.error is not None
        assert "must be a string" in get_result.error

        # Test with empty string
        get_result = service.get_app("")
        assert get_result.is_failure
        assert get_result.error is not None
        assert "cannot be empty" in get_result.error

    def test_start_app_success(self) -> None:
        """Test successful app start."""
        service = FlextWebServices()
        # First create an app
        app_data = FlextWebModels.Service.AppData(
            name="test-app",
            host="localhost",
            port=8080,
        )
        create_result = service.create_app(app_data)
        assert create_result.is_success
        app_response = create_result.value
        app_id = app_response.id

        # Then start it
        start_result = service.start_app(app_id)
        assert start_result.is_success
        started_app = start_result.value
        assert started_app.status == "running"

    def test_start_app_invalid_id(self) -> None:
        """Test app start with invalid ID."""
        service = FlextWebServices()
        # Test with non-string ID - use actual invalid type
        invalid_id: object = 123
        start_result = service.start_app(invalid_id)  # type: ignore[arg-type]
        assert start_result.is_failure
        assert start_result.error is not None
        assert "must be a string" in start_result.error

        # Test with empty string
        start_result = service.start_app("")
        assert start_result.is_failure
        assert start_result.error is not None
        assert "cannot be empty" in start_result.error

        # Test with non-existent app
        start_result = service.start_app("nonexistent-id")
        assert start_result.is_failure
        assert start_result.error is not None
        assert "not found" in start_result.error

    def test_stop_app_success(self) -> None:
        """Test successful app stop."""
        service = FlextWebServices()
        # First create and start an app
        app_data = FlextWebModels.Service.AppData(
            name="test-app",
            host="localhost",
            port=8080,
        )
        create_result = service.create_app(app_data)
        assert create_result.is_success
        app_response = create_result.value
        app_id = app_response.id

        service.start_app(app_id)

        # Then stop it
        stop_result = service.stop_app(app_id)
        assert stop_result.is_success
        stopped_app = stop_result.value
        assert stopped_app.status == "stopped"

    def test_stop_app_invalid_id(self) -> None:
        """Test app stop with invalid ID."""
        service = FlextWebServices()
        # Test with non-string ID - use actual invalid type
        invalid_id: object = 123
        stop_result = service.stop_app(invalid_id)  # type: ignore[arg-type]
        assert stop_result.is_failure
        assert stop_result.error is not None
        assert "must be a string" in stop_result.error

        # Test with empty string
        stop_result = service.stop_app("")
        assert stop_result.is_failure
        assert stop_result.error is not None
        assert "cannot be empty" in stop_result.error

        # Test with non-existent app
        stop_result = service.stop_app("nonexistent-id")
        assert stop_result.is_failure
        assert stop_result.error is not None
        assert "not found" in stop_result.error

    def test_create_web_service_class_method(self) -> None:
        """Test create_web_service class method."""
        result = FlextWebServices.create_web_service()
        assert result.is_success
        service = result.value
        assert isinstance(service, FlextWebServices)

    def test_create_web_service_with_config(self) -> None:
        """Test create_web_service with config."""
        config = FlextWebSettings(host="localhost", port=8080)
        result = FlextWebServices.create_web_service(config)
        assert result.is_success
        service = result.value
        assert isinstance(service, FlextWebServices)

    def test_create_web_service_invalid_config(self) -> None:
        """Test create_web_service with invalid config (Pydantic validation fails on creation)."""
        # Config with invalid port should fail Pydantic validation on creation
        with pytest.raises(ValidationError):  # Pydantic will raise ValidationError
            FlextWebSettings(port=-1)

    def test_create_entity_success(self) -> None:
        """Test successful entity creation."""
        service = FlextWebServices()
        entity_data = FlextWebModels.Service.EntityData(data={"key": "value"})
        create_result = service.create_entity(entity_data)
        assert create_result.is_success
        created_entity = create_result.value
        assert "id" in created_entity.data
        assert created_entity.data["key"] == "value"

    def test_get_entity_success(self) -> None:
        """Test successful entity retrieval."""
        service = FlextWebServices()
        # First create an entity
        entity_data = FlextWebModels.Service.EntityData(data={"key": "value"})
        create_result = service.create_entity(entity_data)
        assert create_result.is_success
        created_entity = create_result.value
        entity_id = created_entity.data["id"]

        # Then get it
        get_result = service.get_entity(entity_id)
        assert get_result.is_success
        retrieved_entity = get_result.value
        assert retrieved_entity.data["id"] == entity_id

    def test_get_entity_not_found(self) -> None:
        """Test entity retrieval with non-existent entity."""
        service = FlextWebServices()
        get_result = service.get_entity("nonexistent-id")
        assert get_result.is_failure
        assert get_result.error is not None
        assert "not found" in get_result.error

    def test_get_entity_invalid_id(self) -> None:
        """Test entity retrieval with invalid ID."""
        service = FlextWebServices()
        # Test with non-string ID - use actual invalid type
        invalid_id: object = 123
        get_result = service.get_entity(invalid_id)  # type: ignore[arg-type]
        assert get_result.is_failure
        assert get_result.error is not None
        assert "must be a string" in get_result.error

        # Test with empty string
        get_result = service.get_entity("")
        assert get_result.is_failure
        assert get_result.error is not None
        assert "cannot be empty" in get_result.error

    def test_list_entities_success(self) -> None:
        """Test successful entity listing."""
        service = FlextWebServices()
        # Create some entities
        entity1 = FlextWebModels.Service.EntityData(data={"key1": "value1"})
        entity2 = FlextWebModels.Service.EntityData(data={"key2": "value2"})
        service.create_entity(entity1)
        service.create_entity(entity2)

        # List all entities
        list_result = service.list_entities()
        assert list_result.is_success
        entities = list_result.value
        assert len(entities) >= 2

    def test_health_status_success(self) -> None:
        """Test health status retrieval."""
        service = FlextWebServices()
        health_result = service.health_status()
        assert health_result.is_success
        health_data = health_result.value
        assert health_data.status == "healthy"
        assert health_data.service == "flext-web"
        assert health_data.timestamp is not None

    def test_dashboard_metrics_success(self) -> None:
        """Test dashboard metrics retrieval."""
        service = FlextWebServices()
        metrics_result = service.dashboard_metrics()
        assert metrics_result.is_success
        metrics_data = metrics_result.value
        assert metrics_data.service_status == "operational"
        assert isinstance(metrics_data.components, list)

    def test_create_configuration_success(self) -> None:
        """Test configuration creation."""
        service = FlextWebServices()
        config = FlextWebSettings(
            secret_key=FlextWebConstants.WebDefaults.TEST_SECRET_KEY,
        )
        create_result = service.create_configuration(config)
        assert create_result.is_success
        created_config = create_result.value
        assert created_config == config

    def test_initialize_routes_already_initialized(self) -> None:
        """Test routes initialization when already initialized."""
        service = FlextWebServices()
        # Initialize once
        result1 = service.initialize_routes()
        assert result1.is_success
        assert service._routes_initialized is True

        # Initialize again (should return success)
        result2 = service.initialize_routes()
        assert result2.is_success

    def test_configure_middleware_already_configured(self) -> None:
        """Test middleware configuration when already configured."""
        service = FlextWebServices()
        # Configure once
        result1 = service.configure_middleware()
        assert result1.is_success
        assert service._middleware_configured is True

        # Configure again (should return success)
        result2 = service.configure_middleware()
        assert result2.is_success

    def test_start_service_already_running(self) -> None:
        """Test service start when already running."""
        service = FlextWebServices()
        # Start service
        start_result1 = service.start_service()
        assert start_result1.is_success

        # Try to start again (should fail)
        start_result2 = service.start_service()
        assert start_result2.is_failure
        assert start_result2.error is not None
        assert "already running" in start_result2.error

    def test_stop_service_not_running(self) -> None:
        """Test service stop when not running."""
        service = FlextWebServices()
        # Service is not running by default
        stop_result = service.stop_service()
        assert stop_result.is_failure
        assert stop_result.error is not None
        assert "not running" in stop_result.error

    def test_validate_business_rules_success(self) -> None:
        """Test business rules validation when service is valid."""
        service = FlextWebServices()
        # Service is valid by default (not running)
        result = service.validate_business_rules()
        assert result.is_success
        assert result.value is True

    def test_validate_business_rules_running_without_routes(self) -> None:
        """Test business rules validation when service is running without routes."""
        service = FlextWebServices()
        # Manually set service as running without initializing routes
        service._service_running = True
        service._routes_initialized = False

        result = service.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert "cannot be running without initialized routes" in result.error

    def test_validate_business_rules_running_without_middleware(self) -> None:
        """Test business rules validation when service is running without middleware."""
        service = FlextWebServices()
        # Manually set service as running without configuring middleware
        service._service_running = True
        service._routes_initialized = True
        service._middleware_configured = False

        result = service.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert "cannot be running without configured middleware" in result.error

    def test_execute_service(self) -> None:
        """Test service execution."""
        service = FlextWebServices()
        result = service.execute()
        assert result.is_success
        assert result.value is True

    def test_create_service_class_method(self) -> None:
        """Test create_service class method."""
        result = FlextWebServices.create_service()
        assert result.is_success
        service = result.value
        assert isinstance(service, FlextWebServices)

    def test_create_service_with_config(self) -> None:
        """Test create_service with config."""
        config = FlextWebSettings(
            secret_key=FlextWebConstants.WebDefaults.TEST_SECRET_KEY,
        )
        result = FlextWebServices.create_service(config)
        assert result.is_success
        service = result.value
        assert isinstance(service, FlextWebServices)
        # Config is cloned by FlextService, so compare attributes instead
        assert service._config.host == config.host
        assert service._config.port == config.port
        assert service._config.secret_key == config.secret_key

    def test_entity_service_execute(self) -> None:
        """Test Entity service execute method."""
        entity_service = FlextWebServices.Entity()
        execute_result = entity_service.execute()
        assert execute_result.is_success
        ready_response = execute_result.value
        assert ready_response.data["message"] == "Entity service ready"
