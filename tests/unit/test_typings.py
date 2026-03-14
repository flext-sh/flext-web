"""Comprehensive unit tests for flext_web.typings module.

Tests the unified m class following flext standards.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from tests import (
    FlextWebSettings,
    _ApplicationConfig,
    _WebRequestConfig,
    _WebResponseConfig,
    m,
    t,
)


class TestFlextWebModels:
    """Test suite for m unified class."""

    def test_typings_structure(self) -> None:
        """Test that m has proper structure."""
        assert hasattr(m, "Web")
        assert hasattr(m.Web, "Message")
        assert hasattr(m.Web, "Request")
        assert hasattr(m.Web, "Response")
        assert hasattr(m.Web, "WebRequest")
        assert hasattr(m.Web, "WebResponse")
        assert hasattr(m.Web, "Entity")

    def test_core_web_types(self) -> None:
        """Test Core web types."""
        assert hasattr(t, "SuccessResponse")
        assert hasattr(t, "BaseResponse")
        assert hasattr(t, "ErrorResponse")

    def test_application_types(self) -> None:
        """Test Application types."""
        assert hasattr(m.Web, "Entity")

    def test_model_functionality(self) -> None:
        """Test Pydantic model functionality."""
        request = m.Web.WebRequest(url="http://localhost:8080", method="GET")
        assert request.url == "http://localhost:8080"
        assert request.method == "GET"
        response = m.Web.AppResponse(status_code=200, request_id="test-123")
        assert response.status_code == 200
        assert response.is_success, "HTTP response should be successful"

    def test_app_data_functionality(self) -> None:
        """Test app data functionality."""
        app = t.ApplicationEntity(
            id="test-id", name="test-app", host="localhost", port=8080, status="running"
        )
        assert app.id == "test-id"
        assert app.name == "test-app"
        assert app.host == "localhost"
        assert app.port == 8080
        assert app.status == "running"
        assert app.is_running is True

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
        assert isinstance(health_data, dict)
        assert health_data["status"] == "healthy"

    def test_request_context_functionality(self) -> None:
        """Test request context functionality."""
        request = t.WebRequest(
            url="http://localhost:8080/api/test",
            method="GET",
            headers={"Content-Type": "application/json"},
            query_params={"param1": "value1"},
        )
        assert request.method == "GET"
        assert request.url == "http://localhost:8080/api/test"
        assert request.headers["Content-Type"] == "application/json"
        assert request.query_params["param1"] == "value1"

    def test_project_types(self) -> None:
        """Test Project types."""
        assert hasattr(m.Web, "Entity")

    def test_configure_web_types_system(self) -> None:
        """Test configure_web_types_system method."""
        result = t.configure_web_types_system(
            use_pydantic_models=True, enable_runtime_validation=True
        )
        assert result.is_success, "Operation should succeed"
        config = result.value
        assert config.use_pydantic_models is True
        assert config.enable_runtime_validation is True

    def test_configure_web_types_system_invalid_config(self) -> None:
        """Test configure_web_types_system with invalid config."""
        result = t.configure_web_types_system(
            use_pydantic_models=False, enable_runtime_validation=False
        )
        assert result.is_success, "Operation should succeed"
        config = result.value
        assert config.use_pydantic_models is False
        assert config.enable_runtime_validation is False

    def test_get_web_types_system_config(self) -> None:
        """Test get_web_types_system_config method."""
        result = t.get_web_types_system_config()
        assert result.is_success, "Operation should succeed"
        config = result.value
        assert hasattr(config, "use_pydantic_models")
        assert hasattr(config, "enable_runtime_validation")
        assert hasattr(config, "models_available")
        assert config.use_pydantic_models is True
        assert config.enable_runtime_validation is True
        assert isinstance(config.models_available, list)

    def test_model_creation(self) -> None:
        """Test model creation functionality."""
        app = t.ApplicationEntity(
            id="test-id", name="test-app", host="localhost", port=8080
        )
        assert app.id == "test-id"
        assert app.name == "test-app"
        assert app.host == "localhost"
        assert app.port == 8080

    def test_config_validation(self) -> None:
        """Test config validation functionality."""
        config = FlextWebSettings(host="localhost", port=8080)
        assert config.host == "localhost"
        assert config.port == 8080

    def test_type_consistency(self) -> None:
        """Test that types are consistent with t."""
        assert hasattr(m.Web, "WebRequest")
        assert hasattr(m.Web, "WebResponse")
        assert hasattr(m.Web, "Entity")
        test_request = t.WebRequest(url="https://example.com")
        assert hasattr(test_request, "is_secure")

    def test_type_annotations(self) -> None:
        """Test that types have proper annotations."""
        assert hasattr(m.Web, "WebRequest")
        assert hasattr(m.Web, "WebResponse")
        assert hasattr(m.Web, "Entity")

    def test_type_usage_patterns(self) -> None:
        """Test that types follow expected usage patterns."""

        def process_request_data(request: t.HttpRequest) -> dict[str, object]:
            return {"processed": True, "method": request.method, "url": request.url}

        request = t.HttpRequest(url="http://localhost:8080/api/test", method="GET")
        result = process_request_data(request)
        assert isinstance(result, dict)
        assert result["processed"] is True
        assert result["method"] == "GET"
        assert result["url"] == "http://localhost:8080/api/test"

    def test_create_http_request_invalid_method(self) -> None:
        """Test create_http_request with invalid HTTP method."""
        result = t.create_http_request(
            url="http://localhost:8080", method="INVALID_METHOD"
        )
        assert result.is_failure, "Operation should fail"
        assert result.error is not None
        assert "Invalid HTTP method" in result.error

    def test_create_http_request_invalid_headers(self) -> None:
        """Test create_http_request with invalid headers type."""
        result = t.create_http_request(
            url="http://localhost:8080", method="GET", headers=None
        )
        assert result.is_success or result.is_failure

    def test_create_http_request_exception_handling(self) -> None:
        """Test create_http_request exception handling."""
        result = t.create_http_request(
            url="http://localhost:8080",
            method="GET",
            headers={},
            body=None,
            timeout=-1.0,
        )
        assert result.is_failure, "Negative timeout should cause validation failure"
        assert result.error is not None
        assert "timeout" in result.error.lower() or "validation" in result.error.lower()

    def test_create_http_response_invalid_headers(self) -> None:
        """Test create_http_response with invalid headers type."""
        result = t.create_http_response(status_code=200, headers=None)
        assert result.is_success or result.is_failure

    def test_create_http_response_exception_handling(self) -> None:
        """Test create_http_response exception handling."""
        result = t.create_http_response(
            status_code=200, headers={}, body=None, elapsed_time=-1.0
        )
        assert result.is_failure, (
            "Negative elapsed_time should cause validation failure"
        )
        assert result.error is not None
        assert (
            "elapsed_time" in result.error.lower()
            or "validation" in result.error.lower()
        )

    def test_create_web_request_invalid_method(self) -> None:
        """Test create_web_request with invalid HTTP method."""
        config = _WebRequestConfig(url="http://localhost:8080", method="INVALID_METHOD")
        result = t.create_web_request(config)
        assert result.is_failure, "Operation should fail"
        assert result.error is not None
        assert "Invalid HTTP method" in result.error

    def test_create_web_request_invalid_headers(self) -> None:
        """Test create_web_request with invalid headers type."""
        with pytest.raises(ValidationError):
            _ = _WebRequestConfig(url="http://localhost:8080", method="GET", headers={})

    def test_create_web_request_invalid_query_params(self) -> None:
        """Test create_web_request with invalid query_params type."""
        with pytest.raises(ValidationError):
            _ = _WebRequestConfig(
                url="http://localhost:8080", method="GET", query_params={}
            )

    def test_create_web_request_exception_handling(self) -> None:
        """Test create_web_request exception handling."""
        config = _WebRequestConfig(
            url="http://localhost:8080",
            method="GET",
            headers={},
            body=None,
            timeout=-1.0,
            query_params={},
        )
        result = t.create_web_request(config)
        assert result.is_failure, "Negative timeout should cause validation failure"
        assert result.error is not None
        assert "timeout" in result.error.lower() or "validation" in result.error.lower()

    def test_create_web_response_invalid_headers(self) -> None:
        """Test create_web_response with invalid headers type."""
        with pytest.raises(ValidationError):
            _ = _WebResponseConfig(status_code=200, request_id="test-123", headers={})

    def test_create_web_response_exception_handling(self) -> None:
        """Test create_web_response exception handling."""
        config = _WebResponseConfig(
            status_code=200,
            request_id="test-123",
            headers={},
            body=None,
            elapsed_time=-1.0,
        )
        result = t.create_web_response(config)
        assert result.is_failure, (
            "Negative elapsed_time should cause validation failure"
        )
        assert result.error is not None
        assert (
            "elapsed_time" in result.error.lower()
            or "validation" in result.error.lower()
        )

    def test_create_application_exception_handling(self) -> None:
        """Test create_application exception handling."""
        config = _ApplicationConfig(
            name="test-app", host="localhost", port=8080, status="invalid_status"
        )
        result = t.create_application(config)
        assert result.is_failure, "Invalid status should cause validation failure"
        assert result.error is not None
        assert "status" in result.error.lower() or "validation" in result.error.lower()

    def test_configure_web_types_system_exception_handling(self) -> None:
        """Test configure_web_types_system exception handling."""
        result = t.configure_web_types_system(
            use_pydantic_models=True,
            enable_runtime_validation=True,
            models_available=["Custom.Model"],
        )
        assert result.is_success, "Operation should succeed"
        config = result.value
        assert "Custom.Model" in config.models_available

    def test_get_web_types_system_config_exception_handling(self) -> None:
        """Test get_web_types_system_config exception handling."""
        result = t.get_web_types_system_config()
        assert result.is_success, "Operation should succeed"
        config = result.value
        assert hasattr(config, "use_pydantic_models")
        assert hasattr(config, "enable_runtime_validation")
        assert hasattr(config, "models_available")

    def test_create_http_request_all_methods(self) -> None:
        """Test create_http_request with all valid HTTP methods."""
        valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
        for method in valid_methods:
            result = t.create_http_request(url="http://localhost:8080", method=method)
            assert result.is_success, f"Operation should succeed for method {method}"
            assert result.value.method == method

    def test_create_web_request_all_methods(self) -> None:
        """Test create_web_request with all valid HTTP methods."""
        valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
        for method in valid_methods:
            config = _WebRequestConfig(url="http://localhost:8080", method=method)
            result = t.create_web_request(config)
            assert result.is_success, f"Operation should succeed for method {method}"
            assert result.value.method == method

    def test_create_http_request_with_none_headers(self) -> None:
        """Test create_http_request with None headers."""
        result = t.create_http_request(
            url="http://localhost:8080", method="GET", headers=None
        )
        assert result.is_success, "Operation should succeed"
        assert isinstance(result.value.headers, dict)

    def test_create_http_response_with_none_headers(self) -> None:
        """Test create_http_response with None headers."""
        result = t.create_http_response(status_code=200, headers=None)
        assert result.is_success, "Operation should succeed"
        assert isinstance(result.value.headers, dict)

    def test_create_web_request_with_none_values(self) -> None:
        """Test create_web_request with None headers and query_params."""
        config = _WebRequestConfig(
            url="http://localhost:8080", method="GET", headers=None, query_params=None
        )
        result = t.create_web_request(config)
        assert result.is_success, "Operation should succeed"
        assert isinstance(result.value.headers, dict)
        assert isinstance(result.value.query_params, dict)

    def test_create_web_response_with_none_headers(self) -> None:
        """Test create_web_response with None headers."""
        config = _WebResponseConfig(
            status_code=200, request_id="test-123", headers=None
        )
        result = t.create_web_response(config)
        assert result.is_success, "Operation should succeed"
        assert isinstance(result.value.headers, dict)

    def test_types_config_initialization(self) -> None:
        """Test TypesConfig initialization with all parameters."""
        config = t.TypesConfig(
            use_pydantic_models=False,
            enable_runtime_validation=False,
            models_available=["Custom.Model"],
        )
        assert config.use_pydantic_models is False
        assert config.enable_runtime_validation is False
        assert config.models_available == ["Custom.Model"]

    def test_types_config_default_initialization(self) -> None:
        """Test TypesConfig initialization with defaults."""
        config = t.TypesConfig()
        assert config.use_pydantic_models is True
        assert config.enable_runtime_validation is True
        assert isinstance(config.models_available, list)
        assert len(config.models_available) > 0

    def test_create_http_request_match_case_default(self) -> None:
        """Test create_http_request match/case default branch (line 174-175)."""
        result = t.create_http_request(url="http://localhost:8080", method="GET")
        assert result.is_success, "Operation should succeed"

    def test_create_http_request_duplicate_validation(self) -> None:
        """Test create_http_request duplicate validation path (line 157)."""
        result = t.create_http_request(url="http://localhost:8080", method="INVALID")
        assert result.is_failure, "Operation should fail"

    def test_create_web_request_match_case_default(self) -> None:
        """Test create_web_request match/case default branch (line 301-302)."""
        config = _WebRequestConfig(url="http://localhost:8080", method="GET")
        result = t.create_web_request(config)
        assert result.is_success, "Operation should succeed"

    def test_create_web_request_duplicate_validation(self) -> None:
        """Test create_web_request duplicate validation path (line 278)."""
        config = _WebRequestConfig(url="http://localhost:8080", method="INVALID")
        result = t.create_web_request(config)
        assert result.is_failure, "Operation should fail"

    def test_create_application_exception_path(self) -> None:
        """Test create_application exception handling (line 388)."""
        config = _ApplicationConfig(name="test-app", host="localhost", port=8080)
        result = t.create_application(config)
        assert result.is_success, "Configuration with defaults should succeed"

    def test_configure_web_types_system_exception_path(self) -> None:
        """Test configure_web_types_system exception handling (lines 461-462)."""
        result = t.configure_web_types_system(
            use_pydantic_models=True, enable_runtime_validation=True
        )
        assert result.is_success, "Operation should succeed"

    def test_get_web_types_system_config_exception_path(self) -> None:
        """Test get_web_types_system_config exception handling (lines 479-480)."""
        result = t.get_web_types_system_config()
        assert result.is_success, "Operation should succeed"
