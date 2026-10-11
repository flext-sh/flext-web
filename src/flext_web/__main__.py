"""Console entry point for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_web import main

if TYPE_CHECKING:
    from flext_web import FlextWebCli


if __name__ == "__main__":
    raise SystemExit(main())

__all__: list[str] = ["FlextWebCli", "main"]
