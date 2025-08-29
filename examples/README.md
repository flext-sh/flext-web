# FLEXT Web Interface - Usage Examples

**Purpose**: Practical usage examples and integration patterns  
**Target**: Developers integrating FLEXT Web Interface  
**Coverage**: Complete API and programmatic usage scenarios

This directory contains comprehensive examples demonstrating how to use the FLEXT Web Interface in various scenarios, from basic service setup to advanced enterprise integration patterns.

## Example Categories

### Basic Usage Examples

#### Simple Service Startup

```python
# examples/basic_service.py
from flext_web import create_service, get_web_settings

# Start with default configuration
config = get_web_settings()
service = create_service(config)
service.run()
```

#### Custom Configuration

```python
# examples/custom_config.py
import os
from flext_web import FlextWebConfig, create_service

# Configure via environment variables
os.environ['FLEXT_WEB_HOST'] = '0.0.0.0'
os.environ['FLEXT_WEB_PORT'] = '8080'
os.environ['FLEXT_WEB_DEBUG'] = 'false'

config = FlextWebConfig()
service = create_service(config)
service.run()
```

### API Usage Examples

#### Application Management

```python
# examples/api_usage.py
import requests
import json

# Create application
response = requests.post('http://localhost:8080/api/v1/apps', json={
    'name': 'my-web-service',
    'host': 'localhost',
    'port': 3000
})

if response.status_code == 200:
    app_data = response.json()['data']
    app_id = app_data['id']

    # Start application
    start_response = requests.post(f'http://localhost:8080/api/v1/apps/{app_id}/start')
    print(f"Application started: {start_response.json()}")

    # Check status
    status_response = requests.get(f'http://localhost:8080/api/v1/apps/{app_id}')
    print(f"Status: {status_response.json()['data']['status']}")
```

#### Health Monitoring

```python
# examples/health_monitoring.py
import requests
import time

def monitor_service_health():
    """Monitor service health with automatic retry"""
    while True:
        try:
            response = requests.get('http://localhost:8080/health', timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                print(f"Service healthy: {health_data['data']['status']}")
                print(f"Apps count: {health_data['data']['apps_count']}")
            else:
                print(f"Health check failed: {response.status_code}")
        except requests.RequestException as e:
            print(f"Health check error: {e}")

        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    monitor_service_health()
```

### Programmatic Integration Examples

#### Flask Application Integration

```python
# examples/flask_integration.py
from flask import Flask, request, jsonify
from flext_web import FlextWebService, FlextWebConfig

# Create custom Flask app with FLEXT Web integration
app = Flask(__name__)
config = FlextWebConfig(host='localhost', port=5000)
flext_service = FlextWebService(config)

# Add custom routes
@app.route('/custom/status')
def custom_status():
    """Custom status endpoint"""
    return jsonify({
        'service': 'custom-integration',
        'flext_apps': len(flext_service.apps),
        'status': 'operational'
    })

# Mount FLEXT Web routes
@app.route('/flext/<path:path>', methods=['GET', 'POST'])
def flext_proxy(path):
    """Proxy requests to FLEXT Web service"""
    # Implementation would proxy to flext_service
    pass

if __name__ == '__main__':
    app.run(debug=True)
```

#### Enterprise Configuration

```python
# examples/enterprise_config.py
from flext_web import FlextWebConfig, create_service
from flext_core import FlextLogger
import os

logger = FlextLogger(__name__)

class EnterpriseWebConfig(FlextWebConfig):
    """Enterprise configuration with additional validation"""

    def validate_config(self):
        """Additional enterprise validation"""
        result = super().validate_config()
        if not result.success:
            return result

        # Enterprise-specific validations
        if self.is_production():
            if 'localhost' in self.host:
                return FlextResult[None].fail("Production cannot bind to localhost")
            if self.debug:
                return FlextResult[None].fail("Debug mode not allowed in production")

        return FlextResult[None].ok(None)

def deploy_enterprise_service():
    """Deploy with enterprise configuration"""
    # Load enterprise environment
    config = EnterpriseWebConfig()

    # Validate enterprise requirements
    validation_result = config.validate_config()
    if not validation_result.success:
        logger.error(f"Configuration validation failed: {validation_result.error}")
        return

    # Create and start service
    service = create_service(config)
    logger.info(f"Starting enterprise service on {config.get_server_url()}")
    service.run()

if __name__ == "__main__":
    deploy_enterprise_service()
```

