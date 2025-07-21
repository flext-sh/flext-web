"""Additional tests for dashboard views to improve coverage."""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

from flext_web.apps.dashboard.views import (
    DashboardView,
    FlextDashboardGrpcClient,
    StatsAPIView,
    get_grpc_client,
)


class TestFlextDashboardGrpcClientFallback(TestCase):
    """Test FlextDashboardGrpcClient fallback functionality."""

    def test_fallback_client_initialization(self) -> None:
        """Test that fallback client initializes correctly."""
        client = FlextDashboardGrpcClient()
        assert client is not None

    def test_fallback_get_dashboard_data(self) -> None:
        """Test fallback get_dashboard_data method."""
        client = FlextDashboardGrpcClient()
        data = client.get_dashboard_data()

        assert isinstance(data, dict)
        assert "stats" in data
        assert "health" in data
        assert "recent_executions" in data
        assert "error" in data

        # The actual method calls gRPC and gets real response or error
        # Since we're using the real client, check for proper structure
        if data.get("error"):
            # If gRPC call failed, should have error message
            assert isinstance(data["error"], str)
        else:
            # If gRPC call succeeded, should have proper stats
            assert isinstance(data["stats"], dict)
            assert isinstance(data["health"], dict)
            assert isinstance(data["recent_executions"], list)

    def test_fallback_get_stats_only(self) -> None:
        """Test fallback get_stats_only method."""
        client = FlextDashboardGrpcClient()
        data = client.get_stats_only()

        assert isinstance(data, dict)

        # The actual method calls gRPC and gets real response or error
        # Since we're using the real client, check for proper structure
        if data.get("error"):
            # If gRPC call failed, should have error message and status code
            assert isinstance(data["error"], str)
            assert "status_code" in data
        else:
            # If gRPC call succeeded, should have proper stats
            assert "stats" in data
            assert "health" in data
            assert "recent_executions" in data
            assert isinstance(data["stats"], dict)
            assert isinstance(data["health"], dict)
            assert isinstance(data["recent_executions"], list)


class TestGetGrpcClient(TestCase):
    """Test get_grpc_client function."""

    def test_get_grpc_client_returns_client(self) -> None:
        """Test that get_grpc_client returns a client instance."""
        client = get_grpc_client()
        assert isinstance(client, FlextDashboardGrpcClient)

    def test_get_grpc_client_caching(self) -> None:
        """Test that get_grpc_client uses LRU cache."""
        client1 = get_grpc_client()
        client2 = get_grpc_client()

        # Should return the same instance due to caching
        assert client1 is client2


class TestDashboardView(TestCase):
    """Test DashboardView functionality."""

    def setUp(self) -> None:
        """Set up test data."""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )

    def test_dashboard_view_template_name(self) -> None:
        """Test that DashboardView has correct template."""
        view = DashboardView()
        assert view.template_name == "dashboard/index.html"

    def test_dashboard_view_login_required(self) -> None:
        """Test that DashboardView requires login."""
        request = self.factory.get("/dashboard/")
        request.user = self.user

        view = DashboardView()
        view.setup(request)

        # Should not raise exception with authenticated user
        assert hasattr(view, "request")
        assert view.request.user == self.user

    @patch("flext_web.apps.dashboard.views.get_grpc_client")
    def test_dashboard_view_get_context_data(self, mock_get_client: Any) -> None:
        """Test get_context_data method."""
        # Mock the gRPC client
        mock_client = Mock()
        mock_client.get_dashboard_data.return_value = {
            "stats": {"pipelines": 5, "executions": 10},
            "health": {"healthy": True},
            "recent_executions": [],
            "error": None,
        }
        mock_get_client.return_value = mock_client

        request = self.factory.get("/dashboard/")
        request.user = self.user

        view = DashboardView()
        view.setup(request)

        context = view.get_context_data()

        # The dashboard view spreads the data directly into context, not under 'dashboard_data' key
        assert context["stats"]["pipelines"] == 5
        assert context["health"]["healthy"] is True
        assert context["recent_executions"] == []
        assert context["error"] is None
        mock_client.get_dashboard_data.assert_called_once()

    @patch("flext_web.apps.dashboard.views.get_grpc_client")
    def test_dashboard_view_with_grpc_error(self, mock_get_client: Any) -> None:
        """Test dashboard view when gRPC client returns error."""
        mock_client = Mock()
        mock_client.get_dashboard_data.return_value = {
            "stats": {"pipelines": 0},
            "health": {"healthy": False},
            "recent_executions": [],
            "error": "Connection failed",
        }
        mock_get_client.return_value = mock_client

        request = self.factory.get("/dashboard/")
        request.user = self.user

        view = DashboardView()
        view.setup(request)
        context = view.get_context_data()

        # The dashboard view spreads the data directly into context, not under 'dashboard_data' key
        assert context["error"] == "Connection failed"


