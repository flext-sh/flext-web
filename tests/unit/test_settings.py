"""Unit tests for flext_web settings.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from flext_tests import tm
from flext_web import FlextWebSettings, c, u

if TYPE_CHECKING:
    from pathlib import Path


class TestsFlextWebSettings:
    """Test suite for FlextWebSettings."""

    @staticmethod
    def setup_method() -> None:
        """Provide ``setup_method``."""
        FlextWebSettings.reset_for_testing()

    @staticmethod
    def test_default_settings() -> None:
        """Default settings are valid."""
        settings = FlextWebSettings()
        tm.that(settings.Web.app_name, eq="FLEXT Web")
        tm.that(settings.Web.host, eq="localhost")
        tm.that(settings.Web.port, eq=8080)

    @staticmethod
    def test_host_validator_rejects_empty() -> None:
        """Host field constraint rejects blank strings."""
        with pytest.raises(c.ValidationError):
            _ = FlextWebSettings().clone(Web={"host": "   "})

    @staticmethod
    def test_port_validator_rejects_out_of_range() -> None:
        """Port field constraint rejects out-of-range values."""
        with pytest.raises(c.ValidationError):
            _ = FlextWebSettings().clone(Web={"port": 70000})

    @staticmethod
    def test_port_constraint_lower_bound() -> None:
        """Port field constraint rejects zero."""
        with pytest.raises(c.ValidationError):
            _ = FlextWebSettings().clone(Web={"port": 0})

    @staticmethod
    def test_secret_key_validator_rejects_short() -> None:
        """Secret key field constraint rejects short values."""
        with pytest.raises(c.ValidationError):
            _ = FlextWebSettings().clone(Web={"secret_key": "short"})

    @staticmethod
    def test_secret_key_minimum_length_accepted() -> None:
        """A 32-character secret key satisfies the field constraint."""
        settings = FlextWebSettings().clone(Web={"secret_key": "a" * 32})
        tm.that(settings.Web.secret_key, eq="a" * 32)

    @staticmethod
    def test_optional_ssl_paths(tmp_path: Path) -> None:
        """Optional SSL paths default to None and accept explicit values."""
        settings = FlextWebSettings()
        tm.that(settings.Web.ssl_cert_path, eq=None)
        tm.that(settings.Web.ssl_key_path, eq=None)
        cert_path = str(tmp_path / "cert.pem")
        key_path = str(tmp_path / "key.pem")
        custom = FlextWebSettings().clone(
            Web={"ssl_cert_path": cert_path, "ssl_key_path": key_path},
        )
        tm.that(custom.Web.ssl_cert_path, eq=cert_path)
        tm.that(custom.Web.ssl_key_path, eq=key_path)

    @staticmethod
    def test_debug_flag() -> None:
        """The universal debug flag is settable on construction."""
        settings = FlextWebSettings(debug=True)
        tm.that(settings.debug is True, eq=True)

    @staticmethod
    def test_protocol_derived_from_tls_flag() -> None:
        """The wire protocol is derived from the TLS flag via u.Web."""
        http_settings = FlextWebSettings().clone(Web={"ssl_enabled": False})
        tm.that(
            u.Web.protocol(ssl_enabled=http_settings.Web.ssl_enabled),
            eq=c.Web.DEFAULT_HTTP_PROTOCOL,
        )
        https_settings = FlextWebSettings().clone(Web={"ssl_enabled": True})
        tm.that(
            u.Web.protocol(ssl_enabled=https_settings.Web.ssl_enabled),
            eq=c.Web.DEFAULT_HTTPS_PROTOCOL,
        )

    @staticmethod
    def test_base_url_derived_from_namespace() -> None:
        """The base URL combines protocol, host, and port via u.Web."""
        settings = FlextWebSettings().clone(Web={"host": "localhost", "port": 8080})
        tm.that(
            u.Web.base_url(
                host=settings.Web.host,
                port=settings.Web.port,
                ssl_enabled=settings.Web.ssl_enabled,
            ),
            eq="http://localhost:8080",
        )

    @staticmethod
    def test_clone_applies_namespaced_overrides() -> None:
        """Clone applies validated overrides inside the Web namespace."""
        settings = FlextWebSettings().clone(
            Web={"host": "127.0.0.1", "port": 9090, "secret_key": "a" * 32},
            debug=True,
        )
        tm.that(settings.Web.host, eq="127.0.0.1")
        tm.that(settings.Web.port, eq=9090)
        tm.that(settings.debug is True, eq=True)

    @staticmethod
    def test_clone_rejects_invalid_overrides() -> None:
        """Clone raises a validation error for invalid overrides."""
        with pytest.raises(c.ValidationError):
            _ = FlextWebSettings().clone(Web={"port": 0})

    @staticmethod
    def test_model_validate_round_trip_success() -> None:
        """A dumped settings instance re-validates successfully."""
        settings = FlextWebSettings()
        validated = FlextWebSettings.model_validate(settings.model_dump())
        tm.that(validated.Web.host, eq=settings.Web.host)
        tm.that(validated.Web.port, eq=settings.Web.port)

    @staticmethod
    def test_model_validate_rejects_invalid_payload() -> None:
        """model_validate rejects payloads violating field constraints."""
        with pytest.raises(c.ValidationError):
            _ = FlextWebSettings.model_validate({"Web": {"port": 0}})
