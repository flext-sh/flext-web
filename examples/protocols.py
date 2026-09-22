"""Protocol definitions for the flext-web examples."""

from __future__ import annotations

from flext_web import p


class FlextWebExamplesProtocols(p):
    """Protocols facade for the flext-web examples."""

    class WebExamplesBase:
        """Explicit composition base for the example protocols namespace."""

    class WebExamples(p.Web, WebExamplesBase):
        """Web-domain protocols composed for example workflows."""


__all__: list[str] = ["FlextWebExamplesProtocols"]
