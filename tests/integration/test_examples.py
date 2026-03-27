"""Integration tests for the canonical flext-web examples."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

from flext_core import FlextLogger
from flext_tests import tm

from flext_web import web

logger = FlextLogger(__name__)


class ExamplesFullFunctionalityTest:
    """Shared example assertions exercised through collected subclasses."""

    @staticmethod
    def _example_path(file_name: str) -> Path:
        return Path(__file__).resolve().parents[2] / "examples" / file_name

    @classmethod
    def _load_example_module(cls, file_name: str, module_name: str) -> ModuleType:
        example_path = cls._example_path(file_name)
        spec = importlib.util.spec_from_file_location(module_name, example_path)
        if spec is None or spec.loader is None:
            msg = f"Unable to load example module: {example_path}"
            raise RuntimeError(msg)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    @staticmethod
    def _reset_public_runtime() -> None:
        apps_result = web.list_apps()
        if apps_result.is_success:
            for app in apps_result.value:
                if app.is_running:
                    _ = web.stop_app(app.id)
        status_result = web.get_service_status()
        if status_result.is_success and status_result.value.status == "operational":
            _ = web.stop_service()

    def setup_method(self) -> None:
        """Reset the shared public runtime before each example test."""
        self._reset_public_runtime()

    def teardown_method(self) -> None:
        """Reset the shared public runtime after each example test."""
        self._reset_public_runtime()

    def test_basic_service_example_exposes_main(self) -> None:
        """The basic service example stays importable and runnable."""
        module = self._load_example_module("01_basic_service.py", "basic_service")
        tm.that(callable(module.main), eq=True)

    def test_api_usage_example_uses_the_public_facade(self) -> None:
        """The API usage example delegates lifecycle operations to `web`."""
        module = self._load_example_module("02_api_usage.py", "api_usage")

        health_result = module.check_service_health()
        tm.ok(health_result)
        tm.that(health_result.value.service, eq="flext-web")

        create_result = module.create_application("example-app", 8191)
        tm.ok(create_result)

        start_result = module.start_application(create_result.value.id)
        tm.ok(start_result)
        tm.that(start_result.value.is_running, eq=True)

        get_result = module.get_application_status(create_result.value.id)
        tm.ok(get_result)
        tm.that(get_result.value.id, eq=create_result.value.id)

        list_result = module.list_applications()
        tm.ok(list_result)
        tm.that(
            any(app.id == create_result.value.id for app in list_result.value), eq=True
        )

        stop_result = module.stop_application(create_result.value.id)
        tm.ok(stop_result)
        tm.that(stop_result.value.is_running, eq=False)

    def test_api_usage_demo_runs_full_lifecycle(self) -> None:
        """The lifecycle demo returns the projected applications after execution."""
        module = self._load_example_module("02_api_usage.py", "api_usage_demo")
        demo_result = module.demo_application_lifecycle()
        tm.ok(demo_result)
        tm.that(demo_result.value, length=2)
        tm.that(all(app.is_running is False for app in demo_result.value), eq=True)


class TestExamples(ExamplesFullFunctionalityTest):
    """Collected integration tests for canonical examples."""


def main() -> int:
    """Module entry point kept for the generated test exports."""
    return 0
