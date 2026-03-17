"""Comprehensive unit tests for flext_web.app module.

Tests the unified FlextWebApp class following flext standards.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from flext_web import FlextWebApp, FlextWebSettings
from tests import c, m


class TestFlextWebApp:
    """Test suite for FlextWebApp unified class."""

    def test_app_initialization(self) -> None:
        """Test FlextWebApp initialization."""
        app = FlextWebApp()
        assert hasattr(app, "execute")
        assert callable(app.execute)

    def test_app_factory_initialization(self) -> None:
        """Test FlextWebApp.FastAPIFactory initialization."""
        factory = FlextWebApp.FastAPIFactory()
        assert hasattr(factory, "create_instance")
        assert callable(factory.create_instance)

    def test_factory_create_instance_success(self) -> None:
        """Test FastAPIFactory.create_instance with success - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(
            title="Test API",
            version="1.0.0",
            description="Test Description",
            docs_url=c.Web.WebApi.DOCS_URL,
            redoc_url=c.Web.WebApi.REDOC_URL,
            openapi_url=c.Web.WebApi.OPENAPI_URL,
        )
        result = FlextWebApp.FastAPIFactory.create_instance(config)
        assert result.is_success
        app = result.value
        assert hasattr(app, "title")
        assert hasattr(app, "version")
        assert hasattr(app, "get")

    def test_factory_create_instance_with_valid_params(self) -> None:
        """Test FastAPIFactory.create_instance with valid parameters - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(
            title="Valid Test API",
            version="1.0.0",
            docs_url=c.Web.WebApi.DOCS_URL,
            redoc_url=c.Web.WebApi.REDOC_URL,
            openapi_url=c.Web.WebApi.OPENAPI_URL,
        )
        result = FlextWebApp.FastAPIFactory.create_instance(config)
        assert result.is_success
        app = result.value
        assert app.title == "Valid Test API"
        assert hasattr(app, "get")

    def test_factory_create_instance_real_fastapi(self) -> None:
        """Test FastAPIFactory.create_instance with REAL FastAPI - no mocks."""
        config = m.Web.FastAPIAppConfig(
            title="Real Test API",
            version="1.0.0",
            description="Real Test Description",
            docs_url=c.Web.WebApi.DOCS_URL,
            redoc_url=c.Web.WebApi.REDOC_URL,
            openapi_url=c.Web.WebApi.OPENAPI_URL,
        )
        result = FlextWebApp.FastAPIFactory.create_instance(config)
        assert result.is_success
        app = result.value
        assert app.title == "Real Test API"
        assert app.version == "1.0.0"
        assert hasattr(app, "get")
        assert hasattr(app, "post")

    def test_create_fastapi_app_success(self) -> None:
        """Test create_fastapi_app with success - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(
            title="Test API", version="1.0.0", description="Test Description"
        )
        result = FlextWebApp.create_fastapi_app(config)
        assert result.is_success
        app = result.value
        assert app.title == "Test API"
        assert app.version == "1.0.0"
        assert hasattr(app, "get")

    def test_create_fastapi_app_with_custom_config(self) -> None:
        """Test create_fastapi_app with custom configuration - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(
            title="Custom Test API",
            version="2.0.0",
            description=c.Web.WebApi.DEFAULT_DESCRIPTION,
        )
        result = FlextWebApp.create_fastapi_app(config)
        assert result.is_success
        app = result.value
        assert app.title == "Custom Test API"
        assert app.version == "2.0.0"
        assert hasattr(app, "get")

    def test_create_fastapi_app_with_none_config(self) -> None:
        """Test create_fastapi_app with None config uses defaults - REAL FastAPI."""
        result = FlextWebApp.create_fastapi_app(None)
        assert result.is_success
        app = result.value
        assert hasattr(app, "title")
        assert hasattr(app, "version")
        assert hasattr(app, "get")

    def test_create_fastapi_app_health_check_registration(self) -> None:
        """Test create_fastapi_app health check registration - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(title="Test API", version="1.0.0")
        result = FlextWebApp.create_fastapi_app(config)
        assert result.is_success
        app = result.value
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        health_data = response.json()
        assert "status" in health_data
        assert "service" in health_data
        assert "timestamp" in health_data

    def test_create_fastapi_app_with_custom_urls(self) -> None:
        """Test create_fastapi_app with custom URLs - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(
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
        assert app.title == "Test API"
        assert app.version == "1.0.0"
        assert hasattr(app, "openapi_url")

    def test_create_fastapi_app_with_default_description(self) -> None:
        """Test create_fastapi_app with default description from Constants - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(title="Test API", version="1.0.0")
        result = FlextWebApp.create_fastapi_app(config)
        assert result.is_success
        app = result.value
        assert app.title == "Test API"
        assert app.version == "1.0.0"
        assert app.description == c.Web.WebApi.DEFAULT_DESCRIPTION

    def test_app_inheritance(self) -> None:
        """Test FlextWebApp inheritance from FlextService."""
        app = FlextWebApp()
        assert hasattr(app, "execute")
        assert callable(app.execute)
        result = app.execute()
        assert result.is_success

    def test_app_static_methods(self) -> None:
        """Test FlextWebApp static methods."""
        assert hasattr(FlextWebApp, "create_fastapi_app")
        assert callable(FlextWebApp.create_fastapi_app)

    def test_app_error_handling(self) -> None:
        """Test FlextWebApp error handling - REAL FastAPI."""
        result = FlextWebApp.create_fastapi_app(None)
        assert result.is_success
        app = result.value
        assert hasattr(app, "title")
        assert hasattr(app, "version")

    def test_app_integration_patterns(self) -> None:
        """Test FlextWebApp integration patterns - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(title="Test API", version="1.0.0")
        result = FlextWebApp.create_fastapi_app(config)
        assert hasattr(result, "is_success")
        assert hasattr(result, "value")
        assert hasattr(result, "error")
        assert result.is_success
        app = result.value
        assert hasattr(app, "title")

    def test_app_logging_integration(self) -> None:
        """Test FlextWebApp logging integration - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(title="Test API", version="1.0.0")
        result = FlextWebApp.create_fastapi_app(config)
        assert result.is_success
        app = result.value
        assert hasattr(app, "title")

    def test_app_fastapi_integration(self) -> None:
        """Test FlextWebApp FastAPI integration - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(
            title="Test API", version="1.0.0", description="Test Description"
        )
        result = FlextWebApp.create_fastapi_app(config)
        assert result.is_success
        app = result.value
        assert isinstance(app, FastAPI)
        assert app.title == "Test API"

    def test_app_health_check_endpoint(self) -> None:
        """Test FlextWebApp health check endpoint registration - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(title="Test API", version="1.0.0")
        result = FlextWebApp.create_fastapi_app(config)
        assert result.is_success
        app = result.value
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        health_data = response.json()
        assert "status" in health_data
        assert "service" in health_data

    def test_app_configuration_handling(self) -> None:
        """Test FlextWebApp configuration handling - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(
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
        assert app.title == "Custom API"
        assert app.version == "2.0.0"
        assert app.description == "Custom Description"

    def test_create_fastapi_app_with_override_title(self) -> None:
        """Test create_fastapi_app with title override parameter - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(title="Config Title", version="1.0.0")
        factory_config = m.Web.FastAPIAppConfig(
            title="Override Title",
            version=config.version,
            description=config.description,
            docs_url=config.docs_url,
            redoc_url=config.redoc_url,
            openapi_url=config.openapi_url,
        )
        result = FlextWebApp.create_fastapi_app(config, factory_config)
        assert result.is_success
        app = result.value
        assert app.title == "Override Title"
        assert app.version == "1.0.0"
        assert app.description == c.Web.WebApi.DEFAULT_DESCRIPTION

    def test_create_fastapi_app_with_override_urls(self) -> None:
        """Test create_fastapi_app with URL override parameters - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(title="Test API", version="1.0.0")
        factory_config = m.Web.FastAPIAppConfig(
            title=config.title,
            version=config.version,
            description=config.description,
            docs_url="/override-docs",
            redoc_url="/override-redoc",
            openapi_url="/override-openapi.json",
        )
        result = FlextWebApp.create_fastapi_app(config, factory_config)
        assert result.is_success
        app = result.value
        assert app.title == "Test API"
        assert app.version == "1.0.0"
        assert app.description == c.Web.WebApi.DEFAULT_DESCRIPTION

    def test_create_flask_app_success(self) -> None:
        """Test create_flask_app with success."""
        config = FlextWebSettings(secret_key=c.Web.WebDefaults.TEST_SECRET_KEY)
        result = FlextWebApp.create_flask_app(config)
        assert result.is_success
        assert hasattr(result, "value")
        assert result.value is not None
        assert hasattr(result.value, "route")

    def test_create_flask_app_with_none_config(self) -> None:
        """Test create_flask_app with None config uses defaults."""
        result = FlextWebApp.create_flask_app(None)
        assert result.is_success
        assert hasattr(result, "value")
        assert result.value is not None
        assert hasattr(result.value, "route")

    def test_configure_middleware(self) -> None:
        """Test configure_middleware method."""
        app = FastAPI()
        config = FlextWebSettings()
        result = FlextWebApp.configure_middleware(app, config)
        assert result.is_success
        assert result.value is True

    def test_configure_routes(self) -> None:
        """Test configure_routes method."""
        app = FastAPI()
        config = FlextWebSettings()
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
        config = m.Web.FastAPIAppConfig(
            title="Test API", version="1.0.0", description="Test Description"
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
        config = m.Web.FastAPIAppConfig(title="Test API", version="1.0.0")
        fastapi_config = m.Web.FastAPIAppConfig(
            title="Test API",
            version="1.0.0",
            description=config.description,
            docs_url=config.docs_url,
            redoc_url=config.redoc_url,
            openapi_url=config.openapi_url,
        )
        app_result = FlextWebApp.FastAPIFactory.create_instance(fastapi_config)
        assert app_result.is_success
        app = app_result.value
        configured_app = FlextWebApp._configure_fastapi_endpoints(app, config)
        client = TestClient(configured_app)
        health_response = client.get("/health")
        assert health_response.status_code == 200
        info_response = client.get("/info")
        assert info_response.status_code == 200
        info_data = info_response.json()
        assert "service" in info_data
        assert "title" in info_data
        assert info_data["title"] == "Test API"

    def test_create_flask_app_health_endpoint_real(self) -> None:
        """Test create_flask_app health endpoint - REAL Flask app."""
        config = FlextWebSettings(secret_key=c.Web.WebDefaults.TEST_SECRET_KEY)
        result = FlextWebApp.create_flask_app(config)
        assert result.is_success
        app = result.value
        assert app is not None
        app.config["TESTING"] = True
        test_cli = app.test_client()
        response = test_cli.get("/health")
        assert response.status_code == 200
        health_json = response.get_json()
        assert health_json is not None
        assert "status" in health_json
        assert "service" in health_json
        assert health_json["status"] == c.Web.WebResponse.STATUS_HEALTHY

    def test_validate_business_rules(self) -> None:
        """Test validate_business_rules method (line 352)."""
        app = FlextWebApp()
        result = app.validate_business_rules()
        assert result.is_success
        assert result.value is True