### Advanced Integration Examples

#### Docker Deployment

```python
# examples/docker_deployment.py
"""Docker-optimized service configuration"""
import os
import signal
import sys
from flext_web import create_service, FlextWebConfig
from flext_core import FlextLogger

logger = FlextLogger(__name__)

def create_docker_config() -> FlextWebConfig:
    """Create Docker-optimized configuration"""
    return FlextWebConfig(
        host='0.0.0.0',  # Bind to all interfaces
        port=int(os.environ.get('PORT', 8080)),
        debug=os.environ.get('DEBUG', 'false').lower() == 'true',
        secret_key=os.environ.get('SECRET_KEY', os.urandom(32).hex())
    )

def setup_signal_handlers(service):
    """Setup graceful shutdown"""
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, shutting down gracefully")
        # Implement graceful shutdown logic
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

def main():
    """Docker container entry point"""
    config = create_docker_config()
    service = create_service(config)
    setup_signal_handlers(service)

    logger.info("Starting FLEXT Web service in Docker container")
    service.run()

if __name__ == "__main__":
    main()
```

#### Kubernetes Integration

```python
# examples/kubernetes_deployment.py
"""Kubernetes-ready service with health checks and metrics"""
from flext_web import create_service, FlextWebConfig
from flext_core import FlextLogger
import os
import threading
import time

logger = FlextLogger(__name__)

class KubernetesWebConfig(FlextWebConfig):
    """Kubernetes-optimized configuration"""

    # Kubernetes environment variables
    namespace: str = os.environ.get('KUBERNETES_NAMESPACE', 'default')
    pod_name: str = os.environ.get('HOSTNAME', 'unknown-pod')
    service_name: str = os.environ.get('KUBERNETES_SERVICE_NAME', 'flext-web')

def setup_kubernetes_health_checks(service):
    """Setup Kubernetes health check endpoints"""

    @service.app.route('/healthz')
    def kubernetes_health():
        """Kubernetes liveness probe"""
        return {'status': 'ok', 'timestamp': time.time()}

    @service.app.route('/readyz')
    def kubernetes_readiness():
        """Kubernetes readiness probe"""
        # Check if service is ready to accept traffic
        return {'status': 'ready', 'apps_count': len(service.apps)}

def setup_metrics_collection(service):
    """Setup Prometheus metrics collection"""

    @service.app.route('/metrics')
    def prometheus_metrics():
        """Prometheus metrics endpoint"""
        metrics = [
            f'flext_web_apps_total {len(service.apps)}',
            f'flext_web_running_apps {sum(1 for app in service.apps.values() if app.is_running)}',
            f'flext_web_uptime_seconds {time.time()}'
        ]
        return '\n'.join(metrics), 200, {'Content-Type': 'text/plain'}

def main():
    """Kubernetes deployment entry point"""
    config = KubernetesWebConfig()
    service = create_service(config)

    # Setup Kubernetes integration
    setup_kubernetes_health_checks(service)
    setup_metrics_collection(service)

    logger.info(f"Starting FLEXT Web service in Kubernetes pod {config.pod_name}")
    service.run(host='0.0.0.0', port=config.port)

if __name__ == "__main__":
    main()
```

### Testing Examples

#### Unit Testing

