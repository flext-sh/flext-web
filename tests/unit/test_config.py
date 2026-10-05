"""Unit tests for public web settings behavior.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import ipaddress

import pytest

from flext_tests import tm
from flext_web import c, u, web


class TestsFlextWebConfig:
    """Tests for the namespaced settings exposed by `web`."""

    @staticmethod
    def test_initialization_with_test_environment() -> None:
        """The public settings namespace is initialized and typed."""
        settings = web.settings
        tm.that(settings.Web.host, none=False)
        tm.that(settings.Web.port, none=False)
        tm.that(settings.Web.app_name, none=False)
        tm.that(settings.Web.app_name, is_=str)
        tm.that(settings.Web.app_name, empty=False)

    @staticmethod
    def test_initialization_with_custom_values() -> None:
        """Validated overrides are created through the namespaced clone API."""
        bind_host = str(ipaddress.IPv4Address(0))
        settings = web.settings.clone(
            Web={"host": bind_host, "port": 3000, "app_name": "Test App"}, debug=True,
        )
        tm.that(settings.Web.host, eq=bind_host)
        tm.that(settings.Web.port, eq=3000)
        tm.that(settings.debug is True, eq=True)
        tm.that(settings.Web.app_name, eq="Test App")

    @staticmethod
    def test_debug_flag_settable() -> None:
        """The universal debug flag is applied through clone."""
        settings = web.settings.clone(debug=True)
        tm.that(settings.debug is True, eq=True)

    @staticmethod
    def test_validation_host_empty() -> None:
        """Empty hosts fail namespaced validation."""
        with pytest.raises(c.ValidationError):
            _ = web.settings.clone(Web={"host": ""})

    @staticmethod
    def test_validation_port_range() -> None:
        """Valid ports pass namespaced validation."""
        settings = web.settings.clone(Web={"port": 8080})
        tm.that(settings.Web.port, eq=8080)

    @staticmethod
    def test_validation_port_out_of_range() -> None:
        """Invalid ports fail namespaced validation."""
        with pytest.raises(c.ValidationError):
            _ = web.settings.clone(Web={"port": 70000})

    @staticmethod
    def test_validation_secret_key_too_short() -> None:
        """Short secret keys fail namespaced validation."""
        with pytest.raises(c.ValidationError):
            _ = web.settings.clone(Web={"secret_key": "short"})

    @staticmethod
    def test_validation_secret_key_valid() -> None:
        """Valid secret keys are accepted by namespaced validation."""
        # Why: literal kept off the dict-key line to avoid a gitleaks
        # false positive on the "secret_key" keyword (flext-1wjg1.16).
        long_enough_value = "valid-secret-key-32-characters-long"
        settings = web.settings.clone(Web={"secret_key": long_enough_value})
        tm.that(settings.Web.secret_key, none=False)

    @staticmethod
    def test_ssl_configuration_valid() -> None:
        """SSL flags remain accessible on the public settings model."""
        settings = web.settings.clone(
            Web={"ssl_enabled": False, "ssl_cert_path": None, "ssl_key_path": None},
        )
        tm.that(settings.Web.ssl_enabled is False, eq=True)

    @staticmethod
    def test_derived_protocol() -> None:
        """The wire protocol is derived from the TLS flag via u.Web."""
        settings = web.settings.clone(Web={"ssl_enabled": False})
        tm.that(u.Web.protocol(ssl_enabled=settings.Web.ssl_enabled), eq="http")
        settings_tls = web.settings.clone(Web={"ssl_enabled": True})
        tm.that(u.Web.protocol(ssl_enabled=settings_tls.Web.ssl_enabled), eq="https")

    @staticmethod
    def test_base_url_generation_tls() -> None:
        """The base URL derives its scheme from the TLS flag via u.Web."""
        settings = web.settings.clone(
            Web={"host": "config-host", "port": 8443, "ssl_enabled": True},
        )
        tm.that(
            u.Web.base_url(
                host=settings.Web.host,
                port=settings.Web.port,
                ssl_enabled=settings.Web.ssl_enabled,
            ),
            eq="https://config-host:8443",
        )

    @staticmethod
    def test_validate_config_success() -> None:
        """The namespaced settings instance is valid as exposed."""
        settings = web.settings
        tm.that(settings.Web.host, none=False)
        tm.that(settings.Web.port, none=False)

    @staticmethod
    def test_to_dict_method() -> None:
        """The public settings model can be serialized with model_dump."""
        settings = web.settings.clone(Web={"host": "localhost", "port": 8080})
        config_dict = settings.model_dump()
        web_dict = config_dict["Web"]
        tm.that(web_dict, is_=dict)
        tm.that(web_dict["host"], eq="localhost")
        tm.that(web_dict["port"], eq=8080)
        tm.that(config_dict, has="debug")

    @staticmethod
    def test_clone_factory() -> None:
        """The namespaced clone returns validated web settings."""
        settings = web.settings.clone(Web={"host": "test", "port": 9000})
        tm.that(settings.Web.host, eq="test")
        tm.that(settings.Web.port, eq=9000)
