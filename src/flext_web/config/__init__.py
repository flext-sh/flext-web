"""FLEXT Web Configuration - Environment-based settings and validation.

This module contains configuration management components for the FLEXT Web Interface,
implementing enterprise-grade configuration patterns with validation and environment
support.

Key Components:
    - FlextWebConfig: Environment-based configuration with comprehensive validation

All configuration follows flext-core patterns and Twelve-Factor App methodology.
"""

from .settings import FlextWebConfig

__all__: list[str] = [
    "FlextWebConfig",
]
