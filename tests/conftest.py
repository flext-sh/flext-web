"""Test configuration for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from flext_web import FlextWebSettings
from tests import u

if TYPE_CHECKING:
    from collections.abc import Generator


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Reset the web settings singleton before each test for isolation."""
    _ = item
    FlextWebSettings.reset_for_testing()
    u.Web.apps_registry.clear()
    u.Web.app_runtimes.clear()
    u.Web.framework_instances.clear()
    u.Web.service_state.update({
        "routes_initialized": False,
        "middleware_configured": False,
        "service_running": False,
    })


def pytest_runtest_teardown(item: pytest.Item, nextitem: pytest.Item | None) -> None:
    """Reset the web settings singleton after each test to prevent leaks."""
    _ = item, nextitem
    u.Web.apps_registry.clear()
    u.Web.app_runtimes.clear()
    u.Web.framework_instances.clear()
    u.Web.service_state.update({
        "routes_initialized": False,
        "middleware_configured": False,
        "service_running": False,
    })
    FlextWebSettings.reset_for_testing()


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
