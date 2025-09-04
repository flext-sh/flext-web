"""Comprehensive test coverage for flext_web.typings module.

This test module targets specific missing coverage areas identified in the coverage report.
Focus on real execution tests without mocks for maximum functional coverage.
"""

from typing import get_args, get_origin

from flext_core import FlextResult, FlextTypes

from flext_web import FlextWebTypes


class TestFlextWebTypesStructure:
    """Test FlextWebTypes class structure and TypedDict definitions."""

    def test_flext_web_types_inheritance(self) -> None:
        """Test FlextWebTypes inherits from FlextTypes."""
        assert issubclass(FlextWebTypes, FlextTypes)

    def test_typed_dicts_exist(self) -> None:
        """Test that all TypedDict classes are defined."""
        typed_dict_classes = [
            "AppData",
            "AppDataDict",
            "SuccessResponse",
            "ErrorResponse",
            "ConfigData",
            "ProductionConfigData",
            "DevelopmentConfigData",
            "RequestContext",
            "ResponseData",
            "StatusInfo",
        ]

        for typed_dict in typed_dict_classes:
            assert hasattr(FlextWebTypes, typed_dict)

    def test_type_aliases_exist(self) -> None:
        """Test that type aliases are defined."""
        type_aliases = [
            "AppResult",
            "ConfigResult",
            "ResponseResult",
            "WebHandler",
            "TemplateFilter",
            "RequestData",
            "ResponseReturnValue",
        ]

        for alias in type_aliases:
            assert hasattr(FlextWebTypes, alias)


class TestAppDataTypedDict:
    """Test AppData TypedDict functionality."""

    def test_app_data_creation(self) -> None:
        """Test creating AppData with required fields."""
        app_data: FlextWebTypes.AppData = {
            "id": "app_test",
            "name": "test",
            "host": "localhost",
            "port": 8000,
            "status": "running",
            "is_running": True,
        }

        assert app_data["id"] == "app_test"
        assert app_data["name"] == "test"
        assert app_data["host"] == "localhost"
        assert app_data["port"] == 8000
        assert app_data["status"] == "running"
        assert app_data["is_running"] is True

    def test_app_data_optional_fields(self) -> None:
        """Test AppData with optional fields."""
        # AppData should work with just required fields
        app_data: FlextWebTypes.AppData = {
            "id": "app_minimal",
            "name": "minimal",
            "host": "localhost",
            "port": 8000,
            "status": "stopped",
            "is_running": False,
        }

        assert isinstance(app_data, dict)
        assert len(app_data) == 6


class TestResponseTypedDicts:
    """Test response-related TypedDict classes."""

    def test_success_response_creation(self) -> None:
        """Test creating SuccessResponse."""
        response: FlextWebTypes.SuccessResponse = {
            "success": True,
            "message": "Operation successful",
            "data": {"result": "ok"},
        }

        assert response["success"] is True
        assert response["message"] == "Operation successful"
        assert response["data"] == {"result": "ok"}

    def test_error_response_creation(self) -> None:
        """Test creating ErrorResponse."""
        response: FlextWebTypes.ErrorResponse = {
            "success": False,
            "message": "Operation failed",
            "error": "Validation error",
        }

        assert response["success"] is False
        assert response["message"] == "Operation failed"
        assert response["error"] == "Validation error"

    def test_response_data_creation(self) -> None:
        """Test creating ResponseData."""
        response_data: FlextWebTypes.ResponseData = {
            "status": "ok",
            "code": 200,
            "payload": {"data": "value"},
        }

        assert response_data["status"] == "ok"
        assert response_data["code"] == 200
        assert response_data["payload"] == {"data": "value"}


class TestConfigurationTypedDicts:
    """Test configuration-related TypedDict classes."""

    def test_config_data_creation(self) -> None:
        """Test creating ConfigData."""
        config: FlextWebTypes.ConfigData = {
            "host": "localhost",
            "port": 8080,
            "debug": True,
            "secret_key": "test-secret",
            "app_name": "Test App",
        }

        assert config["host"] == "localhost"
        assert config["port"] == 8080
        assert config["debug"] is True
        assert config["secret_key"] == "test-secret"
        assert config["app_name"] == "Test App"

    def test_production_config_data_creation(self) -> None:
        """Test creating ProductionConfigData."""
        config: FlextWebTypes.ProductionConfigData = {
            "host": "0.0.0.0",
            "port": 443,
            "secret_key": "production-secret-key",
            "debug": False,
            "enable_cors": False,
        }

        assert config["host"] == "0.0.0.0"
        assert config["port"] == 443
        assert config["debug"] is False
        assert config["enable_cors"] is False

    def test_development_config_data_creation(self) -> None:
        """Test creating DevelopmentConfigData."""
        # DevelopmentConfigData has total=False, so all fields are optional
        config: FlextWebTypes.DevelopmentConfigData = {
            "debug": True,
            "host": "localhost",
        }

        assert config["debug"] is True
        assert config["host"] == "localhost"

        # Can also be empty
        empty_config: FlextWebTypes.DevelopmentConfigData = {}
        assert isinstance(empty_config, dict)


