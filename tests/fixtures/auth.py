"""Typed authentication fixture for public web behavior tests.

Credentials come from the settings SSOT (``settings.Web.auth_username`` /
``auth_password``), which the test session sources from the environment, so no
test module repeats contract literals. The rejected username is derived by
appending a suffix the configured username cannot carry.
"""

from __future__ import annotations

from flext_web import FlextWebSettings, m


class WebAuthFixture:
    """Expose credentials that satisfy the real authenticate() contract."""

    def __init__(self) -> None:
        """Create credentials from the configured runtime contract."""
        web_settings = FlextWebSettings.fetch_global()
        auth_username = web_settings.Web.auth_username
        auth_password = web_settings.Web.auth_password
        if not auth_username or not auth_password:
            msg = (
                "test session must configure FLEXT_WEB_WEB__AUTH_USERNAME and "
                "FLEXT_WEB_WEB__AUTH_PASSWORD"
            )
            raise RuntimeError(
                msg
            )
        self.credentials = m.Web.Credentials(
            username=auth_username, password=auth_password
        )
        self.rejected_username = f"{auth_username}-rejected"


__all__: list[str] = ["WebAuthFixture"]
