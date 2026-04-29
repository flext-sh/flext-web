"""Unit tests for public web settings behavior."""

from __future__ import annotations

from flext_tests import tm

from flext_web import web


class TestsFlextWebConfig:
    """Tests for the namespaced settings exposed by `web`."""

    def test_initialization_with_test_environment(self) -> None:
        """The public settings namespace is initialized and typed."""
        settings = web.settings
        tm.that(settings.host, none=False)
        tm.that(settings.port, none=False)
        tm.that(settings.app_name, none=False)
        tm.that(settings.app_name, is_=str)
        tm.that(settings.app_name, empty=False)

    def test_initialization_with_custom_values(self) -> None:
        """Validated overrides can be created through the public namespace."""
        result = web.settings.create_web_config(
            host="0.0.0.0",
            port=3000,
            debug=True,
        )
        tm.ok(result)
        settings = result.value.clone(app_name="Test App")
        tm.that(settings.host, eq="0.0.0.0")
        tm.that(settings.port, eq=3000)
        tm.that(settings.debug_mode is True, eq=True)
        tm.that(settings.app_name, eq="Test App")

    def test_debug_flags_stay_synchronized(self) -> None:
        """Debug and debug_mode are unified by the settings model itself."""
        result = web.settings.create_web_config(debug=True)
        tm.ok(result)
        tm.that(result.value.debug is True, eq=True)
        tm.that(result.value.debug_mode is True, eq=True)

    def test_validation_host_empty(self) -> None:
        """Empty hosts fail through the public settings factory."""
        result = web.settings.create_web_config(host="")
        tm.fail(result)

    def test_validation_port_range(self) -> None:
        """Valid ports pass through the public settings factory."""
        result = web.settings.create_web_config(port=8080)
        tm.ok(result)
        tm.that(result.value.port, eq=8080)

    def test_validation_port_out_of_range(self) -> None:
        """Invalid ports fail through the public settings factory."""
        result = web.settings.create_web_config(port=70000)
        tm.fail(result)

    def test_validation_secret_key_too_short(self) -> None:
        """Short secret keys fail through the public settings factory."""
        result = web.settings.create_web_config(secret_key="short")
        tm.fail(result)

    def test_validation_secret_key_valid(self) -> None:
        """Valid secret keys are accepted by the public settings factory."""
        result = web.settings.create_web_config(
            secret_key="valid-secret-key-32-characters-long",
        )
        tm.ok(result)
        tm.that(result.value.secret_key, none=False)

    def test_ssl_configuration_valid(self) -> None:
        """SSL flags remain accessible on the public settings model."""
        settings = web.settings.clone(
            ssl_enabled=False,
            ssl_cert_path=None,
            ssl_key_path=None,
        )
        tm.that(settings.ssl_enabled is False, eq=True)

    def test_computed_fields(self) -> None:
        """Computed fields are available from public settings instances."""
        settings = web.settings.clone(ssl_enabled=False)
        tm.that(settings.protocol, eq="http")
        config_https = web.settings.clone(ssl_enabled=False)
        tm.that(config_https.protocol, eq="http")

    def test_base_url_generation(self) -> None:
        """The base URL is derived from the public settings model."""
        settings = web.settings.clone(
            host="localhost",
            port=8080,
            ssl_enabled=False,
        )
        tm.that(settings.base_url, eq="http://localhost:8080")

    def test_validate_config_success(self) -> None:
        """The namespaced settings instance is valid as exposed."""
        settings = web.settings
        tm.that(settings.host, none=False)
        tm.that(settings.port, none=False)

    def test_to_dict_method(self) -> None:
        """The public settings model can be serialized with model_dump."""
        settings = web.settings.clone(host="localhost", port=8080)
        config_dict = settings.model_dump()
        tm.that(config_dict["host"], eq="localhost")
        tm.that(config_dict["port"], eq=8080)
        tm.that(config_dict, has="debug_mode")

    def test_create_web_config_factory(self) -> None:
        """The public factory returns validated web settings."""
        result = web.settings.create_web_config(host="test", port=9000)
        tm.ok(result)
        tm.that(result.value.host, eq="test")
        tm.that(result.value.port, eq=9000)

    def test_create_web_config_class_method(self) -> None:
        """The namespaced factory returns the canonical settings type."""
        result = web.settings.create_web_config()
        tm.ok(result)
        tm.that(result.value, is_=type(web.settings))
        tm.that(result.value.host, none=False)
        tm.that(result.value.port, none=False)
