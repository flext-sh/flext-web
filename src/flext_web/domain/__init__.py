"""FLEXT Web Domain - Domain Entities and Value Objects.

This module contains the core domain entities and value objects for the FLEXT Web Interface,
implementing Domain-Driven Design patterns with Clean Architecture boundaries.

Key Components:
    - FlextWebAppStatus: Application status enumeration with state machine rules
    - FlextWebApp: Rich domain entity for web application lifecycle management

All entities follow flext-core patterns for consistency and enterprise-grade reliability.
"""

from .entities import FlextWebApp, FlextWebAppStatus
from .handlers import FlextWebAppHandler

__all__: list[str] = [
    "FlextWebApp",
    "FlextWebAppHandler",
    "FlextWebAppStatus",
]
