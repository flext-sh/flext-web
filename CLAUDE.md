# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**flext-web** is a Flask-based web interface providing management dashboard and REST API for the FLEXT ecosystem. It implements Clean Architecture patterns with flext-core integration, offering application lifecycle management through both web UI and programmatic API access.

**Current State**: Production-ready Flask service with in-memory storage, comprehensive test coverage (90%+), and enterprise-grade documentation. Authentication and persistence layers are planned for future releases.

## Architecture

### Clean Architecture Pattern

The project follows Clean Architecture with Domain-Driven Design:

- **Domain Layer** (`models.py`): Core business entities and rules
  - `FlextWebApp` - Application entity with state machine
  - `FlextWebAppStatus` - Application lifecycle states
  - `FlextWebAppHandler` - CQRS command handler

- **Application Layer** (`services.py`, `config.py`): Use cases and configuration
  - `FlextWebService` - Main Flask service implementation  
  - `FlextWebConfig` - Environment-based configuration management

- **Infrastructure Layer** (`exceptions.py`, `handlers.py`, `fields.py`): Framework integration
  - Flask route handlers and middleware
  - Exception hierarchy extending flext-core
  - Pydantic field validators and types

### Key Architectural Patterns

- **FLEXT Core Integration**: Extends `FlextDomainService`, uses `FlextResult` for error handling
- **Consolidated Classes**: Single class per module pattern (`FlextWeb*` classes contain nested implementations)
- **CQRS**: Command handlers separate from domain entities
- **Railway-Oriented Programming**: `FlextResult[T]` for consistent error handling
- **State Machine**: Application lifecycle with defined transitions
- **Factory Pattern**: Configuration and service creation utilities

## Development Commands

### Essential Commands

```bash
# Complete setup and validation
make setup                  # Install dependencies and pre-commit hooks
make validate              # Run all quality gates (lint + type + test)
make test                  # Run tests with 90% coverage requirement
make runserver             # Start development server on localhost:8080

# Quality gates (run before commits)
make lint                  # Ruff linting (zero tolerance)
make type-check           # MyPy strict type checking
make security             # Bandit security scanning
make format               # Auto-format code
```

### Testing Commands

```bash
# Test execution
make test-unit            # Unit tests only
make test-integration     # Integration tests with real services
make test-api             # REST API endpoint tests
make test-web             # Web interface tests
make coverage-html        # Generate HTML coverage report

# Individual test files
pytest tests/test_simple_api_fixed.py -v
pytest tests/test_config_comprehensive.py -v
pytest tests/test_domain_entities.py -v
```

### Web Development

```bash
# Server operations
make dev-server           # Development server with hot reload
make web-test             # Test service creation locally
make web-health           # Check running service health

# API testing
curl http://localhost:8080/health                    # Health check
curl -X POST http://localhost:8080/api/v1/apps \     # Create app
  -H "Content-Type: application/json" \
  -d '{"name": "test-app", "port": 3000}'
```

## Code Structure and Architecture

### Source Organization

```
src/flext_web/
├── __init__.py          # Main exports and factory functions
├── __main__.py          # CLI entry point
├── config.py           # FlextWebConfigs with nested WebConfig
├── services.py         # FlextWebServices with nested WebService  
├── models.py           # FlextWebModels with WebApp/WebAppHandler
├── exceptions.py       # Exception hierarchy extending flext-core
├── handlers.py         # Request/response handlers
├── fields.py          # Pydantic field validators
├── protocols.py       # Type protocols for interfaces
├── typings.py         # Type aliases and definitions
├── interfaces.py      # Abstract interfaces
└── templates/         # Flask Jinja2 templates
```

### Key Classes and Patterns

**Main Service Class**:
- `FlextWebService` (alias to `FlextWebServices.WebService`) - Flask integration with REST endpoints
- Routes: `/health`, `/`, `/api/v1/apps/*` 
- In-memory app storage in `service.apps` dictionary

**Domain Model**:
- `FlextWebApp` - Entity with `name`, `host`, `port`, `status` fields
- `FlextWebAppStatus` - Enum: STOPPED, STARTING, RUNNING, STOPPING, ERROR
- `FlextWebAppHandler` - CQRS commands: `create()`, `start()`, `stop()`

**Configuration**:
- `FlextWebConfig` - Pydantic settings with environment variable support
- Prefix: `FLEXT_WEB_*` (e.g., `FLEXT_WEB_HOST`, `FLEXT_WEB_PORT`)
- Factory functions: `get_web_settings()`, `create_service()`, `create_app()`

### Type System

The project uses Python 3.13+ strict typing with comprehensive type annotations:

```python
# FlextResult pattern for error handling
from flext_core import FlextResult

def create_app(name: str) -> FlextResult[FlextWebApp]:
    # Railway-oriented programming
    if not name:
        return FlextResult[FlextWebApp].fail("Name required")
    return FlextResult[FlextWebApp].ok(app)

# Type aliases in typings.py
ResponseData = dict[str, object]
ConfigDict = dict[str, object]  
AppDataDict = TypedDict('AppDataDict', {...})
```

## Testing Architecture

### Test Organization

```
tests/
├── unit/               # Fast unit tests
├── integration/        # Real service integration tests
├── e2e/               # End-to-end tests
├── fixtures/          # Test data and utilities
├── conftest.py        # Real execution fixtures (no mocks)
└── test_*.py          # Test modules
```

