# FLEXT Web Interface - Test Suite

**Coverage**: 90%+ | **Framework**: pytest | **Standards**: Enterprise Testing Patterns

Comprehensive test suite for the FLEXT Web Interface implementing enterprise testing standards with unit, integration, and end-to-end test coverage. The test suite follows Clean Architecture principles with clear separation between domain, application, and infrastructure testing.

## Test Organization

### Test Structure

```
tests/
├── README.md                           # This file - test suite overview
├── conftest.py                         # Shared test configuration and fixtures
├── test_config_comprehensive.py       # Configuration validation tests
├── test_domain_entities.py            # Domain entity and business logic tests
├── test_main_entry.py                 # CLI entry point and argument parsing tests
├── test_simple_api_fixed.py          # REST API endpoint integration tests
└── test_simple_web_fixed.py          # Web interface and dashboard tests
```

### Test Categories

#### Unit Tests (`pytest -m unit`)

- **Domain Entities**: FlextWebApp, FlextWebAppStatus business logic
- **Configuration**: FlextWebConfig validation and environment handling
- **Handlers**: FlextWebAppHandler CQRS command processing
- **Exceptions**: Domain-specific exception hierarchy

#### Integration Tests (`pytest -m integration`)

- **API Endpoints**: REST API request/response validation
- **Flask Integration**: Service initialization and route registration
- **Configuration Integration**: Environment variable loading
- **Error Handling**: Exception propagation and error responses

#### End-to-End Tests (`pytest -m e2e`)

- **Complete Workflows**: Application creation, start, stop lifecycle
- **Web Dashboard**: HTML rendering and user interface
- **CLI Integration**: Command-line argument processing
- **Service Health**: Health check and monitoring endpoints

## Test Standards

### Quality Requirements

- **Coverage**: 90% target
- **Type Safety**: All test code uses type hints
- **Documentation**: Every test function has descriptive docstrings
- **Isolation**: Tests are completely isolated with clean fixtures
- **Performance**: Unit tests complete in < 1 second each

### Testing Patterns

#### FlextResult Testing

```python
def test_successful_operation():
    """Test successful operation returns FlextResult[None].ok()"""
    result = handler.create_app("test-app", 3000)

    assert result.success
    assert result.data is not None
    assert result.error is None

def test_failure_operation():
    """Test failure operation returns FlextResult[None].fail()"""
    result = handler.create_app("", 0)  # Invalid input

    assert result.is_failure
    assert result.data is None
    assert "validation" in result.error.lower()
```

#### Domain Entity Testing

```python
def test_domain_business_rules():
    """Test domain entity enforces business rules"""
    app = FlextWebApp(name="test", host="localhost", port=3000)

    # Test state transitions
    result = app.start()
    assert result.success
    assert app.status == FlextWebAppStatus.RUNNING

    # Test invalid state transition
    result = app.start()  # Already running
    assert result.is_failure
```

#### API Testing

```python
def test_api_endpoint_success():
    """Test API endpoint handles valid requests"""
    client = app.test_client()
    response = client.post('/api/v1/apps', json={
        'name': 'test-app',
        'port': 3000,
        'host': 'localhost'
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'test-app' in data['data']['name']
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests with coverage
make test

# Run specific test categories
pytest -m unit                    # Unit tests only
pytest -m integration             # Integration tests only
pytest -m "not slow"              # Fast tests for development

# Run specific test files
pytest tests/test_domain_entities.py -v
pytest tests/test_simple_api_fixed.py::test_create_app_success
```

### Development Testing

```bash
# Watch mode for continuous testing
pytest --watch

# Run tests with detailed output
pytest -v -s

# Run with coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

### Performance Testing

```bash
# Run performance tests
pytest -m performance

# Benchmark critical paths
pytest --benchmark-only

# Memory profiling
pytest --profile
```

## Test Configuration

### Fixtures (`conftest.py`)

- **clean_config**: Fresh FlextWebConfig for each test
- **test_app**: Isolated Flask application instance
- **mock_handler**: Mocked FlextWebAppHandler for unit tests
- **sample_web_app**: Pre-configured FlextWebApp for testing

### Test Data

Tests use predictable, isolated test data:

```python
SAMPLE_APP_DATA = {
    "name": "test-app",
    "host": "localhost",
    "port": 3000,
    "status": "stopped"
}

INVALID_APP_DATA = {
    "name": "",  # Invalid empty name
    "port": 70000,  # Invalid port range
    "host": ""  # Invalid empty host
}
```

## Test Documentation

### Test File Documentation

#### test_config_comprehensive.py

Comprehensive configuration validation testing including:

- Environment variable loading and precedence
- Configuration validation rules and business logic
- Production vs development mode behavior
- Secret key validation and security checks

#### test_domain_entities.py

Domain entity business logic and validation testing:

- FlextWebApp entity state management
- FlextWebAppStatus enumeration and transitions
- Domain rule validation and error handling
- Entity lifecycle and timestamp management

#### test_main_entry.py

CLI entry point and argument parsing validation:

- Command-line argument processing
- Configuration override behavior
- Error handling and exit codes
- Service initialization and startup

#### test_simple_api_fixed.py

REST API endpoint integration testing:

- Application CRUD operations via HTTP
- Request/response validation and serialization
- Error handling and HTTP status codes
- Authentication and authorization (when implemented)

#### test_simple_web_fixed.py

Web interface and dashboard functionality:

- HTML rendering and template processing
- Dashboard metrics and application display
- User interface responsiveness
- Browser compatibility and accessibility

## Quality Gates

### Pre-Commit Validation

All tests must pass before code commits:

```bash
# Complete validation pipeline
make validate

# Quick test validation
make test-quick

# Test coverage check
make coverage-check
```

### CI/CD Integration

Tests are automatically executed in CI/CD pipeline with:

- Multiple Python versions (3.11, 3.12, 3.13)
- Different operating systems (Linux, macOS, Windows)
- Various dependency versions
- Performance regression detection

## Troubleshooting

### Common Test Issues

#### Test Database Connection

```bash
# Reset test database
make test-db-reset

# Check test database connection
make test-db-check
```

#### Test Coverage Issues

```bash
# Generate detailed coverage report
pytest --cov=src --cov-report=term-missing

# Find uncovered lines
pytest --cov=src --cov-fail-under=90
```

#### Performance Test Failures

```bash
# Run performance tests in isolation
pytest -m performance --no-cov

# Profile slow tests
pytest --profile --profile-svg
```

### Test Environment Setup

```bash
# Setup test environment
make test-setup

# Install test dependencies
pip install -e .[test]

# Verify test environment
make test-env-check
```

## Contributing

### Adding New Tests

1. **Choose appropriate test file** based on functionality
2. **Follow naming conventions**: `test_<functionality>_<scenario>`
3. **Add comprehensive docstrings** explaining test purpose
4. **Use appropriate test markers**: `@pytest.mark.unit`, `@pytest.mark.integration`
5. **Maintain test isolation** with proper fixtures
6. **Validate test coverage** with `make coverage-check`

### Test Review Checklist

- [ ] **Descriptive test names** explaining what is being tested
- [ ] **Comprehensive docstrings** with test purpose and expectations
- [ ] **Proper test isolation** without side effects
- [ ] **Type hints** for all test parameters and variables
- [ ] **Coverage validation** ensuring new code is tested
- [ ] **Performance validation** ensuring tests run efficiently

---

**Maintainers**: FLEXT Development Team  
**Test Framework**: pytest 7.4+ with enterprise plugins  
**Quality Standard**: 90% coverage minimum with comprehensive validation
