"""FLEXT Users Django Models - Enterprise User Management.

This module defines database models for enterprise user management,
extending Django's built-in User model with enterprise features.

Author:
            Datacosmos
Date: 2025-06-22
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, ClassVar

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# from flext_core.config.domain_config import get_domain_constants

if TYPE_CHECKING:

    from django.db.models.query import QuerySet


class UserProfile(models.Model):
    """Extended user profile for enterprise features.

    Extends Django's built-in User model with enterprise-specific
    fields and functionality for comprehensive user management.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    # Enterprise profile information
    employee_id = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
    )
    department = models.CharField(
        max_length=100,
        blank=True,
    )
    job_title = models.CharField(max_length=150, blank=True)
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="direct_reports",
    )

    # Contact information
    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )
    office_location = models.CharField(
        max_length=200,
        blank=True,
    )
    timezone = models.CharField(
        max_length=50,
        default="UTC",
    )

    # Enterprise settings
    preferred_language = models.CharField(
        max_length=10,
        default="en",
    )
    notification_preferences: models.JSONField = models.JSONField(default=dict)
    dashboard_settings: models.JSONField = models.JSONField(default=dict)

    # Account status
    is_enterprise_REDACTED_LDAP_BIND_PASSWORD = models.BooleanField(
        default=False,
    )
    is_project_manager = models.BooleanField(
        default=False,
    )
    account_locked = models.BooleanField(default=False)
    last_password_change = models.DateTimeField(null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(
        default=0,
    )
    last_failed_login = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        """Meta configuration for UserProfile model."""

        db_table = "flext_user_profiles"
        ordering: ClassVar[list[str]] = ["user__username"]
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

        indexes: ClassVar[list[models.Index]] = [
            models.Index(fields=["employee_id"]),
            models.Index(fields=["department"]),
            models.Index(fields=["manager"]),
        ]

    def __str__(self) -> str:
        return f"{self.user.username} Profile"

    @property
    def full_name(self) -> str:
        """Get the user's full name.

        Returns:
            The user's full name or username if name is not available.

        """
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return full_name or str(self.user.username)

    @property
    def display_name(self) -> str:
        """Get the user's display name.

        Returns:
            The user's display name or username if name is not available.

        """
        if self.user.first_name:
            return f"{self.user.first_name} {self.user.last_name}".strip()
        return str(self.user.username)

    def is_manager_of(self, user: User) -> bool:
        """Check if this user is a manager of another user.

        Args:
            user: The user to check management relationship for.

        Returns:
            True if this user is a manager of the given user, False otherwise.

        """
        try:
            profile = user.profile
        except AttributeError:
            return False
        else:
            return profile.manager == self.user

    def get_direct_reports(self) -> QuerySet[User]:
        """Get all users who report directly to this user.

        Returns:
            QuerySet of Users who report directly to this user.

        """
        return User.objects.filter(profile__manager=self.user)

    def reset_failed_login_attempts(self) -> None:
        """Reset the failed login attempts counter.

        Resets the failed login attempts to zero and clears the last failed login timestamp.
        """
        self.failed_login_attempts = 0
        self.last_failed_login = None  # type: ignore[assignment]
        self.save(update_fields=["failed_login_attempts", "last_failed_login"])

    def record_failed_login(self, ip_address: str | None = None) -> None:
        """Record a failed login attempt.

        Args:
            ip_address: The IP address of the failed login attempt.

        """
        self.failed_login_attempts += 1
        self.last_failed_login = timezone.now()
        if ip_address:
            self.last_login_ip = ip_address
        self.save(
            update_fields=[
                "failed_login_attempts",
                "last_failed_login",
                "last_login_ip",
            ],
        )


class Organization(models.Model):
    """Organization model for enterprise multi-tenancy.

    Represents organizational units within the enterprise for
    hierarchical access control and resource organization.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # Organizational hierarchy
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    level = models.IntegerField(
        default=0,
    )  # Depth in hierarchy

    # Organization settings
    settings: models.JSONField = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

    # Contact information
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(
        max_length=20,
        blank=True,
    )
    address = models.TextField(blank=True)

    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_organizations",
    )

    class Meta:
        """Meta configuration for Organization model."""

        db_table = "flext_organizations"
        ordering: ClassVar[list[str]] = ["level", "name"]
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

        indexes: ClassVar[list[models.Index]] = [
            models.Index(fields=["parent"]),
            models.Index(fields=["level"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return self.display_name

    def get_all_children(self) -> QuerySet[Organization]:
        """Get all direct child organizations.

        Returns:
            QuerySet of Organizations that are direct children of this organization.

        """
        return Organization.objects.filter(parent=self)

    def get_all_members(self) -> QuerySet[User]:
        """Get all members of this organization and its child organizations.

        Returns:
            QuerySet of Users who are members of this organization or its children.

        """
        org_ids = [self.id, *list(self.get_all_children().values_list("id", flat=True))]
        return User.objects.filter(organizationmembership__organization_id__in=org_ids)


class OrganizationMembership(models.Model):
    """Organization membership with role-based access control.

    Manages user membership in organizations with specific roles
    for enterprise access control and permission management.:
    """

    class Role(models.TextChoices):
        """Organization role enumeration."""

        MEMBER = "member", "Member"
        ADMIN = "REDACTED_LDAP_BIND_PASSWORD", "Admin"
        OWNER = "owner", "Owner"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER,
    )

    # Membership details
    joined_at = models.DateTimeField(
        auto_now_add=True,
    )
    invited_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="sent_invitations",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        """Meta configuration for OrganizationMembership model."""

        db_table = "flext_organization_memberships"
        unique_together: ClassVar[list[list[str]]] = [["organization", "user"]]
        ordering: ClassVar[list[str]] = ["role", "user__username"]
        verbose_name = "Organization Membership"
        verbose_name_plural = "Organization Memberships"

    def __str__(self) -> str:
        return f"{self.user.username} - {self.organization.name} ({self.role})"


class UserActivity(models.Model):
    """User activity tracking for audit trails and compliance.

    Tracks user actions throughout the system for security
    auditing and compliance reporting requirements.
    """

    class ActionType(models.TextChoices):
        """User action type enumeration."""

        LOGIN = "login", "Login"
        LOGOUT = "logout", "Logout"
        PASSWORD_CHANGE = "password_change", "Password Change"
        PROFILE_UPDATE = "profile_update", "Profile Update"
        PROJECT_CREATE = "project_create", "Project Create"
        PROJECT_UPDATE = "project_update", "Project Update"
        PROJECT_DELETE = "project_delete", "Project Delete"
        DEPLOYMENT = "deployment", "Deployment"
        ADMIN_ACTION = "REDACTED_LDAP_BIND_PASSWORD_action", "Admin Action"
        API_ACCESS = "api_access", "API Access"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="activities",
    )
    action_type = models.CharField(
        max_length=50,
        choices=ActionType.choices,
    )

    # Action details
    description = models.CharField(max_length=500)
    target_object_type = models.CharField(
        max_length=100,
        blank=True,
    )  # Content type
    target_object_id = models.CharField(
        max_length=100,
        blank=True,
    )  # Object ID
    metadata: models.JSONField[dict[str, object], dict[str, object]] = models.JSONField(
        default=dict,
    )  # Additional context

    # Request context
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )
    user_agent = models.TextField(blank=True)
    session_key = models.CharField(
        max_length=40,
        blank=True,
    )

    # Timestamp
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        """Meta configuration for UserActivity model."""

        db_table = "flext_user_activities"
        ordering: ClassVar[list[str]] = ["-timestamp"]
        verbose_name = "User Activity"
        verbose_name_plural = "User Activities"

        indexes: ClassVar[list[models.Index]] = [
            models.Index(fields=["user", "timestamp"]),
            models.Index(fields=["action_type", "timestamp"]),
            models.Index(fields=["ip_address"]),
            models.Index(fields=["timestamp"]),
        ]

    def __str__(self) -> str:
        user_name = getattr(self.user, "username", str(self.user))
        action_display = getattr(
            self,
            "get_action_type_display",
            lambda: str(self.action_type),
        )()
        return f"{user_name} - {action_display} - {self.timestamp}"

    @classmethod
    def log_activity(
        cls,
        *,
        user: User,
        action_type: ActionType,
        description: str,
        target_object_type: str = "",
        target_object_id: str = "",
        metadata: dict[str, object] | None = None,
        ip_address: str | None = None,
        user_agent: str = "",
        session_key: str = "",
    ) -> UserActivity:
        """Log a user activity for audit trails.

        Args:
            user: The user who performed the action.
            action_type: The type of action performed.
            description: Description of the action.
            target_object_type: Type of object targeted by the action.
            target_object_id: ID of the object targeted by the action.
            metadata: Additional metadata about the action.
            ip_address: IP address of the user.
            user_agent: User agent string.
            session_key: Session key for the user.

        Returns:
            The created UserActivity instance.

        """
        return cls.objects.create(
            user=user,
            action_type=action_type,
            description=description,
            target_object_type=target_object_type,
            target_object_id=target_object_id,
            metadata=metadata or {},
            ip_address=ip_address,
            user_agent=user_agent,
            session_key=session_key,
        )


class APIKey(models.Model):
    """API key model for programmatic access.

    Manages API keys for users to access the FLEXT platform
    programmatically with proper access control and monitoring.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )
    name = models.CharField(max_length=255)

    # Key details
    key = models.CharField(
        max_length=64,
        unique=True,
    )  # Hashed key
    prefix = models.CharField(
        max_length=8,
    )  # First 8 chars for identification

    # Permissions and limits
    scopes: models.JSONField[list[str], list[str]] = models.JSONField(
        default=list,
    )  # List of allowed scopes
    rate_limit = models.IntegerField(
        default=1000,  # Default rate limit
    )  # Requests per hour

    # Status and lifecycle
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    usage_count = models.IntegerField(default=0)

    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    created_by_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    class Meta:
        """Meta configuration for APIKey model."""

        db_table = "flext_api_keys"
        ordering: ClassVar[list[str]] = ["-created_at"]
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"

        indexes: ClassVar[list[models.Index]] = [
            models.Index(fields=["user"]),
            models.Index(fields=["prefix"]),
            models.Index(fields=["is_active", "expires_at"]),
        ]

    def __str__(self) -> str:
        user_name = getattr(self.user, "username", str(self.user))
        return f"{user_name} - {self.name} ({self.prefix}***)"

    @property
    def is_expired(self) -> bool:
        """Check if the API key has expired.

        Returns:
            True if the API key has expired, False otherwise.

        """
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    @property
    def is_valid(self) -> bool:
        """Check if the API key is valid.

        Returns:
            True if the API key is active and not expired, False otherwise.

        """
        return self.is_active and not self.is_expired

    def record_usage(self) -> None:
        """Record usage of this API key.

        Increments the usage count and updates the last used timestamp.
        """
        self.usage_count += 1
        self.last_used_at = timezone.now()
        self.save(update_fields=["usage_count", "last_used_at"])
