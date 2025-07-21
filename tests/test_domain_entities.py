"""Tests for domain entities to improve coverage."""

from __future__ import annotations

import uuid
from datetime import datetime

from flext_web.domain.entities import (
    DashboardWidget,
    Deployment,
    NotificationPriority,
    NotificationType,
    PageType,
    Pipeline,
    Project,
    UserSession,
    ViewMode,
    WebNotification,
    WebPage,
)

# Test UUID constants
TEST_USER_ID = uuid.uuid4()
TEST_PIPELINE_ID = uuid.uuid4()
TEST_PROJECT_ID = uuid.uuid4()


class TestPipeline:
    """Test Pipeline entity methods."""

    def test_pipeline_creation(self) -> None:
        """Test basic pipeline entity creation."""
        project_id = uuid.uuid4()
        pipeline = Pipeline(
            name="Test Pipeline",
            description="Test pipeline description",
            project_id=project_id,
            config={"tap": "tap-postgres", "target": "target-snowflake"},
            schedule=None,
            last_run=None,
            next_run=None,
        )

        assert pipeline.name == "Test Pipeline"
        assert pipeline.description == "Test pipeline description"
        assert pipeline.project_id == project_id
        assert pipeline.config["tap"] == "tap-postgres"
        assert pipeline.enabled is True
        assert pipeline.running is False

    def test_pipeline_str(self) -> None:
        """Test pipeline string representation."""
        pipeline = Pipeline(
            name="ETL Pipeline",
            description="Main ETL pipeline",
            project_id=uuid.uuid4(),
            schedule=None,
            last_run=None,
            next_run=None,
        )

        str_repr = str(pipeline)
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0

    def test_pipeline_run_management(self) -> None:
        """Test pipeline run management methods."""
        pipeline = Pipeline(
            name="Run Test Pipeline",
            description="Test pipeline description",
            project_id=uuid.uuid4(),
            schedule=None,
            last_run=None,
            next_run=None,
        )

        # Test start run
        assert pipeline.running is False
        assert pipeline.run_count == 0

        pipeline.start_run()
        assert pipeline.running is True
        assert pipeline.run_count == 1
        assert pipeline.last_run is not None

        # Test complete run - success
        pipeline.complete_run(success=True)
        assert pipeline.running is False
        assert pipeline.success_count == 1

        # Test another run - failure
        pipeline.start_run()
        pipeline.complete_run(success=False)
        assert pipeline.run_count == 2
        assert pipeline.success_count == 1

    def test_pipeline_enable_disable(self) -> None:
        """Test pipeline enable/disable methods."""
        pipeline = Pipeline(
            name="Enable Test Pipeline",
            description="Test pipeline description",
            project_id=uuid.uuid4(),
            schedule=None,
            last_run=None,
            next_run=None,
        )

        assert pipeline.enabled is True

        pipeline.disable()
        assert pipeline.enabled is False

        pipeline.enable()
        assert pipeline.enabled is True


class TestProject:
    """Test Project entity methods."""

    def test_project_creation(self) -> None:
        """Test basic project entity creation."""
        project = Project(
            name="Test Project",
            description="Test project description",
            repository_url="https://github.com/user/repo",
            branch="main",
            owner_id=TEST_USER_ID,
        )

        assert project.name == "Test Project"
        assert project.description == "Test project description"
        assert project.repository_url == "https://github.com/user/repo"
        assert project.branch == "main"
        assert project.owner_id == TEST_USER_ID
        assert project.active is True

    def test_project_str(self) -> None:
        """Test project string representation."""
        project = Project(
            name="Data Project",
            description="Main data project",
            repository_url="https://github.com/user/repo",
            branch="main",
            owner_id=TEST_USER_ID,
        )

        str_repr = str(project)
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0

    def test_project_activate_deactivate(self) -> None:
        """Test project activation methods."""
        project = Project(
            name="Activity Test Project",
            description="Test activation",
            repository_url="https://github.com/user/repo",
            branch="main",
            owner_id=TEST_USER_ID,
        )

        assert project.active is True

        project.deactivate()
        assert project.active is False

        project.activate()
        assert project.active is True

    def test_project_defaults(self) -> None:
        """Test project default values."""
        project = Project(
            name="Default Project",
        )

        assert project.description is None
        assert project.repository_url is None
        assert project.branch == "main"
        assert project.active is True
        assert project.owner_id is None
        assert project.created_at is not None


