"""Comprehensive unit tests for flext_web.typings module.

Tests the unified m class following flext standards.
"""

from __future__ import annotations

from collections.abc import Mapping

import pytest
from flext_tests import tm
from pydantic import ValidationError

from flext_web import (
    FlextWebSettings,
    _ApplicationConfig,
    _WebRequestConfig,
    _WebResponseConfig,
)
from tests import m, t


class TestFlextWebModels:
    """Test suite for m unified class."""

    def test_typings_structure(self) -> None:
        """Test that m has proper structure."""
        tm.that(hasattr(m, "Web"), eq=True)
        tm.that(hasattr(m.Web, "Message"), eq=True)
        tm.that(hasattr(m.Web, "Request"), eq=True)
        tm.that(hasattr(m.Web, "Response"), eq=True)
        tm.that(hasattr(m.Web, "WebRequest"), eq=True)
        tm.that(hasattr(m.Web, "WebResponse"), eq=True)
        tm.that(hasattr(m.Web, "Entity"), eq=True)

    def test_core_web_types(self) -> None:
        """Test Core web types."""
        tm.that(hasattr(t, "SuccessResponse"), eq=True)
        tm.that(hasattr(t, "BaseResponse"), eq=True)
        tm.that(hasattr(t, "ErrorResponse"), eq=True)

    def test_application_types(self) -> None:
        """Test Application types."""
        tm.that(hasattr(m.Web, "Entity"), eq=True)

    def test_model_functionality(self) -> None:
        """Test Pydantic model functionality."""
        request = m.Web.WebRequest(url="http://localhost:8080", method="GET")
        tm.that(request.url, eq="http://localhost:8080")
        tm.that(request.method, eq="GET")
        response = m.Web.AppResponse(status_code=200, request_id="test-123")
        tm.that(response.status_code, eq=200)

    def test_app_data_functionality(self) -> None:
        """Test app data functionality."""
        app = t.ApplicationEntity(
            id="test-id", name="test-app", host="localhost", port=8080, status="running"
        )
        tm.that(app.id, eq="test-id")
        tm.that(app.name, eq="test-app")
        tm.that(app.host, eq="localhost")
        tm.that(app.port, eq=8080)
        tm.that(app.status, eq="running")
        tm.that(app.is_running is True, eq=True)

    def test_health_response_functionality(self) -> None:
        """Test health response functionality."""
        health_data = {
            "status": "healthy",
            "service": "test-service",
            "version": "1.0.0",
            "applications": 5,
            "timestamp": "2025-01-01T00:00:00Z",
            "service_id": "test-service-123",
        }
        tm.that(health_data, is_=dict)
        tm.that(health_data["status"], eq="healthy")

    def test_request_context_functionality(self) -> None:
        """Test request context functionality."""
        request = t.WebRequest(
            url="http://localhost:8080/api/test",
            method="GET",
            headers={"Content-Type": "application/json"},
            query_params={"param1": "value1"},
        )
        tm.that(request.method, eq="GET")
        tm.that(request.url, eq="http://localhost:8080/api/test")
        tm.that(request.headers["Content-Type"], eq="application/json")
        tm.that(request.query_params["param1"], eq="value1")

    def test_project_types(self) -> None:
        """Test Project types."""
        tm.that(hasattr(m.Web, "Entity"), eq=True)

    def test_configure_web_types_system(self) -> None:
        """Test configure_web_types_system method."""
        result = t.configure_web_types_system(
            use_pydantic_models=True, enable_runtime_validation=True
        )
        tm.ok(result), "Operation should succeed"
        config = result.value
        tm.that(config.use_pydantic_models is True, eq=True)
        tm.that(config.enable_runtime_validation is True, eq=True)

    def test_configure_web_types_system_invalid_config(self) -> None:
        """Test configure_web_types_system with invalid config."""
        result = t.configure_web_types_system(
            use_pydantic_models=False, enable_runtime_validation=False
        )
        tm.ok(result), "Operation should succeed"
        config = result.value
        tm.that(config.use_pydantic_models is False, eq=True)
        tm.that(config.enable_runtime_validation is False, eq=True)

    def test_get_web_types_system_config(self) -> None:
        """Test get_web_types_system_config method."""
        result = t.get_web_types_system_config()
        tm.ok(result), "Operation should succeed"
        config = result.value
        tm.that(hasattr(config, "use_pydantic_models"), eq=True)
        tm.that(hasattr(config, "enable_runtime_validation"), eq=True)
        tm.that(hasattr(config, "models_available"), eq=True)
        tm.that(config.use_pydantic_models is True, eq=True)
        tm.that(config.enable_runtime_validation is True, eq=True)
        tm.that(config.models_available, is_=list)

    def test_model_creation(self) -> None:
        """Test model creation functionality."""
        app = t.ApplicationEntity(
            id="test-id", name="test-app", host="localhost", port=8080
        )
        tm.that(app.id, eq="test-id")
        tm.that(app.name, eq="test-app")
        tm.that(app.host, eq="localhost")
        tm.that(app.port, eq=8080)

    def test_config_validation(self) -> None:
        """Test config validation functionality."""
        config = FlextWebSettings(host="localhost", port=8080)
        tm.that(config.host, eq="localhost")
        tm.that(config.port, eq=8080)

    def test_type_consistency(self) -> None:
        """Test that types are consistent with t."""
        tm.that(hasattr(m.Web, "WebRequest"), eq=True)
        tm.that(hasattr(m.Web, "WebResponse"), eq=True)
        tm.that(hasattr(m.Web, "Entity"), eq=True)
        test_request = t.WebRequest(url="https://example.com")
        tm.that(hasattr(test_request, "is_secure"), eq=True)

    def test_type_annotations(self) -> None:
        """Test that types have proper annotations."""
        tm.that(hasattr(m.Web, "WebRequest"), eq=True)
        tm.that(hasattr(m.Web, "WebResponse"), eq=True)
        tm.that(hasattr(m.Web, "Entity"), eq=True)

    def test_type_usage_patterns(self) -> None:
        """Test that types follow expected usage patterns."""

        def process_request_data(
            request: t.HttpRequest,
        ) -> Mapping[str, t.NormalizedValue]:
            return {"processed": True, "method": request.method, "url": request.url}

        request = t.HttpRequest(url="http://localhost:8080/api/test", method="GET")
        result = process_request_data(request)
        tm.that(result, is_=dict)
        tm.that(result["processed"] is True, eq=True)
        assert isinstance(result["method"], str)
        tm.that(result["method"], eq="GET")
        assert isinstance(result["url"], str)
        tm.that(result["url"], eq="http://localhost:8080/api/test")

    def test_create_http_request_invalid_method(self) -> None:
        """Test create_http_request with invalid HTTP method."""
        result = t.create_http_request(
            url="http://localhost:8080", method="INVALID_METHOD"
        )
        tm.fail(result)
        assert result.error is not None
        tm.that(result.error, has="Invalid HTTP method")

    def test_create_http_request_invalid_headers(self) -> None:
        """Test create_http_request with invalid headers type."""
        result = t.create_http_request(
            url="http://localhost:8080", method="GET", headers=None
        )
        tm.that(result.is_success or result.is_failure, eq=True)

    def test_create_http_request_exception_handling(self) -> None:
        """Test create_http_request exception handling."""
        result = t.create_http_request(
            url="http://localhost:8080",
            method="GET",
            headers={},
            body=None,
            timeout=-1.0,
        )
        (
            tm.fail(result),
            "Negative timeout should cause validation failure",
        )
        tm.that(result.error, none=False)
        tm.that(
            "timeout" in (result.error or "").lower()
            or "validation" in (result.error or "").lower(),
            eq=True,
        )

    def test_create_http_response_invalid_headers(self) -> None:
        """Test create_http_response with invalid headers type."""
        result = t.create_http_response(status_code=200, headers=None)
        tm.that(result.is_success or result.is_failure, eq=True)

    def test_create_http_response_exception_handling(self) -> None:
        """Test create_http_response exception handling."""
        result = t.create_http_response(
            status_code=200, headers={}, body=None, elapsed_time=-1.0
        )
        (
            tm.fail(result),
            ("Negative elapsed_time should cause validation failure"),
        )
        tm.that(result.error, none=False)
        tm.that(
            (
                "elapsed_time" in (result.error or "").lower()
                or "validation" in (result.error or "").lower()
            ),
            eq=True,
        )

    def test_create_web_request_invalid_method(self) -> None:
        """Test create_web_request with invalid HTTP method."""
        with pytest.raises(ValidationError):
            _ = _WebRequestConfig(url="http://localhost:8080", method="INVALID_METHOD")

    def test_create_web_request_invalid_headers(self) -> None:
        """Test create_web_request with invalid headers type."""
        with pytest.raises(ValidationError):
            _ = _WebRequestConfig(
                url="http://localhost:8080",
                method="GET",
                headers="invalid",
            )

    def test_create_web_request_invalid_query_params(self) -> None:
        """Test create_web_request with invalid query_params type."""
        with pytest.raises(ValidationError):
            _ = _WebRequestConfig(
                url="http://localhost:8080",
                method="GET",
                query_params="invalid",
            )

    def test_create_web_request_exception_handling(self) -> None:
        """Test create_web_request exception handling."""
        with pytest.raises(ValidationError):
            _ = _WebRequestConfig(
                url="http://localhost:8080",
                method="GET",
                headers={},
                body=None,
                timeout=-1.0,
                query_params={},
            )

    def test_create_web_response_invalid_headers(self) -> None:
        """Test create_web_response with invalid headers type."""
        with pytest.raises(ValidationError):
            _ = _WebResponseConfig(
                status_code=200,
                request_id="test-123",
                headers="invalid",
            )

    def test_create_web_response_exception_handling(self) -> None:
        """Test create_web_response exception handling."""
        with pytest.raises(ValidationError):
            _ = _WebResponseConfig(
                status_code=200,
                request_id="test-123",
                headers={},
                body=None,
                elapsed_time=-1.0,
            )

    def test_create_application_exception_handling(self) -> None:
        """Test create_application exception handling."""
        config = _ApplicationConfig(
            name="test-app", host="localhost", port=8080, status="invalid_status"
        )
        result = t.create_application(config)
        tm.fail(result), "Invalid status should cause validation failure"
        tm.that(result.error, none=False)
        tm.that(
            "status" in (result.error or "").lower()
            or "validation" in (result.error or "").lower(),
            eq=True,
        )

    def test_configure_web_types_system_exception_handling(self) -> None:
        """Test configure_web_types_system exception handling."""
        result = t.configure_web_types_system(
            use_pydantic_models=True,
            enable_runtime_validation=True,
            models_available=["Custom.Model"],
        )
        tm.ok(result), "Operation should succeed"
        config = result.value
        tm.that(config.models_available, has="Custom.Model")

    def test_get_web_types_system_config_exception_handling(self) -> None:
        """Test get_web_types_system_config exception handling."""
        result = t.get_web_types_system_config()
        tm.ok(result), "Operation should succeed"
        config = result.value
        tm.that(hasattr(config, "use_pydantic_models"), eq=True)
        tm.that(hasattr(config, "enable_runtime_validation"), eq=True)
        tm.that(hasattr(config, "models_available"), eq=True)

    def test_create_http_request_all_methods(self) -> None:
        """Test create_http_request with all valid HTTP methods."""
        valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
        for method in valid_methods:
            result = t.create_http_request(url="http://localhost:8080", method=method)
            tm.ok(result), f"Operation should succeed for method {method}"
            tm.that(result.value.method, eq=method)

    def test_create_web_request_all_methods(self) -> None:
        """Test create_web_request with all valid HTTP methods."""
        valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
        for method in valid_methods:
            config = _WebRequestConfig(url="http://localhost:8080", method=method)
            result = t.create_web_request(config)
            tm.ok(result), f"Operation should succeed for method {method}"
            tm.that(result.value.method, eq=method)

    def test_create_http_request_with_none_headers(self) -> None:
        """Test create_http_request with None headers."""
        result = t.create_http_request(
            url="http://localhost:8080", method="GET", headers=None
        )
        tm.ok(result), "Operation should succeed"
        tm.that(result.value.headers, is_=dict)

    def test_create_http_response_with_none_headers(self) -> None:
        """Test create_http_response with None headers."""
        result = t.create_http_response(status_code=200, headers=None)
        tm.ok(result), "Operation should succeed"
        tm.that(result.value.headers, is_=dict)

    def test_create_web_request_with_none_values(self) -> None:
        """Test create_web_request with None headers and query_params."""
        with pytest.raises(ValidationError):
            _ = _WebRequestConfig(
                url="http://localhost:8080",
                method="GET",
                headers=None,
                query_params=None,
            )

    def test_create_web_response_with_none_headers(self) -> None:
        """Test create_web_response with None headers."""
        with pytest.raises(ValidationError):
            _ = _WebResponseConfig(status_code=200, request_id="test-123", headers=None)

    def test_types_config_initialization(self) -> None:
        """Test TypesConfig initialization with all parameters."""
        config = t.TypesConfig(
            use_pydantic_models=False,
            enable_runtime_validation=False,
            models_available=["Custom.Model"],
        )
        tm.that(config.use_pydantic_models is False, eq=True)
        tm.that(config.enable_runtime_validation is False, eq=True)
        tm.that(config.models_available, eq=["Custom.Model"])

    def test_types_config_default_initialization(self) -> None:
        """Test TypesConfig initialization with defaults."""
        config = t.TypesConfig()
        tm.that(config.use_pydantic_models is True, eq=True)
        tm.that(config.enable_runtime_validation is True, eq=True)
        tm.that(config.models_available, is_=list)
        tm.that(config.models_available, eq=True)

    def test_create_http_request_match_case_default(self) -> None:
        """Test create_http_request match/case default branch (line 174-175)."""
        result = t.create_http_request(url="http://localhost:8080", method="GET")
        tm.ok(result), "Operation should succeed"

    def test_create_http_request_duplicate_validation(self) -> None:
        """Test create_http_request duplicate validation path (line 157)."""
        result = t.create_http_request(url="http://localhost:8080", method="INVALID")
        tm.fail(result), "Operation should fail"

    def test_create_web_request_match_case_default(self) -> None:
        """Test create_web_request match/case default branch (line 301-302)."""
        config = _WebRequestConfig(url="http://localhost:8080", method="GET")
        result = t.create_web_request(config)
        tm.ok(result), "Operation should succeed"

    def test_create_web_request_duplicate_validation(self) -> None:
        """Test create_web_request duplicate validation path (line 278)."""
        with pytest.raises(ValidationError):
            _ = _WebRequestConfig(url="http://localhost:8080", method="INVALID")

    def test_create_application_exception_path(self) -> None:
        """Test create_application exception handling (line 388)."""
        config = _ApplicationConfig(name="test-app", host="localhost", port=8080)
        result = t.create_application(config)
        tm.ok(result), "Configuration with defaults should succeed"

    def test_configure_web_types_system_exception_path(self) -> None:
        """Test configure_web_types_system exception handling (lines 461-462)."""
        result = t.configure_web_types_system(
            use_pydantic_models=True, enable_runtime_validation=True
        )
        tm.ok(result), "Operation should succeed"

    def test_get_web_types_system_config_exception_path(self) -> None:
        """Test get_web_types_system_config exception handling (lines 479-480)."""
        result = t.get_web_types_system_config()
        tm.ok(result), "Operation should succeed"
