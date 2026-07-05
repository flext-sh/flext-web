"""Unit tests for flext_web settings."""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_web import FlextWebSettings, c


class TestsFlextWebSettings:
    """Test suite for FlextWebSettings."""

    def setup_method(self) -> None:
        FlextWebSettings.reset_for_testing()

    def test_default_settings(self) -> None:
        """Default settings are valid."""
        settings = FlextWebSettings()
        tm.that(settings.app_name, eq=c.Web.DEFAULT_APP_NAME)
        tm.that(settings.host, eq=c.Web.DEFAULT_HOST)
        tm.that(settings.port, eq=c.Web.DEFAULT_PORT)

    def test_host_validator_rejects_empty(self) -> None:
        """Host validator rejects empty strings."""
        with pytest.raises(c.ValidationError):
            _ = FlextWebSettings(host="   ")

    def test_port_validator_rejects_out_of_range(self) -> None:
        """Port validator rejects out-of-range values."""
        with pytest.raises(c.ValidationError):
            _ = FlextWebSettings(port=70000)

    def test_port_validator_classmethod_error(self) -> None:
        """Port validator classmethod raises ValueError with expected message."""
        with pytest.raises(ValueError, match="Port must be between"):
            FlextWebSettings.validate_port(0)

    def test_secret_key_validator_rejects_empty(self) -> None:
        """Secret key validator rejects empty strings."""
        with pytest.raises(c.ValidationError):
            _ = FlextWebSettings(secret_key="   ")

    def test_secret_key_validator_classmethod_error(self) -> None:
        """Secret key validator classmethod raises ValueError with expected message."""
        with pytest.raises(ValueError, match="Secret key cannot be empty"):
            FlextWebSettings.validate_secret_key("   ")

    def test_optional_path_normalization(self) -> None:
        """Optional SSL paths normalize empty strings to None."""
        settings = FlextWebSettings(ssl_cert_path="  ", ssl_key_path=None)
        tm.that(settings.ssl_cert_path, eq=None)
        tm.that(settings.ssl_key_path, eq=None)

    def test_debug_flags_synchronization(self) -> None:
        """Debug flags are synchronized by model validator."""
        settings = FlextWebSettings(debug_mode=True)
        tm.that(settings.debug is True, eq=True)
        tm.that(settings.debug_mode is True, eq=True)

    def test_protocol_computed_field(self) -> None:
        """Protocol field reflects TLS configuration."""
        http_settings = FlextWebSettings(ssl_enabled=False)
        tm.that(http_settings.protocol, eq=c.Web.DEFAULT_HTTP_PROTOCOL)
        https_settings = FlextWebSettings(ssl_enabled=True)
        tm.that(https_settings.protocol, eq=c.Web.DEFAULT_HTTPS_PROTOCOL)

    def test_base_url_computed_field(self) -> None:
        """Base URL combines protocol, host, and port."""
        settings = FlextWebSettings(host="localhost", port=8080)
        tm.that(settings.base_url, eq="http://localhost:8080")

    def test_create_web_config_success(self) -> None:
        """create_web_config applies overrides and validates."""
        result = FlextWebSettings.create_web_config(
            host="127.0.0.1",
            port=9090,
            debug=True,
            secret_key="a" * 32,
        )
        tm.ok(result)
        tm.that(result.value.host, eq="127.0.0.1")
        tm.that(result.value.port, eq=9090)
        tm.that(result.value.debug is True, eq=True)

    def test_create_web_config_failure(self) -> None:
        """create_web_config returns failure for invalid overrides."""
        result = FlextWebSettings.create_web_config(port=0)
        tm.fail(result)
        tm.that(result.error, none=False)

    def test_validate_settings_success(self) -> None:
        """validate_settings succeeds for a valid instance."""
        settings = FlextWebSettings()
        result = FlextWebSettings.validate_settings(settings)
        tm.ok(result)
        tm.that(result.value is True, eq=True)

    def test_validate_settings_failure(self) -> None:
        """validate_settings fails for an invalid instance."""
        settings = FlextWebSettings.model_construct(port=0)
        result = FlextWebSettings.validate_settings(settings)
        tm.fail(result)
        tm.that(result.error, none=False)
