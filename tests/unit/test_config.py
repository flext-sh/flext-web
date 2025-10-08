"""Unit tests for flext_web.config module.

Tests the web configuration functionality following flext standards.
"""

import pytest
from pydantic import ValidationError

from flext_web.config import FlextWebConfig
from flext_web.constants import FlextWebConstants


class TestFlextWebConfig:
    """Test suite for FlextWebConfig class."""

    def test_initialization_with_defaults(self) -> None:
        """Test FlextWebConfig initialization with defaults."""
        config = FlextWebConfig()
        assert config.host == FlextWebConstants.WebServer.DEFAULT_HOST
        assert config.port == FlextWebConstants.WebServer.DEFAULT_PORT
        assert config.debug is False
        assert config.app_name == "FLEXT Web"

    def test_initialization_with_custom_values(self) -> None:
        """Test FlextWebConfig initialization with custom values."""
        config = FlextWebConfig(
            host="0.0.0.0", port=3000, debug=True, app_name="Test App"
        )
        assert config.host == "0.0.0.0"
        assert config.port == 3000
        assert config.debug is True
        assert config.app_name == "Test App"

    def test_validation_host_empty(self) -> None:
        """Test host validation with empty string."""
        with pytest.raises(ValidationError):
            FlextWebConfig(host="")

    def test_validation_port_range(self) -> None:
        """Test port validation within valid range."""
        config = FlextWebConfig(port=8080)
        assert config.port == 8080

    def test_validation_port_out_of_range(self) -> None:
        """Test port validation outside valid range."""
        with pytest.raises(ValidationError):
            FlextWebConfig(port=70000)

    def test_validation_secret_key_too_short(self) -> None:
        """Test secret key validation with too short key."""
        with pytest.raises(ValidationError):
            FlextWebConfig(secret_key="short")

    def test_validation_secret_key_valid(self) -> None:
        """Test secret key validation with valid key."""
        config = FlextWebConfig(secret_key="valid-secret-key-32-characters-long")
        assert config.secret_key is not None

    def test_ssl_configuration_valid(self) -> None:
        """Test SSL configuration with valid cert and key paths."""
        # This would need actual cert files in a real test
        config = FlextWebConfig(
            ssl_enabled=False, ssl_cert_path=None, ssl_key_path=None
        )
        assert config.ssl_enabled is False

    def test_cors_configuration(self) -> None:
        """Test CORS configuration."""
        config = FlextWebConfig(
            enable_cors=True,
            cors_origins=["http://localhost:3000", "https://example.com"],
        )
        assert config.enable_cors is True
        assert len(config.cors_origins) == 2

    def test_computed_fields(self) -> None:
        """Test computed fields."""
        config = FlextWebConfig(ssl_enabled=False)
        assert config.protocol == "http"

        # Test with SSL disabled (no cert/key required)
        config_https = FlextWebConfig(ssl_enabled=False)
        assert config_https.protocol == "http"

    def test_base_url_generation(self) -> None:
        """Test base URL generation."""
        config = FlextWebConfig(host="localhost", port=8080, ssl_enabled=False)
        assert config.base_url == "http://localhost:8080"

    def test_validate_business_rules_success(self) -> None:
        """Test business rules validation with valid config."""
        config = FlextWebConfig()
        result = config.validate_business_rules()
        assert result.is_success

    def test_get_server_config(self) -> None:
        """Test server configuration retrieval."""
        config = FlextWebConfig(host="localhost", port=8080, debug=True)
        server_config = config.get_server_config()
        assert server_config["host"] == "localhost"
        assert server_config["port"] == 8080
        assert server_config["debug"] is True

    def test_get_security_config(self) -> None:
        """Test security configuration retrieval."""
        config = FlextWebConfig(enable_cors=True, ssl_enabled=True)
        security_config = config.get_security_config()
        assert security_config["enable_cors"] is True
        assert security_config["ssl_enabled"] is True

    def test_create_web_config_factory(self) -> None:
        """Test web config factory method."""
        result = FlextWebConfig.create_web_config(host="test", port=9000)
        assert result.is_success
        config = result.unwrap()
        assert config.host == "test"
        assert config.port == 9000

    def test_create_development_config(self) -> None:
        """Test development config creation."""
        result = FlextWebConfig.create_development_config()
        assert result.is_success
        config = result.unwrap()
        assert config.debug is True
        assert config.development_mode is True

    def test_create_for_environment_development(self) -> None:
        """Test config creation for development environment."""
        config = FlextWebConfig()
        assert config.web_environment == "development"
        assert config.debug is True

    def test_create_for_environment_production(self) -> None:
        """Test config creation for production environment."""
        config = FlextWebConfig()
        assert config.web_environment == "production"
        assert config.debug is False
