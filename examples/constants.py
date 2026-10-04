"""Constants for the flext-web examples.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web import c


class FlextWebExamplesConstants(c):
    """Constants facade for the flext-web examples."""

    class WebExamplesBase:
        """Explicit composition base for the example constants namespace."""

    class WebExamples(c.Web, WebExamplesBase):
        """Web-domain constants composed for example workflows."""


__all__: list[str] = ["FlextWebExamplesConstants"]
