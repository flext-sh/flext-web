"""Test configuration for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from flext_web import FlextWebSettings
from flext_web import web
from tests import u

if TYPE_CHECKING:
    from collections.abc import Generator


def _reset_web_runtime_state() -> None:
    """Reset every shared web runtime registry to its pristine state."""
    u.Web.apps_registry.clear()
    u.Web.app_runtimes.clear()
    u.Web.framework_instances.clear()
    u.Web.service_state.update({
        "routes_initialized": False,
        "middleware_configured": False,
        "service_running": False,
    })
    u.Web.template_config.clear()
    u.Web.template_filters.clear()
    u.Web.template_globals.clear()
    u.Web.web_metrics.clear()


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Reset the web settings singleton and runtime state before each test."""
    _ = item
    FlextWebSettings.reset_for_testing()
    _reset_web_runtime_state()


def pytest_runtest_teardown(item: pytest.Item, nextitem: pytest.Item | None) -> None:
    """Reset the web runtime state and settings singleton after each test."""
    _ = item, nextitem
    _reset_web_runtime_state()
    FlextWebSettings.reset_for_testing()


@pytest.fixture(autouse=True)
def reset_web_runtime() -> None:
    """Stop any running public runtime through the facade before each test."""
    apps_result = web.list_apps()
    if apps_result.success:
        for app in apps_result.value:
            if app.status == "running":
                _ = web.stop_app(app.id)
    status_result = web.service_status()
    if status_result.success and status_result.value.status == "operational":
        _ = web.stop_service()


@pytest.fixture(autouse=True)
def setup_test_environment() -> Generator[None]:
    """Set up test environment with real configuration."""
    with u.Tests.env_vars_context({
        "FLEXT_ENV": "test",
        "FLEXT_LOG_LEVEL": "INFO",
        "FLEXT_WEB_DEBUG_MODE": "true",
        "FLEXT_WEB_WEB__HOST": "localhost",
        "FLEXT_WEB_WEB__SECRET_KEY": "test-secret-key-32-characters-long-for-tests",
        "FLEXT_WEB_WEB__AUTH_USERNAME": "testuser",
        "FLEXT_WEB_WEB__AUTH_PASSWORD": "test-password-from-environment",
    }):
        yield
