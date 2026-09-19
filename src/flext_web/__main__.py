"""Console entry point for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web.cli import FlextWebCli, main

__all__: list[str] = ["FlextWebCli", "main"]

if __name__ == "__main__":
    raise SystemExit(main())
