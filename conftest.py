"""Pytest configuration for flext-web Django application."""

import os
import sys
from pathlib import Path

import django

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Configure Django settings - use simple settings for testing to avoid dependency issues
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flext_web.flext_web_legacy.settings.base_simple")

# Setup Django
django.setup()
