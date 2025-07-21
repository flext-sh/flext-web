"""Domain entities for FLEXT-WEB.

Built on flext-core foundation using DDD patterns.
Web-specific domain models for Django enterprise application.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from flext_core.domain.pydantic_base import DomainEntity, DomainEvent, Field
from flext_core.domain.types import EntityId, FlextConstants, UserId


class PageType(StrEnum):
    """Web page types using StrEnum for type safety."""

    DASHBOARD = "dashboard"
    PIPELINE = "pipeline"
    PLUGIN = "plugin"
    SETTINGS = "settings"
    MONITORING = "monitoring"
    DOCUMENTATION = "documentation"
    API = "api"


class ViewMode(StrEnum):
    """View modes for different interfaces using StrEnum."""

    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"


class NotificationType(StrEnum):
    """Notification types using StrEnum for type safety."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"


class NotificationPriority(StrEnum):
    """Notification priority levels using StrEnum."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class Project(DomainEntity):
    """Project domain entity for web interface."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=FlextConstants.MAX_ENTITY_NAME_LENGTH,  # type: ignore[attr-defined]
        description="Project name",
    )
    description: str | None = Field(
        None,
        max_length=FlextConstants.MAX_ERROR_MESSAGE_LENGTH,  # type: ignore[attr-defined]
        description="Project description",
    )

    # Project details
    repository_url: str | None = Field(None, description="Git repository URL")
    branch: str = Field(default="main", description="Default branch")

    # Status
    active: bool = Field(default=True, description="Project active status")
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Creation timestamp",
    )

    # Owner
    owner_id: UserId | None = Field(None, description="Project owner")

    def activate(self) -> None:
        """Activate the project."""
        self.active = True

    def deactivate(self) -> None:
        """Deactivate the project."""
        self.active = False


class Pipeline(DomainEntity):
    """Pipeline domain entity for web interface."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=FlextConstants.MAX_ENTITY_NAME_LENGTH,  # type: ignore[attr-defined]
        description="Pipeline name",
    )
    description: str | None = Field(
        None,
        max_length=FlextConstants.MAX_ERROR_MESSAGE_LENGTH,  # type: ignore[attr-defined]
        description="Pipeline description",
    )

    # Pipeline configuration
    config: dict[str, Any] = Field(
        default_factory=dict,
        description="Pipeline configuration",
    )
    schedule: str | None = Field(None, description="Cron schedule expression")

    # Relationships
    project_id: EntityId = Field(..., description="Associated project ID")

    # Status
    enabled: bool = Field(default=True, description="Pipeline enabled status")
    last_run: datetime | None = Field(None, description="Last execution time")
    next_run: datetime | None = Field(None, description="Next scheduled run")

    # Execution state
    running: bool = Field(default=False, description="Currently running status")
    run_count: int = Field(default=0, ge=0, description="Total execution count")
    success_count: int = Field(default=0, ge=0, description="Successful executions")

    def start_run(self) -> None:
        """Mark pipeline as running."""
        self.running = True
        self.last_run = datetime.now()
        self.run_count += 1

    def complete_run(self, success: bool) -> None:
        """Complete pipeline run."""
        self.running = False
        if success:
            self.success_count += 1

    def enable(self) -> None:
        """Enable the pipeline."""
        self.enabled = True

    def disable(self) -> None:
        """Disable the pipeline."""
        self.enabled = False


class Deployment(DomainEntity):
    """Deployment domain entity for web interface."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=FlextConstants.MAX_ENTITY_NAME_LENGTH,  # type: ignore[attr-defined]
        description="Deployment name",
    )

    # Deployment details
    project_id: EntityId = Field(..., description="Associated project ID")
    pipeline_id: EntityId | None = Field(None, description="Associated pipeline ID")

    # Version information
    version: str = Field(..., description="Deployment version")
    commit_hash: str | None = Field(None, description="Git commit hash")

    # Environment
    environment: str = Field(..., description="Deployment environment")
    target_url: str | None = Field(None, description="Deployment target URL")

    # Status
    status: str = Field(default="pending", description="Deployment status")
    deployed_at: datetime | None = Field(None, description="Deployment timestamp")

    # Metadata
    deployed_by: UserId | None = Field(None, description="User who deployed")
    notes: str | None = Field(None, description="Deployment notes")

    def mark_deployed(self, user_id: UserId | None = None) -> None:
        """Mark deployment as completed."""
        self.status = "deployed"
        self.deployed_at = datetime.now()
        self.deployed_by = user_id

    def mark_failed(self) -> None:
        """Mark deployment as failed."""
        self.status = "failed"