class TestWebNotification:
    """Test WebNotification entity methods."""

    def test_web_notification_creation(self) -> None:
        """Test basic web notification creation."""
        notification = WebNotification(
            user_id=TEST_USER_ID,
            title="High CPU Usage",
            message="CPU usage exceeded 90%",
            notification_type=NotificationType.ERROR,
            priority=NotificationPriority.HIGH,
            read=False,
            read_at=None,
            expires_at=None,
            action_url="https://example.com/cpu-alert",
            action_label="View Details",
        )

        assert notification.user_id == TEST_USER_ID
        assert notification.title == "High CPU Usage"
        assert notification.message == "CPU usage exceeded 90%"
        assert notification.notification_type == NotificationType.ERROR
        assert notification.priority == NotificationPriority.HIGH
        assert notification.read is False

    def test_web_notification_str(self) -> None:
        """Test web notification string representation."""
        notification = WebNotification(
            user_id=TEST_USER_ID,
            title="Database Connection",
            message="Database connection timeout",
            notification_type=NotificationType.WARNING,
            read=False,
            read_at=None,
            expires_at=None,
            action_url="https://example.com/database-alert",
            action_label="View Details",
        )

        str_repr = str(notification)
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0

    def test_web_notification_mark_as_read(self) -> None:
        """Test mark notification as read."""
        notification = WebNotification(
            user_id=TEST_USER_ID,
            title="Valid Notification",
            message="Valid notification message",
            notification_type=NotificationType.INFO,
            read=False,
            read_at=None,
            expires_at=None,
            action_url="https://example.com/valid-alert",
            action_label="View Details",
        )

        assert notification.read is False
        assert notification.read_at is None

        notification.mark_as_read()
        assert notification.read is True
        assert notification.read_at is not None

    def test_web_notification_expiration(self) -> None:
        """Test notification expiration."""
        from datetime import timedelta

        # Create expired notification
        past_time = datetime.now() - timedelta(hours=1)
        notification = WebNotification(
            user_id=TEST_USER_ID,
            title="Expired Notification",
            message="This notification is expired",
            expires_at=past_time,
            read=False,
            read_at=None,
            action_url="https://example.com/expired-alert",
            action_label="View Details",
        )

        assert notification.is_expired is True

        # Create future notification
        future_time = datetime.now() + timedelta(hours=1)
        notification2 = WebNotification(
            user_id=TEST_USER_ID,
            title="Future Notification",
            message="This notification expires in the future",
            expires_at=future_time,
            read=False,
            read_at=None,
            action_url="https://example.com/future-alert",
            action_label="View Details",
        )

        assert notification2.is_expired is False


