"""Docker-compatible test configuration for flext-web.

Simplified test configuration that works in Docker containers without
external dependencies like FastAPI. Focuses on Flask-based testing.
"""

from __future__ import annotations

import os
from collections.abc import Generator

import pytest


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
    return {"app": "test_app"}


# Authentication fixtures
@pytest.fixture
def test_user_data() -> dict[str, object]:
    """Test user data for authentication."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "test_password",
        "roles": ["user"],
        "permissions": ["read", "write"],
    }


@pytest.fixture
def auth_headers(test_user_data: dict[str, object]) -> dict[str, str]:  # noqa: ARG001
    """Authentication headers for test requests."""
    return {
        "Authorization": "Bearer test_token",
        "Content-Type": "application/json",
    }


# API response fixtures
@pytest.fixture
def api_success_response() -> dict[str, object]:
    """Standard API success response."""
    return {
        "success": True,
        "data": {"message": "Operation completed successfully"},
        "timestamp": "2025-01-20T12:00:00Z",
    }


@pytest.fixture
def api_error_response() -> dict[str, object]:
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
    config.addinivalue_line("markers", "slow: Slow tests")


# Configuration fixtures
@pytest.fixture
def web_config() -> dict[str, object]:
    """Web application configuration for testing."""
    return {
        "host": "127.0.0.1",
        "port": 8080,
        "debug": True,
        "secret_key": "test_secret_key_32_characters_long!",
    }
