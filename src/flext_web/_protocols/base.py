"""FlextWeb protocols base — foundational contracts owner of the private family.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations


class FlextWebProtocolsBase:
    """Base and foundational owner of the FlextWeb private protocols family.

    Every composed ``FlextWebProtocols*`` owner inherits from this base, so the
    family MRO is explicit and the domain namespace composes all owners through
    multiple inheritance.
    """


__all__: list[str] = ["FlextWebProtocolsBase"]
