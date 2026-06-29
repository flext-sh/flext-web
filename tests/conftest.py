"""Test configuration for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Generator

import pytest

from tests.constants import c
from tests.utilities import u


@pytest.fixture(autouse=True)
def setup_test_environment() -> Generator[None]:
    """Set up test environment with real configuration."""
    with u.Tests.env_vars_context({
        "FLEXT_ENV": "test",
        "FLEXT_LOG_LEVEL": "INFO",
        "FLEXT_WEB_DEBUG_MODE": "true",
        "FLEXT_WEB_HOST": c.Web.DEFAULT_HOST,
        "FLEXT_WEB_SECRET_KEY": c.Web.DEFAULT_TEST_SECRET_KEY,
    }):
        yield
