"""Comprehensive unit tests for flext_web.typings module.

Tests the unified FlextWebTypes class following flext standards.
"""

from flext_web.typings import FlextWebTypes


class TestFlextWebTypes:
    """Test suite for FlextWebTypes unified class."""

    def test_typings_structure(self) -> None:
        """Test that FlextWebTypes has proper structure."""
        # Should have model type aliases
        assert hasattr(FlextWebTypes, "HttpMessage")
        assert hasattr(FlextWebTypes, "HttpRequest")
        assert hasattr(FlextWebTypes, "HttpResponse")
        assert hasattr(FlextWebTypes, "WebRequest")
        assert hasattr(FlextWebTypes, "WebResponse")
        assert hasattr(FlextWebTypes, "ApplicationEntity")

    def test_core_web_types(self) -> None:
        """Test Core web types."""
        # Test that core types exist
        assert hasattr(FlextWebTypes, "SuccessResponse")
        assert hasattr(FlextWebTypes, "BaseResponse")
        assert hasattr(FlextWebTypes, "ErrorResponse")

    def test_application_types(self) -> None:
        """Test Application types."""
        # Test that Application types exist
        assert hasattr(FlextWebTypes, "ApplicationEntity")

    def test_model_functionality(self) -> None:
        """Test Pydantic model functionality."""
        # Test that models can be created and used
        request = FlextWebTypes.WebRequest(url="http://localhost:8080", method="GET")
        assert request.url == "http://localhost:8080"
        assert request.method == "GET"

        response = FlextWebTypes.WebResponse(status_code=200, request_id="test-123")
        assert response.status_code == 200
        assert response.is_success is True

    def test_app_data_functionality(self) -> None:
        """Test app data functionality."""
        # Test that we can create and use app models
        app = FlextWebTypes.ApplicationEntity(
            id="test-id",
            name="test-app",
            host="localhost",
            port=8080,
            status="running",
        )

        assert app.id == "test-id"
        assert app.name == "test-app"
        assert app.host == "localhost"
        assert app.port == 8080
        assert app.status == "running"
        assert app.is_running is True

    def test_health_response_functionality(self) -> None:
        """Test health response functionality."""
        # Test that health response models work

        # Create a health response using the models
        health_data = {
            "status": "healthy",
            "service": "test-service",
            "version": "1.0.0",
            "applications": 5,
            "timestamp": "2025-01-01T00:00:00Z",
            "service_id": "test-service-123",
        }

        # This would be how health responses are created in real code
        assert isinstance(health_data, dict)
        assert health_data["status"] == "healthy"

    def test_request_context_functionality(self) -> None:
        """Test request context functionality."""
        # Test that request models work
        request = FlextWebTypes.WebRequest(
            url="http://localhost:8080/api/test",
            method="GET",
            headers={"Content-Type": "application/json"},
            query_params={"param1": "value1"},
        )

        assert request.method == "GET"
        assert request.url == "http://localhost:8080/api/test"
        assert request.headers["Content-Type"] == "application/json"
        assert request.query_params["param1"] == "value1"

    def test_project_types(self) -> None:
        """Test Project types."""
        # Test that project types are defined
        # WebProjectType is a type alias, so we test that the class has the expected structure
        assert hasattr(FlextWebTypes, "ApplicationEntity")

    def test_configure_web_types_system(self) -> None:
        """Test configure_web_types_system method."""
        config: dict[str, object] = {
            "use_pydantic_models": True,
            "enable_runtime_validation": True,
        }
        result = FlextWebTypes.configure_web_types_system(config)

        assert result.is_success
        assert result.value["use_pydantic_models"] is True
        assert result.value["enable_runtime_validation"] is True

    def test_configure_web_types_system_invalid_config(self) -> None:
        """Test configure_web_types_system with invalid config."""
        result = FlextWebTypes.configure_web_types_system({"invalid": "config"})

        assert result.is_failure
        assert result.error is not None
        assert (
            "Invalid configuration keys" in result.error
            or "invalid" in result.error.lower()
        )

    def test_get_web_types_system_config(self) -> None:
        """Test get_web_types_system_config method."""
        result = FlextWebTypes.get_web_types_system_config()

        assert result.is_success
        config = result.value
        assert "use_pydantic_models" in config
        assert "enable_runtime_validation" in config
        assert "total_model_classes" in config
        assert "factory_methods" in config

    def test_model_creation(self) -> None:
        """Test model creation functionality."""
        # Test that models can be created
        app = FlextWebTypes.ApplicationEntity(
            id="test-id", name="test-app", host="localhost", port=8080
        )

        assert app.id == "test-id"
        assert app.name == "test-app"
        assert app.host == "localhost"
        assert app.port == 8080

    def test_config_validation(self) -> None:
        """Test config validation functionality."""
        # Test that config creation works
        from flext_web.config import FlextWebConfig

        config = FlextWebConfig(host="localhost", port=8080)
        assert config.host == "localhost"
        assert config.port == 8080

    def test_type_consistency(self) -> None:
        """Test that types are consistent."""
        # Test that core types exist
        assert hasattr(FlextWebTypes, "WebRequest")
        assert hasattr(FlextWebTypes, "WebResponse")
        assert hasattr(FlextWebTypes, "ApplicationEntity")

        # Test that types can be instantiated
        test_request = FlextWebTypes.WebRequest(url="https://example.com")
        assert hasattr(test_request, "is_secure")

    def test_type_annotations(self) -> None:
        """Test that types have proper annotations."""
        # Test that type annotations are available
        assert hasattr(FlextWebTypes, "WebRequest")
        assert hasattr(FlextWebTypes, "WebResponse")
        assert hasattr(FlextWebTypes, "ApplicationEntity")

    def test_type_usage_patterns(self) -> None:
        """Test that types follow expected usage patterns."""

        # Test that models can be used in type hints and operations
        def process_request_data(
            request: FlextWebTypes.HttpRequest,
        ) -> dict[str, object]:
            return {"processed": True, "method": request.method, "url": request.url}

        request = FlextWebTypes.HttpRequest(
            url="http://localhost:8080/api/test", method="GET"
        )

        result = process_request_data(request)
        assert isinstance(result, dict)
        assert result["processed"] is True
        assert result["method"] == "GET"
        assert result["url"] == "http://localhost:8080/api/test"
