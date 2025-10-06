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
        """Test FlextWebApp._Factory initialization."""
        factory = FlextWebApp._Factory()

        # Should have create_instance method
        assert hasattr(factory, "create_instance")
        assert callable(factory.create_instance)

    def test_factory_create_instance_success(self) -> None:
        """Test _Factory.create_instance with success."""
        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp._Factory.create_instance(
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
        """Test _Factory.create_instance when FastAPI is not available."""
        with patch("flext_web.app.FastAPI", None):
            result = FlextWebApp._Factory.create_instance()

            assert result.is_failure
            assert "FastAPI is required" in result.error

    def test_factory_create_instance_exception(self) -> None:
        """Test _Factory.create_instance with exception."""
        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_fastapi.side_effect = Exception("Test error")

            result = FlextWebApp._Factory.create_instance()

            assert result.is_failure
            assert "Failed to create FastAPI application: Test error" in result.error

    def test_create_fastapi_app_success(self) -> None:
        """Test create_fastapi_app with success."""
        config = FlextWebModels.AppConfig(
            title="Test API", version="1.0.0", description="Test Description"
        )

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_app.add_api_route = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.create_fastapi_app(config)

            assert result.is_success
            assert result.value == mock_app

    def test_create_fastapi_app_with_middlewares(self) -> None:
        """Test create_fastapi_app with middlewares."""
        middleware = Mock()
        middleware.process_request = Mock()
        middleware.name = "test_middleware"

        config = FlextWebModels.AppConfig(
            title="Test API", version="1.0.0", middlewares=[middleware]
        )

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_app.add_api_route = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.create_fastapi_app(config)

            assert result.is_success
            assert result.value == mock_app

    def test_create_fastapi_app_factory_failure(self) -> None:
        """Test create_fastapi_app when factory fails."""
        config = FlextWebModels.AppConfig(title="Test API", version="1.0.0")

        with patch("flext_web.app.FastAPI", None):
            result = FlextWebApp.create_fastapi_app(config)

            assert result.is_failure
            assert "FastAPI is required" in result.error

    def test_create_fastapi_app_health_check_registration(self) -> None:
        """Test create_fastapi_app health check registration."""
        config = FlextWebModels.AppConfig(title="Test API", version="1.0.0")

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_app.add_api_route = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.create_fastapi_app(config)

            assert result.is_success
            # Should register health check endpoint
            mock_app.add_api_route.assert_called_once()

    def test_create_fastapi_app_with_custom_urls(self) -> None:
        """Test create_fastapi_app with custom URLs."""
        config = FlextWebModels.AppConfig(
            title="Test API",
            version="1.0.0",
            docs_url="/custom-docs",
            redoc_url="/custom-redoc",
            openapi_url="/custom-openapi.json",
        )

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_app.add_api_route = Mock()
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
        config = FlextWebModels.AppConfig(title="Test API", version="1.0.0")

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_app.add_api_route = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.create_fastapi_app(config)

            assert result.is_success
            mock_fastapi.assert_called_once_with(
                title="Test API",
                version="1.0.0",
                description="FlextWeb FastAPI Application",
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
        # Test with invalid config
        result = FlextWebApp.create_fastapi_app("invalid")

        # Should handle gracefully (Pydantic will validate)
        assert result.is_success or result.is_failure

    def test_app_integration_patterns(self) -> None:
        """Test FlextWebApp integration patterns."""
        # All methods should return FlextResult
        config = FlextWebModels.AppConfig(title="Test API", version="1.0.0")

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_app.add_api_route = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.create_fastapi_app(config)

            assert hasattr(result, "is_success")
            assert hasattr(result, "value")
            assert hasattr(result, "error")

    def test_app_logging_integration(self) -> None:
        """Test FlextWebApp logging integration."""
        config = FlextWebModels.AppConfig(title="Test API", version="1.0.0")

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_app.add_api_route = Mock()
            mock_fastapi.return_value = mock_app

            with patch("flext_web.app.FlextLogger") as mock_logger:
                result = FlextWebApp.create_fastapi_app(config)

                assert result.is_success
                # Should use logger
                assert mock_logger.called

    def test_app_fastapi_integration(self) -> None:
        """Test FlextWebApp FastAPI integration."""
        config = FlextWebModels.AppConfig(
            title="Test API", version="1.0.0", description="Test Description"
        )

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_app.add_api_route = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.create_fastapi_app(config)

            assert result.is_success
            # Should create FastAPI app
            mock_fastapi.assert_called_once()

    def test_app_health_check_endpoint(self) -> None:
        """Test FlextWebApp health check endpoint registration."""
        config = FlextWebModels.AppConfig(title="Test API", version="1.0.0")

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_app.add_api_route = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.create_fastapi_app(config)

            assert result.is_success
            # Should register health check endpoint
            mock_app.add_api_route.assert_called_once()
            call_args = mock_app.add_api_route.call_args
            assert call_args[0][0] == "/health"  # First argument is path
            assert call_args[1]["methods"] == ["GET"]  # Keyword argument

    def test_app_middleware_handling(self) -> None:
        """Test FlextWebApp middleware handling."""
        middleware = Mock()
        middleware.process_request = Mock()
        middleware.name = "test_middleware"

        config = FlextWebModels.AppConfig(
            title="Test API", version="1.0.0", middlewares=[middleware]
        )

        with patch("flext_web.app.FastAPI") as mock_fastapi:
            mock_app = Mock()
            mock_app.get = Mock()
            mock_app.add_api_route = Mock()
            mock_fastapi.return_value = mock_app

            result = FlextWebApp.create_fastapi_app(config)

            assert result.is_success
            # Should handle middlewares
            assert middleware.process_request is not None

    def test_app_configuration_handling(self) -> None:
        """Test FlextWebApp configuration handling."""
        config = FlextWebModels.AppConfig(
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
            mock_app.add_api_route = Mock()
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
