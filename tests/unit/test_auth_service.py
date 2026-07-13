"""Unit tests for flext_web authentication service."""

from __future__ import annotations

from flext_tests import tm

from flext_web import FlextWebAuth, m


class TestsFlextWebAuth:
    """Test suite for FlextWebAuth."""

    def test_authenticate_success(self) -> None:
        """Auth service accepts canonical credentials."""
        auth = FlextWebAuth()
        credentials = m.Web.Credentials(
            username="testuser",
            password="test_password",
        )
        result = auth.authenticate(credentials)
        tm.ok(result)
        tm.that(result.value.user_id, eq="testuser")
        tm.that(result.value.authenticated is True, eq=True)

    def test_authenticate_unknown_user(self) -> None:
        """Auth service rejects unknown username."""
        auth = FlextWebAuth()
        credentials = m.Web.Credentials(
            username="nonexistent",
            password="test_password",
        )
        result = auth.authenticate(credentials)
        tm.fail(result)
        tm.that(result.error, none=False)

    def test_authenticate_wrong_password(self) -> None:
        """Auth service rejects wrong password."""
        auth = FlextWebAuth()
        credentials = m.Web.Credentials(
            username="testuser",
            password="wrong-password",
        )
        result = auth.authenticate(credentials)
        tm.fail(result)
        tm.that(result.error, none=False)

    def test_execute(self) -> None:
        """Auth service execute returns success."""
        auth = FlextWebAuth()
        result = auth.execute()
        tm.ok(result)
        tm.that(result.value is True, eq=True)

    def test_logout(self) -> None:
        """Logout returns a success payload."""
        auth = FlextWebAuth()
        result = auth.logout()
        tm.ok(result)
        tm.that(result.value.data, has="success")

    def test_register_user_success(self) -> None:
        """Registration succeeds for valid user data."""
        auth = FlextWebAuth()
        user_data = m.Web.UserData(
            username="newuser",
            email="newuser@example.com",
            password="password123",
        )
        result = auth.register_user(user_data)
        tm.ok(result)
        tm.that(result.value.created is True, eq=True)

    def test_register_user_numeric_username(self) -> None:
        """Registration rejects numeric-only usernames."""
        auth = FlextWebAuth()
        user_data = m.Web.UserData(
            username="12345",
            email="numeric@example.com",
            password="password123",
        )
        result = auth.register_user(user_data)
        tm.fail(result)
        tm.that(result.error, none=False)

    def test_validate_business_rules(self) -> None:
        """Auth service validates business rules."""
        auth = FlextWebAuth()
        result = auth.validate_business_rules()
        tm.ok(result)
        tm.that(result.value is True, eq=True)