class TestFactoryMethods:
    """Test FlextWebTypes factory methods."""

    def test_create_app_data(self) -> None:
        """Test creating app data via factory method."""
        app_data = FlextWebTypes.create_app_data(
            app_id="app_test",
            name="test-app",
            host="localhost",
            port=8000,
            status="running",
            is_running=True,
        )

        assert app_data["id"] == "app_test"
        assert app_data["name"] == "test-app"
        assert app_data["host"] == "localhost"
        assert app_data["port"] == 8000
        assert app_data["status"] == "running"
        assert app_data["is_running"] is True

    def test_create_success_response(self) -> None:
        """Test creating success response via factory method."""
        response = FlextWebTypes.create_success_response(
            "Success message", {"key": "value"}
        )

        assert response["success"] is True
        assert response["message"] == "Success message"
        assert response["data"] == {"key": "value"}

    def test_create_error_response(self) -> None:
        """Test creating error response via factory method."""
        response = FlextWebTypes.create_error_response(
            "Error message", "Validation failed"
        )

        assert response["success"] is False
        assert response["message"] == "Error message"
        assert response["error"] == "Validation failed"

    def test_create_config_data_defaults(self) -> None:
        """Test creating config data with defaults."""
        config = FlextWebTypes.create_config_data()

        assert config["host"] == "localhost"
        assert config["port"] == 8080
        assert config["debug"] is True
        assert config["secret_key"] == "dev-secret-key"
        assert config["app_name"] == "FLEXT Web"

    def test_create_config_data_custom(self) -> None:
        """Test creating config data with custom values."""
        config = FlextWebTypes.create_config_data(
            host="0.0.0.0",
            port=9000,
            debug=False,
            secret_key="custom-secret",
            app_name="Custom App",
        )

        assert config["host"] == "0.0.0.0"
        assert config["port"] == 9000
        assert config["debug"] is False
        assert config["secret_key"] == "custom-secret"
        assert config["app_name"] == "Custom App"

    def test_create_request_context(self) -> None:
        """Test creating request context."""
        context = FlextWebTypes.create_request_context(
            method="POST",
            path="/api/test",
            headers={"Content-Type": "application/json"},
            data={"key": "value"},
        )

        assert context["method"] == "POST"
        assert context["path"] == "/api/test"
        assert context["headers"]["Content-Type"] == "application/json"
        assert context["data"] == {"key": "value"}

    def test_create_request_context_defaults(self) -> None:
        """Test creating request context with defaults."""
        context = FlextWebTypes.create_request_context()

        assert context["method"] == "GET"
        assert context["path"] == "/"
        assert context["headers"] == {}
        assert context["data"] == {}


class TestValidationMethods:
    """Test FlextWebTypes validation methods."""

    def test_validate_app_data_valid(self) -> None:
        """Test validating valid app data."""
        app_data = {
            "id": "app_test",
            "name": "test",
            "host": "localhost",
            "port": 8000,
            "status": "running",
            "is_running": True,
        }

        result = FlextWebTypes.validate_app_data(app_data)

        assert result.is_success
        validated_data = result.value
        assert validated_data["id"] == "app_test"

    def test_validate_app_data_missing_required_field(self) -> None:
        """Test validating app data missing required fields."""
        app_data = {
            "name": "test",
            "host": "localhost",
            # Missing id, port, status, is_running
        }

        result = FlextWebTypes.validate_app_data(app_data)

        assert result.is_failure
        assert "required" in result.error.lower()

    def test_validate_app_data_invalid_type(self) -> None:
        """Test validating app data with invalid types."""
        app_data = {
            "id": "app_test",
            "name": "test",
            "host": "localhost",
            "port": "not_an_integer",  # Should be int
            "status": "running",
            "is_running": True,
        }

        result = FlextWebTypes.validate_app_data(app_data)

        assert result.is_failure
        assert "type" in result.error.lower() or "validation" in result.error.lower()

    def test_validate_config_data_valid(self) -> None:
        """Test validating valid config data."""
        config_data = {
            "host": "localhost",
            "port": 8080,
            "debug": True,
            "secret_key": "test-secret",
            "app_name": "Test App",
        }

        result = FlextWebTypes.validate_config_data(config_data)

        assert result.is_success
        validated_config = result.value
        assert validated_config["host"] == "localhost"

    def test_validate_config_data_missing_fields(self) -> None:
        """Test validating config data missing required fields."""
        config_data = {
            "host": "localhost"
            # Missing port, debug, secret_key, app_name
        }

        result = FlextWebTypes.validate_config_data(config_data)

        assert result.is_failure
        assert "required" in result.error.lower()

    def test_validate_config_data_invalid_port_type(self) -> None:
        """Test validating config data with string port (gets converted)."""
        config_data = {
            "host": "localhost",
            "port": "8080",  # String gets converted to int
            "debug": True,
            "secret_key": "test-secret",
            "app_name": "Test App",
        }

        result = FlextWebTypes.validate_config_data(config_data)

        # String port gets converted to int, so validation succeeds
        assert result.is_success
        assert result.value["port"] == 8080  # Converted to int
        assert isinstance(result.value["port"], int)


