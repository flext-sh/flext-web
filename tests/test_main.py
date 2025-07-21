"""Tests for main.py universal view."""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import patch

from django.http import JsonResponse
from django.test import RequestFactory, TestCase

from flext_web.main import universal_django_view, urlpatterns


class TestUniversalDjangoView(TestCase):
    """Test universal Django view functionality."""

    def setUp(self) -> None:
        """Set up test request factory."""
        self.factory = RequestFactory()

    def test_universal_view_get_request(self) -> None:
        """Test universal view with GET request."""
        request = self.factory.get("/test-command", {"param1": "value1"})
        request.content_type = "text/html"

        response = universal_django_view(request, "test-command")

        assert isinstance(response, JsonResponse)
        assert response.status_code == 200

        data = json.loads(response.content)
        assert data["command"] == "test-command"
        assert data["method"] == "GET"
        assert data["status"] == "success_fallback"
        assert "data" in data
        assert data["data"]["query_params"] == {"param1": "value1"}

    def test_universal_view_post_request(self) -> None:
        """Test universal view with POST request."""
        request = self.factory.post("/api/pipeline", {"name": "test-pipeline"})
        request.content_type = "application/x-www-form-urlencoded"

        response = universal_django_view(request, "api/pipeline")

        assert isinstance(response, JsonResponse)
        assert response.status_code == 200

        data = json.loads(response.content)
        assert data["command"] == "api/pipeline"
        assert data["method"] == "POST"
        assert data["status"] == "success_fallback"

    def test_universal_view_json_body(self) -> None:
        """Test universal view with JSON body."""
        json_data = {"key": "value", "number": 42}
        request = self.factory.post(
            "/api/data",
            data=json.dumps(json_data),
            content_type="application/json",
        )

        response = universal_django_view(request, "api/data")

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["data"]["json_data"] == json_data

    def test_universal_view_invalid_json_body(self) -> None:
        """Test universal view with invalid JSON body."""
        request = self.factory.post(
            "/api/data",
            data="invalid json {",
            content_type="application/json",
        )

        response = universal_django_view(request, "api/data")

        # Should still work, just without json_data
        assert response.status_code == 200
        data = json.loads(response.content)
        assert "json_data" not in data["data"]

    def test_universal_view_empty_body(self) -> None:
        """Test universal view with empty body."""
        request = self.factory.post("/api/test")
        request.content_type = "application/json"

        response = universal_django_view(request, "api/test")

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["data"]["body"] is None

    def test_universal_view_with_headers(self) -> None:
        """Test universal view captures headers correctly."""
        request = self.factory.get("/test", HTTP_AUTHORIZATION="Bearer token123")

        response = universal_django_view(request, "test")

        assert response.status_code == 200
        data = json.loads(response.content)
        assert "Authorization" in data["data"]["headers"]
        assert data["data"]["headers"]["Authorization"] == "Bearer token123"

    @patch(
        "flext_web.main.PipelineService",
        side_effect=ImportError("Module not found"),
    )
    def test_universal_view_import_error_fallback(self, mock_service: Any) -> None:
        """Test universal view handles ImportError gracefully."""
        request = self.factory.get("/test")

        response = universal_django_view(request, "test")

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["status"] == "fallback_mode"
        assert "message" in data

    def test_universal_view_general_exception(self) -> None:
        """Test universal view handles general exceptions."""
        request = self.factory.get("/test")

        # Mock request.method to raise an exception
        with patch.object(request, "method", side_effect=Exception("Test error")):
            response = universal_django_view(request, "test")

        assert response.status_code == 500
        data = json.loads(response.content)
        assert data["status"] == "error"
        assert "error" in data
        assert data["command"] == "test"


class TestUrlPatterns(TestCase):
    """Test URL patterns are correctly defined."""

    def test_url_patterns_exist(self) -> None:
        """Test that URL patterns are defined."""
        assert len(urlpatterns) == 3

    def test_health_endpoint(self) -> None:
        """Test health endpoint using direct URL pattern."""
        # Get the health endpoint function (third pattern)
        health_view = urlpatterns[2].callback
        response = health_view(None)  # Lambda doesn't use request

        assert isinstance(response, JsonResponse)
        data = json.loads(response.content)
        assert data["status"] == "healthy"

    def test_root_endpoint(self) -> None:
        """Test root endpoint using direct URL pattern."""
        # Get the root endpoint function (second pattern)
        root_view = urlpatterns[1].callback
        response = root_view(None)  # Lambda doesn't use request

        assert isinstance(response, JsonResponse)
        data = json.loads(response.content)
        assert data["service"] == "FLEXT Universal Web"
        assert data["status"] == "active"


class TestMainModuleIntegration(TestCase):
    """Integration tests for main module."""

    def test_module_imports_correctly(self) -> None:
        """Test that all imports work correctly."""
        from flext_web import main

        # Check main components are available
        assert hasattr(main, "universal_django_view")
        assert hasattr(main, "urlpatterns")
        assert len(main.urlpatterns) == 3

    def test_csrf_exempt_decorator_applied(self) -> None:
        """Test that CSRF exempt is applied to universal view."""
        # The view should have the csrf_exempt attribute
        assert hasattr(universal_django_view, "csrf_exempt")
        assert universal_django_view.csrf_exempt