### Testing Philosophy

**Real Execution Over Mocking**:
- Tests use actual Flask applications and HTTP requests
- `conftest.py` provides real service fixtures with port allocation
- Integration tests start actual services in background threads
- 90%+ coverage requirement with functional validation

**Test Categories**:
```bash
pytest -m unit          # Fast unit tests
pytest -m integration   # Real service tests  
pytest -m api          # HTTP endpoint tests
pytest -m web          # Web interface tests
```

## Configuration Management

### Environment Variables

```bash
# Core web service settings
FLEXT_WEB_HOST=localhost        # Server bind address
FLEXT_WEB_PORT=8080            # Server port
FLEXT_WEB_DEBUG=true           # Debug mode (disable in production)
FLEXT_WEB_SECRET_KEY=secret    # Must change in production (32+ chars)
FLEXT_WEB_APP_NAME="FLEXT Web" # Application identifier

# Advanced settings
FLEXT_WEB_MAX_CONTENT_LENGTH=16777216  # 16MB request limit
FLEXT_WEB_REQUEST_TIMEOUT=30           # Request timeout seconds
FLEXT_WEB_ENABLE_CORS=false            # CORS support
FLEXT_WEB_LOG_LEVEL=INFO               # Logging level
```

### Configuration Patterns

```python
# Singleton configuration access
from flext_web import get_web_settings, reset_web_settings

config = get_web_settings()  # Cached singleton
reset_web_settings()         # Reset for testing

# Service creation with configuration
from flext_web import create_service, create_app

service = create_service()           # Uses default config
service = create_service(config)     # Uses provided config
flask_app = create_app(config)       # Direct Flask app access
```

## API Endpoints

### REST API Structure

**Health and Status**:
- `GET /health` - Service health check with app count
- `GET /` - HTML dashboard with application list

**Application Management**:
- `GET /api/v1/apps` - List all applications
- `POST /api/v1/apps` - Create new application  
- `GET /api/v1/apps/<id>` - Get application details
- `POST /api/v1/apps/<id>/start` - Start application
- `POST /api/v1/apps/<id>/stop` - Stop application

### API Response Format

```json
{
  "success": true,
  "message": "Operation completed",
  "data": {
    "name": "app-name",
    "host": "localhost", 
    "port": 3000,
    "status": "running",
    "id": "app_app-name"
  }
}
```

## Quality Standards

### Mandatory Quality Gates

- **Linting**: Ruff with comprehensive rule set (zero warnings/errors)
- **Type Checking**: MyPy strict mode (zero type errors)
- **Security**: Bandit scanning + pip-audit
- **Testing**: 90%+ coverage with real execution tests
- **Code Quality**: All quality gates must pass before commits

### Type Safety Requirements

- Python 3.13+ with strict type annotations
- All public methods must have complete type signatures
- Use `FlextResult[T]` for error-prone operations
- Leverage Pydantic for data validation and serialization

## Common Development Patterns

### Adding New API Endpoints

1. Add route registration in `FlextWebService._register_routes()`:
```python
self.app.route("/api/v1/new-endpoint", methods=["GET"])(self.new_endpoint)
```

2. Implement handler method:
```python
def new_endpoint(self) -> ResponseReturnValue:
    """Handle new endpoint with validation."""
    return jsonify({
        "success": True,
        "message": "Success message",
        "data": response_data
    })
```

3. Add comprehensive tests in appropriate test file
4. Run `make validate` to ensure quality gates pass

### Extending Domain Models

1. Modify `FlextWebApp` entity with new fields (use Pydantic Field)
2. Update validation in `validate_business_rules()`
3. Extend `FlextWebAppHandler` if new operations needed
4. Add unit tests for business logic validation
5. Update API responses to include new fields

### Configuration Changes

1. Add new field to `FlextWebConfig` in `config.py`
2. Add validation logic if needed
3. Update environment variable documentation
4. Add configuration tests with various scenarios
5. Test both development and production configurations

## Integration with FLEXT Ecosystem

### FLEXT Core Dependencies

```python
from flext_core import (
    FlextCore,           # Base facade class
    FlextDomainService,  # Service base class  
    FlextEntity,         # Domain entity base
    FlextResult,         # Error handling type
    get_logger,         # Structured logging
)
```

### Service Integration Points

- **flext-observability**: Monitoring and metrics collection (planned)
- **flext-auth**: Authentication and authorization (planned)  
- **FlexCore (Go)**: Runtime service coordination (future)
- **FLEXT Service**: Data platform integration (future)

## Troubleshooting

### Common Issues

**Service won't start**:
```bash
# Check port availability
netstat -tulpn | grep 8080

# Verify configuration
python -c "from flext_web import get_web_settings; print(get_web_settings())"

# Test service creation
make web-test
```

**Test failures**:
```bash
# Run specific test with verbose output
pytest tests/test_simple_api_fixed.py -v -s

# Check coverage gaps
make coverage-html
```

**Type errors**:
```bash
# Check MyPy errors with context
make type-check

# Fix imports and type annotations
# Ensure all FlextResult usage is correct
```

### Development Workflow

1. **Make changes**: Edit source code following architectural patterns
2. **Run quality gates**: `make validate` (must pass completely)
3. **Test thoroughly**: `make test` with coverage validation  
4. **Start service**: `make runserver` for manual testing
5. **API testing**: Use curl commands or Postman for endpoint validation