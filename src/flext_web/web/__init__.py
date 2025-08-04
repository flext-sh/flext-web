"""FLEXT Web Interface - Web Layer Components.

This module contains the web presentation layer components for the FLEXT Web Interface,
implementing Flask-based services with Clean Architecture patterns.

Key Components:
    - FlextWebService: Flask-based web service with REST API and dashboard

All components follow flext-core patterns for enterprise-grade reliability.
"""

from .service import FlextWebService

__all__: list[str] = [
    "FlextWebService",
]
