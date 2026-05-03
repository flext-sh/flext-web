"""Test configuration for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os
from collections.abc import Generator

import pytest

from tests import c, t


@pytest.fixture(autouse=True)
def setup_test_environment() -> Generator[None]:
    """Set up test environment with real configuration."""
    original_env: t.StrMapping = dict(os.environ)
    os.environ["FLEXT_ENV"] = "test"
    os.environ["FLEXT_LOG_LEVEL"] = "INFO"
    os.environ["FLEXT_WEB_DEBUG_MODE"] = "true"
    os.environ["FLEXT_WEB_HOST"] = c.Web.DEFAULT_HOST
    os.environ["FLEXT_WEB_SECRET_KEY"] = c.Web.DEFAULT_TEST_SECRET_KEY
    yield
    os.environ.clear()
    for key, value in original_env.items():
        os.environ[key] = value
