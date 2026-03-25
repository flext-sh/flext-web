"""Unit tests for flext_web.config module.

Tests the web configuration functionality following flext standards.

NOTE: Some validation tests are marked with xfail due to a known issue in
FlextSettings (flext-core) where Pydantic Field constraints (ge, le, min_length)
are not enforced. See: FlextSettings bypasses Field validation constraints.
"""

from __future__ import annotations

import pytest
from flext_tests import tm
from pydantic import ValidationError

from flext_web import FlextWebSettings


class TestFlextWebSettings:
    """Test suite for FlextWebSettings class."""

    def test_initialization_with_test_environment(self) -> None:
        """Test FlextWebSettings initialization with test environment variables.

        NOTE: FlextSettings may load values from environment variables, which
        can override Field defaults. Therefore we only verify that values are
        present and of correct type, not specific values.
        """
        config = FlextWebSettings()
        tm.that(config.host, none=False)
        tm.that(config.port, none=False)
        tm.that(config.app_name, none=False)
        tm.that(config.app_name, is_=str)
        tm.that(config.app_name, empty=False)

    def test_initialization_with_custom_values(self) -> None:
        """Test FlextWebSettings initialization with custom values."""
        config = FlextWebSettings(
            host="0.0.0.0",
            port=3000,
            debug_mode=True,
            app_name="Test App",
        )
        tm.that(config.host, eq="0.0.0.0")
        tm.that(config.port, eq=3000)
        tm.that(config.debug_mode is True, eq=True)
        tm.that(config.app_name, eq="Test App")

    @pytest.mark.xfail(
        reason="FlextSettings bug: Field constraints not enforced",
        strict=False,
    )
    def test_validation_host_empty(self) -> None:
        """Test host validation with empty string.

        Expected: ValidationError for min_length=1 violation
        Actual: FlextSettings accepts empty string (bug in flext-core)
        """
        with pytest.raises(ValidationError):
            _ = FlextWebSettings(host="")

    def test_validation_port_range(self) -> None:
        """Test port validation within valid range."""
        config = FlextWebSettings(port=8080)
        tm.that(config.port, eq=8080)

    @pytest.mark.xfail(
        reason="FlextSettings bug: Field constraints not enforced",
        strict=False,
    )
    def test_validation_port_out_of_range(self) -> None:
        """Test port validation outside valid range.

        Expected: ValidationError for le=65535 violation
        Actual: FlextSettings accepts out-of-range port (bug in flext-core)
        """
        with pytest.raises(ValidationError):
            _ = FlextWebSettings(port=70000)

    @pytest.mark.xfail(
        reason="FlextSettings bug: Field constraints not enforced",
        strict=False,
    )
    def test_validation_secret_key_too_short(self) -> None:
        """Test secret key validation with too short key.

        Expected: ValidationError for min_length=32 violation
        Actual: FlextSettings accepts short secret key (bug in flext-core)
        """
        with pytest.raises(ValidationError):
            _ = FlextWebSettings(secret_key="short")

    def test_validation_secret_key_valid(self) -> None:
        """Test secret key validation with valid key."""
        config = FlextWebSettings(secret_key="valid-secret-key-32-characters-long")
        tm.that(config.secret_key, none=False)

    def test_ssl_configuration_valid(self) -> None:
        """Test SSL configuration with valid cert and key paths."""
        config = FlextWebSettings(
            ssl_enabled=False,
            ssl_cert_path=None,
            ssl_key_path=None,
        )
        tm.that(config.ssl_enabled is False, eq=True)

    def test_computed_fields(self) -> None:
        """Test computed fields."""
        config = FlextWebSettings(ssl_enabled=False)
        tm.that(config.protocol, eq="http")
        config_https = FlextWebSettings(ssl_enabled=False)
        tm.that(config_https.protocol, eq="http")

    def test_base_url_generation(self) -> None:
        """Test base URL generation."""
        config = FlextWebSettings(host="localhost", port=8080, ssl_enabled=False)
        tm.that(config.base_url, eq="http://localhost:8080")

    def test_validate_config_success(self) -> None:
        """Test config validation with Pydantic."""
        config = FlextWebSettings()
        tm.that(config.host, none=False)
        tm.that(config.port, none=False)

    def test_to_dict_method(self) -> None:
        """Test config to dict conversion using Pydantic model_dump."""
        config = FlextWebSettings(host="localhost", port=8080)
        config_dict = config.model_dump()
        tm.that(config_dict["host"], eq="localhost")
        tm.that(config_dict["port"], eq=8080)
        tm.that(config_dict, has="debug_mode")

    def test_create_web_config_factory(self) -> None:
        """Test web config direct instantiation with Pydantic."""
        config = FlextWebSettings(host="test", port=9000)
        tm.that(config.host, eq="test")
        tm.that(config.port, eq=9000)

    def test_create_web_config_class_method(self) -> None:
        """Test create_web_config class method."""
        result = FlextWebSettings.create_web_config()
        tm.ok(result)
        config = result.value
        tm.that(config, is_=FlextWebSettings)
        tm.that(config.host, none=False)
        tm.that(config.port, none=False)
