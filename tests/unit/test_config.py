"""Unit tests for public web settings behavior."""

from __future__ import annotations

import pytest

from flext_tests import tm
from flext_web import c, u, web


class TestsFlextWebConfig:
    """Tests for the namespaced settings exposed by `web`."""

    def test_initialization_with_test_environment(self) -> None:
        """The public settings namespace is initialized and typed."""
        settings = web.settings
        tm.that(settings.Web.host, none=False)
        tm.that(settings.Web.port, none=False)
        tm.that(settings.Web.app_name, none=False)
        tm.that(settings.Web.app_name, is_=str)
        tm.that(settings.Web.app_name, empty=False)

    def test_initialization_with_custom_values(self) -> None:
        """Validated overrides are created through the namespaced clone API."""
        settings = web.settings.clone(
            Web={"host": "0.0.0.0", "port": 3000, "app_name": "Test App"}, debug=True
        )
        tm.that(settings.Web.host, eq="0.0.0.0")
        tm.that(settings.Web.port, eq=3000)
        tm.that(settings.debug is True, eq=True)
        tm.that(settings.Web.app_name, eq="Test App")

    def test_debug_flag_settable(self) -> None:
        """The universal debug flag is applied through clone."""
        settings = web.settings.clone(debug=True)
        tm.that(settings.debug is True, eq=True)

    def test_validation_host_empty(self) -> None:
        """Empty hosts fail namespaced validation."""
        with pytest.raises(c.ValidationError):
            _ = web.settings.clone(Web={"host": ""})

    def test_validation_port_range(self) -> None:
        """Valid ports pass namespaced validation."""
        settings = web.settings.clone(Web={"port": 8080})
        tm.that(settings.Web.port, eq=8080)

    def test_validation_port_out_of_range(self) -> None:
        """Invalid ports fail namespaced validation."""
        with pytest.raises(c.ValidationError):
            _ = web.settings.clone(Web={"port": 70000})

    def test_validation_secret_key_too_short(self) -> None:
        """Short secret keys fail namespaced validation."""
        with pytest.raises(c.ValidationError):
            _ = web.settings.clone(Web={"secret_key": "short"})

    def test_validation_secret_key_valid(self) -> None:
        """Valid secret keys are accepted by namespaced validation."""
        settings = web.settings.clone(
            Web={"secret_key": "valid-secret-key-32-characters-long"}
        )
        tm.that(settings.Web.secret_key, none=False)

    def test_ssl_configuration_valid(self) -> None:
        """SSL flags remain accessible on the public settings model."""
        settings = web.settings.clone(
            Web={"ssl_enabled": False, "ssl_cert_path": None, "ssl_key_path": None}
        )
        tm.that(settings.Web.ssl_enabled is False, eq=True)

    def test_derived_protocol(self) -> None:
        """The wire protocol is derived from the TLS flag via u.Web."""
        settings = web.settings.clone(Web={"ssl_enabled": False})
        tm.that(u.Web.protocol(ssl_enabled=settings.Web.ssl_enabled), eq="http")
        settings_tls = web.settings.clone(Web={"ssl_enabled": True})
        tm.that(u.Web.protocol(ssl_enabled=settings_tls.Web.ssl_enabled), eq="https")

    def test_base_url_generation(self) -> None:
        """The base URL is derived from the settings namespace via u.Web."""
        settings = web.settings.clone(
            Web={"host": "localhost", "port": 8080, "ssl_enabled": False}
        )
        tm.that(
            u.Web.base_url(
                host=settings.Web.host,
                port=settings.Web.port,
                ssl_enabled=settings.Web.ssl_enabled,
            ),
            eq="http://localhost:8080",
        )

    def test_validate_config_success(self) -> None:
        """The namespaced settings instance is valid as exposed."""
        settings = web.settings
        tm.that(settings.Web.host, none=False)
        tm.that(settings.Web.port, none=False)

    def test_to_dict_method(self) -> None:
        """The public settings model can be serialized with model_dump."""
        settings = web.settings.clone(Web={"host": "localhost", "port": 8080})
        config_dict = settings.model_dump()
        web_dict = config_dict["Web"]
        tm.that(web_dict, is_=dict)
        tm.that(web_dict["host"], eq="localhost")
        tm.that(web_dict["port"], eq=8080)
        tm.that(config_dict, has="debug")

    def test_clone_factory(self) -> None:
        """The namespaced clone returns validated web settings."""
        settings = web.settings.clone(Web={"host": "test", "port": 9000})
        tm.that(settings.Web.host, eq="test")
        tm.that(settings.Web.port, eq=9000)

    def test_clone_preserves_canonical_type(self) -> None:
        """The namespaced clone returns the canonical settings type."""
        settings = web.settings.clone()
        tm.that(settings, is_=type(web.settings))
        tm.that(settings.Web.host, none=False)
        tm.that(settings.Web.port, none=False)
