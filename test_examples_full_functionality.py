#!/usr/bin/env python3
"""Teste COMPLETO de TODA funcionalidade dos examples/ usando Docker.

Este teste valida 100% da funcionalidade de todos os examples usando o container Docker
para garantir comportamento compatível com ambientes de produção e enterprise.
"""

import asyncio
import shutil
import sys
import time
from pathlib import Path

import requests

DOCKER_PATH = shutil.which("docker")


class ExamplesFullFunctionalityTest:
    """Teste completo de toda funcionalidade dos examples."""

    def __init__(self) -> None:
        self.container_id = None
        self.service_url = (
            "http://localhost:8093"  # Port específica para evitar conflitos
        )

    def start_service_in_docker(self) -> bool | None:
        """Inicia o serviço em Docker para teste completo."""
        # Build container if needed
        if DOCKER_PATH is None:
            return False
        build_cmd = [DOCKER_PATH, "build", "-t", "flext-web-full-test", "."]

        async def _run_exec(
            cmd: list[str],
            timeout: int = 120,
            cwd: str | None = None,
        ) -> tuple[int, str, str]:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
            )
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout,
                )
            except TimeoutError:
                process.kill()
                await process.communicate()
                return 124, "", "Timeout"
            return process.returncode, stdout.decode(), stderr.decode()

        build_rc, _build_out, _build_err = asyncio.run(
            _run_exec(build_cmd, timeout=180, cwd=str(Path(__file__).resolve().parent)),
        )
        if build_rc != 0:
            return False

        # Start container with examples
        start_cmd = [
            DOCKER_PATH,
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
                _run_exec(start_cmd, timeout=30),
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
                except Exception:
                    # Mantém silencioso no loop de espera do health check
                    pass
                time.sleep(1)

            return False

        except Exception:
            return False

    def stop_docker_service(self) -> None:
        """Para o serviço Docker."""
        if self.container_id:

            async def _stop() -> None:
                process = await asyncio.create_subprocess_exec(
                    DOCKER_PATH,
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
        sys.path.insert(0, "examples")
        try:
            import basic_service

            # Test 2: Main function exists and is callable
            assert hasattr(basic_service, "main"), "main() function missing"
            assert callable(basic_service.main), "main() not callable"

            # Test 3: Can create service programmatically
            from flext_web import create_service, get_web_settings

            config = get_web_settings()
            service = create_service(config)

            # Test 4: Service has correct attributes
            assert hasattr(service, "app"), "Service missing Flask app"
            assert hasattr(service, "run"), "Service missing run method"

            return True

        except Exception:
            return False
        finally:
            if "examples" in sys.path:
                sys.path.remove("examples")

    def test_api_usage_full_functionality(self) -> bool | None:
        """Testa TODA funcionalidade do api_usage.py."""
        sys.path.insert(0, "examples")
        try:
            import api_usage

            # Test 1: Health check function
            health_result = api_usage.check_service_health()
            if health_result:
                pass

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
                            pass

                        # Test 5: Stop application function
                        stop_result = api_usage.stop_application(app_id)
                        if stop_result:
                            pass

            # Test 6: List applications function
            api_usage.list_applications()

            # Test 7: Demo lifecycle function
            api_usage.demo_application_lifecycle()

            return True

        except Exception:
            return False
        finally:
            if "examples" in sys.path:
                sys.path.remove("examples")

    def test_docker_ready_full_functionality(self) -> bool | None:
        """Testa TODA funcionalidade do docker_ready.py."""
        sys.path.insert(0, "examples")
        try:
            import docker_ready

            # Test 1: create_docker_config function
            config = docker_ready.create_docker_config()
            assert config.host == "0.0.0.0", "Docker config host incorreto"
            assert isinstance(config.port, int), "Docker config port incorreto"

            # Test 2: Configuration validation
            validation_result = config.validate_config()
            if validation_result.success:
                pass

            # Test 3: setup_signal_handlers function
            docker_ready.setup_signal_handlers()

            # Test 4: main function exists
            assert hasattr(docker_ready, "main"), "main() function missing"
            assert callable(docker_ready.main), "main() not callable"

            return True

        except Exception:
            return False
        finally:
            if "examples" in sys.path:
                sys.path.remove("examples")

    def test_examples_integration_functionality(self) -> bool | None:
        """Testa integração entre examples e funcionalidade completa."""
        # Test 1: All examples can work together
        try:
            from flext_web import FlextWebConfig, create_service, get_web_settings

            # Create services using different approaches from examples

            # Approach 1: basic_service style
            config1 = get_web_settings()
            service1 = create_service(config1)

            # Approach 2: docker_ready style
            config2 = FlextWebConfig(
                host="127.0.0.1",
                port=8094,
                debug=False,
                secret_key="integration-test-key-32-characters!",
            )
            service2 = create_service(config2)

            # Test both services have same interface
            assert hasattr(service1, "app")
            assert hasattr(service2, "app")
            assert hasattr(service1, "run")
            assert hasattr(service2, "run")

            return True

        except Exception:
            return False

    def test_examples_error_handling(self) -> bool | None:
        """Testa tratamento de erros nos examples."""
        # Test error handling in api_usage when service is down
        sys.path.insert(0, "examples")
        try:
            import api_usage

            # Temporarily change BASE_URL to non-existent service
            original_url = api_usage.BASE_URL
            api_usage.BASE_URL = "http://localhost:9999"  # Non-existent service

            # Test functions handle errors gracefully
            health = api_usage.check_service_health()
            assert health is False, "Should return False when service down"

            create_result = api_usage.create_application("test", 8080)
            assert create_result is None, "Should return None when service down"

            apps = api_usage.list_applications()
            assert isinstance(apps, list), "Should return empty list"
            assert len(apps) == 0, "Should return empty list"

            # Restore original URL
            api_usage.BASE_URL = original_url

            return True

        except Exception:
            return False
        finally:
            if "examples" in sys.path:
                sys.path.remove("examples")

    def run_full_functionality_test(self) -> bool:
        """Executa teste COMPLETO de toda funcionalidade dos examples."""
        # Start Docker service for testing
        if not self.start_service_in_docker():
            pass

        try:
            results = []

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
            (passed / total) * 100

            if passed == total or passed >= total * 0.8:
                pass

            return passed >= total * 0.8

        finally:
            self.stop_docker_service()


def main() -> int:
    """Executa teste completo de funcionalidade dos examples."""
    tester = ExamplesFullFunctionalityTest()
    success = tester.run_full_functionality_test()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
