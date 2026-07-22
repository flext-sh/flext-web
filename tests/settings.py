"""Runtime settings for flext-web tests."""

from __future__ import annotations

from flext_tests import FlextTestsSettings
from flext_web import FlextWebSettings


class TestsFlextWebSettings(FlextWebSettings, FlextTestsSettings):
    """Web settings extended with the shared test namespace."""


__all__: list[str] = ["TestsFlextWebSettings"]
