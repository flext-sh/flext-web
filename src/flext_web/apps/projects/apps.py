"""FLEXT Projects Django App Configuration - Project Management.

This module configures the Projects application for the FLEXT Django
web interface, providing enterprise project management capabilities.
"""

from __future__ import annotations


class ProjectsConfig:
    """Django application configuration for Project Management.

    Configures the projects application that handles enterprise project
    creation, template management, deployment tracking, and team collaboration
    within the FLEXT Meltano Enterprise platform.

    Features:
        - Project CRUD operations with templates
        - Team member management and permissions
        - Deployment tracking and environment management
        - Integration with Meltano project structure
        - Enterprise audit trails and compliance

    Attributes:
        default_auto_field: Uses BigAutoField for primary keys
        name: Full Python path to the application
        verbose_name: Human-readable name for REDACTED_LDAP_BIND_PASSWORD interface

    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "flext_web.apps.projects"
    verbose_name = "Projects"