class DashboardWidget(DomainEntity):
    """Dashboard widget domain entity."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=FlextConstants.MAX_ENTITY_NAME_LENGTH,  # type: ignore[attr-defined]
        description="Widget name",
    )
    widget_type: str = Field(
        ...,
        min_length=1,
        max_length=FlextConstants.MAX_ENTITY_NAME_LENGTH,  # type: ignore[attr-defined]
        description="Widget type identifier",
    )

    # Position
    x: int = Field(default=0, ge=0, description="X position on grid")
    y: int = Field(default=0, ge=0, description="Y position on grid")
    width: int = Field(default=4, ge=1, le=12, description="Widget width")
    height: int = Field(default=4, ge=1, le=12, description="Widget height")

    # Configuration
    config: dict[str, Any] = Field(
        default_factory=dict,
        description="Widget configuration",
    )

    # Data source
    data_source: str | None = Field(None, description="Data source identifier")
    query: str | None = Field(None, description="Data query")
    refresh_interval: int = Field(
        default=FlextConstants.DEFAULT_TIMEOUT,  # type: ignore[attr-defined]
        ge=5,
        description="Refresh interval in seconds",
    )

    # Appearance
    title: str | None = Field(None, description="Widget title")
    description: str | None = Field(
        None,
        max_length=FlextConstants.MAX_ERROR_MESSAGE_LENGTH,  # type: ignore[attr-defined]
        description="Widget description",
    )

    # Status
    enabled: bool = Field(default=True, description="Widget enabled status")

    # Access control
    user_id: UserId | None = Field(None, description="Widget owner")
    is_public: bool = Field(default=False, description="Public widget flag")

    def update_position(self, x: int, y: int, width: int, height: int) -> None:
        """Update widget position and size."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def update_config(self, config: dict[str, Any]) -> None:
        """Update widget configuration."""
        self.config = config


