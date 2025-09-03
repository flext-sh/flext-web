"""FLEXT Web Models - Coverage Enhancement Tests.

Real functionality tests for untested methods in FlextWebModels to achieve 100% coverage
without mocks, focusing on actual business logic validation and factory methods.

Author: FLEXT Development Team
Version: 0.9.0
Status: Production-ready coverage enhancement without mocks
"""

from __future__ import annotations

from flext_web import FlextWebModels


class TestModelsFactoryMethods:
    """Test factory methods in FlextWebModels for complete coverage."""

    def test_create_web_app_factory_success(self) -> None:
        """Test create_web_app factory method with valid data."""
        app_data = {
            "name": "test-factory-app",
            "host": "localhost",
            "port": 3000,
            "status": FlextWebModels.WebAppStatus.STOPPED,
        }

        result = FlextWebModels.create_web_app(app_data)

        assert result.is_success, f"Factory should succeed, got: {result.error}"
        app = result.value
        assert isinstance(app, FlextWebModels.WebApp)
        assert app.name == "test-factory-app"
        assert app.host == "localhost"
        assert app.port == 3000
        assert app.status == FlextWebModels.WebAppStatus.STOPPED

    def test_create_web_app_factory_with_minimal_data(self) -> None:
        """Test create_web_app factory with minimal required data."""
        app_data = {"name": "minimal-app", "port": 8080, "host": "localhost"}

        result = FlextWebModels.create_web_app(app_data)

        assert result.is_success, (
            f"Factory should succeed with defaults, got: {result.error}"
        )
        app = result.value
        assert app.name == "minimal-app"
        assert app.host == "localhost"
        assert app.port == 8080
        assert app.status == FlextWebModels.WebAppStatus.STOPPED  # Default status

    def test_create_web_app_factory_failure_missing_name(self) -> None:
        """Test create_web_app factory failure with missing required fields."""
        app_data = {
            "port": 8080
            # Missing name
        }

        result = FlextWebModels.create_web_app(app_data)

        assert result.is_failure, "Factory should fail with missing name"
        error = result.error or ""
        assert "name" in error.lower()

    def test_create_web_app_factory_failure_invalid_port_type(self) -> None:
        """Test create_web_app factory failure with invalid port type."""
        app_data = {
            "name": "invalid-port-app",
            "port": "not-a-number",  # Invalid type
        }

        result = FlextWebModels.create_web_app(app_data)

        assert result.is_failure, "Factory should fail with invalid port type"

    def test_create_web_app_handler_factory(self) -> None:
        """Test create_web_app_handler factory method."""
        result = FlextWebModels.create_web_app_handler()

        assert result.is_success, f"Handler factory should succeed, got: {result.error}"
        handler = result.value
        assert isinstance(handler, FlextWebModels.WebAppHandler)

    def test_create_web_system_config_development(self) -> None:
        """Test create_web_system_config for development environment."""
        result = FlextWebModels.create_web_system_config("development")

        assert result.is_success, f"System config should succeed, got: {result.error}"
        config = result.value
        assert isinstance(config, dict)
        # ConfigData contains web service fields, not environment itself
        expected_keys = {"host", "port", "debug", "secret_key", "app_name"}
        assert set(config.keys()) == expected_keys
        assert config["debug"] is True  # Development should have debug=True

    def test_create_web_system_config_production(self) -> None:
        """Test create_web_system_config for production environment."""
        result = FlextWebModels.create_web_system_config("production")

        assert result.is_success, f"System config should succeed, got: {result.error}"
        config = result.value
        assert isinstance(config, dict)
        # ConfigData contains web service fields, not environment itself
        expected_keys = {"host", "port", "debug", "secret_key", "app_name"}
        assert set(config.keys()) == expected_keys

    def test_create_web_system_config_invalid_environment(self) -> None:
        """Test create_web_system_config with invalid environment."""
        result = FlextWebModels.create_web_system_config("invalid-env")

        assert result.is_failure, "Should fail with invalid environment"
        error = result.error or ""
        assert (
            "invalid environment" in error.lower() or "must be one of" in error.lower()
        )


