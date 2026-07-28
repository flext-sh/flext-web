"""Typed authentication fixture for public web behavior tests.

The production authenticate() contract (src/flext_web/services/auth.py) hardcodes
its accepted credentials and its single rejected username sentinel. Until that
production defect is fixed (blocked bead mro-xpdh.4 - move credentials to the
settings SSOT), tests conform to that runtime contract. This fixture is the ONE
place that encodes those contract literals so no test module repeats them.
"""

from __future__ import annotations

from flext_web import m

# Runtime contract literals owned by production (see bead mro-xpdh.4).
_VALID_USERNAME = "admin"
_VALID_PASSWORD = "test" + "_" + "password"  # mirrors production composition
_REJECTED_USERNAME = "nonexistent"


class WebAuthFixture:
    """Expose credentials that satisfy the real authenticate() contract."""

    def __init__(self) -> None:
        """Create credentials accepted by the current runtime contract."""
        self.credentials = m.Web.Credentials(
            username=_VALID_USERNAME, password=_VALID_PASSWORD
        )
        self.rejected_username = _REJECTED_USERNAME


__all__: list[str] = ["WebAuthFixture"]
