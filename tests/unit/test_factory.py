"""Unit tests for flext_web model factory methods."""

from __future__ import annotations

from flext_tests import tm

from flext_web import m, settings
from tests import c


class TestsFlextWebFactory:
    """Test suite for m.Web factory helpers."""

    def test_create_web_app_success(self) -> None:
        """Factory creates a valid web app entity."""
        result = m.Web.create_web_app(
            name="factory-app", host=settings.Web.host, port=settings.Web.port
        )
        tm.ok(result)
        tm.that(result.value.name, eq="factory-app")
        tm.that(result.value.host, eq=settings.Web.host)
        tm.that(result.value.port, eq=settings.Web.port)

    def test_create_web_request_success(self) -> None:
        """Factory creates a valid web request model."""
        result = m.Web.create_web_request(
            method=c.Web.Method.GET,
            url="http://localhost:8080/api",
            headers={"Content-Type": "application/json"},
            body='{"test": true}',
        )
        tm.ok(result)
        tm.that(result.value.method, eq=c.Web.Method.GET)
        tm.that(result.value.url, eq="http://localhost:8080/api")
        tm.that(result.value.headers, has="Content-Type")

    def test_create_web_request_failure(self) -> None:
        """Factory returns failure for an invalid request model."""
        result = m.Web.create_web_request(method=c.Web.Method.GET, url="")
        tm.fail(result)
        tm.that(result.error, none=False)

    def test_create_web_response_success(self) -> None:
        """Factory creates a valid web response model."""
        result = m.Web.create_web_response(
            request_id="req-123",
            status_code=200,
            headers={"Content-Type": "application/json"},
            body='{"ok": true}',
        )
        tm.ok(result)
        tm.that(result.value.request_id, eq="req-123")
        tm.that(result.value.status_code, eq=200)

    def test_create_web_response_failure(self) -> None:
        """Factory returns failure for an invalid response model."""
        result = m.Web.create_web_response(request_id="", status_code=99)
        tm.fail(result)
        tm.that(result.error, none=False)