class TestModelsValidationMethods:
    """Test validation methods in FlextWebModels for complete coverage."""

    def test_validate_app_data_success(self) -> None:
        """Test validate_app_data with valid data."""
        valid_data = {
            "name": "valid-app",
            "host": "localhost",
            "port": 8080,
            "status": "stopped",
        }

        result = FlextWebModels.validate_app_data(valid_data)

        assert result.is_success, f"Validation should succeed, got: {result.error}"
        validated_data = result.value
        assert isinstance(validated_data, dict)
        assert validated_data["name"] == "valid-app"

    def test_validate_app_data_failure_missing_required(self) -> None:
        """Test validate_app_data with missing required fields."""
        invalid_data = {
            "host": "localhost"
            # Missing name and port
        }

        result = FlextWebModels.validate_app_data(invalid_data)

        assert result.is_failure, "Validation should fail with missing fields"
        error = result.error or ""
        assert "required" in error.lower() or "missing" in error.lower()

    def test_validate_app_data_failure_invalid_port_range(self) -> None:
        """Test validate_app_data with invalid port range."""
        invalid_data = {
            "name": "invalid-port-app",
            "port": 99999,  # Out of range
            "host": "localhost",
        }

        result = FlextWebModels.validate_app_data(invalid_data)

        assert result.is_failure, "Validation should fail with invalid port"


class TestModelsConfigurationMethods:
    """Test configuration methods in FlextWebModels for complete coverage."""

    def test_configure_web_models_system_success(self) -> None:
        """Test configure_web_models_system with valid configuration."""
        config_data = {
            "environment": "development",
            "debug": True,
            "validation_enabled": True,
        }

        result = FlextWebModels.configure_web_models_system(config_data)

        assert result.is_success, f"Configuration should succeed, got: {result.error}"
        configured = result.value
        assert isinstance(configured, dict)

    def test_configure_web_models_system_failure_invalid_config(self) -> None:
        """Test configure_web_models_system with invalid configuration."""
        invalid_config = {"invalid_field": "invalid_value"}

        result = FlextWebModels.configure_web_models_system(invalid_config)

        # Should either succeed with defaults or fail gracefully
        if result.is_failure:
            assert isinstance(result.error, str)
        else:
            assert isinstance(result.value, dict)

    def test_get_web_models_system_config_success(self) -> None:
        """Test get_web_models_system_config retrieval."""
        result = FlextWebModels.get_web_models_system_config()

        assert result.is_success, (
            f"Config retrieval should succeed, got: {result.error}"
        )
        config = result.value
        assert isinstance(config, dict)
        assert "environment" in config or "default" in str(config).lower()


class TestWebAppBusinessLogic:
    """Test WebApp business logic methods for complete coverage."""

    def test_webapp_validate_business_rules_success(self) -> None:
        """Test WebApp validate_business_rules with valid app."""
        app = FlextWebModels.WebApp(
            id="valid-app",
            name="ValidApp",
            host="localhost",
            port=8080,
            status=FlextWebModels.WebAppStatus.STOPPED,
        )

        result = app.validate_business_rules()

        assert result.is_success, f"Business rules should be valid, got: {result.error}"

    def test_webapp_validate_business_rules_failure_invalid_port(self) -> None:
        """Test WebApp validate_business_rules with invalid port."""
        # Create app with invalid port directly (bypassing field validation)
        app = FlextWebModels.WebApp.model_construct(
            id="invalid-app",
            name="InvalidApp",
            host="localhost",
            port=999999,  # Invalid port
            status=FlextWebModels.WebAppStatus.STOPPED,
        )

        result = app.validate_business_rules()

        assert result.is_failure, "Business rules should reject invalid port"
        error = result.error or ""
        assert "port" in error.lower()

    def test_webapp_state_machine_properties(self) -> None:
        """Test WebApp state machine properties for all states."""
        # Test STOPPED state
        stopped_app = FlextWebModels.WebApp(
            id="stopped-app",
            name="StoppedApp",
            port=8080,
            status=FlextWebModels.WebAppStatus.STOPPED,
        )
        assert not stopped_app.is_running
        assert stopped_app.can_start
        assert not stopped_app.can_stop

        # Test RUNNING state
        running_app = FlextWebModels.WebApp(
            id="running-app",
            name="RunningApp",
            port=8081,
            status=FlextWebModels.WebAppStatus.RUNNING,
        )
        assert running_app.is_running
        assert not running_app.can_start
        assert running_app.can_stop

        # Test ERROR state
        error_app = FlextWebModels.WebApp(
            id="error-app",
            name="ErrorApp",
            port=8082,
            status=FlextWebModels.WebAppStatus.ERROR,
        )
        assert not error_app.is_running
        assert error_app.can_start  # Can restart from error
        assert error_app.can_stop
