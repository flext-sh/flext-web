# AUTO-GENERATED FILE — Regenerate with: make gen
"""Package version and metadata for flext-web.

Subclass of ``FlextVersion`` — overrides only ``_metadata``.
All derived attributes (``__version__``, ``__title__``, etc.) are
computed automatically via ``FlextVersion.__init_subclass__``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib.metadata import PackageMetadata, metadata

from flext_core import FlextVersion


class FlextWebVersion(FlextVersion):
    """flext-web version — MRO-derived from FlextVersion."""

    _metadata: PackageMetadata = metadata("flext-web")


__version__ = FlextWebVersion.__version__
__version_info__ = FlextWebVersion.__version_info__
__title__ = FlextWebVersion.__title__
__description__ = FlextWebVersion.__description__
__author__ = FlextWebVersion.__author__
__author_email__ = FlextWebVersion.__author_email__
__license__ = FlextWebVersion.__license__
__url__ = FlextWebVersion.__url__
__all__: list[str] = [
    "FlextWebVersion",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
]
