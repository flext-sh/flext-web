"""Comprehensive tests for FLEXT Web Interface legacy compatibility layer.

Tests all legacy functionality and backward compatibility patterns to achieve
complete coverage of the legacy module.
"""

from __future__ import annotations

import warnings

import pytest

import flext_web.legacy as legacy_module
from flext_web.legacy import (
    AppStatus,
    FlaskApp,
    FlaskService,
    WebApp,
    WebAppHandler,
    WebAuthenticationError,
    WebConfig,
    WebConfigurationError,
    WebConnectionError,
    WebError,
    WebMiddlewareError,
    WebRoutingError,
    WebService,
    WebSessionError,
    WebTemplateError,
    WebValidationError,
    create_flask_app,
    create_web_service,
    get_web_config,
    reset_config,
)


class TestLegacyWebConfig:
    """Test legacy WebConfig functionality."""

    def test_web_config_creation(self) -> None:
        """Test WebConfig can be created with deprecation warning."""
        with pytest.warns(DeprecationWarning, match="WebConfig is deprecated"):
            config = WebConfig()
        assert config is not None

    def test_web_config_with_parameters(self) -> None:
        """Test WebConfig with parameters."""
        with pytest.warns(DeprecationWarning, match="WebConfig is deprecated"):
            config = WebConfig(host="0.0.0.0", port=9000, debug=False)
        assert config.host == "0.0.0.0"
        assert config.port == 9000
        assert config.debug is False


class TestLegacyWebService:
    """Test legacy WebService functionality."""

    def test_web_service_creation(self) -> None:
        """Test WebService can be created with deprecation warning."""
        with pytest.warns(DeprecationWarning, match="WebConfig is deprecated"):
            config = WebConfig()

        with pytest.warns(DeprecationWarning, match="WebService is deprecated"):
            service = WebService(config)
        assert service is not None

    def test_flask_service_alias(self) -> None:
        """Test FlaskService alias functionality."""
        with pytest.warns(DeprecationWarning, match="WebConfig is deprecated"):
            config = WebConfig()

        with pytest.warns(DeprecationWarning, match="FlaskService is deprecated"):
            service = FlaskService(config)
        assert service is not None


class TestLegacyWebApp:
    """Test legacy WebApp functionality."""

    def test_web_app_creation(self) -> None:
        """Test WebApp can be created with deprecation warning."""
        with pytest.warns(DeprecationWarning, match="WebApp is deprecated"):
            app = WebApp(id="app_test-app", name="test-app")
        assert app.name == "test-app"

    def test_web_app_handler_creation(self) -> None:
        """Test WebAppHandler can be created with deprecation warning."""
        with pytest.warns(DeprecationWarning, match="WebAppHandler is deprecated"):
            handler = WebAppHandler()
        assert handler is not None

    def test_app_status_creation(self) -> None:
        """Test AppStatus can be created with deprecation warning."""
        with pytest.warns(DeprecationWarning, match="AppStatus is deprecated"):
            status = AppStatus("running")
        assert status.value == "running"


class TestLegacyExceptions:
    """Test legacy exception functionality."""

    def test_web_error_creation(self) -> None:
        """Test WebError can be created with deprecation warning."""
        with pytest.warns(DeprecationWarning, match="WebError is deprecated"):
            error = WebError("Test error")
        assert "Test error" in str(error)

    def test_web_validation_error_creation(self) -> None:
        """Test WebValidationError can be created with deprecation warning."""
        with pytest.warns(DeprecationWarning, match="WebValidationError is deprecated"):
            error = WebValidationError("Validation failed")
        assert "Validation failed" in str(error)

    def test_web_configuration_error_creation(self) -> None:
        """Test WebConfigurationError can be created with deprecation warning."""
        with pytest.warns(
            DeprecationWarning, match="WebConfigurationError is deprecated"
        ):
            error = WebConfigurationError("Config error")
        assert "Config error" in str(error)

    def test_web_connection_error_creation(self) -> None:
        """Test WebConnectionError can be created with deprecation warning."""
        with pytest.warns(DeprecationWarning, match="WebConnectionError is deprecated"):
            error = WebConnectionError("Connection failed")
        assert "Connection failed" in str(error)

    def test_web_authentication_error_creation(self) -> None:
        """Test WebAuthenticationError can be created with deprecation warning."""
        with pytest.warns(
            DeprecationWarning, match="WebAuthenticationError is deprecated"
        ):
            error = WebAuthenticationError("Auth failed")
        assert "Auth failed" in str(error)

    def test_web_template_error_creation(self) -> None:
        """Test WebTemplateError can be created with deprecation warning."""
        with pytest.warns(DeprecationWarning, match="WebTemplateError is deprecated"):
            error = WebTemplateError("Template error")
        assert "Template error" in str(error)

    def test_web_routing_error_creation(self) -> None:
        """Test WebRoutingError can be created with deprecation warning."""
        with pytest.warns(DeprecationWarning, match="WebRoutingError is deprecated"):
            error = WebRoutingError("Routing error")
        assert "Routing error" in str(error)

    def test_web_session_error_creation(self) -> None:
        """Test WebSessionError can be created with deprecation warning."""
        with pytest.warns(DeprecationWarning, match="WebSessionError is deprecated"):
            error = WebSessionError("Session error")
        assert "Session error" in str(error)

    def test_web_middleware_error_creation(self) -> None:
        """Test WebMiddlewareError can be created with deprecation warning."""
        with pytest.warns(DeprecationWarning, match="WebMiddlewareError is deprecated"):
            error = WebMiddlewareError("Middleware error")
        assert "Middleware error" in str(error)