class TestDashboardWidget:
    """Test DashboardWidget entity methods."""

    def test_dashboard_widget_creation(self) -> None:
        """Test basic dashboard widget creation."""
        widget = DashboardWidget(
            name="CPU Monitor",
            widget_type="metric_chart",
            x=0,
            y=0,
            width=6,
            height=4,
            config={"metric": "cpu_usage", "chart_type": "line"},
            user_id=TEST_USER_ID,
            enabled=True,
            data_source="database",
            query="SELECT * FROM cpu_usage",
            title="CPU Usage",
            description="CPU usage over time",
        )

        assert widget.name == "CPU Monitor"
        assert widget.widget_type == "metric_chart"
        assert widget.x == 0
        assert widget.y == 0
        assert widget.width == 6
        assert widget.height == 4
        assert widget.config["metric"] == "cpu_usage"
        assert widget.user_id == TEST_USER_ID
        assert widget.enabled is True

    def test_dashboard_widget_str(self) -> None:
        """Test dashboard widget string representation."""
        widget = DashboardWidget(
            name="Memory Monitor",
            widget_type="gauge",
            enabled=True,
            data_source="database",
            query="SELECT * FROM memory_usage",
            title="Memory Usage",
            description="Memory usage over time",
            user_id=TEST_USER_ID,
        )

        str_repr = str(widget)
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0

    def test_dashboard_widget_position_update(self) -> None:
        """Test widget position update."""
        widget = DashboardWidget(
            name="Position Test Widget",
            widget_type="chart",
            enabled=True,
            data_source="database",
            query="SELECT * FROM memory_usage",
            title="Memory Usage",
            description="Memory usage over time",
            user_id=TEST_USER_ID,
        )

        assert widget.x == 0
        assert widget.y == 0
        assert widget.width == 4
        assert widget.height == 4

        widget.update_position(x=2, y=3, width=8, height=6)
        assert widget.x == 2
        assert widget.y == 3
        assert widget.width == 8
        assert widget.height == 6

    def test_dashboard_widget_config_update(self) -> None:
        """Test widget configuration update."""
        widget = DashboardWidget(
            name="Config Test Widget",
            widget_type="table",
            config={"columns": ["name", "status"]},
            enabled=True,
            data_source="database",
            query="SELECT * FROM memory_usage",
            title="Memory Usage",
            description="Memory usage over time",
            user_id=TEST_USER_ID,
        )

        assert widget.config["columns"] == ["name", "status"]

        new_config = {"columns": ["name", "status", "created"], "sort": "name"}
        widget.update_config(new_config)
        assert widget.config["columns"] == ["name", "status", "created"]
        assert widget.config["sort"] == "name"


