"""Test configuration for flext-web.

Provides pytest fixtures and configuration for testing web interface functionality
using FastAPI, frontend components, and flext-core patterns.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Generator


# Test environment setup
@pytest.fixture(autouse=True)
def set_test_environment() -> Generator[None]:
    """Set test environment variables."""
    os.environ["FLEXT_ENV"] = "test"
    os.environ["FLEXT_LOG_LEVEL"] = "debug"
    os.environ["FLEXT_WEB_DEBUG"] = "true"
    yield
    # Cleanup
    os.environ.pop("FLEXT_ENV", None)
    os.environ.pop("FLEXT_LOG_LEVEL", None)
    os.environ.pop("FLEXT_WEB_DEBUG", None)


# Web application fixtures
@pytest.fixture
def web_app() -> dict[str, str]:
    """Web application for testing."""
    # Simple mock app for testing
    return {"app": "test_app"}


@pytest.fixture
async def test_client(web_app: Any) -> AsyncGenerator[Any]:
    """HTTP test client for web application."""
    from fastapi.testclient import TestClient

    with TestClient(web_app) as client:
        yield client


@pytest.fixture
def async_test_client(web_app: Any) -> Any:
    """Async HTTP test client for web application."""

    # Simple mock client for testing
    class MockClient:
        async def get(self, url: str) -> dict[str, Any]:
            return {"status": 200, "url": url}

        async def post(self, url: str, **kwargs: object) -> dict[str, Any]:
            return {"status": 200, "url": url, "data": kwargs}

    return MockClient()


# Authentication fixtures
@pytest.fixture
def test_user_data() -> dict[str, Any]:
    """Test user data for authentication."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "test_password",
        "roles": ["user"],
        "permissions": ["read", "write"],
    }


@pytest.fixture
def REDACTED_LDAP_BIND_PASSWORD_user_data() -> dict[str, Any]:
    """Test REDACTED_LDAP_BIND_PASSWORD user data."""
    return {
        "username": "REDACTED_LDAP_BIND_PASSWORD",
        "email": "REDACTED_LDAP_BIND_PASSWORD@example.com",
        "password": "REDACTED_LDAP_BIND_PASSWORD_password",
        "roles": ["REDACTED_LDAP_BIND_PASSWORD", "user"],
        "permissions": ["read", "write", "REDACTED_LDAP_BIND_PASSWORD"],
    }


@pytest.fixture
def auth_headers(test_user_data: dict[str, Any]) -> dict[str, str]:
    """Authentication headers for test requests."""
    # In real implementation, this would generate valid JWT tokens
    return {
        "Authorization": "Bearer test_token",
        "Content-Type": "application/json",
    }


@pytest.fixture
def REDACTED_LDAP_BIND_PASSWORD_auth_headers(REDACTED_LDAP_BIND_PASSWORD_user_data: dict[str, Any]) -> dict[str, str]:
    """Admin authentication headers for test requests."""
    return {
        "Authorization": "Bearer REDACTED_LDAP_BIND_PASSWORD_token",
        "Content-Type": "application/json",
    }


# Dashboard fixtures
@pytest.fixture
def dashboard_data() -> dict[str, Any]:
    """Sample dashboard data for testing."""
    return {
        "pipelines": {
            "total": 25,
            "running": 5,
            "succeeded": 18,
            "failed": 2,
        },
        "executions": {
            "today": 100,
            "this_week": 650,
            "this_month": 2800,
        },
        "plugins": {
            "total": 15,
            "enabled": 12,
            "disabled": 3,
        },
        "system": {
            "cpu_usage": 45.2,
            "memory_usage": 67.8,
            "disk_usage": 23.5,
            "uptime": "5 days, 3 hours",
        },
    }


@pytest.fixture
def pipeline_list_data() -> list[dict[str, Any]]:
    """Sample pipeline list for testing."""
    return [
        {
            "id": "pipeline-1",
            "name": "Data Import Pipeline",
            "description": "Import data from external API",
            "status": "running",
            "last_run": "2025-01-20T10:30:00Z",
            "next_run": "2025-01-21T10:30:00Z",
            "success_rate": 95.5,
        },
        {
            "id": "pipeline-2",
            "name": "ETL Processing",
            "description": "Transform and load data",
            "status": "succeeded",
            "last_run": "2025-01-20T09:00:00Z",
            "next_run": "2025-01-21T09:00:00Z",
            "success_rate": 98.2,
        },
        {
            "id": "pipeline-3",
            "name": "Data Export",
            "description": "Export processed data",
            "status": "failed",
            "last_run": "2025-01-20T08:15:00Z",
            "next_run": "2025-01-21T08:15:00Z",
            "success_rate": 87.3,
        },
    ]


