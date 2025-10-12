#!/usr/bin/env python3
"""Debug script to test WebService initialization."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from flext_core import (
        FlextBus,
        FlextContainer,
        FlextDispatcher,
        FlextLogger,
        FlextProcessors,
        FlextRegistry,
    )

    from flext_web import FlextWebService

    container = FlextContainer.get_global()

    logger = FlextLogger(__name__)

    bus = FlextBus()

    dispatcher = FlextDispatcher()

    processors = FlextProcessors()

    registry = FlextRegistry(dispatcher=dispatcher)

    result = FlextWebService.create_web_service()


except Exception:
    import traceback

    traceback.print_exc()
