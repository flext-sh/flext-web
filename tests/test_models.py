"""Test Django models for flext-api.web.flext-web."""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model

from flext_web.apps.monitoring.models import MonitoringAlert
from flext_web.apps.pipelines.models import PipelineWeb
from flext_web.apps.projects.models import MeltanoProject, ProjectTemplate

User = get_user_model()


@pytest.mark.django_db
class TestProjectModels:
    """Test project models."""

    def test_project_template_creation(self) -> None:
        """Test creating project template."""
        template = ProjectTemplate.objects.create(
            name="ETL Template",
            description="Template for ETL projects",
            category="etl",
            version="1.0.0",
        )

        assert template.id is not None
        assert template.name == "ETL Template"
        assert template.category == "etl"
        assert template.is_active is True

    def test_meltano_project_creation(self) -> None:
        """Test creating Meltano project."""
        user = User.objects.create_user(
            username="projectowner",
            email="owner@example.com",
            password="testpass123",
        )

        template = ProjectTemplate.objects.create(
            name="Default Template",
            description="Default template",
        )

        project = MeltanoProject.objects.create(
            name="Test ETL Project",
            description="Test ETL project for data integration",
            template=template,
            created_by=user,
            status="active",
        )

        assert project.id is not None
        assert project.name == "Test ETL Project"
        assert project.template == template
        assert project.created_by == user
        assert project.status == "active"
        assert project.is_active is True


@pytest.mark.django_db
class TestPipelineModels:
    """Test pipeline models."""

    def test_pipeline_creation(self) -> None:
        """Test creating pipeline."""
        user = User.objects.create_user(
            username="pipelineowner",
            email="owner@example.com",
            password="testpass123",
        )

        template = ProjectTemplate.objects.create(
            name="Pipeline Template",
            description="Template for pipelines",
        )

        project = MeltanoProject.objects.create(
            name="Test Pipeline Project",
            description="Test project for pipelines",
            template=template,
            created_by=user,
        )

        pipeline = PipelineWeb.objects.create(
            name="Data Sync Pipeline",
            project=project,
            extractor="tap-postgres",
            loader="target-snowflake",
            created_by=user,
        )

        assert pipeline.id is not None
        assert pipeline.name == "Data Sync Pipeline"
        assert pipeline.extractor == "tap-postgres"
        assert pipeline.loader == "target-snowflake"
        assert pipeline.created_by == user
        assert pipeline.status == "draft"  # Default status
        assert pipeline.is_active is True  # Default is_active


@pytest.mark.django_db
class TestMonitoringModels:
    """Test monitoring models."""

    def test_alert_creation(self) -> None:
        """Test creating monitoring alert."""
        alert = MonitoringAlert.objects.create(
            alert_id="test-alert-001",
            title="High CPU Usage",
            description="CPU usage exceeded 90% threshold",
            severity="critical",
            component="monitoring-service",
        )

        assert alert.id is not None
        assert alert.alert_id == "test-alert-001"
        assert alert.title == "High CPU Usage"
        assert alert.severity == "critical"
        assert alert.is_active is True  # Property, not field
        assert alert.resolved is False  # Default value
