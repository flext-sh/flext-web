"""DEPRECATED: Use flext_web.__version__ instead.

This module is deprecated and maintained only for backward compatibility.
All code should import from flext_web.__version__ directly.

For version metadata, use:
    from flext_web import __version__, __version_info__, VERSION, FlextWebVersion
"""

from __future__ import annotations

# Re-export from canonical location for backward compatibility
from flext_web.__version__ import (
    VERSION,
    FlextWebVersion,
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

__all__ = [
    "VERSION",
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
