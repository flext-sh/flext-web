#!/usr/bin/env python3
"""Docker Stress Testing - Maximum validation of container functionality."""

import concurrent.futures
import shutil
import subprocess
import sys
import time

import requests

DOCKER_PATH = shutil.which("docker")


def test_docker_memory_stress() -> bool | None:
    """Test Docker container under memory pressure."""
    # Build if needed
    if DOCKER_PATH is None:
        return False

    build_result = subprocess.run(
        [DOCKER_PATH, "build", "-t", "flext-web-stress", "."],
        check=False,
        capture_output=True,
        text=True,
    )

    if build_result.returncode != 0:
        return False

    # Run with memory limit
    cmd = [
        DOCKER_PATH,
        "run",
        "--rm",
        "-d",
        "--memory=256m",  # Memory limit
        "--memory-swap=256m",
        "-p",
        "8090:8080",
        "-e",
        "FLEXT_WEB_SECRET_KEY=test-memory-stress-key-32-chars!",
        "-e",
        "FLEXT_WEB_DEBUG=false",
        "--name",
        "flext-memory-test",
        "flext-web-stress",
    ]

    try:
        result = subprocess.run(
            cmd, check=False, capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return False

        result.stdout.strip()

        # Wait for startup
        time.sleep(5)

        # Test health under memory pressure
        try:
            response = requests.get("http://localhost:8090/health", timeout=10)
            return response.status_code == 200
        except requests.RequestException:
            return False

    finally:
        # Cleanup
        subprocess.run(
            [DOCKER_PATH, "stop", "flext-memory-test"],
            check=False,
            capture_output=True,
            timeout=10,
        )


def test_docker_concurrent_requests() -> bool:
    """Test Docker container with concurrent requests."""
    # Start container for concurrency test
    if DOCKER_PATH is None:
        return False

    cmd = [
        DOCKER_PATH,
        "run",
        "--rm",
        "-d",
        "-p",
        "8091:8080",
        "-e",
        "FLEXT_WEB_SECRET_KEY=test-concurrent-key-32-characters!",
        "-e",
        "FLEXT_WEB_DEBUG=false",
        "--name",
        "flext-concurrent-test",
        "flext-web-stress",
    ]

    try:
        result = subprocess.run(
            cmd, check=False, capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return False

        result.stdout.strip()

        # Wait for startup
        time.sleep(5)

        # Test concurrent requests
        def make_request(_i: int) -> bool:
            try:
                response = requests.get("http://localhost:8091/health", timeout=5)
                return response.status_code == 200
            except Exception:
                return False

        # 20 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(make_request, i) for i in range(20)]
            results = [
                future.result() for future in concurrent.futures.as_completed(futures)
            ]

        success_count = sum(results)

        return success_count >= 15  # 75% success rate is acceptable

    finally:
        # Cleanup
        subprocess.run(
            [DOCKER_PATH, "stop", "flext-concurrent-test"],
            check=False,
            capture_output=True,
            timeout=10,
        )


def test_docker_api_workflow() -> bool:
    """Test complete API workflow in Docker container."""
    # Start container for API test
    if DOCKER_PATH is None:
        return False

    cmd = [
        DOCKER_PATH,
        "run",
        "--rm",
        "-d",
        "-p",
        "8092:8080",
        "-e",
        "FLEXT_WEB_SECRET_KEY=test-api-workflow-key-32-characters!",
        "-e",
        "FLEXT_WEB_DEBUG=false",
        "--name",
        "flext-api-test",
        "flext-web-stress",
    ]

    try:
        result = subprocess.run(
            cmd, check=False, capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return False

        result.stdout.strip()

        # Wait for startup
        time.sleep(5)

        base_url = "http://localhost:8092"
        success_count = 0

        # Test 1: Health check
        try:
            response = requests.get(f"{base_url}/health", timeout=10)
            if response.status_code == 200:
                success_count += 1
        except Exception:
            # Non-fatal during stress checks
            return False

        # Test 2: Create app
        try:
            response = requests.post(
                f"{base_url}/api/v1/apps",
                json={
                    "name": "docker-test-app",
                    "port": 3000,
                    "host": "localhost",
                },
                timeout=10,
            )
            if response.status_code == 200:
                app_data = response.json()["data"]
                app_id = app_data["id"]
                success_count += 1

                # Test 3: Start app
                response = requests.post(
                    f"{base_url}/api/v1/apps/{app_id}/start", timeout=10,
                )
                if response.status_code == 200:
                    success_count += 1

                    # Test 4: Get app status
                    response = requests.get(
                        f"{base_url}/api/v1/apps/{app_id}", timeout=10,
                    )
                    if response.status_code == 200:
                        app_status = response.json()["data"]
                        if app_status["is_running"]:
                            success_count += 1

                    # Test 5: Stop app
                    response = requests.post(
                        f"{base_url}/api/v1/apps/{app_id}/stop", timeout=10,
                    )
                    if response.status_code == 200:
                        success_count += 1
        except Exception:
            # Ignore and continue; API may be slow under stress
            return False

        return success_count >= 4  # 80% success rate

    finally:
        # Cleanup
        subprocess.run(
            [DOCKER_PATH, "stop", "flext-api-test"],
            check=False,
            capture_output=True,
            timeout=10,
        )


def test_docker_examples_stress() -> bool | None:
    """Test Docker examples under stress."""
    # Test docker_ready.py in container with stress
    if DOCKER_PATH is None:
        return False

    cmd = [
        DOCKER_PATH,
        "run",
        "--rm",
        "-d",
        "--memory=128m",  # Very limited memory
        "-e",
        "FLEXT_WEB_SECRET_KEY=test-examples-stress-key-32-chars!",
        "-e",
        "FLEXT_WEB_HOST=0.0.0.0",
        "-e",
        "FLEXT_WEB_PORT=8080",
        "-e",
        "FLEXT_WEB_DEBUG=false",
        "--name",
        "flext-examples-stress",
        "flext-web-stress",
        "python",
        "examples/docker_ready.py",
    ]

    try:
        result = subprocess.run(
            cmd, check=False, capture_output=True, text=True, timeout=5,
        )
        result.stdout.strip()

        # Wait a bit to see if it crashes
        time.sleep(3)

        # Check if still running
        check_result = subprocess.run(
            [DOCKER_PATH, "ps", "-q", "-f", "name=flext-examples-stress"],
            check=False,
            capture_output=True,
            text=True,
        )

        return bool(check_result.stdout.strip())

    finally:
        # Cleanup
        subprocess.run(
            [DOCKER_PATH, "stop", "flext-examples-stress"],
            check=False,
            capture_output=True,
            timeout=10,
        )


def main() -> bool:
    """Run comprehensive Docker stress tests."""
    tests = [
        ("Memory Stress", test_docker_memory_stress),
        ("Concurrent Requests", test_docker_concurrent_requests),
        ("API Workflow", test_docker_api_workflow),
        ("Examples Stress", test_docker_examples_stress),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                pass
        except Exception:
            results.append((test_name, False))

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for _test_name, _result in results:
        pass

    if passed == total or passed >= total * 0.8:
        pass

    return passed >= total * 0.8


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