class TestLegacyFunctions:
    """Test legacy function functionality."""

    def test_get_web_config(self) -> None:
        """Test get_web_config function with deprecation warning."""
        with pytest.warns(DeprecationWarning, match="get_web_config is deprecated"):
            config = get_web_config()
        assert config is not None

    def test_create_web_service(self) -> None:
        """Test create_web_service function with deprecation warning."""
        with pytest.warns(DeprecationWarning, match="create_web_service is deprecated"):
            service = create_web_service()
        assert service is not None

    def test_create_flask_app(self) -> None:
        """Test create_flask_app function with deprecation warning."""
        with pytest.warns(DeprecationWarning, match="create_flask_app is deprecated"):
            app = create_flask_app()
        assert app is not None

    def test_flask_app_alias(self) -> None:
        """Test FlaskApp function with deprecation warning."""
        with pytest.warns(DeprecationWarning, match="FlaskApp is deprecated"):
            app = FlaskApp()
        assert app is not None

    def test_reset_config(self) -> None:
        """Test reset_config function with deprecation warning."""
        with pytest.warns(DeprecationWarning, match="reset_config is deprecated"):
            reset_config()


class TestLegacyErrorHandling:
    """Test legacy error handling patterns."""

    def test_exceptions_with_none_message(self) -> None:
        """Test legacy exceptions handle None messages."""
        with pytest.warns(DeprecationWarning, match="WebError is deprecated"):
            error = WebError(None)
        assert "Legacy error" in str(error)

        with pytest.warns(DeprecationWarning, match="WebValidationError is deprecated"):
            error = WebValidationError(None)
        assert "Legacy validation error" in str(error)

    def test_exceptions_with_empty_message(self) -> None:
        """Test legacy exceptions handle empty messages."""
        with pytest.warns(DeprecationWarning, match="WebError is deprecated"):
            error = WebError("")
        # Should fall back to default message
        assert "Legacy error" in str(error)


class TestLegacyCompatibilityPatterns:
    """Test legacy compatibility patterns and edge cases."""

    def test_deprecation_warnings(self) -> None:
        """Test all legacy items issue deprecation warnings."""
        # Test that each legacy function/class issues a warning
        with pytest.warns(DeprecationWarning, match="WebConfig is deprecated"):
            WebConfig()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")  # Ignore config warning
            config = WebConfig()
        with pytest.warns(DeprecationWarning, match="WebService is deprecated"):
            WebService(config)

        with pytest.warns(DeprecationWarning, match="get_web_config is deprecated"):
            get_web_config()

    def test_legacy_integration_patterns(self) -> None:
        """Test legacy components work together."""
        # Suppress warnings for this integration test
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            config = WebConfig()
            service = WebService(config)
            app = WebApp(id="app_legacy-app", name="legacy-app")
            handler = WebAppHandler()

            # Should all be valid objects
            assert config is not None
            assert service is not None
            assert app is not None
            assert handler is not None
            assert app.name == "legacy-app"

    def test_legacy_function_parameters(self) -> None:
        """Test legacy functions handle parameters."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            # Test create_web_service with config
            config = WebConfig()
            service = create_web_service(config)
            assert service is not None

            # Test create_flask_app with config
            app = create_flask_app(config)
            assert app is not None

    def test_legacy_exception_inheritance(self) -> None:
        """Test legacy exceptions maintain proper inheritance."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            error = WebError("Test")
            validation_error = WebValidationError("Validation")

            # Should be proper exception instances
            assert isinstance(error, Exception)
            assert isinstance(validation_error, Exception)

    def test_module_all_exports(self) -> None:
        """Test module __all__ exports are complete."""
        # Test that __all__ is defined
        assert hasattr(legacy_module, "__all__")
        assert isinstance(legacy_module.__all__, list)

        # Test that all listed exports are actually available
        for export_name in legacy_module.__all__:
            assert hasattr(legacy_module, export_name)

    def test_legacy_arg_type_handling(self) -> None:
        """Test legacy functions handle various argument types."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            # Should handle None config
            service = create_web_service(None)
            assert service is not None

            app = create_flask_app(None)
            assert app is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