# Form fixtures
@pytest.fixture
def pipeline_form_data() -> dict[str, Any]:
    """Pipeline form data for testing."""
    return {
        "name": "Test Pipeline",
        "description": "Pipeline created for testing",
        "extractor": "tap-postgres",
        "loader": "target-snowflake",
        "transform": "dbt",
        "schedule": "0 9 * * *",  # Daily at 9 AM
        "config": {
            "database_url": "postgresql://localhost/test",
            "warehouse": "test_warehouse",
        },
    }


@pytest.fixture
def plugin_form_data() -> dict[str, Any]:
    """Plugin form data for testing."""
    return {
        "name": "test-plugin",
        "type": "extractor",
        "package": "tap-test",
        "version": "1.0.0",
        "config": {
            "api_key": "test_key",
            "base_url": "https://api.test.com",
        },
    }


# WebSocket fixtures
@pytest.fixture
async def websocket_client(web_app: Any) -> AsyncGenerator[Any]:
    """WebSocket test client."""
    from fastapi.testclient import TestClient

    with TestClient(web_app) as client, client.websocket_connect("/ws") as websocket:
        yield websocket


# Static files fixtures
@pytest.fixture
def static_files_config() -> dict[str, Any]:
    """Static files configuration for testing."""
    return {
        "static_directory": "static",
        "templates_directory": "templates",
        "static_url": "/static",
        "cdn_enabled": False,
        "compression": True,
    }


# Theme and UI fixtures
@pytest.fixture
def ui_theme_config() -> dict[str, Any]:
    """UI theme configuration for testing."""
    return {
        "theme": "light",
        "primary_color": "#007bff",
        "secondary_color": "#6c757d",
        "success_color": "#28a745",
        "warning_color": "#ffc107",
        "error_color": "#dc3545",
        "font_family": "Inter, sans-serif",
    }


# API response fixtures
@pytest.fixture
def api_success_response() -> dict[str, Any]:
    """Standard API success response."""
    return {
        "success": True,
        "data": {"message": "Operation completed successfully"},
        "timestamp": "2025-01-20T12:00:00Z",
    }


@pytest.fixture
def api_error_response() -> dict[str, Any]:
    """Standard API error response."""
    return {
        "success": False,
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Invalid input data",
            "details": {"field": "name", "error": "required"},
        },
        "timestamp": "2025-01-20T12:00:00Z",
    }


# Pytest markers for test categorization
def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "web: Web interface tests")
    config.addinivalue_line("markers", "api: API endpoint tests")
    config.addinivalue_line("markers", "auth: Authentication tests")
    config.addinivalue_line("markers", "ui: User interface tests")
    config.addinivalue_line("markers", "websocket: WebSocket tests")
    config.addinivalue_line("markers", "slow: Slow tests")


# Performance fixtures
@pytest.fixture
def performance_config() -> dict[str, Any]:
    """Performance testing configuration."""
    return {
        "max_response_time": 2000,  # milliseconds
        "concurrent_users": 10,
        "test_duration": 60,  # seconds
        "ramp_up_time": 10,  # seconds
    }


# Configuration fixtures
@pytest.fixture
def web_config() -> dict[str, Any]:
    """Web application configuration for testing."""
    return {
        "host": "127.0.0.1",
        "port": 8080,
        "debug": True,
        "reload": False,
        "workers": 1,
        "cors_origins": ["http://localhost:3000"],
        "session_secret": "test_secret_key",
        "csrf_enabled": True,
        "rate_limiting": {
            "enabled": True,
            "requests_per_minute": 100,
        },
    }


# Database fixtures for web sessions
@pytest.fixture
def web_session_data() -> dict[str, Any]:
    """Web session data for testing."""
    return {
        "session_id": "test_session_123",
        "user_id": "user_123",
        "username": "testuser",
        "roles": ["user"],
        "csrf_token": "csrf_token_123",
        "created_at": "2025-01-20T10:00:00Z",
        "expires_at": "2025-01-20T22:00:00Z",
    }


# Mock external services
@pytest.fixture
def mock_pipeline_service() -> Any:
    """Mock pipeline service for testing."""

    class MockPipelineService:
        async def list_pipelines(self) -> list[dict[str, Any]]:
            return []

        async def get_pipeline(self, pipeline_id: str) -> dict[str, Any]:
            return {"id": pipeline_id, "name": "Test Pipeline"}

        async def create_pipeline(self, data: dict[str, Any]) -> dict[str, Any]:
            return {"id": "new_pipeline", **data}

    return MockPipelineService()


@pytest.fixture
def mock_plugin_service() -> Any:
    """Mock plugin service for testing."""

    class MockPluginService:
        async def list_plugins(self) -> list[dict[str, Any]]:
            return []

        async def get_plugin(self, plugin_name: str) -> dict[str, Any]:
            return {"name": plugin_name, "status": "enabled"}

        async def install_plugin(self, data: dict[str, Any]) -> dict[str, Any]:
            return {"name": data["name"], "status": "installed"}

    return MockPluginService()
