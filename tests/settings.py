"""Runtime settings for flext-web tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsSettings

from flext_web import FlextWebSettings


class TestsFlextWebSettings(FlextWebSettings, FlextTestsSettings):
    """Web settings extended with the shared test namespace."""


__all__: list[str] = ["TestsFlextWebSettings"]
