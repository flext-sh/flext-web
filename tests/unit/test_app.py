"""Comprehensive unit tests for flext_web.app module.

Tests the unified FlextWebApp class following flext standards.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient
from flext_tests import tm

from flext_web import FlextWebApp, FlextWebSettings
from tests import c, m


class TestFlextWebApp:
    """Test suite for FlextWebApp unified class."""

    def test_app_initialization(self) -> None:
        """Test FlextWebApp initialization."""
        app = FlextWebApp()
        tm.that(hasattr(app, "execute"), eq=True)
        tm.that(callable(app.execute), eq=True)

    def test_app_factory_initialization(self) -> None:
        """Test FlextWebApp.FastAPIFactory initialization."""
        factory = FlextWebApp.FastAPIFactory()
        tm.that(hasattr(factory, "create_instance"), eq=True)
        tm.that(callable(factory.create_instance), eq=True)

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
        tm.ok(result)
        app = result.value
        tm.that(hasattr(app, "title"), eq=True)
        tm.that(hasattr(app, "version"), eq=True)
        tm.that(hasattr(app, "get"), eq=True)

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
        tm.ok(result)
        app = result.value
        tm.that(app.title, eq="Valid Test API")
        tm.that(hasattr(app, "get"), eq=True)

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
        tm.ok(result)
        app = result.value
        tm.that(app.title, eq="Real Test API")
        tm.that(app.version, eq="1.0.0")
        tm.that(hasattr(app, "get"), eq=True)
        tm.that(hasattr(app, "post"), eq=True)

    def test_create_fastapi_app_success(self) -> None:
        """Test create_fastapi_app with success - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(
            title="Test API", version="1.0.0", description="Test Description"
        )
        result = FlextWebApp.create_fastapi_app(config)
        tm.ok(result)
        app = result.value
        tm.that(app.title, eq="Test API")
        tm.that(app.version, eq="1.0.0")
        tm.that(hasattr(app, "get"), eq=True)

    def test_create_fastapi_app_with_custom_config(self) -> None:
        """Test create_fastapi_app with custom configuration - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(
            title="Custom Test API",
            version="2.0.0",
            description=c.Web.WebApi.DEFAULT_DESCRIPTION,
        )
        result = FlextWebApp.create_fastapi_app(config)
        tm.ok(result)
        app = result.value
        tm.that(app.title, eq="Custom Test API")
        tm.that(app.version, eq="2.0.0")
        tm.that(hasattr(app, "get"), eq=True)

    def test_create_fastapi_app_with_none_config(self) -> None:
        """Test create_fastapi_app with None config uses defaults - REAL FastAPI."""
        result = FlextWebApp.create_fastapi_app(None)
        tm.ok(result)
        app = result.value
        tm.that(hasattr(app, "title"), eq=True)
        tm.that(hasattr(app, "version"), eq=True)
        tm.that(hasattr(app, "get"), eq=True)

    def test_create_fastapi_app_health_check_registration(self) -> None:
        """Test create_fastapi_app health check registration - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(title="Test API", version="1.0.0")
        result = FlextWebApp.create_fastapi_app(config)
        tm.ok(result)
        app = result.value
        client = TestClient(app)
        response = client.get("/health")
        tm.that(response.status_code, eq=200)
        health_data = response.json()
        tm.that(health_data, has="status")
        tm.that(health_data, has="service")
        tm.that(health_data, has="timestamp")

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
        tm.ok(result)
        app = result.value
        tm.that(app.title, eq="Test API")
        tm.that(app.version, eq="1.0.0")
        tm.that(hasattr(app, "openapi_url"), eq=True)

    def test_create_fastapi_app_with_default_description(self) -> None:
        """Test create_fastapi_app with default description from Constants - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(title="Test API", version="1.0.0")
        result = FlextWebApp.create_fastapi_app(config)
        tm.ok(result)
        app = result.value
        tm.that(app.title, eq="Test API")
        tm.that(app.version, eq="1.0.0")
        tm.that(app.description, eq=c.Web.WebApi.DEFAULT_DESCRIPTION)

    def test_app_inheritance(self) -> None:
        """Test FlextWebApp inheritance from FlextService."""
        app = FlextWebApp()
        tm.that(hasattr(app, "execute"), eq=True)
        tm.that(callable(app.execute), eq=True)
        result = app.execute()
        tm.ok(result)

    def test_app_static_methods(self) -> None:
        """Test FlextWebApp static methods."""
        tm.that(hasattr(FlextWebApp, "create_fastapi_app"), eq=True)
        tm.that(callable(FlextWebApp.create_fastapi_app), eq=True)

    def test_app_error_handling(self) -> None:
        """Test FlextWebApp error handling - REAL FastAPI."""
        result = FlextWebApp.create_fastapi_app(None)
        tm.ok(result)
        app = result.value
        tm.that(hasattr(app, "title"), eq=True)
        tm.that(hasattr(app, "version"), eq=True)

    def test_app_integration_patterns(self) -> None:
        """Test FlextWebApp integration patterns - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(title="Test API", version="1.0.0")
        result = FlextWebApp.create_fastapi_app(config)
        tm.that(hasattr(result, "is_success"), eq=True)
        tm.that(hasattr(result, "value"), eq=True)
        tm.that(hasattr(result, "error"), eq=True)
        tm.ok(result)
        app = result.value
        tm.that(hasattr(app, "title"), eq=True)

    def test_app_logging_integration(self) -> None:
        """Test FlextWebApp logging integration - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(title="Test API", version="1.0.0")
        result = FlextWebApp.create_fastapi_app(config)
        tm.ok(result)
        app = result.value
        tm.that(hasattr(app, "title"), eq=True)

    def test_app_fastapi_integration(self) -> None:
        """Test FlextWebApp FastAPI integration - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(
            title="Test API", version="1.0.0", description="Test Description"
        )
        result = FlextWebApp.create_fastapi_app(config)
        tm.ok(result)
        app = result.value
        tm.that(app, is_=FastAPI)
        tm.that(app.title, eq="Test API")

    def test_app_health_check_endpoint(self) -> None:
        """Test FlextWebApp health check endpoint registration - REAL FastAPI."""
        config = m.Web.FastAPIAppConfig(title="Test API", version="1.0.0")
        result = FlextWebApp.create_fastapi_app(config)
        tm.ok(result)
        app = result.value
        client = TestClient(app)
        response = client.get("/health")
        tm.that(response.status_code, eq=200)
        health_data = response.json()
        tm.that(health_data, has="status")
        tm.that(health_data, has="service")

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
        tm.ok(result)
        app = result.value
        tm.that(app.title, eq="Custom API")
        tm.that(app.version, eq="2.0.0")
        tm.that(app.description, eq="Custom Description")

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
        tm.ok(result)
        app = result.value
        tm.that(app.title, eq="Override Title")
        tm.that(app.version, eq="1.0.0")
        tm.that(app.description, eq=c.Web.WebApi.DEFAULT_DESCRIPTION)

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
        tm.ok(result)
        app = result.value
        tm.that(app.title, eq="Test API")
        tm.that(app.version, eq="1.0.0")
        tm.that(app.description, eq=c.Web.WebApi.DEFAULT_DESCRIPTION)

    def test_create_flask_app_success(self) -> None:
        """Test create_flask_app with success."""
        config = FlextWebSettings(secret_key=c.Web.WebDefaults.TEST_SECRET_KEY)
        result = FlextWebApp.create_flask_app(config)
        tm.ok(result)
        tm.that(hasattr(result, "value"), eq=True)
        tm.that(result.value, none=False)
        tm.that(hasattr(result.value, "route"), eq=True)

    def test_create_flask_app_with_none_config(self) -> None:
        """Test create_flask_app with None config uses defaults."""
        result = FlextWebApp.create_flask_app(None)
        tm.ok(result)
        tm.that(hasattr(result, "value"), eq=True)
        tm.that(result.value, none=False)
        tm.that(hasattr(result.value, "route"), eq=True)

    def test_configure_middleware(self) -> None:
        """Test configure_middleware method."""
        app = FastAPI()
        config = FlextWebSettings()
        result = FlextWebApp.configure_middleware(app, config)
        tm.ok(result)
        tm.that(result.value is True, eq=True)

    def test_configure_routes(self) -> None:
        """Test configure_routes method."""
        app = FastAPI()
        config = FlextWebSettings()
        result = FlextWebApp.configure_routes(app, config)
        tm.ok(result)
        tm.that(result.value is True, eq=True)

    def test_configure_error_handlers(self) -> None:
        """Test configure_error_handlers method."""
        app = FastAPI()
        result = FlextWebApp.configure_error_handlers(app)
        tm.ok(result)
        tm.that(result.value is True, eq=True)

    def test_health_handler_create_handler(self) -> None:
        """Test HealthHandler.create_handler method."""
        handler_func = FlextWebApp.HealthHandler.create_handler()
        tm.that(callable(handler_func), eq=True)
        result = handler_func()
        tm.that(result, has="status")
        tm.that(result, has="service")
        tm.that(result, has="timestamp")

    def test_info_handler_create_handler(self) -> None:
        """Test InfoHandler.create_handler method - REAL execution."""
        config = m.Web.FastAPIAppConfig(
            title="Test API", version="1.0.0", description="Test Description"
        )
        handler_func = FlextWebApp.InfoHandler.create_handler(config)
        tm.that(callable(handler_func), eq=True)
        result = handler_func()
        tm.that(result, has="service")
        tm.that(result, has="title")
        tm.that(result, has="version")
        tm.that(result, has="description")
        tm.that(result, has="debug")
        tm.that(result, has="timestamp")
        tm.that(result["title"], eq="Test API")
        tm.that(result["version"], eq="1.0.0")

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
        tm.ok(app_result)
        app = app_result.value
        configured_app = FlextWebApp._configure_fastapi_endpoints(app, config)
        client = TestClient(configured_app)
        health_response = client.get("/health")
        tm.that(health_response.status_code, eq=200)
        info_response = client.get("/info")
        tm.that(info_response.status_code, eq=200)
        info_data = info_response.json()
        tm.that(info_data, has="service")
        tm.that(info_data, has="title")
        tm.that(info_data["title"], eq="Test API")

    def test_create_flask_app_health_endpoint_real(self) -> None:
        """Test create_flask_app health endpoint - REAL Flask app."""
        config = FlextWebSettings(secret_key=c.Web.WebDefaults.TEST_SECRET_KEY)
        result = FlextWebApp.create_flask_app(config)
        tm.ok(result)
        app = result.value
        tm.that(app, none=False)
        app.config["TESTING"] = True
        test_cli = app.test_client()
        response = test_cli.get("/health")
        tm.that(response.status_code, eq=200)
        health_json = response.get_json()
        tm.that(health_json, none=False)
        tm.that(health_json, has="status")
        tm.that(health_json, has="service")
        tm.that(health_json["status"], eq=c.Web.WebResponse.STATUS_HEALTHY)

    def test_validate_business_rules(self) -> None:
        """Test validate_business_rules method (line 352)."""
        app = FlextWebApp()
        result = app.validate_business_rules()
        tm.ok(result)
        tm.that(result.value is True, eq=True)
