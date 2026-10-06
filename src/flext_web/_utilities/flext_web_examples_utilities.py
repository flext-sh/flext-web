"""Flext web examples utilities module.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_web/_utilities/flext_web_examples_utilities
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web import u


class FlextWebExamplesUtilities(u):
    """Utilities facade for the flext-web examples."""

    class WebExamplesBase:
        """Explicit composition base for the example utilities namespace."""

    class WebExamples(u.Web, WebExamplesBase):
        """Web-domain utilities composed for example workflows."""
