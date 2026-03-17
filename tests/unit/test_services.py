"""Unit tests for flext_web.services module.

Tests the web services functionality following flext standards.
"""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from flext_web import FlextWebServices as s
from flext_web import FlextWebSettings
from tests import c, m


class TestFlextWebService:
    """Test suite for s class."""

    def test_initialization_without_config(self) -> None:
        """Test s initialization without config.

        NOTE: FlextService (from flext-core) does not expose _logger as a direct
        attribute - logging is accessed through the container or runtime.
        Host/port defaults may be overridden by environment variables loaded by
        FlextSettings.
        """
        service = s()
        assert service is not None
        assert hasattr(service, "_container")
        assert hasattr(service, "_config")
        assert service._config is not None

    def test_initialization_with_config(self) -> None:
        """Test s initialization with config."""
        config = FlextWebSettings(host="localhost", port=8080)
        service = s(_config=config)
        assert service is not None
        assert hasattr(service, "_config")

    def test_initialize_routes(self) -> None:
        """Test routes initialization."""
        service = s()
        _ = service.initialize_routes()
        assert service._routes_initialized is True

    def test_configure_middleware(self) -> None:
        """Test middleware configuration."""
        service = s()
        _ = service.configure_middleware()
        assert service._middleware_configured is True

    def test_start_service(self) -> None:
        """Test service start."""
        service = s()
        _ = service.start_service("localhost", 8080, _debug=True)
        assert service._service_running is True

    def test_stop_service(self) -> None:
        """Test service stop."""
        service = s()
        service._service_running = True
        _ = service.stop_service()
        assert service._service_running is False

    def test_auth_property_lazy_initialization(self) -> None:
        """Test auth service access."""
        service = s()
        assert hasattr(service, "authenticate")

    def test_authenticate_success(self) -> None:
        """Test successful authenticate."""
        service = s()
        credentials = m.Web.Credentials(
            username="testuser", password=c.Test.DEFAULT_PASSWORD
        )
        authenticate_result = service.authenticate(credentials)
        assert authenticate_result.is_success, "Authentication should succeed"
        authenticate_data = authenticate_result.value
        assert authenticate_data.authenticated is True
        assert authenticate_data.token is not None
        assert authenticate_data.user_id == "testuser"

    def test_authenticate_invalid_credentials(self) -> None:
        """Test authenticate with invalid credentials."""
        service = s()
        credentials = m.Web.Credentials(
            username=c.Test.NONEXISTENT_USERNAME, password="wrongpassword"
        )
        authenticate_result = service.authenticate(credentials)
        assert authenticate_result.is_failure
        assert authenticate_result.error is not None
        assert "Authentication failed" in authenticate_result.error

    def test_authenticate_wrong_password(self) -> None:
        """Test authenticate with wrong password."""
        service = s()
        credentials = m.Web.Credentials(username="testuser", password="wrongpassword")
        authenticate_result = service.authenticate(credentials)
        assert authenticate_result.is_failure
        assert authenticate_result.error is not None
        assert "Authentication failed" in authenticate_result.error

    def test_authenticate_invalid_input(self) -> None:
        """Test authentication with invalid input types."""
        service = s()
        try:
            credentials = m.Web.Credentials(username="123", password="password")
            auth_result = service.authenticate(credentials)
            assert auth_result.is_failure
            assert auth_result.error is not None
        except ValidationError:
            pass

    def test_logout(self) -> None:
        """Test logout functionality."""
        service = s()
        logout_result = service.logout()
        assert logout_result.is_success
        logout_data = logout_result.value
        assert logout_data.data["success"] is True

    def test_register_success(self) -> None:
        """Test successful user registration."""
        service = s()
        user_data = m.Web.UserData(
            username="newuser", email="newuser@example.com", password="password123"
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
        service = s()
        first_user_data = m.Web.UserData(
            username="duplicate", email="user1@example.com", password="password123"
        )
        first_result = service.register_user(first_user_data)
        assert first_result.is_success
        second_user_data = m.Web.UserData(
            username="duplicate", email="user2@example.com", password="password456"
        )
        register_result = service.register_user(second_user_data)
        assert register_result.is_success

    def test_register_invalid_input(self) -> None:
        """Test registration with invalid input types."""
        service = s()
        try:
            user_data = m.Web.UserData(username="123", email="test@example.com")
            register_result = service.register_user(user_data)
            assert register_result.is_failure
        except ValidationError:
            pass

    def test_health_check(self) -> None:
        """Test health check functionality."""
        service = s()
        health_result = service.health_check()
        assert health_result.is_success
        health_data = health_result.value
        assert health_data["status"] == "healthy"
        assert health_data["service"] == "flext-web"
        assert "timestamp" in health_data

    def test_dashboard(self) -> None:
        """Test dashboard functionality."""
        service = s()
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
        service = s()
        list_result = service.list_apps()
        assert list_result.is_success
        apps_data: list[Any] = list_result.value
        assert isinstance(apps_data, list)
        assert all(hasattr(app, "id") for app in apps_data)

    def test_create_app_success(self) -> None:
        """Test successful app creation."""
        service = s()
        app_data = m.Web.AppData(name="test-app", host="localhost", port=8080)
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
        service = s()
        try:
            app_data = m.Web.AppData(name="123", host="localhost", port=8080)
            create_result = service.create_app(app_data)
            assert create_result.is_failure
        except ValidationError:
            pass

    def test_get_app_success(self) -> None:
        """Test successful app retrieval."""
        service = s()
        app_data = m.Web.AppData(name="test-app", host="localhost", port=8080)
        create_result = service.create_app(app_data)
        assert create_result.is_success
        app_response = create_result.value
        app_id = app_response.id
        get_result = service.get_app(app_id)
        assert get_result.is_success
        retrieved_app = get_result.value
        assert retrieved_app.id == app_id

    def test_get_app_not_found(self) -> None:
        """Test app retrieval with non-existent app."""
        service = s()
        get_result = service.get_app("nonexistent-id")
        assert get_result.is_failure
        assert get_result.error is not None
        assert "not found" in get_result.error

    def test_get_app_invalid_id(self) -> None:
        """Test app retrieval with invalid ID."""
        service = s()
        invalid_id = str(123)
        get_result = service.get_app(invalid_id)
        assert get_result.is_failure
        assert get_result.error is not None
        assert "must be a string" in get_result.error or "not found" in get_result.error
        get_result = service.get_app("")
        assert get_result.is_failure
        assert get_result.error is not None
        assert "cannot be empty" in get_result.error

    def test_start_app_success(self) -> None:
        """Test successful app start."""
        service = s()
        app_data = m.Web.AppData(name="test-app", host="localhost", port=8080)
        create_result = service.create_app(app_data)
        assert create_result.is_success
        app_response = create_result.value
        app_id = app_response.id
        start_result = service.start_app(app_id)
        assert start_result.is_success
        started_app = start_result.value
        assert started_app.status == "running"

    def test_start_app_invalid_id(self) -> None:
        """Test app start with invalid ID."""
        service = s()
        invalid_id = str(123)
        start_result = service.start_app(invalid_id)
        assert start_result.is_failure
        assert start_result.error is not None
        assert (
            "must be a string" in start_result.error
            or "not found" in start_result.error
        )
        start_result = service.start_app("")
        assert start_result.is_failure
        assert start_result.error is not None
        assert "cannot be empty" in start_result.error
        start_result = service.start_app("nonexistent-id")
        assert start_result.is_failure
        assert start_result.error is not None
        assert "not found" in start_result.error

    def test_stop_app_success(self) -> None:
        """Test successful app stop."""
        service = s()
        app_data = m.Web.AppData(name="test-app", host="localhost", port=8080)
        create_result = service.create_app(app_data)
        assert create_result.is_success
        app_response = create_result.value
        app_id = app_response.id
        _ = service.start_app(app_id)
        stop_result = service.stop_app(app_id)
        assert stop_result.is_success
        stopped_app = stop_result.value
        assert stopped_app.status == "stopped"

    def test_stop_app_invalid_id(self) -> None:
        """Test app stop with invalid ID."""
        service = s()
        invalid_id = str(123)
        stop_result = service.stop_app(invalid_id)
        assert stop_result.is_failure
        assert stop_result.error is not None
        assert (
            "must be a string" in stop_result.error or "not found" in stop_result.error
        )
        stop_result = service.stop_app("")
        assert stop_result.is_failure
        assert stop_result.error is not None
        assert "cannot be empty" in stop_result.error
        stop_result = service.stop_app("nonexistent-id")
        assert stop_result.is_failure
        assert stop_result.error is not None
        assert "not found" in stop_result.error

    def test_create_web_service_class_method(self) -> None:
        """Test create_web_service class method."""
        result = s.create_web_service()
        assert result.is_success
        service = result.value
        assert isinstance(service, s)

    def test_create_web_service_with_config(self) -> None:
        """Test create_web_service with config."""
        config = FlextWebSettings(host="localhost", port=8080)
        result = s.create_web_service(config)
        assert result.is_success
        service = result.value
        assert isinstance(service, s)

    @pytest.mark.xfail(
        reason="FlextSettings bug: Field constraints not enforced", strict=False
    )
    def test_create_web_service_invalid_config(self) -> None:
        """Test create_web_service with invalid config.

        Expected: ValidationError for port=-1 (Field constraint ge=0)
        Actual: FlextSettings accepts invalid port (bug in flext-core)
        """
        with pytest.raises(ValidationError):
            _ = FlextWebSettings(port=-1)

    def test_create_entity_success(self) -> None:
        """Test successful entity creation."""
        service = s()
        entity_data = m.Web.EntityData(data={"key": "value"})
        create_result = service.create_entity(entity_data)
        assert create_result.is_success
        created_entity = create_result.value
        assert "id" in created_entity.data
        assert created_entity.data["key"] == "value"

    def test_get_entity_success(self) -> None:
        """Test successful entity retrieval."""
        service = s()
        entity_data = m.Web.EntityData(data={"key": "value"})
        create_result = service.create_entity(entity_data)
        assert create_result.is_success
        created_entity = create_result.value
        entity_id_value = created_entity.data["id"]
        entity_id = str(entity_id_value) if entity_id_value is not None else "unknown"
        get_result = service.get_entity(entity_id)
        assert get_result.is_success
        retrieved_entity = get_result.value
        assert retrieved_entity.data["id"] == entity_id_value

    def test_get_entity_not_found(self) -> None:
        """Test entity retrieval with non-existent entity."""
        service = s()
        get_result = service.get_entity("nonexistent-id")
        assert get_result.is_failure
        assert get_result.error is not None
        assert "not found" in get_result.error

    def test_get_entity_invalid_id(self) -> None:
        """Test entity retrieval with invalid ID."""
        service = s()
        invalid_id = str(123)
        get_result = service.get_entity(invalid_id)
        assert get_result.is_failure
        assert get_result.error is not None
        assert "must be a string" in get_result.error or "not found" in get_result.error
        get_result = service.get_entity("")
        assert get_result.is_failure
        assert get_result.error is not None
        assert "cannot be empty" in get_result.error

    def test_list_entities_success(self) -> None:
        """Test successful entity listing."""
        service = s()
        entity1 = m.Web.EntityData(data={"key1": "value1"})
        entity2 = m.Web.EntityData(data={"key2": "value2"})
        _ = service.create_entity(entity1)
        _ = service.create_entity(entity2)
        list_result = service.list_entities()
        assert list_result.is_success
        entities = list_result.value
        assert len(entities) >= 2

    def test_health_status_success(self) -> None:
        """Test health status retrieval."""
        service = s()
        health_result = service.health_status()
        assert health_result.is_success
        health_data = health_result.value
        assert health_data.status == "healthy"
        assert health_data.service == "flext-web"
        assert health_data.timestamp is not None

    def test_dashboard_metrics_success(self) -> None:
        """Test dashboard metrics retrieval."""
        service = s()
        metrics_result = service.dashboard_metrics()
        assert metrics_result.is_success
        metrics_data = metrics_result.value
        assert metrics_data.service_status == "operational"
        assert isinstance(metrics_data.components, list)

    def test_create_configuration_success(self) -> None:
        """Test configuration creation."""
        service = s()
        config = FlextWebSettings(secret_key=c.Web.WebDefaults.TEST_SECRET_KEY)
        create_result = service.create_configuration(config)
        assert create_result.is_success
        created_config = create_result.value
        assert created_config == config

    def test_initialize_routes_already_initialized(self) -> None:
        """Test routes initialization when already initialized."""
        service = s()
        result1 = service.initialize_routes()
        assert result1.is_success
        assert service._routes_initialized is True
        result2 = service.initialize_routes()
        assert result2.is_success

    def test_configure_middleware_already_configured(self) -> None:
        """Test middleware configuration when already configured."""
        service = s()
        result1 = service.configure_middleware()
        assert result1.is_success
        assert service._middleware_configured is True
        result2 = service.configure_middleware()
        assert result2.is_success

    def test_start_service_already_running(self) -> None:
        """Test service start when already running."""
        service = s()
        start_result1 = service.start_service()
        assert start_result1.is_success
        start_result2 = service.start_service()
        assert start_result2.is_failure
        assert start_result2.error is not None
        assert "already running" in start_result2.error

    def test_stop_service_not_running(self) -> None:
        """Test service stop when not running."""
        service = s()
        stop_result = service.stop_service()
        assert stop_result.is_failure
        assert stop_result.error is not None
        assert "not running" in stop_result.error

    def test_validate_business_rules_success(self) -> None:
        """Test business rules validation when service is valid."""
        service = s()
        result = service.validate_business_rules()
        assert result.is_success
        assert result.value is True

    def test_validate_business_rules_running_without_routes(self) -> None:
        """Test business rules validation when service is running without routes."""
        service = s()
        service._service_running = True
        service._routes_initialized = False
        result = service.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert "cannot be running without initialized routes" in result.error

    def test_validate_business_rules_running_without_middleware(self) -> None:
        """Test business rules validation when service is running without middleware."""
        service = s()
        service._service_running = True
        service._routes_initialized = True
        service._middleware_configured = False
        result = service.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert "cannot be running without configured middleware" in result.error

    def test_execute_service(self) -> None:
        """Test service execution."""
        service = s()
        result = service.execute()
        assert result.is_success
        assert result.value is True

    def test_create_service_class_method(self) -> None:
        """Test create_service class method."""
        result = s.create_service()
        assert result.is_success
        service = result.value
        assert isinstance(service, s)

    def test_create_service_with_config(self) -> None:
        """Test create_service with config."""
        config = FlextWebSettings(secret_key=c.Web.WebDefaults.TEST_SECRET_KEY)
        result = s.create_service(config)
        assert result.is_success
        service = result.value
        assert isinstance(service, s)
        assert service._config is not None

    def test_entity_service_execute(self) -> None:
        """Test Entity service execute method."""
        entity_service = s.Entity()
        execute_result = entity_service.execute()
        assert execute_result.is_success
        ready_response = execute_result.value
        assert ready_response.data["message"] == "Entity service ready"
