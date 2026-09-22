"""Type aliases for the flext-web examples."""

from __future__ import annotations

from flext_web import t


class FlextWebExamplesTypes(t):
    """Type aliases facade for the flext-web examples."""

    class WebExamplesBase:
        """Explicit composition base for the example typings namespace."""

    class WebExamples(t.Web, WebExamplesBase):
        """Web-domain type aliases composed for example workflows."""


__all__: list[str] = ["FlextWebExamplesTypes"]
