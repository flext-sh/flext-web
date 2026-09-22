"""Domain models for the flext-web examples."""

from __future__ import annotations

from flext_web import m


class FlextWebExamplesModels(m):
    """Models facade for the flext-web examples."""

    class WebExamplesBase:
        """Explicit composition base for the example models namespace."""

    class WebExamples(m.Web, WebExamplesBase):
        """Web-domain models composed for example workflows."""


__all__: list[str] = ["FlextWebExamplesModels"]
