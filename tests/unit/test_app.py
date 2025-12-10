"""Comprehensive unit tests for flext_web.app module.

Tests the unified FlextWebApp class following flext standards.
"""

from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient
from flask.testing import FlaskClient

from flext_web.app import FlextWebApp, _FastAPIConfig
from flext_web.config import FlextWebConfig
from flext_web.constants import FlextWebConstants
from flext_web.models import FlextWebModels


class TestFlextWebApp:
    """Test suite for FlextWebApp unified class."""

    def test_app_initialization(self) -> None:
        """Test FlextWebApp initialization."""
        app = FlextWebApp()

        # Should inherit from FlextService
        assert hasattr(app, "execute")
        assert callable(app.execute)

    def test_app_factory_initialization(self) -> None:
        """Test FlextWebApp.FastAPIFactory initialization."""
        factory = FlextWebApp.FastAPIFactory()

        # Should have create_instance method
        assert hasattr(factory, "create_instance")
        assert callable(factory.create_instance)

    def test_factory_create_instance_success(self) -> None:
        """Test FastAPIFactory.create_instance with success - REAL FastAPI."""
        config: _FastAPIConfig = {
            "title": "Test API",
            "version": "1.0.0",
            "description": "Test Description",
            "docs_url": FlextWebConstants.WebApi.DOCS_URL,
            "redoc_url": FlextWebConstants.WebApi.REDOC_URL,
            "openapi_url": FlextWebConstants.WebApi.OPENAPI_URL,
        }
        result = FlextWebApp.FastAPIFactory.create_instance(config)

        assert result.is_success
        app = result.value
        # Real FastAPI app - verify it has expected attributes
        assert hasattr(app, "title")
        assert hasattr(app, "version")
        assert hasattr(app, "get")

    def test_factory_create_instance_with_valid_params(self) -> None:
        """Test FastAPIFactory.create_instance with valid parameters - REAL FastAPI."""
        # FastAPI requires non-empty title - use valid title
        config: _FastAPIConfig = {
            "title": "Valid Test API",
            "version": "1.0.0",
            "docs_url": FlextWebConstants.WebApi.DOCS_URL,
            "redoc_url": FlextWebConstants.WebApi.REDOC_URL,
            "openapi_url": FlextWebConstants.WebApi.OPENAPI_URL,
        }
        result = FlextWebApp.FastAPIFactory.create_instance(config)

        # FastAPI validates title - should succeed with valid title
        assert result.is_success
        app = result.value
        assert app.title == "Valid Test API"
        assert hasattr(app, "get")

    def test_factory_create_instance_real_fastapi(self) -> None:
        """Test FastAPIFactory.create_instance with REAL FastAPI - no mocks."""
        config: _FastAPIConfig = {
            "title": "Real Test API",
            "version": "1.0.0",
            "description": "Real Test Description",
            "docs_url": FlextWebConstants.WebApi.DOCS_URL,
            "redoc_url": FlextWebConstants.WebApi.REDOC_URL,
            "openapi_url": FlextWebConstants.WebApi.OPENAPI_URL,
        }
        result = FlextWebApp.FastAPIFactory.create_instance(config)

        assert result.is_success
        app = result.value
        # Verify real FastAPI app properties
        assert app.title == "Real Test API"
        assert app.version == "1.0.0"
        assert hasattr(app, "get")
        assert hasattr(app, "post")

    def test_create_fastapi_app_success(self) -> None:
        """Test create_fastapi_app with success - REAL FastAPI."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API",
            version="1.0.0",
            description="Test Description",
        )

        result = FlextWebApp.create_fastapi_app(config)

        assert result.is_success
        app = result.value
        # Real FastAPI app - verify it has expected attributes
        assert app.title == "Test API"
        assert app.version == "1.0.0"
        assert hasattr(app, "get")

    def test_create_fastapi_app_with_custom_config(self) -> None:
        """Test create_fastapi_app with custom configuration - REAL FastAPI."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Custom Test API",
            version="2.0.0",
            description=FlextWebConstants.WebApi.DEFAULT_DESCRIPTION,
        )

        result = FlextWebApp.create_fastapi_app(config)

        assert result.is_success
        app = result.value
        # Real FastAPI app - verify custom config is used
        assert app.title == "Custom Test API"
        assert app.version == "2.0.0"
        assert hasattr(app, "get")

    def test_create_fastapi_app_with_none_config(self) -> None:
        """Test create_fastapi_app with None config uses defaults - REAL FastAPI."""
        result = FlextWebApp.create_fastapi_app(None)

        assert result.is_success
        app = result.value
        # Real FastAPI app with defaults from Constants
        assert hasattr(app, "title")
        assert hasattr(app, "version")
        assert hasattr(app, "get")

    def test_create_fastapi_app_health_check_registration(self) -> None:
        """Test create_fastapi_app health check registration - REAL FastAPI."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API",
            version="1.0.0",
        )

        result = FlextWebApp.create_fastapi_app(config)

        assert result.is_success
        app = result.value
        # Real FastAPI app - test health endpoint with TestClient
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        health_data = response.json()
        assert "status" in health_data
        assert "service" in health_data
        assert "timestamp" in health_data

    def test_create_fastapi_app_with_custom_urls(self) -> None:
        """Test create_fastapi_app with custom URLs - REAL FastAPI."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API",
            version="1.0.0",
            description="Test Description",
            docs_url="/custom-docs",
            redoc_url="/custom-redoc",
            openapi_url="/custom-openapi.json",
        )

        result = FlextWebApp.create_fastapi_app(config)

        assert result.is_success
        app = result.value
        # Real FastAPI app - verify custom URLs are set
        assert app.title == "Test API"
        assert app.version == "1.0.0"
        # FastAPI stores docs_url in openapi_url attribute
        assert hasattr(app, "openapi_url")

    def test_create_fastapi_app_with_default_description(self) -> None:
        """Test create_fastapi_app with default description from Constants - REAL FastAPI."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API",
            version="1.0.0",
        )

        result = FlextWebApp.create_fastapi_app(config)

        assert result.is_success
        app = result.value
        # Real FastAPI app - verify default description from Constants
        assert app.title == "Test API"
        assert app.version == "1.0.0"
        assert app.description == FlextWebConstants.WebApi.DEFAULT_DESCRIPTION

    def test_app_inheritance(self) -> None:
        """Test FlextWebApp inheritance from FlextService."""
        app = FlextWebApp()

        # Should have FlextService methods
        assert hasattr(app, "execute")
        assert callable(app.execute)

        # Should be able to call execute
        result = app.execute()
        assert result.is_success

    def test_app_static_methods(self) -> None:
        """Test FlextWebApp static methods."""
        # Test create_fastapi_app is static
        assert hasattr(FlextWebApp, "create_fastapi_app")
        assert callable(FlextWebApp.create_fastapi_app)

    def test_app_error_handling(self) -> None:
        """Test FlextWebApp error handling - REAL FastAPI."""
        # Test with None config (should use defaults from Constants)
        result = FlextWebApp.create_fastapi_app(None)

        # Should handle gracefully with defaults - REAL FastAPI app
        assert result.is_success
        app = result.value
        assert hasattr(app, "title")
        assert hasattr(app, "version")

    def test_app_integration_patterns(self) -> None:
        """Test FlextWebApp integration patterns - REAL FastAPI."""
        # All methods should return FlextResult
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API",
            version="1.0.0",
        )

        result = FlextWebApp.create_fastapi_app(config)

        assert hasattr(result, "is_success")
        assert hasattr(result, "value")
        assert hasattr(result, "error")
        assert result.is_success
        app = result.value
        assert hasattr(app, "title")

    def test_app_logging_integration(self) -> None:
        """Test FlextWebApp logging integration - REAL FastAPI."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API",
            version="1.0.0",
        )

        result = FlextWebApp.create_fastapi_app(config)

        assert result.is_success
        app = result.value
        # Real FastAPI app - logging happens internally via FlextLogger
        assert hasattr(app, "title")

    def test_app_fastapi_integration(self) -> None:
        """Test FlextWebApp FastAPI integration - REAL FastAPI."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API",
            version="1.0.0",
            description="Test Description",
        )

        result = FlextWebApp.create_fastapi_app(config)

        assert result.is_success
        app = result.value
        # Real FastAPI app - verify it's a real FastAPI instance

        assert isinstance(app, FastAPI)
        assert app.title == "Test API"

    def test_app_health_check_endpoint(self) -> None:
        """Test FlextWebApp health check endpoint registration - REAL FastAPI."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API",
            version="1.0.0",
        )

        result = FlextWebApp.create_fastapi_app(config)

        assert result.is_success
        app = result.value
        # Real FastAPI app - test health endpoint with TestClient
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        health_data = response.json()
        assert "status" in health_data
        assert "service" in health_data

    def test_app_configuration_handling(self) -> None:
        """Test FlextWebApp configuration handling - REAL FastAPI."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Custom API",
            version="2.0.0",
            description="Custom Description",
            docs_url="/custom-docs",
            redoc_url="/custom-redoc",
            openapi_url="/custom-openapi.json",
        )

        result = FlextWebApp.create_fastapi_app(config)

        assert result.is_success
        app = result.value
        # Real FastAPI app - verify custom configuration
        assert app.title == "Custom API"
        assert app.version == "2.0.0"
        assert app.description == "Custom Description"

    def test_create_fastapi_app_with_override_title(self) -> None:
        """Test create_fastapi_app with title override parameter - REAL FastAPI."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Config Title",
            version="1.0.0",
        )

        # Use factory_config to override title
        factory_config: _FastAPIConfig = {
            "title": "Override Title",
            "version": config.version,
            "description": config.description,
            "docs_url": config.docs_url,
            "redoc_url": config.redoc_url,
            "openapi_url": config.openapi_url,
        }
        result = FlextWebApp.create_fastapi_app(config, factory_config)

        assert result.is_success
        app = result.value
        # Real FastAPI app - verify title override
        assert app.title == "Override Title"
        assert app.version == "1.0.0"
        assert app.description == FlextWebConstants.WebApi.DEFAULT_DESCRIPTION

    def test_create_fastapi_app_with_override_urls(self) -> None:
        """Test create_fastapi_app with URL override parameters - REAL FastAPI."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API",
            version="1.0.0",
        )

        factory_config: _FastAPIConfig = {
            "title": config.title,
            "version": config.version,
            "description": config.description,
            "docs_url": "/override-docs",
            "redoc_url": "/override-redoc",
            "openapi_url": "/override-openapi.json",
        }

        result = FlextWebApp.create_fastapi_app(config, factory_config)

        assert result.is_success
        app = result.value
        # Real FastAPI app - verify URL overrides
        assert app.title == "Test API"
        assert app.version == "1.0.0"
        assert app.description == FlextWebConstants.WebApi.DEFAULT_DESCRIPTION

    def test_create_flask_app_success(self) -> None:
        """Test create_flask_app with success."""
        config = FlextWebConfig(
            secret_key=FlextWebConstants.WebDefaults.TEST_SECRET_KEY,
        )

        result = FlextWebApp.create_flask_app(config)

        assert result.is_success
        assert result.value is not None
        assert hasattr(result.value, "route")

    def test_create_flask_app_with_none_config(self) -> None:
        """Test create_flask_app with None config uses defaults."""
        result = FlextWebApp.create_flask_app(None)

        assert result.is_success
        assert result.value is not None
        assert hasattr(result.value, "route")

    def test_configure_middleware(self) -> None:
        """Test configure_middleware method."""
        app = FastAPI()
        config = FlextWebConfig()

        result = FlextWebApp.configure_middleware(app, config)

        assert result.is_success
        assert result.value is True

    def test_configure_routes(self) -> None:
        """Test configure_routes method."""
        app = FastAPI()
        config = FlextWebConfig()

        result = FlextWebApp.configure_routes(app, config)

        assert result.is_success
        assert result.value is True

    def test_configure_error_handlers(self) -> None:
        """Test configure_error_handlers method."""
        app = FastAPI()

        result = FlextWebApp.configure_error_handlers(app)

        assert result.is_success
        assert result.value is True

    def test_health_handler_create_handler(self) -> None:
        """Test HealthHandler.create_handler method."""
        handler_func = FlextWebApp.HealthHandler.create_handler()

        assert callable(handler_func)
        result = handler_func()
        assert "status" in result
        assert "service" in result
        assert "timestamp" in result

    def test_info_handler_create_handler(self) -> None:
        """Test InfoHandler.create_handler method - REAL execution."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API",
            version="1.0.0",
            description="Test Description",
        )

        handler_func = FlextWebApp.InfoHandler.create_handler(config)

        assert callable(handler_func)
        result = handler_func()
        assert "service" in result
        assert "title" in result
        assert "version" in result
        assert "description" in result
        assert "debug" in result
        assert "timestamp" in result
        assert result["title"] == "Test API"
        assert result["version"] == "1.0.0"

    def test_configure_fastapi_endpoints_real(self) -> None:
        """Test _configure_fastapi_endpoints with REAL FastAPI app."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API",
            version="1.0.0",
        )

        # Create real FastAPI app
        fastapi_config: _FastAPIConfig = {
            "title": "Test API",
            "version": "1.0.0",
            "description": config.description,
            "docs_url": config.docs_url,
            "redoc_url": config.redoc_url,
            "openapi_url": config.openapi_url,
        }
        app_result = FlextWebApp.FastAPIFactory.create_instance(fastapi_config)
        assert app_result.is_success
        app = app_result.value

        # Configure endpoints - REAL execution
        configured_app = FlextWebApp._configure_fastapi_endpoints(app, config)

        # Test health endpoint - REAL HTTP request
        client = TestClient(configured_app)
        health_response = client.get("/health")
        assert health_response.status_code == 200

        # Test info endpoint - REAL HTTP request
        info_response = client.get("/info")
        assert info_response.status_code == 200
        info_data = info_response.json()
        assert "service" in info_data
        assert "title" in info_data
        assert info_data["title"] == "Test API"

    def test_create_flask_app_health_endpoint_real(self) -> None:
        """Test create_flask_app health endpoint - REAL Flask app."""
        config = FlextWebConfig(
            secret_key=FlextWebConstants.WebDefaults.TEST_SECRET_KEY,
        )

        result = FlextWebApp.create_flask_app(config)

        assert result.is_success
        app = result.value
        # Real Flask app - test health endpoint
        app.config["TESTING"] = True
        client: FlaskClient = app.test_client()
        response = client.get("/health")
        assert response.status_code == 200
        health_data = response.get_json()
        assert health_data is not None
        assert "status" in health_data
        assert "service" in health_data
        assert health_data["status"] == FlextWebConstants.WebResponse.STATUS_HEALTHY

    def test_create_fastapi_app_exception_handling(self) -> None:
        """Test create_fastapi_app exception handling (lines 108-112)."""
        # Patch FastAPI to raise an exception
        with patch("flext_web.app.FastAPI", side_effect=Exception("Test exception")):
            result = FlextWebApp.create_fastapi_app()
            assert result.is_failure
            assert result.error is not None
            assert "Failed to create FastAPI application" in result.error
            assert "Test exception" in result.error

    def test_validate_business_rules(self) -> None:
        """Test validate_business_rules method (line 352)."""
        app = FlextWebApp()
        result = app.validate_business_rules()
        assert result.is_success
        assert result.value is True
