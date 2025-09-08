"""Thread-safe port allocation for test isolation.

Provides unique port allocation to ensure tests don't conflict when
running Flask servers in parallel threads.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import threading
from typing import ClassVar


class TestPortManager:
    """Thread-safe port allocation manager for tests."""

    # Port range constants
    _PORT_START: ClassVar[int] = 9000
    _PORT_END: ClassVar[int] = 9999

    _lock: ClassVar[threading.Lock] = threading.Lock()
    _allocated_ports: ClassVar[set[int]] = set()
    _current_port: ClassVar[int] = _PORT_START

    @classmethod
    def allocate_port(cls) -> int:
        """Allocate a unique port for testing.

        Returns:
            Unique port number in the range 9000-9999

        Thread Safety:
            This method is thread-safe and can be called from
            multiple test threads simultaneously.

        """
        with cls._lock:
            # Find next available port
            while cls._current_port in cls._allocated_ports:
                cls._current_port += 1

                # Wrap around if we hit the limit
                if cls._current_port > cls._PORT_END:
                    cls._current_port = cls._PORT_START

            port = cls._current_port
            cls._allocated_ports.add(port)
            cls._current_port += 1

            return port

    @classmethod
    def release_port(cls, port: int) -> None:
        """Release a previously allocated port.

        Args:
            port: Port number to release

        Thread Safety:
            This method is thread-safe.

        """
        with cls._lock:
            cls._allocated_ports.discard(port)

    @classmethod
    def reset(cls) -> None:
        """Reset the port manager (for testing only).

        Thread Safety:
            This method is thread-safe.
        """
        with cls._lock:
            cls._allocated_ports.clear()
            cls._current_port = 9000
