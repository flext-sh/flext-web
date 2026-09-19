"""Test utilities for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import socket
from threading import Lock
from typing import ClassVar

from flext_tests import FlextTestsUtilities

from flext_web import u
from tests import c


class TestsFlextWebUtilities(u, FlextTestsUtilities):
    """Test utilities for flext-web."""

    class Tests(FlextTestsUtilities.Tests):
        """Web domain test utilities."""

        class TestPortManager:
            """Thread-safe port allocation manager for test services."""

            _lock: ClassVar[Lock] = Lock()
            _allocated_ports: ClassVar[set[int]] = set()
            _current_port: ClassVar[int] = c.Tests.PORT_START

            @classmethod
            def allocate_port(cls) -> int:
                """Allocate a unique port for testing."""
                with cls._lock:
                    for _ in range(c.Tests.PORT_START, c.Tests.PORT_END + 1):
                        port = cls._current_port
                        cls._current_port += 1
                        if cls._current_port > c.Tests.PORT_END:
                            cls._current_port = c.Tests.PORT_START
                        if port in cls._allocated_ports:
                            continue
                        if cls.is_port_available(port):
                            cls._allocated_ports.add(port)
                            return port
                    msg = "No available TCP port in flext-web test range"
                    raise RuntimeError(msg)

            @staticmethod
            def is_port_available(port: int) -> bool:
                """Return whether localhost can bind the candidate test port."""
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        sock.bind((c.Tests.DEFAULT_HOST, port))
                except OSError:
                    return False
                return True

            @classmethod
            def release_port(cls, port: int) -> None:
                """Release a previously allocated port."""
                with cls._lock:
                    cls._allocated_ports.discard(port)

            @classmethod
            def reset(cls) -> None:
                """Reset the allocated test ports."""
                with cls._lock:
                    cls._allocated_ports.clear()
                    cls._current_port = c.Tests.PORT_START


u = TestsFlextWebUtilities
__all__: list[str] = ["TestsFlextWebUtilities", "u"]
