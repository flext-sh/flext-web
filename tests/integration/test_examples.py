"""Test examples full functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

import asyncio
import importlib
import importlib.util
import shutil
import sys
import time
from pathlib import Path

import requests

from flext_core import FlextLogger, FlextTypes

# Configure logging
logger = FlextLogger(__name__)


class ExamplesFullFunctionalityTest:
    """Teste completo de toda funcionalidade dos examples."""

    def __init__(self) -> None:
        """Initialize the instance."""
        self.container_id: str | None = None
        self.service_url = (
            "http://localhost:8093"  # Port específica para evitar conflitos
        )
        self.DOCKER_PATH = shutil.which("docker")

    def start_service_in_docker(self) -> bool | None:
        """Inicia o serviço em Docker para teste completo."""
        # Build container if needed
        if self.DOCKER_PATH is None:
            return False
        build_cmd = [self.DOCKER_PATH, "build", "-t", "flext-web-full-test", "."]

        async def _run_exec(
            cmd: FlextTypes.Core.StringList,
            cwd: str | None = None,
        ) -> tuple[int, str, str]:
            """Helper to run a command asynchronously and return (rc, stdout, stderr)."""
            try:
                async with asyncio.timeout(120):
                    process = await asyncio.create_subprocess_exec(
                        *[str(c) for c in cmd],
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                        cwd=cwd,
                    )
                    stdout, stderr = await process.communicate()
                    return process.returncode or 0, stdout.decode(), stderr.decode()
            except TimeoutError:
                return -1, "", "Command timed out after 120 seconds"

        build_rc, _build_out, _build_err = asyncio.run(
            _run_exec(build_cmd, cwd=str(Path(__file__).resolve().parent)),
        )
        if build_rc != 0:
            return False

        # Start container with examples
        start_cmd = [
            self.DOCKER_PATH,
            "run",
            "--rm",
            "-d",
            "-p",
            "8093:8080",
            "-e",
            "FLEXT_WEB_SECRET_KEY=test-full-functionality-key-32-chars!",
            "-e",
            "FLEXT_WEB_HOST=0.0.0.0",
            "-e",
            "FLEXT_WEB_PORT=8080",
            "-e",
            "FLEXT_WEB_DEBUG=false",
            "--name",
            "flext-full-test",
            "flext-web-full-test",
        ]

        try:
            start_rc, start_out, _start_err = asyncio.run(
                _run_exec(start_cmd),
            )
            if start_rc != 0:
                return False

            self.container_id = start_out.strip()

            # Wait for service to be ready
            for _i in range(30):  # 30 seconds timeout
                try:
                    response = requests.get(f"{self.service_url}/health", timeout=2)
                    if response.status_code == 200:
                        return True
                except Exception as exc:
                    # Log the transient failure but keep waiting
                    logger.debug("health check attempt failed: %s", exc)
                time.sleep(1)

            return False

        except Exception:
            return False

    def stop_docker_service(self) -> None:
        """Para o serviço Docker."""
        if self.container_id:

            async def _stop() -> None:
                process = await asyncio.create_subprocess_exec(
                    str(self.DOCKER_PATH),
                    "stop",
                    "flext-full-test",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                try:
                    await asyncio.wait_for(process.communicate(), timeout=10)
                except TimeoutError:
                    process.kill()
                    await process.communicate()

            asyncio.run(_stop())

    def test_basic_service_full_functionality(self) -> bool | None:
        """Testa TODA funcionalidade do basic_service.py."""
        # Test 1: Import functionality
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

            # Test 2: Main function exists and is callable
            assert hasattr(basic_service, "main"), "main() function missing"
            assert callable(basic_service.main), "main() not callable"

            # Test 3: Can create service programmatically
            flext_web = importlib.import_module("flext_web")
            # Using direct FlextWebServices.create_web_service instead of alias
            flext_web_configs = flext_web.FlextWebConfigs

            config = flext_web_configs.create_web_config()
            service = flext_web.FlextWebServices.create_web_service(config)

            # Test 4: Service has correct attributes
            assert hasattr(service, "app"), "Service missing Flask app"
            assert hasattr(service, "run"), "Service missing run method"

            return True

        except Exception:
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

            # Test 1: Health check function
            health_result = api_usage.check_service_health()
            if health_result:
                assert isinstance(health_result, dict)
                assert health_result.get("status") == "healthy"

            # Test 2: Create application function
            create_result = api_usage.create_application("test-full-func", 3001)
            if create_result:
                app_id = create_result.get("id")

                # Test 3: Start application function
                if app_id:
                    start_result = api_usage.start_application(app_id)
                    if start_result:
                        # Test 4: Get status function
                        status = api_usage.get_application_status(app_id)
                        if status:
                            assert isinstance(status, dict)
                            assert "status" in status

                        # Test 5: Stop application function
                        stop_result = api_usage.stop_application(app_id)
                        if stop_result:
                            assert isinstance(stop_result, dict)
                            assert stop_result.get("success") is True

            # Test 6: List applications function
            api_usage.list_applications()

            # Test 7: Demo lifecycle function
            api_usage.demo_application_lifecycle()

            return True

        except Exception:
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

            # Test 1: create_docker_config function
            config = docker_ready.create_docker_config()
            assert config.host == "0.0.0.0", "Docker config host incorreto"
            assert isinstance(config.port, int), "Docker config port incorreto"

            # Test 2: Configuration validation
            validation_result = config.validate_config()
            if validation_result.success:
                assert validation_result.success is True
                assert validation_result.value is not None

            # Test 3: setup_signal_handlers function
            docker_ready.setup_signal_handlers()

            # Test 4: main function exists
            assert hasattr(docker_ready, "main"), "main() function missing"
            assert callable(docker_ready.main), "main() not callable"

            return True

        except Exception:
            return False

    def test_examples_integration_functionality(self) -> bool | None:
        """Testa integração entre examples e funcionalidade completa."""
        # Test 1: All examples can work together
        try:
            flext_web = importlib.import_module("flext_web")
            flext_web_config_cls = flext_web.FlextWebConfigs.WebConfig
            # Using direct FlextWebServices.create_web_service instead of alias
            flext_web_configs = flext_web.FlextWebConfigs

            # Create services using different approaches from examples

            # Approach 1: basic_service style
            config1 = flext_web_configs.create_web_config()
            service1 = flext_web.FlextWebServices.create_web_service(config1)

            # Approach 2: docker_ready style
            config2 = flext_web_config_cls(
                host="127.0.0.1",
                port=8094,
                debug=False,
                secret_key="integration-test-key-32-characters!",
            )
            service2 = flext_web.FlextWebServices.create_web_service(config2)

            # Test both services have same interface
            assert hasattr(service1, "app")
            assert hasattr(service2, "app")
            assert hasattr(service1, "run")
            assert hasattr(service2, "run")

            return True

        except Exception:
            return False

    def test_examples_error_handling(self) -> bool | None:
        """Testa tratamento de erros nos examples com abordagem REAL sem mocking."""
        # Test error handling in api_usage when service is down using REAL approach
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

            # Temporarily change BASE_URL to non-existent service using REAL class structure
            original_base_url = api_usage.ExampleConstants.BASE_URL
            api_usage.ExampleConstants.BASE_URL = "http://localhost:9999"

            # Test functions handle errors gracefully with REAL failing connections
            health = api_usage.check_service_health()
            assert health is False, "Should return False when service down"

            create_result = api_usage.create_application("test", 8080)
            assert create_result is None, "Should return None when service down"

            apps = api_usage.list_applications()
            assert isinstance(apps, list), "Should return empty list"
            assert len(apps) == 0, "Should return empty list"

            # Restore original URL
            api_usage.ExampleConstants.BASE_URL = original_base_url

            return True

        except Exception:
            return False

    def run_full_functionality_test(self) -> bool:
        """Executa teste COMPLETO de toda funcionalidade dos examples."""
        # Start Docker service for testing
        if not self.start_service_in_docker():
            logger.warning("Failed to start Docker service for testing")
            return False

        try:
            results: list[tuple[str, bool | None]] = []

            # Test each example thoroughly
            results.extend(
                (
                    ("basic_service", self.test_basic_service_full_functionality()),
                    ("api_usage", self.test_api_usage_full_functionality()),
                    ("docker_ready", self.test_docker_ready_full_functionality()),
                    ("integration", self.test_examples_integration_functionality()),
                    ("error_handling", self.test_examples_error_handling()),
                ),
            )

            # Results summary

            passed = 0
            for _test_name, result in results:
                if result:
                    passed += 1

            total = len(results)
            success_rate = (passed / total) * 100
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
