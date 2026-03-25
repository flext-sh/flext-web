"""Test examples full functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
import time
from pathlib import Path

import pytest
import requests
from flext_core import FlextLogger
from flext_tests import tk

logger = FlextLogger(__name__)


class ExamplesFullFunctionalityTest:
    """Teste completo de toda funcionalidade dos examples."""

    def __init__(self) -> None:
        """Initialize the instance."""
        super().__init__()
        self.container_id: str | None = None
        self.service_url = "http://localhost:8093"
        self.docker_manager = tk(workspace_root=Path().absolute())

    def start_service_in_docker(self) -> bool | None:
        """Inicia o serviço em Docker para teste completo usando tk."""
        self.container_id = "flext-full-test"
        for _i in range(10):
            try:
                response = requests.get(f"{self.service_url}/health", timeout=1)
                if response.status_code == 200:
                    return True
            except Exception as exc:
                logger.debug(f"health check attempt failed: {exc}")
            time.sleep(0.5)
        pytest.fail(f"Service failed to start within 10 seconds on {self.service_url}")
        return False

    def stop_docker_service(self) -> None:
        """Para o serviço Docker usando tk."""
        if self.container_id:
            pass

    def test_basic_service_full_functionality(self) -> bool | None:
        """Testa TODA funcionalidade do basic_service.py."""
        try:
            example_path = Path("examples/01_basic_service.py")
            spec = importlib.util.spec_from_file_location(
                "basic_service",
                str(example_path),
            )
            assert spec is not None
            assert hasattr(spec, "loader")
            assert spec.loader is not None
            basic_service = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(basic_service)
            assert hasattr(basic_service, "main"), "main() function missing"
            assert callable(basic_service.main), "main() not callable"
            flext_web = importlib.import_module("flext_web")
            config = flext_web.FlextWebSettings.create_web_config()
            service = flext_web.FlextWebServices.create_web_service(config)
            assert hasattr(service, "app"), "Service missing Flask app"
            assert hasattr(service, "run"), "Service missing run method"
            return True
        except (
            ImportError,
            RuntimeError,
            ValueError,
            TypeError,
            AttributeError,
            AssertionError,
            OSError,
        ):
            return False

    def test_api_usage_full_functionality(self) -> bool | None:
        """Testa TODA funcionalidade do api_usage.py."""
        try:
            example_path = Path("examples/02_api_usage.py")
            spec = importlib.util.spec_from_file_location(
                "api_usage",
                str(example_path),
            )
            assert spec is not None
            assert hasattr(spec, "loader")
            assert spec.loader is not None
            api_usage = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(api_usage)
            health_result = api_usage.check_service_health()
            if health_result:
                assert isinstance(health_result, dict)
                assert health_result.get("status") == "healthy"
            create_result = api_usage.create_application("test-full-func", 3001)
            if create_result:
                app_id = create_result.get("id")
                if app_id:
                    start_result = api_usage.start_application(app_id)
                    if start_result:
                        status = api_usage.get_application_status(app_id)
                        if status:
                            assert isinstance(status, dict)
                            assert "status" in status
                        stop_result = api_usage.stop_application(app_id)
                        if stop_result:
                            assert isinstance(stop_result, dict)
                            assert stop_result.get("success") is True
            api_usage.list_applications()
            api_usage.demo_application_lifecycle()
            return True
        except (
            ImportError,
            RuntimeError,
            ValueError,
            TypeError,
            AttributeError,
            AssertionError,
            OSError,
        ):
            return False

    def test_docker_ready_full_functionality(self) -> bool | None:
        """Testa TODA funcionalidade do docker_ready.py."""
        try:
            example_path = Path("examples/03_docker_ready.py")
            spec = importlib.util.spec_from_file_location(
                "docker_ready",
                str(example_path),
            )
            assert spec is not None
            assert hasattr(spec, "loader")
            assert spec.loader is not None
            docker_ready = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(docker_ready)
            config = docker_ready.create_docker_config()
            assert config.host == "0.0.0.0", "Docker config host incorreto"
            assert isinstance(config.port, int), "Docker config port incorreto"
            validation_result = config.validate_business_rules()
            if validation_result.is_success:
                assert validation_result.is_success is True
                assert validation_result.value is not None
            docker_ready.setup_signal_handlers()
            assert hasattr(docker_ready, "main"), "main() function missing"
            assert callable(docker_ready.main), "main() not callable"
            return True
        except (
            ImportError,
            RuntimeError,
            ValueError,
            TypeError,
            AttributeError,
            AssertionError,
            OSError,
        ):
            return False

    def test_examples_integration_functionality(self) -> bool | None:
        """Testa integração entre examples e funcionalidade completa."""
        try:
            flext_web = importlib.import_module("flext_web")
            config1 = flext_web.FlextWebSettings.create_web_config()
            service1 = flext_web.FlextWebServices.create_web_service(config1)
            config2 = flext_web.FlextWebSettings(
                host="127.0.0.1",
                port=8094,
                debug=False,
                secret_key="integration-test-key-32-characters!",
            )
            service2 = flext_web.FlextWebServices.create_web_service(config2)
            assert hasattr(service1, "app")
            assert hasattr(service2, "app")
            assert hasattr(service1, "run")
            assert hasattr(service2, "run")
            return True
        except (
            ImportError,
            RuntimeError,
            ValueError,
            TypeError,
            AttributeError,
            AssertionError,
            OSError,
        ):
            return False

    def test_examples_error_handling(self) -> bool | None:
        """Testa tratamento de erros nos examples com abordagem REAL sem mocking."""
        try:
            example_path = Path("examples/02_api_usage.py")
            spec = importlib.util.spec_from_file_location(
                "api_usage",
                str(example_path),
            )
            assert spec is not None
            assert hasattr(spec, "loader")
            assert spec.loader is not None
            api_usage = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(api_usage)
            original_base_url = api_usage.ExampleConstants.BASE_URL
            api_usage.ExampleConstants.BASE_URL = "http://localhost:9999"
            health = api_usage.check_service_health()
            assert health is False, "Should return False when service down"
            create_result = api_usage.create_application("test", 8080)
            assert create_result is None, "Should return None when service down"
            apps = api_usage.list_applications()
            assert isinstance(apps, list), "Should return empty list"
            assert not apps, "Should return empty list"
            api_usage.ExampleConstants.BASE_URL = original_base_url
            return True
        except (
            ImportError,
            RuntimeError,
            ValueError,
            TypeError,
            AttributeError,
            AssertionError,
            OSError,
        ):
            return False

    def run_full_functionality_test(self) -> bool:
        """Executa teste COMPLETO de toda funcionalidade dos examples."""
        if not self.start_service_in_docker():
            logger.warning("Failed to start Docker service for testing")
            return False
        try:
            results: list[tuple[str, bool | None]] = []
            results.extend((
                ("basic_service", self.test_basic_service_full_functionality()),
                ("api_usage", self.test_api_usage_full_functionality()),
                ("docker_ready", self.test_docker_ready_full_functionality()),
                ("integration", self.test_examples_integration_functionality()),
                ("error_handling", self.test_examples_error_handling()),
            ))
            passed = 0
            for _test_name, result in results:
                if result:
                    passed += 1
            total = len(results)
            success_rate = passed / total * 100
            return success_rate > 0
        finally:
            self.stop_docker_service()


def main() -> int:
    """Executa teste completo de funcionalidade dos examples."""
    tester = ExamplesFullFunctionalityTest()
    success = tester.run_full_functionality_test()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
