"""Constants for the flext-web examples."""

from __future__ import annotations

from flext_web import c


class FlextWebExamplesConstants(c):
    """Constants facade for the flext-web examples."""

    class WebExamplesBase:
        """Explicit composition base for the example constants namespace."""

    class WebExamples(c.Web, WebExamplesBase):
        """Web-domain constants composed for example workflows."""


__all__: list[str] = ["FlextWebExamplesConstants"]
