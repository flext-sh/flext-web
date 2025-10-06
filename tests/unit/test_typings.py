"""Comprehensive unit tests for flext_web.typings module.

Tests the unified FlextWebTypes class following flext standards.
"""

from flext_web.typings import FlextWebTypes


class TestFlextWebTypes:
    """Test suite for FlextWebTypes unified class."""

    def test_typings_inheritance(self) -> None:
        """Test that FlextWebTypes inherits from FlextTypes."""
        # Should have access to base FlextTypes
        assert hasattr(FlextWebTypes, "Dict")
        assert hasattr(FlextWebTypes, "List")
        assert hasattr(FlextWebTypes, "StringDict")
        assert hasattr(FlextWebTypes, "JsonValue")
        assert hasattr(FlextWebTypes, "ConfigValue")

    def test_core_web_types(self) -> None:
        """Test Core web types."""
        # Test WebResponse type
        assert hasattr(FlextWebTypes.Core, "WebResponse")
        assert hasattr(FlextWebTypes.Core, "JsonResponse")
        assert hasattr(FlextWebTypes.Core, "SuccessResponse")
        assert hasattr(FlextWebTypes.Core, "BaseResponse")
        assert hasattr(FlextWebTypes.Core, "ErrorResponse")
        assert hasattr(FlextWebTypes.Core, "ResponseDataDict")
        assert hasattr(FlextWebTypes.Core, "ConfigData")
        assert hasattr(FlextWebTypes.Core, "ProductionConfigData")
        assert hasattr(FlextWebTypes.Core, "DevelopmentConfigData")
        assert hasattr(FlextWebTypes.Core, "StatusInfo")
        assert hasattr(FlextWebTypes.Core, "AppData")
        assert hasattr(FlextWebTypes.Core, "RequestContext")

    def test_application_types(self) -> None:
        """Test Application types."""
        # Test application configuration types
        assert hasattr(FlextWebTypes.Application, "ApplicationConfiguration")
        assert hasattr(FlextWebTypes.Application, "ApplicationMetadata")
        assert hasattr(FlextWebTypes.Application, "ApplicationLifecycle")
        assert hasattr(FlextWebTypes.Application, "ApplicationSecurity")
        assert hasattr(FlextWebTypes.Application, "ApplicationMiddleware")
        assert hasattr(FlextWebTypes.Application, "ApplicationRouting")

    def test_request_response_types(self) -> None:
        """Test RequestResponse types."""
        # Test request/response types
        assert hasattr(FlextWebTypes.RequestResponse, "RequestConfiguration")
        assert hasattr(FlextWebTypes.RequestResponse, "RequestHeaders")
        assert hasattr(FlextWebTypes.RequestResponse, "RequestParameters")
        assert hasattr(FlextWebTypes.RequestResponse, "RequestBody")
        assert hasattr(FlextWebTypes.RequestResponse, "ResponseConfiguration")
        assert hasattr(FlextWebTypes.RequestResponse, "ResponseHeaders")
        assert hasattr(FlextWebTypes.RequestResponse, "ResponseBody")

    def test_web_service_types(self) -> None:
        """Test WebService types."""
        # Test web service types
        assert hasattr(FlextWebTypes.WebService, "ServiceConfiguration")
        assert hasattr(FlextWebTypes.WebService, "ServiceRegistration")
        assert hasattr(FlextWebTypes.WebService, "ServiceDiscovery")
        assert hasattr(FlextWebTypes.WebService, "ServiceHealth")
        assert hasattr(FlextWebTypes.WebService, "ServiceMetrics")
        assert hasattr(FlextWebTypes.WebService, "ServiceDeployment")

    def test_security_types(self) -> None:
        """Test Security types."""
        # Test security types
        assert hasattr(FlextWebTypes.Security, "SecurityConfiguration")
        assert hasattr(FlextWebTypes.Security, "AuthenticationConfig")
        assert hasattr(FlextWebTypes.Security, "AuthorizationPolicy")
        assert hasattr(FlextWebTypes.Security, "CorsConfiguration")
        assert hasattr(FlextWebTypes.Security, "CsrfProtection")
        assert hasattr(FlextWebTypes.Security, "SecurityHeaders")

    def test_api_endpoint_types(self) -> None:
        """Test ApiEndpoint types."""
        # Test API endpoint types
        assert hasattr(FlextWebTypes.ApiEndpoint, "EndpointConfiguration")
        assert hasattr(FlextWebTypes.ApiEndpoint, "EndpointValidation")
        assert hasattr(FlextWebTypes.ApiEndpoint, "EndpointDocumentation")
        assert hasattr(FlextWebTypes.ApiEndpoint, "RouteConfiguration")
        assert hasattr(FlextWebTypes.ApiEndpoint, "ApiVersioning")
        assert hasattr(FlextWebTypes.ApiEndpoint, "RateLimiting")

    def test_app_data_dataclass(self) -> None:
        """Test AppData dataclass."""
        # Test AppData creation
        app_data = FlextWebTypes.AppData(
            id="test-id",
            name="test-app",
            host="localhost",
            port=8080,
            status="running",
            is_running=True,
        )

        assert app_data.id == "test-id"
        assert app_data.name == "test-app"
        assert app_data.host == "localhost"
        assert app_data.port == 8080
        assert app_data.status == "running"
        assert app_data.is_running is True

    def test_app_data_optional_fields(self) -> None:
        """Test AppData optional fields."""
        app_data = FlextWebTypes.AppData(
            id="test-id",
            name="test-app",
            host="localhost",
            port=8080,
            status="running",
            is_running=True,
            created_at="2025-01-01T00:00:00Z",
            updated_at="2025-01-01T00:00:00Z",
            description="Test app",
            environment="development",
            debug_mode=True,
        )

        assert app_data.created_at == "2025-01-01T00:00:00Z"
        assert app_data.updated_at == "2025-01-01T00:00:00Z"
        assert app_data.description == "Test app"
        assert app_data.environment == "development"
        assert app_data.debug_mode is True

    def test_health_response_dataclass(self) -> None:
        """Test HealthResponse dataclass."""
        health_response = FlextWebTypes.HealthResponse(
            status="healthy",
            service="test-service",
            version="1.0.0",
            applications=5,
            timestamp="2025-01-01T00:00:00Z",
            service_id="test-service-123",
        )

        assert health_response.status == "healthy"
        assert health_response.service == "test-service"
        assert health_response.version == "1.0.0"
        assert health_response.applications == 5
        assert health_response.timestamp == "2025-01-01T00:00:00Z"
        assert health_response.service_id == "test-service-123"

    def test_health_response_optional_fields(self) -> None:
        """Test HealthResponse optional fields."""
        health_response = FlextWebTypes.HealthResponse(
            status="healthy",
            service="test-service",
            version="1.0.0",
            applications=5,
            timestamp="2025-01-01T00:00:00Z",
            service_id="test-service-123",
            created_at="2025-01-01T00:00:00Z",
        )

        assert health_response.created_at == "2025-01-01T00:00:00Z"

    def test_request_context_dataclass(self) -> None:
        """Test RequestContext dataclass."""
        request_context = FlextWebTypes.RequestContext(
            method="GET",
            path="/api/test",
            headers={"Content-Type": "application/json"},
            query_params={"param1": "value1"},
            body='{"key": "value"}',
            client_ip="127.0.0.1",
        )

        assert request_context.method == "GET"
        assert request_context.path == "/api/test"
        assert request_context.headers == {"Content-Type": "application/json"}
        assert request_context.query_params == {"param1": "value1"}
        assert request_context.body == '{"key": "value"}'
        assert request_context.client_ip == "127.0.0.1"

    def test_request_context_optional_fields(self) -> None:
        """Test RequestContext optional fields."""
        request_context = FlextWebTypes.RequestContext(
            method="GET",
            path="/api/test",
            headers={"Content-Type": "application/json"},
            query_params={"param1": "value1"},
        )

        assert request_context.body is None
        assert request_context.client_ip is None

    def test_project_types(self) -> None:
        """Test Project types."""
        # Test project type literals
        assert hasattr(FlextWebTypes.Project, "WebProjectType")
        assert hasattr(FlextWebTypes.Project, "WebProjectConfig")
        assert hasattr(FlextWebTypes.Project, "FlaskProjectConfig")
        assert hasattr(FlextWebTypes.Project, "ApiProjectConfig")
        assert hasattr(FlextWebTypes.Project, "SecurityProjectConfig")

    def test_configure_web_types_system(self) -> None:
        """Test configure_web_types_system method."""
        config = {"enable_strict_typing": True, "enable_runtime_validation": True}
        result = FlextWebTypes.configure_web_types_system(config)

        assert result.is_success
        assert result.value["enable_strict_typing"] is True
        assert result.value["enable_runtime_validation"] is True

    def test_configure_web_types_system_invalid_config(self) -> None:
        """Test configure_web_types_system with invalid config."""
        result = FlextWebTypes.configure_web_types_system("invalid")

        assert result.is_failure
        assert "Failed to configure web types system" in result.error

    def test_get_web_types_system_config(self) -> None:
        """Test get_web_types_system_config method."""
        result = FlextWebTypes.get_web_types_system_config()

        assert result.is_success
        config = result.value
        assert "enable_strict_typing" in config
        assert "enable_runtime_validation" in config
        assert "total_type_definitions" in config
        assert "factory_methods" in config

    def test_create_app_data(self) -> None:
        """Test create_app_data method."""
        data = FlextWebTypes.create_app_data(
            id="test-id", name="test-app", host="localhost", port=8080
        )

        assert isinstance(data, dict)
        assert data["id"] == "test-id"
        assert data["name"] == "test-app"
        assert data["host"] == "localhost"
        assert data["port"] == 8080

    def test_create_config_data(self) -> None:
        """Test create_config_data method."""
        data = FlextWebTypes.create_config_data()

        assert isinstance(data, dict)
        assert data == {}

    def test_create_request_context(self) -> None:
        """Test create_request_context method."""
        context = FlextWebTypes.create_request_context(
            method="POST",
            path="/api/test",
            headers={"Content-Type": "application/json"},
            data={"key": "value"},
        )

        assert isinstance(context, dict)
        assert context["method"] == "POST"
        assert context["path"] == "/api/test"
        assert context["headers"] == {"Content-Type": "application/json"}
        assert context["data"] == {"key": "value"}

    def test_create_request_context_defaults(self) -> None:
        """Test create_request_context with defaults."""
        context = FlextWebTypes.create_request_context()

        assert isinstance(context, dict)
        assert context["method"] == "GET"
        assert context["path"] == "/"
        assert context["headers"] == {}
        assert context["data"] == {}

    def test_validate_app_data(self) -> None:
        """Test validate_app_data method."""
        # Test with valid data
        data = {"id": "test-id", "name": "test-app"}
        result = FlextWebTypes.validate_app_data(data)

        assert result.is_success
        assert result.value == data

        # Test with invalid data
        result = FlextWebTypes.validate_app_data("invalid")

        assert result.is_failure
        assert "App data must be a dictionary" in result.error

    def test_validate_config_data(self) -> None:
        """Test validate_config_data method."""
        # Test with valid dict data
        data = {"key": "value"}
        result = FlextWebTypes.validate_config_data(data)

        assert result.is_success
        assert result.value == data

        # Test with invalid string data
        result = FlextWebTypes.validate_config_data("invalid")

        assert result.is_failure
        assert "Config data must be a dictionary" in result.error

    def test_type_consistency(self) -> None:
        """Test that types are consistent."""
        # All types should be properly defined
        type_categories = [
            FlextWebTypes.Core,
            FlextWebTypes.Application,
            FlextWebTypes.RequestResponse,
            FlextWebTypes.WebService,
            FlextWebTypes.Security,
            FlextWebTypes.ApiEndpoint,
        ]

        for category in type_categories:
            assert hasattr(category, "__dict__")
            # Should have some type definitions
            assert len(category.__dict__) > 0

    def test_dataclass_functionality(self) -> None:
        """Test dataclass functionality."""
        # AppData should work as a dictionary
        app_data = FlextWebTypes.AppData(
            id="test-id",
            name="test-app",
            host="localhost",
            port=8080,
            status="running",
            is_running=True,
        )

        # Should be able to access as dict
        assert app_data["id"] == "test-id"
        assert app_data["name"] == "test-app"
        assert app_data["host"] == "localhost"
        assert app_data["port"] == 8080
        assert app_data["status"] == "running"
        assert app_data["is_running"] is True

    def test_type_annotations(self) -> None:
        """Test that types have proper annotations."""
        # Test that type annotations are available
        assert hasattr(FlextWebTypes.Core, "WebResponse")
        assert hasattr(FlextWebTypes.Core, "JsonResponse")
        assert hasattr(FlextWebTypes.Application, "ApplicationConfiguration")
        assert hasattr(FlextWebTypes.RequestResponse, "RequestConfiguration")

    def test_inheritance_chain(self) -> None:
        """Test that FlextWebTypes properly inherits from FlextTypes."""
        # Should have access to base types
        assert hasattr(FlextWebTypes, "Dict")
        assert hasattr(FlextWebTypes, "List")
        assert hasattr(FlextWebTypes, "StringDict")
        assert hasattr(FlextWebTypes, "JsonValue")
        assert hasattr(FlextWebTypes, "ConfigValue")
        assert hasattr(FlextWebTypes, "NestedDict")

    def test_web_specific_extensions(self) -> None:
        """Test that web-specific types extend base types appropriately."""
        # Web-specific types should not conflict with base types
        assert FlextWebTypes.Core.WebResponse != FlextWebTypes.Dict
        assert FlextWebTypes.Core.JsonResponse != FlextWebTypes.JsonValue

    def test_type_usage_patterns(self) -> None:
        """Test that types follow expected usage patterns."""

        # Types should be usable in type hints
        def process_app_data(
            data: FlextWebTypes.AppData,
        ) -> FlextWebTypes.Core.ResponseDict:
            return {"processed": True, "data": data}

        app_data = FlextWebTypes.AppData(
            id="test-id",
            name="test-app",
            host="localhost",
            port=8080,
            status="running",
            is_running=True,
        )

        result = process_app_data(app_data)
        assert isinstance(result, dict)
        assert result["processed"] is True
        assert result["data"] == app_data
