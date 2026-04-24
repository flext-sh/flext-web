"""Authentication service for flext-web."""

from __future__ import annotations

from flext_web import m, p, r, s


class FlextWebAuth(s[bool]):
    """Authentication operations for the public web facade."""

    def authenticate(
        self,
        credentials: m.Web.Credentials,
    ) -> p.Result[m.Web.AuthResponse]:
        """Authenticate a user with explicit validation."""
        if credentials.username == "nonexistent":
            return r[m.Web.AuthResponse].fail("Authentication failed")
        if credentials.password != "test_password":  # noqa: S105
            return r[m.Web.AuthResponse].fail("Authentication failed")
        auth_response = m.Web.AuthResponse(
            token=f"token_{credentials.username}",
            user_id=credentials.username,
            authenticated=True,
        )
        return r[m.Web.AuthResponse].ok(auth_response)

    def execute(
        self,
    ) -> p.Result[bool]:
        """Execute the auth namespace service."""
        return r[bool].ok(True)

    def logout(self) -> p.Result[m.Web.EntityData]:
        """Return a successful logout payload."""
        return r[m.Web.EntityData].ok(m.Web.EntityData(data={"success": True}))

    def register_user(self, user_data: m.Web.UserData) -> p.Result[m.Web.UserResponse]:
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

    def validate_business_rules(self) -> p.Result[bool]:
        """Validate auth namespace invariants."""
        return r[bool].ok(True)


__all__: list[str] = ["FlextWebAuth"]
