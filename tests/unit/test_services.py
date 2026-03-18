"""Unit tests for flext_web.services module.

Tests the web services functionality following flext standards.
"""

from __future__ import annotations

from typing import Any

import pytest
from flext_tests import tm
from pydantic import ValidationError

from flext_web import FlextWebServices as s, FlextWebSettings
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
        tm.that(service is not None, eq=True)
        tm.that(hasattr(service, "_container"), eq=True)
        tm.that(hasattr(service, "_config"), eq=True)
        tm.that(service._config is not None, eq=True)

    def test_initialization_with_config(self) -> None:
        """Test s initialization with config."""
        config = FlextWebSettings(host="localhost", port=8080)
        service = s(_config=config)
        tm.that(service is not None, eq=True)
        tm.that(hasattr(service, "_config"), eq=True)

    def test_initialize_routes(self) -> None:
        """Test routes initialization."""
        service = s()
        _ = service.initialize_routes()
        tm.that(service._routes_initialized is True, eq=True)

    def test_configure_middleware(self) -> None:
        """Test middleware configuration."""
        service = s()
        _ = service.configure_middleware()
        tm.that(service._middleware_configured is True, eq=True)

    def test_start_service(self) -> None:
        """Test service start."""
        service = s()
        _ = service.start_service("localhost", 8080, _debug=True)
        tm.that(service._service_running is True, eq=True)

    def test_stop_service(self) -> None:
        """Test service stop."""
        service = s()
        service._service_running = True
        _ = service.stop_service()
        tm.that(service._service_running is False, eq=True)

    def test_auth_property_lazy_initialization(self) -> None:
        """Test auth service access."""
        service = s()
        tm.that(hasattr(service, "authenticate"), eq=True)

    def test_authenticate_success(self) -> None:
        """Test successful authenticate."""
        service = s()
        credentials = m.Web.Credentials(
            username="testuser", password=c.Test.DEFAULT_PASSWORD
        )
        authenticate_result = service.authenticate(credentials)
        tm.ok(authenticate_result), "Authentication should succeed"
        authenticate_data = authenticate_result.value
        tm.that(authenticate_data.authenticated is True, eq=True)
        tm.that(authenticate_data.token is not None, eq=True)
        tm.that(authenticate_data.user_id, eq="testuser")

    def test_authenticate_invalid_credentials(self) -> None:
        """Test authenticate with invalid credentials."""
        service = s()
        credentials = m.Web.Credentials(
            username=c.Test.NONEXISTENT_USERNAME, password="wrongpassword"
        )
        authenticate_result = service.authenticate(credentials)
        tm.fail(authenticate_result)
        tm.that(authenticate_result.error is not None, eq=True)
        tm.that("Authentication failed" in authenticate_result.error, eq=True)

    def test_authenticate_wrong_password(self) -> None:
        """Test authenticate with wrong password."""
        service = s()
        credentials = m.Web.Credentials(username="testuser", password="wrongpassword")
        authenticate_result = service.authenticate(credentials)
        tm.fail(authenticate_result)
        tm.that(authenticate_result.error is not None, eq=True)
        tm.that("Authentication failed" in authenticate_result.error, eq=True)

    def test_authenticate_invalid_input(self) -> None:
        """Test authentication with invalid input types."""
        service = s()
        try:
            credentials = m.Web.Credentials(username="123", password="password")
            auth_result = service.authenticate(credentials)
            tm.fail(auth_result)
            tm.that(auth_result.error is not None, eq=True)
        except ValidationError:
            pass

    def test_logout(self) -> None:
        """Test logout functionality."""
        service = s()
        logout_result = service.logout()
        tm.ok(logout_result)
        logout_data = logout_result.value
        tm.that(logout_data.data["success"] is True, eq=True)

    def test_register_success(self) -> None:
        """Test successful user registration."""
        service = s()
        user_data = m.Web.UserData(
            username="newuser", email="newuser@example.com", password="password123"
        )
        register_result = service.register_user(user_data)
        tm.ok(register_result)
        user_response = register_result.value
        tm.that(user_response.id is not None, eq=True)
        tm.that(user_response.username, eq="newuser")
        tm.that(user_response.email, eq="newuser@example.com")
        tm.that(user_response.created is True, eq=True)

    def test_register_duplicate_user(self) -> None:
        """Test registration with duplicate username."""
        service = s()
        first_user_data = m.Web.UserData(
            username="duplicate", email="user1@example.com", password="password123"
        )
        first_result = service.register_user(first_user_data)
        tm.ok(first_result)
        second_user_data = m.Web.UserData(
            username="duplicate", email="user2@example.com", password="password456"
        )
        register_result = service.register_user(second_user_data)
        tm.ok(register_result)

    def test_register_invalid_input(self) -> None:
        """Test registration with invalid input types."""
        service = s()
        try:
            user_data = m.Web.UserData(username="123", email="test@example.com")
            register_result = service.register_user(user_data)
            tm.fail(register_result)
        except ValidationError:
            pass

    def test_health_check(self) -> None:
        """Test health check functionality."""
        service = s()
        health_result = service.health_check()
        tm.ok(health_result)
        health_data = health_result.value
        tm.that(health_data["status"], eq="healthy")
        tm.that(health_data["service"], eq="flext-web")
        tm.that("timestamp" in health_data, eq=True)

    def test_dashboard(self) -> None:
        """Test dashboard functionality."""
        service = s()
        dashboard_result = service.dashboard()
        tm.ok(dashboard_result)
        dashboard_data = dashboard_result.value
        tm.that(dashboard_data.total_applications >= 0, eq=True)
        tm.that(dashboard_data.running_applications >= 0, eq=True)
        tm.that(dashboard_data.service_status in {"operational", "stopped"}, eq=True)
        tm.that(isinstance(dashboard_data.routes_initialized, bool), eq=True)
        tm.that(isinstance(dashboard_data.middleware_configured, bool), eq=True)
        tm.that(dashboard_data.timestamp is not None, eq=True)

    def test_list_apps(self) -> None:
        """Test list apps functionality."""
        service = s()
        list_result = service.list_apps()
        tm.ok(list_result)
        apps_data: list[Any] = list_result.value
        tm.that(isinstance(apps_data, list), eq=True)
        tm.that(all(hasattr(app, "id") for app in apps_data), eq=True)

    def test_create_app_success(self) -> None:
        """Test successful app creation."""
        service = s()
        app_data = m.Web.AppData(name="test-app", host="localhost", port=8080)
        create_result = service.create_app(app_data)
        tm.ok(create_result)
        app_response = create_result.value
        tm.that(app_response.name, eq="test-app")
        tm.that(app_response.host, eq="localhost")
        tm.that(app_response.port, eq=8080)
        tm.that(app_response.id is not None, eq=True)
        tm.that(app_response.status, eq="stopped")
        tm.that(app_response.created_at is not None, eq=True)

    def test_create_app_invalid_input(self) -> None:
        """Test app creation with invalid input."""
        service = s()
        try:
            app_data = m.Web.AppData(name="123", host="localhost", port=8080)
            create_result = service.create_app(app_data)
            tm.fail(create_result)
        except ValidationError:
            pass

    def test_get_app_success(self) -> None:
        """Test successful app retrieval."""
        service = s()
        app_data = m.Web.AppData(name="test-app", host="localhost", port=8080)
        create_result = service.create_app(app_data)
        tm.ok(create_result)
        app_response = create_result.value
        app_id = app_response.id
        get_result = service.get_app(app_id)
        tm.ok(get_result)
        retrieved_app = get_result.value
        tm.that(retrieved_app.id, eq=app_id)

    def test_get_app_not_found(self) -> None:
        """Test app retrieval with non-existent app."""
        service = s()
        get_result = service.get_app("nonexistent-id")
        tm.fail(get_result)
        tm.that(get_result.error is not None, eq=True)
        tm.that("not found" in get_result.error, eq=True)

    def test_get_app_invalid_id(self) -> None:
        """Test app retrieval with invalid ID."""
        service = s()
        invalid_id = str(123)
        get_result = service.get_app(invalid_id)
        tm.fail(get_result)
        tm.that(get_result.error is not None, eq=True)
        tm.that(
            "must be a string" in get_result.error or "not found" in get_result.error,
            eq=True,
        )
        get_result = service.get_app("")
        tm.fail(get_result)
        tm.that(get_result.error is not None, eq=True)
        tm.that("cannot be empty" in get_result.error, eq=True)

    def test_start_app_success(self) -> None:
        """Test successful app start."""
        service = s()
        app_data = m.Web.AppData(name="test-app", host="localhost", port=8080)
        create_result = service.create_app(app_data)
        tm.ok(create_result)
        app_response = create_result.value
        app_id = app_response.id
        start_result = service.start_app(app_id)
        tm.ok(start_result)
        started_app = start_result.value
        tm.that(started_app.status, eq="running")

    def test_start_app_invalid_id(self) -> None:
        """Test app start with invalid ID."""
        service = s()
        invalid_id = str(123)
        start_result = service.start_app(invalid_id)
        tm.fail(start_result)
        tm.that(start_result.error is not None, eq=True)
        tm.that(
            (
                "must be a string" in start_result.error
                or "not found" in start_result.error
            ),
            eq=True,
        )
        start_result = service.start_app("")
        tm.fail(start_result)
        tm.that(start_result.error is not None, eq=True)
        tm.that("cannot be empty" in start_result.error, eq=True)
        start_result = service.start_app("nonexistent-id")
        tm.fail(start_result)
        tm.that(start_result.error is not None, eq=True)
        tm.that("not found" in start_result.error, eq=True)

    def test_stop_app_success(self) -> None:
        """Test successful app stop."""
        service = s()
        app_data = m.Web.AppData(name="test-app", host="localhost", port=8080)
        create_result = service.create_app(app_data)
        tm.ok(create_result)
        app_response = create_result.value
        app_id = app_response.id
        _ = service.start_app(app_id)
        stop_result = service.stop_app(app_id)
        tm.ok(stop_result)
        stopped_app = stop_result.value
        tm.that(stopped_app.status, eq="stopped")

    def test_stop_app_invalid_id(self) -> None:
        """Test app stop with invalid ID."""
        service = s()
        invalid_id = str(123)
        stop_result = service.stop_app(invalid_id)
        tm.fail(stop_result)
        tm.that(stop_result.error is not None, eq=True)
        tm.that(
            (
                "must be a string" in stop_result.error
                or "not found" in stop_result.error
            ),
            eq=True,
        )
        stop_result = service.stop_app("")
        tm.fail(stop_result)
        tm.that(stop_result.error is not None, eq=True)
        tm.that("cannot be empty" in stop_result.error, eq=True)
        stop_result = service.stop_app("nonexistent-id")
        tm.fail(stop_result)
        tm.that(stop_result.error is not None, eq=True)
        tm.that("not found" in stop_result.error, eq=True)

    def test_create_web_service_class_method(self) -> None:
        """Test create_web_service class method."""
        result = s.create_web_service()
        tm.ok(result)
        service = result.value
        tm.that(isinstance(service, s), eq=True)

    def test_create_web_service_with_config(self) -> None:
        """Test create_web_service with config."""
        config = FlextWebSettings(host="localhost", port=8080)
        result = s.create_web_service(config)
        tm.ok(result)
        service = result.value
        tm.that(isinstance(service, s), eq=True)

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
        tm.ok(create_result)
        created_entity = create_result.value
        tm.that("id" in created_entity.data, eq=True)
        tm.that(created_entity.data["key"], eq="value")

    def test_get_entity_success(self) -> None:
        """Test successful entity retrieval."""
        service = s()
        entity_data = m.Web.EntityData(data={"key": "value"})
        create_result = service.create_entity(entity_data)
        tm.ok(create_result)
        created_entity = create_result.value
        entity_id_value = created_entity.data["id"]
        entity_id = str(entity_id_value) if entity_id_value is not None else "unknown"
        get_result = service.get_entity(entity_id)
        tm.ok(get_result)
        retrieved_entity = get_result.value
        tm.that(retrieved_entity.data["id"], eq=entity_id_value)

    def test_get_entity_not_found(self) -> None:
        """Test entity retrieval with non-existent entity."""
        service = s()
        get_result = service.get_entity("nonexistent-id")
        tm.fail(get_result)
        tm.that(get_result.error is not None, eq=True)
        tm.that("not found" in get_result.error, eq=True)

    def test_get_entity_invalid_id(self) -> None:
        """Test entity retrieval with invalid ID."""
        service = s()
        invalid_id = str(123)
        get_result = service.get_entity(invalid_id)
        tm.fail(get_result)
        tm.that(get_result.error is not None, eq=True)
        tm.that(
            "must be a string" in get_result.error or "not found" in get_result.error,
            eq=True,
        )
        get_result = service.get_entity("")
        tm.fail(get_result)
        tm.that(get_result.error is not None, eq=True)
        tm.that("cannot be empty" in get_result.error, eq=True)

    def test_list_entities_success(self) -> None:
        """Test successful entity listing."""
        service = s()
        entity1 = m.Web.EntityData(data={"key1": "value1"})
        entity2 = m.Web.EntityData(data={"key2": "value2"})
        _ = service.create_entity(entity1)
        _ = service.create_entity(entity2)
        list_result = service.list_entities()
        tm.ok(list_result)
        entities = list_result.value
        tm.that(len(entities) >= 2, eq=True)

    def test_health_status_success(self) -> None:
        """Test health status retrieval."""
        service = s()
        health_result = service.health_status()
        tm.ok(health_result)
        health_data = health_result.value
        tm.that(health_data.status, eq="healthy")
        tm.that(health_data.service, eq="flext-web")
        tm.that(health_data.timestamp is not None, eq=True)

    def test_dashboard_metrics_success(self) -> None:
        """Test dashboard metrics retrieval."""
        service = s()
        metrics_result = service.dashboard_metrics()
        tm.ok(metrics_result)
        metrics_data = metrics_result.value
        tm.that(metrics_data.service_status, eq="operational")
        tm.that(isinstance(metrics_data.components, list), eq=True)

    def test_create_configuration_success(self) -> None:
        """Test configuration creation."""
        service = s()
        config = FlextWebSettings(secret_key=c.Web.WebDefaults.TEST_SECRET_KEY)
        create_result = service.create_configuration(config)
        tm.ok(create_result)
        created_config = create_result.value
        tm.that(created_config, eq=config)

    def test_initialize_routes_already_initialized(self) -> None:
        """Test routes initialization when already initialized."""
        service = s()
        result1 = service.initialize_routes()
        tm.ok(result1)
        tm.that(service._routes_initialized is True, eq=True)
        result2 = service.initialize_routes()
        tm.ok(result2)

    def test_configure_middleware_already_configured(self) -> None:
        """Test middleware configuration when already configured."""
        service = s()
        result1 = service.configure_middleware()
        tm.ok(result1)
        tm.that(service._middleware_configured is True, eq=True)
        result2 = service.configure_middleware()
        tm.ok(result2)

    def test_start_service_already_running(self) -> None:
        """Test service start when already running."""
        service = s()
        start_result1 = service.start_service()
        tm.ok(start_result1)
        start_result2 = service.start_service()
        tm.fail(start_result2)
        tm.that(start_result2.error is not None, eq=True)
        tm.that("already running" in start_result2.error, eq=True)

    def test_stop_service_not_running(self) -> None:
        """Test service stop when not running."""
        service = s()
        stop_result = service.stop_service()
        tm.fail(stop_result)
        tm.that(stop_result.error is not None, eq=True)
        tm.that("not running" in stop_result.error, eq=True)

    def test_validate_business_rules_success(self) -> None:
        """Test business rules validation when service is valid."""
        service = s()
        result = service.validate_business_rules()
        tm.ok(result)
        tm.that(result.value is True, eq=True)

    def test_validate_business_rules_running_without_routes(self) -> None:
        """Test business rules validation when service is running without routes."""
        service = s()
        service._service_running = True
        service._routes_initialized = False
        result = service.validate_business_rules()
        tm.fail(result)
        tm.that(result.error is not None, eq=True)
        tm.that("cannot be running without initialized routes" in result.error, eq=True)

    def test_validate_business_rules_running_without_middleware(self) -> None:
        """Test business rules validation when service is running without middleware."""
        service = s()
        service._service_running = True
        service._routes_initialized = True
        service._middleware_configured = False
        result = service.validate_business_rules()
        tm.fail(result)
        tm.that(result.error is not None, eq=True)
        tm.that(
            "cannot be running without configured middleware" in result.error, eq=True
        )

    def test_execute_service(self) -> None:
        """Test service execution."""
        service = s()
        result = service.execute()
        tm.ok(result)
        tm.that(result.value is True, eq=True)

    def test_create_service_class_method(self) -> None:
        """Test create_service class method."""
        result = s.create_service()
        tm.ok(result)
        service = result.value
        tm.that(isinstance(service, s), eq=True)

    def test_create_service_with_config(self) -> None:
        """Test create_service with config."""
        config = FlextWebSettings(secret_key=c.Web.WebDefaults.TEST_SECRET_KEY)
        result = s.create_service(config)
        tm.ok(result)
        service = result.value
        tm.that(isinstance(service, s), eq=True)
        tm.that(service._config is not None, eq=True)

    def test_entity_service_execute(self) -> None:
        """Test Entity service execute method."""
        entity_service = s.Entity()
        execute_result = entity_service.execute()
        tm.ok(execute_result)
        ready_response = execute_result.value
        tm.that(ready_response.data["message"], eq="Entity service ready")
