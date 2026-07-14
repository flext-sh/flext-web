"""Unit tests for flext_web settings."""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_web import FlextWebSettings, c, u


class TestsFlextWebSettings:
    """Test suite for FlextWebSettings."""

    def setup_method(self) -> None:
        FlextWebSettings.reset_for_testing()

    def test_default_settings(self) -> None:
        """Default settings are valid."""
        settings = FlextWebSettings()
        tm.that(settings.Web.app_name, eq="FLEXT Web")
        tm.that(settings.Web.host, eq="localhost")
        tm.that(settings.Web.port, eq=8080)

    def test_host_validator_rejects_empty(self) -> None:
        """Host field constraint rejects blank strings."""
        with pytest.raises(c.ValidationError):
            _ = FlextWebSettings(Web={"host": "   "})

    def test_port_validator_rejects_out_of_range(self) -> None:
        """Port field constraint rejects out-of-range values."""
        with pytest.raises(c.ValidationError):
            _ = FlextWebSettings(Web={"port": 70000})

    def test_port_constraint_lower_bound(self) -> None:
        """Port field constraint rejects zero."""
        with pytest.raises(c.ValidationError):
            _ = FlextWebSettings(Web={"port": 0})

    def test_secret_key_validator_rejects_short(self) -> None:
        """Secret key field constraint rejects short values."""
        with pytest.raises(c.ValidationError):
            _ = FlextWebSettings(Web={"secret_key": "short"})

    def test_secret_key_minimum_length_accepted(self) -> None:
        """A 32-character secret key satisfies the field constraint."""
        settings = FlextWebSettings(Web={"secret_key": "a" * 32})
        tm.that(settings.Web.secret_key, eq="a" * 32)

    def test_optional_ssl_paths(self) -> None:
        """Optional SSL paths default to None and accept explicit values."""
        settings = FlextWebSettings()
        tm.that(settings.Web.ssl_cert_path, eq=None)
        tm.that(settings.Web.ssl_key_path, eq=None)
        custom = FlextWebSettings(
            Web={"ssl_cert_path": "/tmp/cert.pem", "ssl_key_path": "/tmp/key.pem"}
        )
        tm.that(custom.Web.ssl_cert_path, eq="/tmp/cert.pem")
        tm.that(custom.Web.ssl_key_path, eq="/tmp/key.pem")

    def test_debug_flag(self) -> None:
        """The universal debug flag is settable on construction."""
        settings = FlextWebSettings(debug=True)
        tm.that(settings.debug is True, eq=True)

    def test_protocol_derived_from_tls_flag(self) -> None:
        """The wire protocol is derived from the TLS flag via u.Web."""
        http_settings = FlextWebSettings(Web={"ssl_enabled": False})
        tm.that(
            u.Web.protocol(ssl_enabled=http_settings.Web.ssl_enabled),
            eq=c.Web.DEFAULT_HTTP_PROTOCOL,
        )
        https_settings = FlextWebSettings(Web={"ssl_enabled": True})
        tm.that(
            u.Web.protocol(ssl_enabled=https_settings.Web.ssl_enabled),
            eq=c.Web.DEFAULT_HTTPS_PROTOCOL,
        )

    def test_base_url_derived_from_namespace(self) -> None:
        """The base URL combines protocol, host, and port via u.Web."""
        settings = FlextWebSettings(Web={"host": "localhost", "port": 8080})
        tm.that(
            u.Web.base_url(
                host=settings.Web.host,
                port=settings.Web.port,
                ssl_enabled=settings.Web.ssl_enabled,
            ),
            eq="http://localhost:8080",
        )

    def test_clone_applies_namespaced_overrides(self) -> None:
        """Clone applies validated overrides inside the Web namespace."""
        settings = FlextWebSettings().clone(
            Web={"host": "127.0.0.1", "port": 9090, "secret_key": "a" * 32}, debug=True
        )
        tm.that(settings.Web.host, eq="127.0.0.1")
        tm.that(settings.Web.port, eq=9090)
        tm.that(settings.debug is True, eq=True)

    def test_clone_rejects_invalid_overrides(self) -> None:
        """Clone raises a validation error for invalid overrides."""
        with pytest.raises(c.ValidationError):
            _ = FlextWebSettings().clone(Web={"port": 0})

    def test_model_validate_round_trip_success(self) -> None:
        """A dumped settings instance re-validates successfully."""
        settings = FlextWebSettings()
        validated = FlextWebSettings.model_validate(settings.model_dump())
        tm.that(validated.Web.host, eq=settings.Web.host)
        tm.that(validated.Web.port, eq=settings.Web.port)

    def test_model_validate_rejects_invalid_payload(self) -> None:
        """model_validate rejects payloads violating field constraints."""
        with pytest.raises(c.ValidationError):
            _ = FlextWebSettings.model_validate({"Web": {"port": 0}})
