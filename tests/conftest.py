"""Test configuration for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Generator

import pytest

from flext_web import FlextWebSettings
from tests import u


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Reset the web settings singleton before each test for isolation."""
    _ = item
    FlextWebSettings.reset_for_testing()


def pytest_runtest_teardown(item: pytest.Item, nextitem: pytest.Item | None) -> None:
    """Reset the web settings singleton after each test to prevent leaks."""
    _ = item, nextitem
    FlextWebSettings.reset_for_testing()


@pytest.fixture
def setup_test_environment() -> Generator[None]:
    """Set up test environment with real configuration."""
    with u.Tests.env_vars_context({
        "FLEXT_ENV": "test",
        "FLEXT_LOG_LEVEL": "INFO",
        "FLEXT_WEB_DEBUG_MODE": "true",
        "FLEXT_WEB_WEB__HOST": "localhost",
        "FLEXT_WEB_WEB__SECRET_KEY": "test-secret-key-32-characters-long-for-tests",
    }):
        yield
