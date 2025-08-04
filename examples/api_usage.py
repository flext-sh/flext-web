#!/usr/bin/env python3
"""FLEXT Web Interface - API Usage Example.

Demonstrates how to interact with the FLEXT Web Interface REST API
for application lifecycle management.
"""


import requests

BASE_URL = "http://localhost:8080"


def check_service_health() -> bool | None:
    """Check if the service is running and healthy."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Service healthy: {health_data.get('success', True)}")
            return True
        print(f"❌ Service unhealthy: {response.status_code}")
        return False
    except requests.RequestException as e:
        print(f"❌ Service unreachable: {e}")
        return False


def create_application(name, port, host="localhost"):
    """Create a new application."""
    data = {"name": name, "port": port, "host": host}

    try:
        response = requests.post(f"{BASE_URL}/api/v1/apps", json=data)
        if response.status_code == 200:
            app_data = response.json()["data"]
            print(f"✅ Created app: {app_data['name']} (ID: {app_data['id']})")
            return app_data
        error_data = response.json()
        print(f"❌ Failed to create app: {error_data.get('error', 'Unknown error')}")
        return None
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None


def start_application(app_id):
    """Start an application."""
    try:
        response = requests.post(f"{BASE_URL}/api/v1/apps/{app_id}/start")
        if response.status_code == 200:
            app_data = response.json()["data"]
            print(f"🚀 Started app: {app_data['name']} (Status: {app_data['status']})")
            return app_data
        error_data = response.json()
        print(f"❌ Failed to start app: {error_data.get('error', 'Unknown error')}")
        return None
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None


def get_application_status(app_id):
    """Get application status."""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/apps/{app_id}")
        if response.status_code == 200:
            return response.json()["data"]
        return None
    except requests.RequestException:
        return None


def stop_application(app_id):
    """Stop an application."""
    try:
        response = requests.post(f"{BASE_URL}/api/v1/apps/{app_id}/stop")
        if response.status_code == 200:
            app_data = response.json()["data"]
            print(f"🛑 Stopped app: {app_data['name']} (Status: {app_data['status']})")
            return app_data
        error_data = response.json()
        print(f"❌ Failed to stop app: {error_data.get('error', 'Unknown error')}")
        return None
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None


def list_applications():
    """List all applications."""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/apps")
        if response.status_code == 200:
            data = response.json()["data"]
            apps = data["apps"]
            print(f"📋 Applications ({len(apps)}):")
            for app in apps:
                status_icon = "🟢" if app["is_running"] else "🔴"
                print(f"  {status_icon} {app['name']} (ID: {app['id']}, Status: {app['status']})")
            return apps
        error_data = response.json()
        print(f"❌ Failed to list apps: {error_data.get('error', 'Unknown error')}")
        return []
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return []


def demo_application_lifecycle() -> None:
    """Demonstrate complete application lifecycle."""
    print("🚀 Starting FLEXT Web API Demo")
    print("=" * 50)

    # Check service health
    print("\n1️⃣ Checking service health...")
    if not check_service_health():
        print("❌ Service not available, exiting demo")
        return

    print("\n2️⃣ Creating applications...")
    # Create applications
    app1 = create_application("web-service", 3000)
    app2 = create_application("api-gateway", 4000, "0.0.0.0")

    if not app1 or not app2:
        print("❌ Failed to create applications, exiting demo")
        return

    print("\n3️⃣ Initial application list:")
    # List applications
    list_applications()

    print("\n4️⃣ Starting applications...")
    # Start applications
    start_application(app1["id"])
    start_application(app2["id"])

    print("\n5️⃣ Checking individual status...")
    # Check status
    for app_id in [app1["id"], app2["id"]]:
        status = get_application_status(app_id)
        if status:
            status_icon = "🟢" if status["is_running"] else "🔴"
            print(f"  {status_icon} {status['name']}: {status['status']}")

    print("\n6️⃣ Updated application list:")
    # List applications again
    list_applications()

    print("\n7️⃣ Stopping applications...")
    # Stop applications
    stop_application(app1["id"])
    stop_application(app2["id"])

    print("\n8️⃣ Final application list:")
    # Final status
    list_applications()

    print("\n✅ Demo completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    demo_application_lifecycle()