class TestUserSession:
    """Test UserSession entity methods."""

    def test_user_session_creation(self) -> None:
        """Test basic user session creation."""
        from datetime import timedelta

        expires_at = datetime.now() + timedelta(hours=24)
        session = UserSession(
            user_id=TEST_USER_ID,
            session_token="token-abc-123",
            ip_address="192.168.1.100",
            user_agent="Mozilla/5.0 Chrome",
            expires_at=expires_at,
            active=True,
            view_mode=ViewMode.LIGHT,
            current_page=None,
            last_activity=datetime.now(),
            preferences={"theme": "dark", "language": "en"},
            created_at=datetime.now(),
            browser="Chrome",
            os="Windows",
            device="Desktop",
        )

        assert session.user_id == TEST_USER_ID
        assert session.session_token == "token-abc-123"
        assert session.ip_address == "192.168.1.100"
        assert session.user_agent == "Mozilla/5.0 Chrome"
        assert session.expires_at == expires_at
        assert session.active is True
        assert session.view_mode == ViewMode.LIGHT

    def test_user_session_str(self) -> None:
        """Test user session string representation."""
        from datetime import timedelta

        session = UserSession(
            user_id=TEST_USER_ID,
            session_token="token-def-456",
            expires_at=datetime.now() + timedelta(hours=12),
            active=True,
            view_mode=ViewMode.LIGHT,
            current_page=None,
            last_activity=datetime.now(),
            preferences={"theme": "dark", "language": "en"},
            created_at=datetime.now(),
            updated_at=datetime.now(),
            browser="Chrome",
            os="Windows",
            device="Desktop",
            ip_address="192.168.1.100",
            user_agent="Mozilla/5.0 Chrome",
        )

        str_repr = str(session)
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0

    def test_user_session_validity(self) -> None:
        """Test session validity checks."""
        from datetime import timedelta

        # Valid session
        future_time = datetime.now() + timedelta(hours=1)
        valid_session = UserSession(
            user_id=TEST_USER_ID,
            session_token="token-valid",
            expires_at=future_time,
            active=True,
            view_mode=ViewMode.LIGHT,
            current_page=None,
            last_activity=datetime.now(),
            preferences={"theme": "dark", "language": "en"},
            created_at=datetime.now(),
            updated_at=datetime.now(),
            browser="Chrome",
            os="Windows",
            device="Desktop",
            ip_address="192.168.1.100",
            user_agent="Mozilla/5.0 Chrome",
        )

        assert valid_session.is_expired is False
        assert valid_session.is_valid is True

        # Expired session
        past_time = datetime.now() - timedelta(hours=1)
        expired_session = UserSession(
            user_id=TEST_USER_ID,
            session_token="token-expired",
            expires_at=past_time,
            active=True,
            view_mode=ViewMode.LIGHT,
            current_page=None,
            last_activity=datetime.now(),
            preferences={"theme": "dark", "language": "en"},
            created_at=datetime.now(),
            updated_at=datetime.now(),
            browser="Chrome",
            os="Windows",
            device="Desktop",
            ip_address="192.168.1.100",
            user_agent="Mozilla/5.0 Chrome",
        )

        assert expired_session.is_expired is True
        assert expired_session.is_valid is False

        # Inactive session
        inactive_session = UserSession(
            user_id=TEST_USER_ID,
            session_token="token-inactive",
            expires_at=future_time,
            active=False,
            view_mode=ViewMode.LIGHT,
            current_page=None,
            last_activity=datetime.now(),
            preferences={"theme": "dark", "language": "en"},
            created_at=datetime.now(),
            updated_at=datetime.now(),
            browser="Chrome",
            os="Windows",
            device="Desktop",
            ip_address="192.168.1.100",
            user_agent="Mozilla/5.0 Chrome",
        )

        assert inactive_session.is_expired is False
        assert inactive_session.is_valid is False

    def test_user_session_activity_update(self) -> None:
        """Test session activity update."""
        from datetime import timedelta

        session = UserSession(
            user_id=TEST_USER_ID,
            session_token="token-activity",
            expires_at=datetime.now() + timedelta(hours=1),
            active=True,
            view_mode=ViewMode.LIGHT,
            current_page=None,
            last_activity=datetime.now(),
            preferences={"theme": "dark", "language": "en"},
            created_at=datetime.now(),
            updated_at=datetime.now(),
            browser="Chrome",
            os="Windows",
            device="Desktop",
            ip_address="192.168.1.100",
            user_agent="Mozilla/5.0 Chrome",
        )

        original_activity = session.last_activity
        assert session.current_page is None

        session.update_activity(page="/dashboard")
        assert session.last_activity > original_activity
        assert session.current_page == "/dashboard"

    def test_user_session_preferences(self) -> None:
        """Test session preferences management."""
        from datetime import timedelta

        session = UserSession(
            user_id=TEST_USER_ID,
            session_token="token-prefs",
            expires_at=datetime.now() + timedelta(hours=1),
            preferences={"theme": "dark", "language": "en"},
            active=True,
            view_mode=ViewMode.LIGHT,
            current_page=None,
            last_activity=datetime.now(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            browser="Chrome",
            os="Windows",
            device="Desktop",
            ip_address="192.168.1.100",
            user_agent="Mozilla/5.0 Chrome",
        )

        assert session.preferences["theme"] == "dark"
        assert session.preferences["language"] == "en"

        session.update_preferences({"theme": "light", "notifications": True})
        assert session.preferences["theme"] == "light"
        assert session.preferences["language"] == "en"
        assert session.preferences["notifications"] is True

    def test_user_session_end(self) -> None:
        """Test session termination."""
        from datetime import timedelta

        session = UserSession(
            user_id=TEST_USER_ID,
            session_token="token-end",
            expires_at=datetime.now() + timedelta(hours=1),
            active=True,
            view_mode=ViewMode.LIGHT,
            current_page=None,
            last_activity=datetime.now(),
            preferences={"theme": "dark", "language": "en"},
            created_at=datetime.now(),
            updated_at=datetime.now(),
            browser="Chrome",
            os="Windows",
            device="Desktop",
            ip_address="192.168.1.100",
            user_agent="Mozilla/5.0 Chrome",
        )

        assert session.active is True

        session.end_session()
        assert session.active is False


class TestWebPage:
    """Test WebPage entity methods."""

    def test_web_page_creation(self) -> None:
        """Test basic web page creation."""
        page = WebPage(
            title="Dashboard",
            slug="dashboard",
            page_type=PageType.DASHBOARD,
            content="Main dashboard page content",
            user_id=TEST_USER_ID,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            published=False,
            published_at=None,
            is_public=True,
        )

        assert page.title == "Dashboard"
        assert page.slug == "dashboard"
        assert page.page_type == PageType.DASHBOARD
        assert page.content == "Main dashboard page content"
        assert page.user_id == TEST_USER_ID
        assert page.published is False
        assert page.is_public is True

    def test_web_page_str(self) -> None:
        """Test web page string representation."""
        page = WebPage(
            title="API Documentation",
            slug="api-docs",
            page_type=PageType.API,
        )

        str_repr = str(page)
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0

    def test_web_page_publish_unpublish(self) -> None:
        """Test page publishing methods."""
        page = WebPage(
            title="Pipeline Guide",
            slug="pipeline-guide",
            page_type=PageType.PIPELINE,
            published=False,
            published_at=None,
            is_public=True,
        )

        assert page.published is False
        assert page.published_at is None

        page.publish()
        assert page.published is True
        assert page.published_at is not None

        page.unpublish()
        assert page.published is False
        assert page.published_at is None

    def test_web_page_meta_data(self) -> None:
        """Test page meta data fields."""
        page = WebPage(
            title="Settings Page",
            slug="settings",
            page_type=PageType.SETTINGS,
            meta_title="FLEXT Settings",
            meta_description="Configure your FLEXT settings",
            meta_keywords=["settings", "configuration", "preferences"],
        )

        assert page.meta_title == "FLEXT Settings"
        assert page.meta_description == "Configure your FLEXT settings"
        assert "settings" in page.meta_keywords
        assert "configuration" in page.meta_keywords


class TestDeployment:
    """Test Deployment entity methods."""

    def test_deployment_creation(self) -> None:
        """Test basic deployment creation."""
        deployment = Deployment(
            name="Production Deploy v1.2.0",
            project_id=TEST_PROJECT_ID,
            version="1.2.0",
            environment="production",
            commit_hash="abc123def456",
            target_url="https://api.example.com",
            status="pending",
            deployed_at=None,
            deployed_by=None,
        )

        assert deployment.name == "Production Deploy v1.2.0"
        assert deployment.project_id == TEST_PROJECT_ID
        assert deployment.version == "1.2.0"
        assert deployment.environment == "production"
        assert deployment.commit_hash == "abc123def456"
        assert deployment.target_url == "https://api.example.com"
        assert deployment.status == "pending"

    def test_deployment_str(self) -> None:
        """Test deployment string representation."""
        deployment = Deployment(
            name="Staging Deploy",
            project_id=TEST_PROJECT_ID,
            version="1.1.0",
            environment="staging",
            status="pending",
            deployed_at=None,
            deployed_by=None,
        )

        str_repr = str(deployment)
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0

    def test_deployment_mark_deployed(self) -> None:
        """Test marking deployment as completed."""
        deployment = Deployment(
            name="Test Deploy",
            project_id=TEST_PROJECT_ID,
            version="1.0.0",
            environment="development",
            status="pending",
        )

        assert deployment.status == "pending"
        assert deployment.deployed_at is None
        assert deployment.deployed_by is None

        deployment.mark_deployed(user_id=TEST_USER_ID)
        assert deployment.status == "deployed"
        assert deployment.deployed_at is not None
        assert deployment.deployed_by == TEST_USER_ID

    def test_deployment_mark_failed(self) -> None:
        """Test marking deployment as failed."""
        deployment = Deployment(
            name="Failed Deploy",
            project_id=TEST_PROJECT_ID,
            version="0.9.0",
            environment="testing",
            status="pending",
        )

        assert deployment.status == "pending"

        deployment.mark_failed()
        assert deployment.status == "failed"

    def test_deployment_with_pipeline(self) -> None:
        """Test deployment with associated pipeline."""
        deployment = Deployment(
            name="Pipeline Deploy",
            project_id=TEST_PROJECT_ID,
            pipeline_id=TEST_PIPELINE_ID,
            version="2.0.0",
            environment="production",
            notes="Automated deployment via pipeline",
        )

        assert deployment.pipeline_id == TEST_PIPELINE_ID
        assert deployment.notes == "Automated deployment via pipeline"
