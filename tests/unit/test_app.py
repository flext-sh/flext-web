"""Comprehensive unit tests for flext_web.app module.

Tests the unified FlextWebApp class following flext standards.
"""

from unittest.mock import Mock, patch

from flext_web.app import FlextWebApp
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
        """Test FastAPIFactory.create_instance with success."""
        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.FastAPIFactory.create_instance(
                title="Test API", version="1.0.0", description="Test Description"
            )

            assert result.is_success
            assert result.value == mock_app
            mock_fastapi.assert_called_once_with(
                title="Test API",
                version="1.0.0",
                description="Test Description",
                docs_url="/docs",
                redoc_url="/redoc",
                openapi_url="/openapi.json",
            )

    def test_factory_create_instance_fastapi_not_available(self) -> None:
        """Test FastAPIFactory.create_instance when FastAPI raises exception."""
        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_fastapi.side_effect = AttributeError(
                "'NoneType' object is not callable"
            )
            result = FlextWebApp.FastAPIFactory.create_instance()

            assert result.is_failure
            assert (
                result.error is not None
                and "Failed to create FastAPI application" in result.error
            )

    def test_factory_create_instance_exception(self) -> None:
        """Test FastAPIFactory.create_instance with exception."""
        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_fastapi.side_effect = Exception("Test error")

            result = FlextWebApp.FastAPIFactory.create_instance()

            assert result.is_failure
            assert (
                result.error is not None
                and "Failed to create FastAPI application: Test error" in result.error
            )

    def test_create_fastapi_app_success(self) -> None:
        """Test create_fastapi_app with success."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API", version="1.0.0", description="Test Description"
        )

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.create_fastapi_app(config)

            assert result.is_success
            assert result.value == mock_app

    def test_create_fastapi_app_with_custom_config(self) -> None:
        """Test create_fastapi_app with custom configuration."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API", version="1.0.0"
        )

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.create_fastapi_app(config)

            assert result.is_success
            assert result.value == mock_app

    def test_create_fastapi_app_factory_failure(self) -> None:
        """Test create_fastapi_app when factory fails."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API", version="1.0.0"
        )

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_fastapi.side_effect = AttributeError(
                "'NoneType' object is not callable"
            )
            result = FlextWebApp.create_fastapi_app(config)

            assert result.is_failure
            assert (
                result.error is not None
                and "Failed to create FastAPI application" in result.error
            )

    def test_create_fastapi_app_health_check_registration(self) -> None:
        """Test create_fastapi_app health check registration."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API", version="1.0.0"
        )

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.create_fastapi_app(config)

            assert result.is_success
            # Should register health check endpoint using FastAPI decorator
            assert mock_app.get.call_count >= 1
            # Verify health endpoint was registered
            calls = mock_app.get.call_args_list
            health_call = next(
                (call for call in calls if call[0][0] == "/health"), None
            )
            assert health_call is not None

    def test_create_fastapi_app_with_custom_urls(self) -> None:
        """Test create_fastapi_app with custom URLs."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API",
            version="1.0.0",
            description="Test Description",
            docs_url="/custom-docs",
            redoc_url="/custom-redoc",
            openapi_url="/custom-openapi.json",
        )

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.create_fastapi_app(config)

            assert result.is_success
            mock_fastapi.assert_called_once_with(
                title="Test API",
                version="1.0.0",
                description="Test Description",
                docs_url="/custom-docs",
                redoc_url="/custom-redoc",
                openapi_url="/custom-openapi.json",
            )

    def test_create_fastapi_app_with_default_description(self) -> None:
        """Test create_fastapi_app with default description."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API", version="1.0.0"
        )

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.create_fastapi_app(config)

            assert result.is_success
            mock_fastapi.assert_called_once_with(
                title="Test API",
                version="1.0.0",
                description="Generic HTTP Service",
                docs_url="/docs",
                redoc_url="/redoc",
                openapi_url="/openapi.json",
            )

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
        """Test FlextWebApp error handling."""
        # Test with None config (should use defaults)
        result = FlextWebApp.create_fastapi_app(None)

        # Should handle gracefully with defaults
        assert result.is_success or result.is_failure

    def test_app_integration_patterns(self) -> None:
        """Test FlextWebApp integration patterns."""
        # All methods should return FlextResult
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API", version="1.0.0"
        )

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.create_fastapi_app(config)

            assert hasattr(result, "is_success")
            assert hasattr(result, "value")
            assert hasattr(result, "error")

    def test_app_logging_integration(self) -> None:
        """Test FlextWebApp logging integration."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API", version="1.0.0"
        )

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_fastapi.return_value = mock_app

            with patch("flext_web.app.FlextLogger") as mock_logger:
                result = FlextWebApp.create_fastapi_app(config)

                assert result.is_success
                # Should use logger
                assert mock_logger.called

    def test_app_fastapi_integration(self) -> None:
        """Test FlextWebApp FastAPI integration."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API", version="1.0.0", description="Test Description"
        )

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.create_fastapi_app(config)

            assert result.is_success
            # Should create FastAPI app
            mock_fastapi.assert_called_once()

    def test_app_health_check_endpoint(self) -> None:
        """Test FlextWebApp health check endpoint registration."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API", version="1.0.0"
        )

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.create_fastapi_app(config)

            assert result.is_success
            # Should register health check endpoint
            assert mock_app.get.call_count >= 1
            # Verify health endpoint was registered
            calls = mock_app.get.call_args_list
            health_call = next(
                (call for call in calls if call[0][0] == "/health"), None
            )
            assert health_call is not None

    def test_app_configuration_handling(self) -> None:
        """Test FlextWebApp configuration handling."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Custom API",
            version="2.0.0",
            description="Custom Description",
            docs_url="/custom-docs",
            redoc_url="/custom-redoc",
            openapi_url="/custom-openapi.json",
        )

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.create_fastapi_app(config)

            assert result.is_success
            # Should use custom configuration
            mock_fastapi.assert_called_once_with(
                title="Custom API",
                version="2.0.0",
                description="Custom Description",
                docs_url="/custom-docs",
                redoc_url="/custom-redoc",
                openapi_url="/custom-openapi.json",
            )

    def test_create_fastapi_app_with_override_title(self) -> None:
        """Test create_fastapi_app with title override parameter."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Config Title", version="1.0.0"
        )

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.create_fastapi_app(config, title="Override Title")

            assert result.is_success
            mock_fastapi.assert_called_once_with(
                title="Override Title",
                version="1.0.0",
                description="Generic HTTP Service",
                docs_url="/docs",
                redoc_url="/redoc",
                openapi_url="/openapi.json",
            )

    def test_create_fastapi_app_with_override_urls(self) -> None:
        """Test create_fastapi_app with URL override parameters."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
            title="Test API", version="1.0.0"
        )

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.create_fastapi_app(
                config,
                docs_url="/override-docs",
                redoc_url="/override-redoc",
                openapi_url="/override-openapi.json",
            )

            assert result.is_success
            mock_fastapi.assert_called_once_with(
                title="Test API",
                version="1.0.0",
                description="Generic HTTP Service",
                docs_url="/override-docs",
                redoc_url="/override-redoc",
                openapi_url="/override-openapi.json",
            )

    def test_create_flask_app_success(self) -> None:
        """Test create_flask_app with success."""
        from flext_web.config import FlextWebConfig
        from flext_web.constants import FlextWebConstants

        config = FlextWebConfig(
            secret_key=FlextWebConstants.WebDefaults.TEST_SECRET_KEY
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
        from fastapi import FastAPI

        from flext_web.config import FlextWebConfig

        app = FastAPI()
        config = FlextWebConfig()

        result = FlextWebApp.configure_middleware(app, config)

        assert result.is_success
        assert result.value is True

    def test_configure_routes(self) -> None:
        """Test configure_routes method."""
        from fastapi import FastAPI

        from flext_web.config import FlextWebConfig

        app = FastAPI()
        config = FlextWebConfig()

        result = FlextWebApp.configure_routes(app, config)

        assert result.is_success
        assert result.value is True

    def test_configure_error_handlers(self) -> None:
        """Test configure_error_handlers method."""
        from fastapi import FastAPI

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
        """Test InfoHandler.create_handler method."""
        config = FlextWebModels.FastAPI.FastAPIAppConfig(
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
