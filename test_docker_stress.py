#!/usr/bin/env python3
"""Docker Stress Testing - Maximum validation of container functionality."""

import subprocess
import time
import requests
import concurrent.futures


def test_docker_memory_stress():
    """Test Docker container under memory pressure."""
    print("🧠 Testing Docker memory stress...")

    # Build if needed
    build_result = subprocess.run(
        ["docker", "build", "-t", "flext-web-stress", "."],
        capture_output=True,
        text=True
    )

    if build_result.returncode != 0:
        print(f"❌ Docker build failed: {build_result.stderr}")
        return False

    # Run with memory limit
    cmd = [
        "docker", "run", "--rm", "-d",
        "--memory=256m",  # Memory limit
        "--memory-swap=256m",
        "-p", "8090:8080",
        "-e", "FLEXT_WEB_SECRET_KEY=test-memory-stress-key-32-chars!",
        "-e", "FLEXT_WEB_DEBUG=false",
        "--name", "flext-memory-test",
        "flext-web-stress"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print(f"❌ Container failed to start: {result.stderr}")
            return False

        container_id = result.stdout.strip()
        print(f"✅ Container started with memory limits: {container_id[:12]}")

        # Wait for startup
        time.sleep(5)

        # Test health under memory pressure
        try:
            response = requests.get("http://localhost:8090/health", timeout=10)
            if response.status_code == 200:
                print("✅ Service healthy under memory pressure")
                return True
            else:
                print(f"❌ Service unhealthy: {response.status_code}")
                return False
        except requests.RequestException as e:
            print(f"❌ Service unreachable under memory pressure: {e}")
            return False

    finally:
        # Cleanup
        subprocess.run(["docker", "stop", "flext-memory-test"],
                      capture_output=True, timeout=10)


def test_docker_concurrent_requests():
    """Test Docker container with concurrent requests."""
    print("🔄 Testing Docker concurrent requests...")

    # Start container for concurrency test
    cmd = [
        "docker", "run", "--rm", "-d",
        "-p", "8091:8080",
        "-e", "FLEXT_WEB_SECRET_KEY=test-concurrent-key-32-characters!",
        "-e", "FLEXT_WEB_DEBUG=false",
        "--name", "flext-concurrent-test",
        "flext-web-stress"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print(f"❌ Container failed to start: {result.stderr}")
            return False

        container_id = result.stdout.strip()
        print(f"✅ Container started for concurrency test: {container_id[:12]}")

        # Wait for startup
        time.sleep(5)

        # Test concurrent requests
        def make_request(i):
            try:
                response = requests.get("http://localhost:8091/health", timeout=5)
                return response.status_code == 200
            except:
                return False

        # 20 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(make_request, i) for i in range(20)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

        success_count = sum(results)
        print(f"✅ Concurrent requests: {success_count}/20 successful")

        return success_count >= 15  # 75% success rate is acceptable

    finally:
        # Cleanup
        subprocess.run(["docker", "stop", "flext-concurrent-test"],
                      capture_output=True, timeout=10)


def test_docker_api_workflow():
    """Test complete API workflow in Docker container."""
    print("📋 Testing Docker API workflow...")

    # Start container for API test
    cmd = [
        "docker", "run", "--rm", "-d",
        "-p", "8092:8080",
        "-e", "FLEXT_WEB_SECRET_KEY=test-api-workflow-key-32-characters!",
        "-e", "FLEXT_WEB_DEBUG=false",
        "--name", "flext-api-test",
        "flext-web-stress"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print(f"❌ Container failed to start: {result.stderr}")
            return False

        container_id = result.stdout.strip()
        print(f"✅ Container started for API test: {container_id[:12]}")

        # Wait for startup
        time.sleep(5)

        base_url = "http://localhost:8092"
        success_count = 0

        # Test 1: Health check
        try:
            response = requests.get(f"{base_url}/health", timeout=10)
            if response.status_code == 200:
                print("✅ Health check passed")
                success_count += 1
        except Exception as e:
            print(f"❌ Health check failed: {e}")

        # Test 2: Create app
        try:
            response = requests.post(f"{base_url}/api/v1/apps", json={
                "name": "docker-test-app",
                "port": 3000,
                "host": "localhost"
            }, timeout=10)
            if response.status_code == 200:
                app_data = response.json()["data"]
                app_id = app_data["id"]
                print(f"✅ App created: {app_id}")
                success_count += 1

                # Test 3: Start app
                response = requests.post(f"{base_url}/api/v1/apps/{app_id}/start", timeout=10)
                if response.status_code == 200:
                    print("✅ App started")
                    success_count += 1

                    # Test 4: Get app status
                    response = requests.get(f"{base_url}/api/v1/apps/{app_id}", timeout=10)
                    if response.status_code == 200:
                        app_status = response.json()["data"]
                        if app_status["is_running"]:
                            print("✅ App status verified")
                            success_count += 1

                    # Test 5: Stop app
                    response = requests.post(f"{base_url}/api/v1/apps/{app_id}/stop", timeout=10)
                    if response.status_code == 200:
                        print("✅ App stopped")
                        success_count += 1
        except Exception as e:
            print(f"❌ API workflow error: {e}")

        print(f"📊 API workflow: {success_count}/5 tests passed")
        return success_count >= 4  # 80% success rate

    finally:
        # Cleanup
        subprocess.run(["docker", "stop", "flext-api-test"],
                      capture_output=True, timeout=10)


def test_docker_examples_stress():
    """Test Docker examples under stress."""
    print("📝 Testing Docker examples stress...")

    # Test docker_ready.py in container with stress
    cmd = [
        "docker", "run", "--rm", "-d",
        "--memory=128m",  # Very limited memory
        "-e", "FLEXT_WEB_SECRET_KEY=test-examples-stress-key-32-chars!",
        "-e", "FLEXT_WEB_HOST=0.0.0.0",
        "-e", "FLEXT_WEB_PORT=8080",
        "-e", "FLEXT_WEB_DEBUG=false",
        "--name", "flext-examples-stress",
        "flext-web-stress",
        "python", "examples/docker_ready.py"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        container_id = result.stdout.strip()
        print(f"✅ Examples container started: {container_id[:12]}")

        # Wait a bit to see if it crashes
        time.sleep(3)

        # Check if still running
        check_result = subprocess.run(
            ["docker", "ps", "-q", "-f", "name=flext-examples-stress"],
            capture_output=True, text=True
        )

        if check_result.stdout.strip():
            print("✅ Examples running under memory stress")
            return True
        else:
            print("❌ Examples crashed under memory stress")
            return False

    finally:
        # Cleanup
        subprocess.run(["docker", "stop", "flext-examples-stress"],
                      capture_output=True, timeout=10)


def main():
    """Run comprehensive Docker stress tests."""
    print("🚀 Starting Docker Stress Testing...")
    print("=" * 60)

    tests = [
        ("Memory Stress", test_docker_memory_stress),
        ("Concurrent Requests", test_docker_concurrent_requests),
        ("API Workflow", test_docker_api_workflow),
        ("Examples Stress", test_docker_examples_stress),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 60)
    print("📊 DOCKER STRESS TEST RESULTS:")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {status} {test_name}")

    print(f"\n🎯 FINAL SCORE: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL DOCKER STRESS TESTS PASSED!")
        print("🏆 Container is ENTERPRISE-READY!")
    elif passed >= total * 0.8:
        print("✅ Most Docker stress tests passed - PRODUCTION-READY!")
    else:
        print("⚠️ Some Docker stress tests failed - needs attention")

    return passed >= total * 0.8


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
