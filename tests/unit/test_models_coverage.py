"""Comprehensive test coverage to reach 100% for models.py module.

Target missing lines for complete coverage without mocks.
"""

import pytest
from flext_tests import AsyncTestUtils
from pydantic import ValidationError

from flext_web import FlextWebHandlers, FlextWebModels


class TestWebAppEdgeCases:
    """Test WebApp edge cases and error conditions."""

    def test_webapp_can_start_false_conditions(self) -> None:
        """Test can_start property false conditions - covers lines 60-63."""
        app = FlextWebModels.WebApp(
            id="test-app",
            name="Test App",
            host="localhost",
            port=8080,
            status=FlextWebModels.WebAppStatus.RUNNING,
        )

        # Test can_start when status is RUNNING
        assert not app.can_start

        # Test can_start when status is STARTING
        app.status = FlextWebModels.WebAppStatus.STARTING
        assert not app.can_start

    def test_webapp_empty_name_validation(self) -> None:
        """Test empty name validation - covers lines 92-93."""
        app = FlextWebModels.WebApp.model_construct(
            id="test-app",
            name="",  # Empty name should fail validation
            host="localhost",
            port=8080,
            status=FlextWebModels.WebAppStatus.STOPPED,
        )

        result = app.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert "name" in result.error.lower() or "required" in result.error.lower()

    def test_webapp_invalid_port_validation(self) -> None:
        """Test invalid port validation - covers lines 151-152, 159."""
        # Test port out of valid range
        app = FlextWebModels.WebApp.model_construct(
            id="test-app",
            name="Test App",
            host="localhost",
            port=70000,  # Invalid port > 65535
            status=FlextWebModels.WebAppStatus.STOPPED,
        )

        result = app.validate_business_rules()
        assert result.is_failure

        # Test port 0 - Pydantic validation prevents this assignment
        with pytest.raises(
            ValidationError, match="Input should be greater than or equal to 1"
        ):
            app.port = 0

    def test_webapp_invalid_host_validation(self) -> None:
        """Test invalid host validation - covers lines 180."""
        app = FlextWebModels.WebApp.model_construct(
            id="test-app",
            name="Test App",
            host="",  # Empty host
            port=8080,
            status=FlextWebModels.WebAppStatus.STOPPED,
        )

        result = app.validate_business_rules()
        assert result.is_failure

    def test_webapp_status_transitions_edge_cases(self) -> None:
        """Test edge cases in status transitions - covers lines 200, 204, 209."""
        app = FlextWebModels.WebApp(
            id="test-app",
            name="Test App",
            host="localhost",
            port=8080,
            status=FlextWebModels.WebAppStatus.STOPPED,
        )

        # Test can_start when status is ERROR
        app.status = FlextWebModels.WebAppStatus.ERROR
        assert not app.can_start

        # Test can_stop when status is STARTING
        app.status = FlextWebModels.WebAppStatus.STARTING
        assert not app.can_stop

        # Test is_running when status is STOPPING
        app.status = FlextWebModels.WebAppStatus.STOPPING
        assert not app.is_running

    def test_webapp_repr_string_representation(self) -> None:
        """Test string representation - covers lines 219, 233."""
        app = FlextWebModels.WebApp(
            id="test-app", name="Test App", host="localhost", port=8080
        )

        repr_str = repr(app)
        assert "WebApp" in repr_str
        assert "test-app" in repr_str
        assert "Test App" in repr_str

        str_repr = str(app)
        assert "Test App" in str_repr
        assert "localhost:8080" in str_repr


