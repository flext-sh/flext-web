"""Unit tests for the flext_web model/typing surface (`m.Web`).

Every test constructs real models through the public `m` facade and asserts
observable behavior or validation outcomes. Empty tests, tautologies
(`result.success or result.failure`, asserting on a local literal), facade-only
type checks, and implementation-line-coupled duplicates are prohibited and absent.
"""

from __future__ import annotations

from flext_tests import tm
from flext_web import web
from tests import c, m


class TestsFlextWebTypesUnit:
    """Real-behavior tests for the web model surface via `m.Web`."""

    def test_model_functionality(self) -> None:
        """WebRequest and AppResponse carry through their constructed values."""
        request = m.Web.WebRequest(url="http://localhost:8080", method=c.Web.Method.GET)
        tm.that(request.url, eq="http://localhost:8080")
        tm.that(request.method, eq=c.Web.Method.GET)
        response = m.Web.AppResponse(status_code=200, request_id="test-123")
        tm.that(response.status_code, eq=200)

    def test_app_data_functionality(self) -> None:
        """Entity exposes its fields and derives the running flag from status."""
        app = m.Web.Entity(
            id="test-id", name="test-app", host="localhost", port=8080, status="running"
        )
        tm.that(app.id, eq="test-id")
        tm.that(app.name, eq="test-app")
        tm.that(app.host, eq="localhost")
        tm.that(app.port, eq=8080)
        tm.that(app.status, eq="running")
        tm.that(app.running is True, eq=True)

    def test_request_context_functionality(self) -> None:
        """AppRequest preserves method, url, headers and query params."""
        request = m.Web.AppRequest(
            url="http://localhost:8080/api/test",
            method=c.Web.Method.GET,
            headers={"Content-Type": "application/json"},
            query_params={"param1": "value1"},
        )
        tm.that(request.method, eq="GET")
        tm.that(request.url, eq="http://localhost:8080/api/test")
        tm.that(request.headers["Content-Type"], eq="application/json")
        tm.that(request.query_params["param1"], eq="value1")

    def test_model_creation(self) -> None:
        """Entity can be created without an explicit status."""
        app = m.Web.Entity(id="test-id", name="test-app", host="localhost", port=8080)
        tm.that(app.id, eq="test-id")
        tm.that(app.name, eq="test-app")
        tm.that(app.host, eq="localhost")
        tm.that(app.port, eq=8080)

    def test_config_validation(self) -> None:
        """Settings clone applies the overridden Web host and port."""
        settings = web.settings.clone(Web={"host": "localhost", "port": 8080})
        tm.that(settings.Web.host, eq="localhost")
        tm.that(settings.Web.port, eq=8080)

    def test_create_http_request_invalid_method(self) -> None:
        """An invalid HTTP method fails with a method-related error."""
        result = m.Web.Request.create_http_request(
            url="http://localhost:8080", method="INVALID_METHOD"
        )
        tm.fail(result)
        tm.that(result.error, has="method")

    def test_create_http_request_exception_handling(self) -> None:
        """A negative timeout fails validation."""
        result = m.Web.Request.create_http_request(
            url="http://localhost:8080",
            method="GET",
            headers={},
            body=None,
            timeout=-1.0,
        )
        tm.fail(result)
        error = (result.error or "").lower()
        tm.that("timeout" in error or "validation" in error, eq=True)

    def test_create_http_response_exception_handling(self) -> None:
        """A negative elapsed_time fails validation."""
        result = m.Web.Response.create_http_response(
            status_code=200, headers={}, body=None, elapsed_time=-1.0
        )
        tm.fail(result)
        error = (result.error or "").lower()
        tm.that("elapsed_time" in error or "validation" in error, eq=True)

    def test_create_http_request_all_methods(self) -> None:
        """Every valid HTTP method yields a request carrying that method."""
        valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
        for method in valid_methods:
            result = m.Web.Request.create_http_request(
                url="http://localhost:8080", method=method
            )
            tm.ok(result)
            tm.that(result.value.method, eq=method)

    def test_create_http_request_with_none_headers(self) -> None:
        """None headers normalize to an empty dict on the created request."""
        result = m.Web.Request.create_http_request(
            url="http://localhost:8080", method="GET", headers=None
        )
        tm.ok(result)
        tm.that(result.value.headers, eq={})

    def test_create_http_response_with_none_headers(self) -> None:
        """None headers normalize to an empty dict on the created response."""
        result = m.Web.Response.create_http_response(status_code=200, headers=None)
        tm.ok(result)
        tm.that(result.value.headers, eq={})