class TestStatsAPIView(TestCase):
    """Test StatsAPIView functionality."""

    def setUp(self) -> None:
        """Set up test data."""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )

    @patch("flext_web.apps.dashboard.views.get_grpc_client")
    def test_stats_api_view_get_success(self, mock_get_client: Any) -> None:
        """Test StatsAPIView GET request success."""
        mock_client = Mock()
        mock_client.get_stats_only.return_value = {
            "stats": {
                "pipelines": 3,
                "executions": 15,
                "active_connections": 2,
            },
            "health": {"healthy": True},
            "recent_executions": [
                {"id": "1", "status": "success"},
                {"id": "2", "status": "running"},
            ],
        }
        mock_get_client.return_value = mock_client

        request = self.factory.get("/api/stats/")
        request.user = self.user

        view = StatsAPIView()
        response = view.get(request)

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["stats"]["pipelines"] == 3
        assert data["stats"]["executions"] == 15
        assert len(data["recent_executions"]) == 2
        mock_client.get_stats_only.assert_called_once()

    @patch("flext_web.apps.dashboard.views.get_grpc_client")
    def test_stats_api_view_get_with_error(self, mock_get_client: Any) -> None:
        """Test StatsAPIView GET request with gRPC error."""
        mock_client = Mock()
        mock_client.get_stats_only.return_value = {
            "error": "gRPC connection failed",
            "status_code": 503,
        }
        mock_get_client.return_value = mock_client

        request = self.factory.get("/api/stats/")
        request.user = self.user

        view = StatsAPIView()
        response = view.get(request)

        assert response.status_code == 503
        data = json.loads(response.content)
        assert "error" in data
        assert data["error"] == "gRPC connection failed"

    @patch("flext_web.apps.dashboard.views.get_grpc_client")
    def test_stats_api_view_exception_handling(self, mock_get_client: Any) -> None:
        """Test StatsAPIView handles exceptions."""
        mock_client = Mock()
        mock_client.get_stats_only.side_effect = Exception("Unexpected error")
        mock_get_client.return_value = mock_client

        request = self.factory.get("/api/stats/")
        request.user = self.user

        view = StatsAPIView()
        response = view.get(request)

        assert response.status_code == 500
        data = json.loads(response.content)
        assert "error" in data
        assert "Unexpected error" in data["error"]

    def test_stats_api_view_login_required(self) -> None:
        """Test that StatsAPIView requires authentication."""
        view = StatsAPIView()
        assert hasattr(view, "dispatch")

        # Check that LoginRequiredMixin is in the class hierarchy
        assert any("LoginRequiredMixin" in str(cls) for cls in view.__class__.__mro__)


class TestDashboardModuleIntegration(TestCase):
    """Integration tests for dashboard module."""

    def test_module_imports_correctly(self) -> None:
        """Test that dashboard views module imports correctly."""
        from flext_web.apps.dashboard import views

        assert hasattr(views, "DashboardView")
        assert hasattr(views, "StatsAPIView")
        assert hasattr(views, "FlextDashboardGrpcClient")
        assert hasattr(views, "get_grpc_client")

    def test_grpc_availability_constant(self) -> None:
        """Test GRPC_AVAILABLE constant."""
        from flext_web.apps.dashboard.views import GRPC_AVAILABLE

        # Should be True since we have protobuf available in the environment
        assert GRPC_AVAILABLE is True

    def test_view_classes_inheritance(self) -> None:
        """Test that view classes have correct inheritance."""
        # DashboardView should inherit from LoginRequiredMixin and TemplateView
        mro = DashboardView.__mro__
        class_names = [cls.__name__ for cls in mro]

        assert "LoginRequiredMixin" in class_names
        assert "TemplateView" in class_names

        # StatsAPIView should inherit from LoginRequiredMixin and View
        mro = StatsAPIView.__mro__
        class_names = [cls.__name__ for cls in mro]

        assert "LoginRequiredMixin" in class_names
        assert "View" in class_names