class TestTypeAliases:
    """Test type aliases are properly defined."""

    def test_app_result_type_alias(self) -> None:
        """Test AppResult type alias."""
        # Should be FlextResult[AppData]
        alias = FlextWebTypes.AppResult

        # Check it's a generic type alias
        origin = get_origin(alias)
        get_args(alias)

        assert origin is FlextResult
        # The args should include the TypedDict type

    def test_config_result_type_alias(self) -> None:
        """Test ConfigResult type alias."""
        alias = FlextWebTypes.ConfigResult

        origin = get_origin(alias)
        assert origin is FlextResult

    def test_response_result_type_alias(self) -> None:
        """Test ResponseResult type alias."""
        alias = FlextWebTypes.ResponseResult

        origin = get_origin(alias)
        assert origin is FlextResult


class TestRequestContextTypedDict:
    """Test RequestContext TypedDict functionality."""

    def test_request_context_creation(self) -> None:
        """Test creating RequestContext."""
        context: FlextWebTypes.RequestContext = {
            "method": "POST",
            "path": "/api/apps",
            "headers": {"Authorization": "Bearer token"},
            "data": {"name": "test-app"},
        }

        assert context["method"] == "POST"
        assert context["path"] == "/api/apps"
        assert context["headers"]["Authorization"] == "Bearer token"
        assert context["data"]["name"] == "test-app"

    def test_request_context_empty_data(self) -> None:
        """Test RequestContext with empty data."""
        context: FlextWebTypes.RequestContext = {
            "method": "GET",
            "path": "/health",
            "headers": {},
            "data": {},
        }

        assert context["method"] == "GET"
        assert context["path"] == "/health"
        assert context["headers"] == {}
        assert context["data"] == {}


class TestStatusInfoTypedDict:
    """Test StatusInfo TypedDict functionality."""

    def test_status_info_creation(self) -> None:
        """Test creating StatusInfo."""
        status: FlextWebTypes.StatusInfo = {
            "code": 200,
            "message": "OK",
            "details": "Request processed successfully",
        }

        assert status["code"] == 200
        assert status["message"] == "OK"
        assert status["details"] == "Request processed successfully"

    def test_status_info_error(self) -> None:
        """Test creating StatusInfo for error."""
        status: FlextWebTypes.StatusInfo = {
            "code": 500,
            "message": "Internal Server Error",
            "details": "Database connection failed",
        }

        assert status["code"] == 500
        assert status["message"] == "Internal Server Error"
        assert status["details"] == "Database connection failed"


class TestFactoryMethodEdgeCases:
    """Test factory method edge cases and error handling."""

    def test_create_app_data_edge_values(self) -> None:
        """Test creating app data with edge values."""
        app_data = FlextWebTypes.create_app_data(
            app_id="", name="", host="", port=0, status="", is_running=False
        )

        # Should handle empty values
        assert app_data["id"] == ""
        assert app_data["name"] == ""
        assert app_data["port"] == 0

    def test_create_config_data_boundary_values(self) -> None:
        """Test creating config data with boundary values."""
        config = FlextWebTypes.create_config_data(
            host="a" * 255,  # Very long hostname
            port=65535,  # Max port
            debug=False,
            secret_key="x" * 32,  # Long secret
            app_name="y" * 100,  # Long app name
        )

        assert len(config["host"]) == 255
        assert config["port"] == 65535
        assert len(config["secret_key"]) == 32

    def test_validation_method_exception_handling(self) -> None:
        """Test validation methods handle exceptions gracefully."""
        # Pass invalid data that might cause validation to raise
        invalid_data = "not a dict"

        # Should not raise exception, should return failure result
        result = FlextWebTypes.validate_app_data(invalid_data)
        assert result.is_failure