class WebPage(DomainEntity):
    """Web page domain entity."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=FlextConstants.MAX_ENTITY_NAME_LENGTH,  # type: ignore[attr-defined]
        description="Page title",
    )
    slug: str = Field(
        ...,
        min_length=1,
        max_length=FlextConstants.MAX_ENTITY_NAME_LENGTH,  # type: ignore[attr-defined]
        description="URL slug",
    )
    page_type: PageType = Field(
        default=PageType.DASHBOARD,
        description="Page type",
    )

    # Content
    content: str | None = Field(None, description="Page content")
    template: str | None = Field(None, description="Template name")

    # Navigation
    parent_page_id: EntityId | None = Field(None, description="Parent page ID")
    menu_order: int = Field(default=0, description="Menu order")

    # SEO
    meta_title: str | None = Field(None, description="Meta title")
    meta_description: str | None = Field(None, description="Meta description")
    meta_keywords: list[str] = Field(
        default_factory=list,
        description="Meta keywords",
    )

    # Status
    published: bool = Field(default=False, description="Published status")
    published_at: datetime | None = Field(None, description="Publication time")

    # Access control
    user_id: UserId | None = Field(None, description="Page owner")
    is_public: bool = Field(default=True, description="Public page flag")
    requires_auth: bool = Field(default=False, description="Requires authentication")

    def publish(self) -> None:
        """Publish the page."""
        self.published = True
        self.published_at = datetime.now()

    def unpublish(self) -> None:
        """Unpublish the page."""
        self.published = False
        self.published_at = None


class UserSession(DomainEntity):
    """User web session domain entity."""

    user_id: UserId = Field(..., description="Associated user ID")
    session_token: str = Field(..., min_length=1, description="Session token")

    # Session details
    ip_address: str | None = Field(None, description="Client IP address")
    user_agent: str | None = Field(None, description="User agent string")
    browser: str | None = Field(None, description="Browser name")
    os: str | None = Field(None, description="Operating system")
    device: str | None = Field(None, description="Device type")

    # Activity
    last_activity: datetime = Field(
        default_factory=datetime.now,
        description="Last activity timestamp",
    )
    current_page: str | None = Field(None, description="Current page")

    # Preferences
    preferences: dict[str, Any] = Field(
        default_factory=dict,
        description="User preferences",
    )
    view_mode: ViewMode = Field(
        default=ViewMode.LIGHT,
        description="View mode preference",
    )

    # Expiration
    expires_at: datetime = Field(..., description="Session expiration time")

    # Status
    active: bool = Field(default=True, description="Session active status")

    @property
    def is_expired(self) -> bool:
        """Check if session is expired."""
        return datetime.now() > self.expires_at

    @property
    def is_valid(self) -> bool:
        """Check if session is valid."""
        return self.active and not self.is_expired

    def update_activity(self, page: str | None = None) -> None:
        """Update session activity."""
        self.last_activity = datetime.now()
        if page:
            self.current_page = page

    def update_preferences(self, preferences: dict[str, Any]) -> None:
        """Update user preferences."""
        self.preferences.update(preferences)

    def end_session(self) -> None:
        """End the session."""
        self.active = False


class WebNotification(DomainEntity):
    """Web notification domain entity."""

    user_id: UserId = Field(..., description="Target user ID")
    title: str = Field(
        ...,
        min_length=1,
        max_length=FlextConstants.MAX_ENTITY_NAME_LENGTH,  # type: ignore[attr-defined]
        description="Notification title",
    )
    message: str = Field(
        ...,
        min_length=1,
        max_length=FlextConstants.MAX_ERROR_MESSAGE_LENGTH,  # type: ignore[attr-defined]
        description="Notification message",
    )

    # Type and priority
    notification_type: NotificationType = Field(
        default=NotificationType.INFO,
        description="Notification type",
    )
    priority: NotificationPriority = Field(
        default=NotificationPriority.NORMAL,
        description="Notification priority",
    )

    # Status
    read: bool = Field(default=False, description="Read status")
    read_at: datetime | None = Field(None, description="Read timestamp")

    # Action
    action_url: str | None = Field(None, description="Action URL")
    action_label: str | None = Field(None, description="Action label")

    # Expiration
    expires_at: datetime | None = Field(None, description="Expiration time")

    @property
    def is_expired(self) -> bool:
        """Check if notification is expired."""
        return self.expires_at is not None and datetime.now() > self.expires_at

    def mark_as_read(self) -> None:
        """Mark notification as read."""
        self.read = True
        self.read_at = datetime.now()


# Domain Events
class ProjectCreatedEvent(DomainEvent):
    """Event raised when project is created."""

    project_id: EntityId = Field(..., description="Project ID")
    project_name: str = Field(..., description="Project name")
    owner_id: UserId | None = Field(None, description="Project owner")


class PipelineExecutedEvent(DomainEvent):
    """Event raised when pipeline is executed."""

    pipeline_id: EntityId = Field(..., description="Pipeline ID")
    pipeline_name: str = Field(..., description="Pipeline name")
    success: bool = Field(..., description="Execution success status")
    duration_seconds: float | None = Field(None, description="Execution duration")


class DeploymentCompletedEvent(DomainEvent):
    """Event raised when deployment is completed."""

    deployment_id: EntityId = Field(..., description="Deployment ID")
    project_id: EntityId = Field(..., description="Project ID")
    environment: str = Field(..., description="Target environment")
    success: bool = Field(..., description="Deployment success status")


class PagePublishedEvent(DomainEvent):
    """Event raised when page is published."""

    page_id: EntityId = Field(..., description="Page ID")
    page_title: str = Field(..., description="Page title")
    page_type: PageType = Field(..., description="Page type")


class UserSessionStartedEvent(DomainEvent):
    """Event raised when user session starts."""

    session_id: EntityId = Field(..., description="Session ID")
    user_id: UserId = Field(..., description="User ID")
    user_agent: str | None = Field(None, description="User agent string")
    ip_address: str | None = Field(None, description="Client IP address")


class UserSessionEndedEvent(DomainEvent):
    """Event raised when user session ends."""

    session_id: EntityId = Field(..., description="Session ID")
    user_id: UserId = Field(..., description="User ID")
    duration_minutes: int | None = Field(
        None,
        description="Session duration in minutes",
    )
    pages_viewed: int | None = Field(None, description="Number of pages viewed")


class NotificationCreatedEvent(DomainEvent):
    """Event raised when notification is created."""

    notification_id: EntityId = Field(..., description="Notification ID")
    user_id: UserId = Field(..., description="Target user ID")
    title: str = Field(..., description="Notification title")
    notification_type: NotificationType = Field(..., description="Notification type")
    priority: NotificationPriority = Field(..., description="Notification priority")


# Rebuild models to resolve forward references
Project.model_rebuild()
Pipeline.model_rebuild()
Deployment.model_rebuild()
DashboardWidget.model_rebuild()
WebPage.model_rebuild()
UserSession.model_rebuild()
WebNotification.model_rebuild()
ProjectCreatedEvent.model_rebuild()
PipelineExecutedEvent.model_rebuild()
DeploymentCompletedEvent.model_rebuild()
PagePublishedEvent.model_rebuild()
UserSessionStartedEvent.model_rebuild()
UserSessionEndedEvent.model_rebuild()
NotificationCreatedEvent.model_rebuild()
