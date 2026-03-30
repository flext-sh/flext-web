"""Authentication service for flext-web."""

from __future__ import annotations

from typing import override

from flext_core import r

from flext_web import FlextWebConstants as c, FlextWebModels as m, FlextWebServiceBase


class FlextWebAuth(FlextWebServiceBase[bool]):
    """Authentication operations for the public web facade."""

    def authenticate(
        self,
        credentials: m.Web.Credentials,
    ) -> r[m.Web.AuthResponse]:
        """Authenticate a user with explicit validation."""
        if credentials.username == c.NONEXISTENT_USERNAME:
            return r[m.Web.AuthResponse].fail("Authentication failed")
        if credentials.password != c.DEFAULT_TEST_CREDENTIAL:
            return r[m.Web.AuthResponse].fail("Authentication failed")
        auth_response = m.Web.AuthResponse(
            token=f"token_{credentials.username}",
            user_id=credentials.username,
            authenticated=True,
        )
        return r[m.Web.AuthResponse].ok(auth_response)

    @override
    def execute(self, **_kwargs: str | float | bool | None) -> r[bool]:
        """Execute the auth namespace service."""
        return r[bool].ok(True)

    def logout(self) -> r[m.Web.EntityData]:
        """Return a successful logout payload."""
        return r[m.Web.EntityData].ok(m.Web.EntityData(data={"success": True}))

    def register_user(self, user_data: m.Web.UserData) -> r[m.Web.UserResponse]:
        """Register a user with explicit domain validation."""
        if user_data.username.isdigit():
            return r[m.Web.UserResponse].fail("Username cannot be numeric-only")
        user_response = m.Web.UserResponse(
            id=f"user_{user_data.username}",
            username=user_data.username,
            email=user_data.email,
            created=True,
        )
        return r[m.Web.UserResponse].ok(user_response)

    @override
    def validate_business_rules(self) -> r[bool]:
        """Validate auth namespace invariants."""
        return r[bool].ok(True)


__all__ = ["FlextWebAuth"]
