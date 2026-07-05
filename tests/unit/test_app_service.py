"""Unit tests for flext_web application service."""

from __future__ import annotations

from flext_tests import tm

from flext_web import FlextWebApp, FlextWebSettings, c, m


class TestsFlextWebApp:
    """Test suite for FlextWebApp."""

    def setup_method(self) -> None:
        FlextWebSettings.reset_for_testing()

    def test_execute(self) -> None:
        """App service execute returns success."""
        service = FlextWebApp()
        result = service.execute()
        tm.ok(result)
        tm.that(result.value is True, eq=True)

    def test_fastapi_factory_create_instance(self) -> None:
        """FastAPI factory creates an application instance."""
        result = FlextWebApp.FastAPIFactory.create_instance()
        tm.ok(result)
        tm.that(result.value.title, eq="FastAPI")

    def test_create_fastapi_app_with_defaults(self) -> None:
        """Service creates a FastAPI app using default settings."""
        service = FlextWebApp()
        result = service.create_fastapi_app()
        tm.ok(result)
        tm.that(result.value.title, eq=FlextWebSettings().app_name)

    def test_create_fastapi_app_with_custom_config(self) -> None:
        """Service creates a FastAPI app with custom config."""
        service = FlextWebApp()
        config = m.Web.FastAPIAppConfig(title="Custom App", version="2.0.0")
        result = service.create_fastapi_app(settings=config)
        tm.ok(result)
        tm.that(result.value.title, eq="Custom App")

    def test_create_flask_app(self) -> None:
        """Service creates a Flask app."""
        service = FlextWebApp()
        settings = FlextWebSettings(app_name="flask-test")
        result = service.create_flask_app(settings=settings)
        tm.ok(result)
        tm.that(result.value.name, eq="flask-test")

    def test_configure_error_handlers(self) -> None:
        """Error handler configuration returns success."""
        service = FlextWebApp()
        fastapi_result = service.create_fastapi_app()
        tm.ok(fastapi_result)
        result = service.configure_fastapi_error_handlers(fastapi_result.value)
        tm.ok(result)
        tm.that(result.value is True, eq=True)

    def test_configure_middleware(self) -> None:
        """Middleware configuration returns success."""
        service = FlextWebApp()
        fastapi_result = service.create_fastapi_app()
        tm.ok(fastapi_result)
        result = service.configure_fastapi_middleware(fastapi_result.value)
        tm.ok(result)
        tm.that(result.value is True, eq=True)

    def test_configure_routes(self) -> None:
        """Routes configuration returns success."""
        service = FlextWebApp()
        fastapi_result = service.create_fastapi_app()
        tm.ok(fastapi_result)
        result = service.configure_fastapi_routes(fastapi_result.value)
        tm.ok(result)
        tm.that(result.value is True, eq=True)

    def test_health_handler(self) -> None:
        """Health handler returns a healthy payload."""
        handler = FlextWebApp.HealthHandler.create_handler()
        payload = handler()
        tm.that(payload, has="status")
        tm.that(payload["status"], eq=c.Web.ResponseStatus.HEALTHY.value)

    def test_info_handler(self) -> None:
        """Info handler returns metadata payload."""
        config = m.Web.FastAPIAppConfig(title="Info App", version="1.0.0")
        handler = FlextWebApp.InfoHandler.create_handler(config)
        payload = handler()
        tm.that(payload, has="title")
        tm.that(payload["title"], eq="Info App")

    def test_validate_business_rules(self) -> None:
        """App service validates business rules."""
        service = FlextWebApp()
        result = service.validate_business_rules()
        tm.ok(result)
        tm.that(result.value is True, eq=True)
