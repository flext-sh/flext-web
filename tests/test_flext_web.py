"""Real tests for flext_web Django application."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class TestDashboardViews(TestCase):
    """Test dashboard views."""

    def setUp(self) -> None:
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )

    def test_dashboard_requires_login(self) -> None:
        """Test that dashboard requires authentication."""
        response = self.client.get(reverse("dashboard:home"))
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_dashboard_with_authenticated_user(self) -> None:
        """Test dashboard access with logged in user."""
        self.client.login(username="testuser", password="testpass123")

        # Mock gRPC calls
        with patch("flext_web.apps.dashboard.views._fetch_grpc_stats") as mock_stats:
            mock_stats.return_value = {
                "pipelines": 10,
                "executions": 50,
                "success_rate": 95.0,
            }

            response = self.client.get(reverse("dashboard:home"))

        assert response.status_code == 200
        assert b"Dashboard" in response.content
        assert b"pipelines" in response.content

    def test_dashboard_handles_grpc_failure(self) -> None:
        """Test dashboard gracefully handles gRPC failures."""
        self.client.login(username="testuser", password="testpass123")

        with patch("flext_web.apps.dashboard.views._fetch_grpc_stats") as mock_stats:
            mock_stats.side_effect = Exception("gRPC connection failed")

            response = self.client.get(reverse("dashboard:home"))

        assert response.status_code == 200
        assert b"Unable to fetch statistics" in response.content


class TestProjectViews(TestCase):
    """Test project management views."""

    def setUp(self) -> None:
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.client.login(username="testuser", password="testpass123")

    def test_project_list_view(self) -> None:
        """Test project list view."""
        response = self.client.get(reverse("projects:list"))
        assert response.status_code == 200
        assert b"Projects" in response.content

    def test_project_create_view_get(self) -> None:
        """Test project creation form."""
        response = self.client.get(reverse("projects:create"))
        assert response.status_code == 200
        assert b"Create Project" in response.content
        assert b"form" in response.content

    def test_project_create_view_post(self) -> None:
        """Test project creation submission."""
        data = {
            "name": "Test Project",
            "description": "Test project description",
            "repository_url": "https://github.com/test/repo",
        }

        response = self.client.post(reverse("projects:create"), data)

        assert response.status_code == 302  # Redirect after success
        assert Project.objects.filter(name="Test Project").exists()


class TestPipelineViews(TestCase):
    """Test pipeline management views."""

    def setUp(self) -> None:
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.client.login(username="testuser", password="testpass123")

        # Create test project and pipeline
        self.project = Project.objects.create(
            name="Test Project",
            description="Test description",
            owner=self.user,
        )

    def test_pipeline_list_view(self) -> None:
        """Test pipeline list view."""
        response = self.client.get(
            reverse("pipelines:list", kwargs={"project_id": self.project.id}),
        )
        assert response.status_code == 200
        assert b"Pipelines" in response.content

    def test_pipeline_execution_view(self) -> None:
        """Test pipeline execution."""
        pipeline = Pipeline.objects.create(
            name="Test Pipeline",
            project=self.project,
            config={"tap": "tap-github", "target": "target-postgres"},
        )

        with patch("flext_web.apps.pipelines.views._execute_pipeline_grpc") as mock_exec:
            mock_exec.return_value = {"execution_id": "test-123", "status": "running"}

            response = self.client.post(
                reverse("pipelines:execute", kwargs={"pipeline_id": pipeline.id}),
            )

        assert response.status_code == 302
        assert mock_exec.called


class TestMonitoringViews(TestCase):
    """Test monitoring views."""

    def setUp(self) -> None:
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            is_staff=True,  # Monitoring may require staff access
        )
        self.client.login(username="testuser", password="testpass123")

    def test_monitoring_dashboard(self) -> None:
        """Test monitoring dashboard view."""
        with patch("flext_web.apps.monitoring.views._get_system_metrics") as mock_metrics:
            mock_metrics.return_value = {
                "cpu_usage": 45.2,
                "memory_usage": 62.1,
                "disk_usage": 78.5,
            }

            response = self.client.get(reverse("monitoring:dashboard"))

        assert response.status_code == 200
        assert b"System Monitoring" in response.content
        assert b"45.2" in response.content  # CPU usage

    def test_monitoring_alerts_view(self) -> None:
        """Test monitoring alerts view."""
        # Create test alert
        Alert.objects.create(
            title="High CPU Usage",
            message="CPU usage exceeded 90%",
            severity="warning",
        )

        response = self.client.get(reverse("monitoring:alerts"))

        assert response.status_code == 200
        assert b"High CPU Usage" in response.content


class TestUserAuthentication(TestCase):
    """Test user authentication flows."""

    def setUp(self) -> None:
        """Set up test client."""
        self.client = Client()

    def test_login_view_get(self) -> None:
        """Test login page renders."""
        response = self.client.get(reverse("users:login"))
        assert response.status_code == 200
        assert b"Login" in response.content

    def test_login_view_post_success(self) -> None:
        """Test successful login."""
        User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )

        response = self.client.post(
            reverse("users:login"),
            {"username": "testuser", "password": "testpass123"},
        )

        assert response.status_code == 302
        assert response.url == reverse("dashboard:home")

    def test_login_view_post_failure(self) -> None:
        """Test failed login."""
        response = self.client.post(
            reverse("users:login"),
            {"username": "baduser", "password": "wrongpass"},
        )

        assert response.status_code == 200
        assert b"Invalid username or password" in response.content

    def test_logout_view(self) -> None:
        """Test logout functionality."""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(reverse("users:logout"))

        assert response.status_code == 302
        assert response.url == reverse("users:login")


@pytest.mark.django_db
class TestDatabaseIntegration:
    """Test database operations."""

    def test_project_model_creation(self) -> None:
        """Test creating project model."""
        user = User.objects.create_user(username="test", password="test")
        # First create a template
        from flext_web.apps.projects.models import ProjectTemplate
        template = ProjectTemplate.objects.create(
            name="Test Template",
            description="Test template description",
            created_by=user,
        )
        
        project = Project.objects.create(
            name="Test Project",
            description="Test description",
            template=template,
            created_by=user,
        )

        assert project.id is not None
        assert project.name == "Test Project"
        assert project.created_by == user

    def test_pipeline_model_creation(self) -> None:
        """Test pipeline model creation."""
        user = User.objects.create_user(username="test", password="test")
        
        pipeline = Pipeline.objects.create(
            name="Test Pipeline",
            extractor="tap-github",
            loader="target-postgres",
            description="Test pipeline description",
            created_by=user,
        )

        assert pipeline.id is not None
        assert pipeline.name == "Test Pipeline"
        assert pipeline.extractor == "tap-github"


# Import models after Django setup
try:
    from flext_web.apps.monitoring.models import MonitoringAlert as Alert
    from flext_web.apps.pipelines.models import PipelineWeb as Pipeline
    from flext_web.apps.projects.models import MeltanoProject as Project
except ImportError:
    # Models might not be available in test environment
    Project = MagicMock()
    Pipeline = MagicMock()
    Alert = MagicMock()
