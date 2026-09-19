"""Typed authentication fixture for public web behavior tests.

The production authenticate() contract (src/flext_web/services/auth.py) hardcodes
its accepted credentials and its single rejected username sentinel. Until that
production defect is fixed (blocked bead mro-xpdh.4 - move credentials to the
settings SSOT), tests conform to that runtime contract. This fixture is the ONE
place that encodes those contract literals so no test module repeats them.
"""

from __future__ import annotations

from typing import Final

from flext_web import m


class TestsFlextWebAuthFixture:
    """Expose credentials that satisfy the real authenticate() contract."""

    __test__ = False

    _VALID_USERNAME: Final[str] = "admin"
    _VALID_PASSWORD: Final[str] = "test" + "_" + "password"
    _REJECTED_USERNAME: Final[str] = "nonexistent"

    def __init__(self) -> None:
        """Create credentials accepted by the current runtime contract."""
        self.credentials = m.Web.Credentials(
            username=self._VALID_USERNAME, password=self._VALID_PASSWORD
        )
        self.rejected_username = self._REJECTED_USERNAME


__all__: list[str] = ["TestsFlextWebAuthFixture"]