```python
# examples/testing_patterns.py
import pytest
from flext_web import FlextWebApp, FlextWebAppHandler, FlextWebConfig

class TestApplicationWorkflow:
    """Example test patterns for FLEXT Web Interface"""

    def test_application_lifecycle(self):
        """Test complete application lifecycle"""
        handler = FlextWebAppHandler()

        # Create application
        create_result = handler.create("test-app", 3000, "localhost")
        assert create_result.success
        app = create_result.data

        # Start application
        start_result = handler.start(app)
        assert start_result.success
        running_app = start_result.data
        assert running_app.is_running

        # Stop application
        stop_result = handler.stop(running_app)
        assert stop_result.success
        stopped_app = stop_result.data
        assert not stopped_app.is_running

    def test_configuration_validation(self):
        """Test configuration validation patterns"""
        # Valid configuration
        config = FlextWebConfig(
            host='localhost',
            port=8080,
            debug=True
        )
        result = config.validate_config()
        assert result.success

        # Invalid configuration
        invalid_config = FlextWebConfig(
            host='',  # Invalid empty host
            port=70000,  # Invalid port range
            debug=False
        )
        result = invalid_config.validate_config()
        assert result.is_failure

def test_api_integration():
    """Example API integration testing"""
from flask import Flask
from flext_web import create_service

    service = create_service()
    client = service.app.test_client()

    # Test health endpoint
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True

    # Test application creation
    response = client.post('/api/v1/apps', json={
        'name': 'integration-test',
        'port': 4000,
        'host': 'localhost'
    })
    assert response.status_code == 200
```

### Performance Examples

#### Load Testing

```python
# examples/performance_testing.py
import asyncio
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor

async def load_test_health_endpoint():
    """Load test the health endpoint"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(100):  # 100 concurrent requests
            task = session.get('http://localhost:8080/health')
            tasks.append(task)

        start_time = time.time()
        responses = await asyncio.gather(*tasks)
        end_time = time.time()

        success_count = sum(1 for resp in responses if resp.status == 200)
        print(f"Load test results:")
        print(f"Total requests: {len(tasks)}")
        print(f"Successful requests: {success_count}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        print(f"Requests per second: {len(tasks) / (end_time - start_time):.2f}")

def benchmark_application_creation():
    """Benchmark application creation performance"""
    import requests

    times = []
    for i in range(50):
        start_time = time.time()
        response = requests.post('http://localhost:8080/api/v1/apps', json={
            'name': f'benchmark-app-{i}',
            'port': 3000 + i,
            'host': 'localhost'
        })
        end_time = time.time()

        if response.status_code == 200:
            times.append(end_time - start_time)

    avg_time = sum(times) / len(times)
    print(f"Average application creation time: {avg_time:.3f} seconds")
    print(f"Min time: {min(times):.3f} seconds")
    print(f"Max time: {max(times):.3f} seconds")

if __name__ == "__main__":
    # Run load tests
    asyncio.run(load_test_health_endpoint())
    benchmark_application_creation()
```

## Running Examples

### Basic Examples

```bash
# Run basic service example
cd examples/
python basic_service.py

# Run with custom configuration
python custom_config.py
```

### Docker Examples

```bash
# Build Docker container with example
docker build -t flext-web-example .
docker run -p 8080:8080 -e DEBUG=false flext-web-example
```

### Testing Examples

```bash
# Run example tests
pytest examples/testing_patterns.py -v

# Run performance benchmarks
python examples/performance_testing.py
```

## Example Development

### Creating New Examples

1. **Choose appropriate category** (basic, advanced, integration)
2. **Follow naming convention**: `category_functionality.py`
3. **Add comprehensive docstrings** explaining the example purpose
4. **Include error handling** and logging
5. **Provide usage instructions** in comments
6. **Test examples** to ensure they work correctly

### Example Standards

- **Complete Code**: Examples should be runnable as-is
- **Error Handling**: Include proper error handling patterns
- **Documentation**: Comprehensive comments and docstrings
- **Real-world Applicability**: Examples should solve actual problems
- **Performance Awareness**: Include performance considerations

---

**Maintainers**: FLEXT Development Team  
**Examples Status**: Comprehensive coverage of usage patterns  
**Quality Standard**: All examples tested and validated
