"""Test configuration for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import contextlib

import pytest

from flext_web import FlextWebSettings
from tests import u

# Why: session-scoped env context replaces an autouse fixture (flext-1wjg1.16)
_ENV_CONTEXT_KEY: pytest.StashKey[contextlib.ExitStack] = pytest.StashKey()


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


def pytest_configure(config: pytest.Config) -> None:
    """Establish the fixed test-environment variables for the whole session."""
    stack = contextlib.ExitStack()
    stack.enter_context(
        u.Tests.env_vars_context({
            "FLEXT_ENV": "test",
            "FLEXT_LOG_LEVEL": "INFO",
            "FLEXT_WEB_DEBUG_MODE": "true",
            "FLEXT_WEB_WEB__HOST": "localhost",
            "FLEXT_WEB_WEB__SECRET_KEY": "test-secret-key-32-characters-long-for-tests",
            "FLEXT_WEB_WEB__AUTH_USERNAME": "testuser",
            "FLEXT_WEB_WEB__AUTH_PASSWORD": "test-password-from-environment",
        })
    )
    config.stash[_ENV_CONTEXT_KEY] = stack


def pytest_unconfigure(config: pytest.Config) -> None:
    """Restore the environment captured by pytest_configure."""
    stack = config.stash.get(_ENV_CONTEXT_KEY, None)
    if stack is not None:
        stack.close()
