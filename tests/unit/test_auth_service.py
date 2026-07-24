"""Unit tests for flext_web authentication service."""

from __future__ import annotations

from flext_tests import tm
from flext_web import FlextWebAuth
from tests import m
from tests.fixtures import WebAuthFixture


class TestsFlextWebAuth:
    """Test suite for FlextWebAuth."""

    def test_authenticate_success(self) -> None:
        """Auth service accepts canonical credentials."""
        authenticator = WebAuthFixture()
        auth = FlextWebAuth()
        result = auth.authenticate(authenticator.credentials)
        tm.ok(result)
        tm.that(result.value.user_id, eq=authenticator.credentials.username)
        tm.that(result.value.authenticated is True, eq=True)

    def test_authenticate_unknown_user(self) -> None:
        """Auth service rejects unknown username."""
        authenticator = WebAuthFixture()
        auth = FlextWebAuth()
        credentials = authenticator.credentials.model_copy(
            update={"username": authenticator.rejected_username}
        )
        result = auth.authenticate(credentials)
        tm.fail(result)
        tm.that(result.error, none=False)

    def test_authenticate_wrong_password(self) -> None:
        """Auth service rejects wrong password."""
        authenticator = WebAuthFixture()
        auth = FlextWebAuth()
        credentials = authenticator.credentials.model_copy(
            update={"password": f"invalid-{authenticator.credentials.password}"}
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
        credentials = WebAuthFixture().credentials
        auth = FlextWebAuth()
        user_data = m.Web.UserData(
            username="newuser",
            email="newuser@example.com",
            password=credentials.password,
        )
        result = auth.register_user(user_data)
        tm.ok(result)
        tm.that(result.value.created is True, eq=True)

    def test_register_user_numeric_username(self) -> None:
        """Registration rejects numeric-only usernames."""
        credentials = WebAuthFixture().credentials
        auth = FlextWebAuth()
        user_data = m.Web.UserData(
            username="12345", email="numeric@example.com", password=credentials.password
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
