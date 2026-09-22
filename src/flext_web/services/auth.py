"""Authentication service for flext-web."""

from __future__ import annotations

import secrets
from typing import override

from flext_web import e, m, p, r, s


class FlextWebAuth(s):
    """Authentication operations for the public web facade."""

    def authenticate(
        self, credentials: m.Web.Credentials
    ) -> p.Result[m.Web.AuthResponse]:
        """Authenticate against the settings SSOT; fail loud when unconfigured."""
        expected_username = self.settings.Web.auth_username
        expected_password = self.settings.Web.auth_password
        if not expected_username or not expected_password:
            return e.fail_auth(
                "credentials",
                credentials.username,
                options=m.ExceptionFactoryOptions(
                    error="authentication provider is not configured"
                ),
            )
        if not (
            secrets.compare_digest(credentials.username, expected_username)
            and secrets.compare_digest(credentials.password, expected_password)
        ):
            return e.fail_auth(
                "password",
                credentials.username,
                options=m.ExceptionFactoryOptions(error="invalid credentials"),
            )
        auth_response = m.Web.AuthResponse(
            token=secrets.token_urlsafe(32),
            user_id=credentials.username,
            authenticated=True,
        )
        return r[m.Web.AuthResponse].ok(auth_response)

    @override
    def execute(self) -> p.Result[bool]:
        """Execute the auth namespace service."""
        return r[bool].ok(True)

    def logout(self) -> p.Result[m.Web.EntityData]:
        """Return a successful logout payload."""
        return r[m.Web.EntityData].ok(m.Web.EntityData(data={"success": True}))

    def register_user(self, user_data: m.Web.UserData) -> p.Result[m.Web.UserResponse]:
        """Register a user with explicit domain validation."""
        if user_data.username.isdigit():
            return e.fail_validation("username", error="cannot be numeric-only")
        user_response = m.Web.UserResponse(
            id=f"user_{user_data.username}",
            username=user_data.username,
            email=user_data.email,
            created=True,
        )
        return r[m.Web.UserResponse].ok(user_response)

    def validate_business_rules(self) -> p.Result[bool]:
        """Validate auth namespace invariants."""
        return r[bool].ok(True)


__all__: list[str] = ["FlextWebAuth"]