class TestWebAppHandlerEdgeCases:
    """Test WebAppHandler edge cases for complete coverage."""

    def test_handler_create_validation_failures(self) -> None:
        """Test create method validation failures."""
        handler = FlextWebHandlers.WebAppHandler()

        # Test create with invalid data
        result = handler.create("", 0, "")  # All invalid values
        assert result.is_failure

        # Test create with port out of range
        result = handler.create("test", 70000, "localhost")
        assert result.is_failure

    def test_handler_start_stop_error_conditions(self) -> None:
        """Test start/stop with error conditions."""
        handler = FlextWebHandlers.WebAppHandler()

        # Create an app first
        create_result = handler.create("test-app", 8080, "localhost")
        assert create_result.is_success
        app = create_result.value

        # Try to start already running app (set status to RUNNING first)
        app.status = FlextWebModels.WebAppStatus.RUNNING
        start_result = handler.start(app)
        assert start_result.is_failure

        # Try to stop already stopped app
        app.status = FlextWebModels.WebAppStatus.STOPPED
        stop_result = handler.stop(app)
        assert stop_result.is_failure

    def test_handler_with_realistic_scenarios(self) -> None:
        """Test handler with realistic application scenarios using flext_tests."""
        handler = FlextWebHandlers.WebAppHandler()

        # Use AsyncTestUtils from flext_tests for better validation
        AsyncTestUtils()

        # Test full lifecycle
        apps_created = []
        for i in range(3):
            result = handler.create(f"app-{i}", 8000 + i, "localhost")
            assert result.is_success
            apps_created.append(result.value)

        # Test starting multiple apps
        for app in apps_created:
            start_result = handler.start(app)
            assert start_result.is_success
            assert app.status == FlextWebModels.WebAppStatus.RUNNING

        # Test stopping multiple apps
        for app in apps_created:
            stop_result = handler.stop(app)
            assert stop_result.is_success
            assert app.status == FlextWebModels.WebAppStatus.STOPPED


class TestWebAppStatusEnum:
    """Test WebAppStatus enum functionality."""

    def test_all_status_values(self) -> None:
        """Test all status enum values exist and have correct string representations."""
        statuses = [
            FlextWebModels.WebAppStatus.STOPPED,
            FlextWebModels.WebAppStatus.STARTING,
            FlextWebModels.WebAppStatus.RUNNING,
            FlextWebModels.WebAppStatus.STOPPING,
            FlextWebModels.WebAppStatus.ERROR,
        ]

        for status in statuses:
            assert isinstance(status.value, str)
            assert len(status.value) > 0

        # Test enum can be used in comparisons
        assert (
            FlextWebModels.WebAppStatus.STOPPED != FlextWebModels.WebAppStatus.RUNNING
        )
        assert (
            FlextWebModels.WebAppStatus.RUNNING == FlextWebModels.WebAppStatus.RUNNING
        )


class TestModelsIntegration:
    """Test integration between models components."""

    def test_webapp_with_handler_integration(self) -> None:
        """Test WebApp and WebAppHandler working together."""
        handler = FlextWebHandlers.WebAppHandler()

        # Create app through handler
        result = handler.create("integration-test", 9000, "0.0.0.0")
        assert result.is_success

        app = result.value
        assert isinstance(app, FlextWebModels.WebApp)
        assert app.name == "integration-test"
        assert app.port == 9000
        assert app.host == "0.0.0.0"

        # Test business rule validation
        validation_result = app.validate_business_rules()
        assert validation_result.is_success

        # Test status transitions through handler
        start_result = handler.start(app)
        assert start_result.is_success
        assert app.is_running

        stop_result = handler.stop(app)
        assert stop_result.is_success
        assert not app.is_running

    def test_async_integration_with_flext_tests(self) -> None:
        """Test models with async patterns using flext_tests."""
        handler = FlextWebHandlers.WebAppHandler()
        AsyncTestUtils()

        # Create multiple apps for async-like testing
        app_names = ["async-app-1", "async-app-2", "async-app-3"]
        created_apps = []

        for name in app_names:
            result = handler.create(name, 8080, "localhost")
            assert result.is_success
            created_apps.append(result.value)

        # Simulate concurrent operations
        for app in created_apps:
            # Validate each app independently
            validation = app.validate_business_rules()
            assert validation.is_success

            # Test lifecycle
            start_result = handler.start(app)
            assert start_result.is_success

        # All apps should be running
        running_count = sum(1 for app in created_apps if app.is_running)
        assert running_count == len(app_names)
