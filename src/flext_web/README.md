# FLEXT Web Interface - Source Code

**Module**: `flext_web` - Enterprise web management console for FLEXT ecosystem  
**Architecture**: Clean Architecture + Domain-Driven Design + FLEXT Core Integration  
**Version**: 0.9.0 (Development)

## Overview

This directory contains the source code for the FLEXT Web Interface, an enterprise-grade web management console that provides comprehensive dashboard and REST API endpoints for monitoring and managing applications within the FLEXT distributed data integration ecosystem.

## Module Structure

### Current Implementation (Monolithic - Requires Refactoring)

```
src/flext_web/
├── __init__.py          # Main module (518 lines) - ALL layers consolidated
│                        # ⚠️ CRITICAL: Violates Clean Architecture separation
├── __main__.py          # CLI entry point with argument parsing
├── exceptions.py        # Domain-specific exception hierarchy
├── py.typed            # Type checking marker for MyPy
└── templates/          # Flask templates (currently unused)
    ├── base.html       # Django-style template (incompatible)
    └── dashboard.html  # Dashboard template (not used)
```

### Target Architecture (Post-Refactoring)

```
src/flext_web/
├── __init__.py          # Public API exports only
├── domain/              # Domain Layer (Business Logic)
│   ├── entities.py      # FlextWebApp domain entity
│   ├── value_objects.py # WebAppStatus, HostPort value objects
│   ├── repositories.py  # Repository interfaces
│   └── services.py      # Domain services
├── application/         # Application Layer (Use Cases)
│   ├── handlers.py      # CQRS command handlers
│   ├── commands.py      # Command definitions
│   ├── queries.py       # Query definitions
│   └── config.py        # Configuration management
├── infrastructure/     # Infrastructure Layer (External Concerns)
│   ├── persistence/     # Database and storage
│   ├── web/            # Web framework integration
│   └── external/       # External service integration
└── interfaces/         # Interface Layer (Controllers)
    ├── api/            # REST API endpoints
    ├── web/            # Web dashboard
    └── cli/            # Command-line interface
```

## Components

### Domain Layer

#### FlextWebApp Entity

Rich domain entity implementing application lifecycle management with state machine patterns.

**Key Features**:

- State management (STOPPED, STARTING, RUNNING, STOPPING, ERROR)
- Business rule validation using flext-core patterns
- State transition validation with comprehensive error handling
- Integration with FlextResult for railway-oriented programming

**Usage**:

```python
from flext_web import FlextWebApp, FlextWebAppStatus

app = FlextWebApp(
    id="app_web-service",
    name="web-service",
    host="localhost",
    port=3000
)

# Start application with validation
result = app.start()
if result.success:
    running_app = result.data
    print(f"Started: {running_app.name}")
```

#### FlextWebAppStatus Enumeration

Application status enumeration with state transition rules and business logic.

**States**:

- `STOPPED`: Application not running, can be started
- `STARTING`: Transitional state during startup
- `RUNNING`: Application actively running
- `STOPPING`: Transitional state during shutdown
- `ERROR`: Error state requiring intervention

### Application Layer

#### FlextWebAppHandler

CQRS command handler implementing application service patterns with comprehensive validation.

**Operations**:

- `create()`: Create new application with validation
- `start()`: Start application with state management
- `stop()`: Stop application with graceful shutdown

**Usage**:

```python
from flext_web import FlextWebAppHandler

handler = FlextWebAppHandler()

# Create application
result = handler.create("api-service", port=8080, host="0.0.0.0")
if result.success:
    app = result.data

    # Start application
    start_result = handler.start(app)
    if start_result.success:
        print(f"Application {start_result.data.name} is running")
```

#### FlextWebConfig

Environment-based configuration management with comprehensive validation and production safety checks.

**Features**:

- Environment variable integration (`FLEXT_WEB_*` prefix)
- Comprehensive validation with business rules
- Production safety checks and security validation
- Integration with flext-core configuration patterns

**Usage**:

```python
from flext_web import FlextWebConfig, get_web_settings

# Get validated configuration
config = get_web_settings()
print(f"Server URL: {config.get_server_url()}")
print(f"Production mode: {config.is_production()}")
```

### Infrastructure Layer

#### FlextWebService

Flask integration service providing REST API endpoints and web dashboard with comprehensive route management.

**Features**:

- REST API endpoints for application management
- Inline HTML dashboard generation
- Health check endpoints with system status
- Standardized JSON response patterns
- Integration with CQRS handlers

**API Endpoints**:

- `GET /health` - Service health check
- `GET /` - Web dashboard
- `GET /api/v1/apps` - List applications
- `POST /api/v1/apps` - Create application
- `GET /api/v1/apps/<id>` - Get application details
- `POST /api/v1/apps/<id>/start` - Start application
- `POST /api/v1/apps/<id>/stop` - Stop application

### CLI Interface

#### Entry Point (`__main__.py`)

Command-line interface with argument parsing and service initialization.

**Features**:

- Host and port override options
- Debug mode control
- Configuration validation
- Service startup with error handling

**Usage**:

```bash
# Development mode
python -m flext_web --debug --host localhost --port 8080

# Production mode
python -m flext_web --no-debug --host 0.0.0.0 --port 8080
```

## FLEXT Core Integration

### Foundation Patterns

The module extensively uses flext-core foundation patterns for consistency across the FLEXT ecosystem:

- **FlextResult**: Railway-oriented programming for error handling
- **FlextEntity**: Domain entity base class with validation
- **FlextConfig**: Configuration management with validation
- **FlextHandlers**: CQRS command handler patterns
- **FlextValidators**: Consistent validation rules

### Error Handling

All operations use FlextResult for consistent error handling:

```python
from flext_core import FlextResult

def process_request(data: dict) -> FlextResult[FlextWebApp]:
    return (
        validate_input(data)
        .flat_map(create_application)
        .flat_map(save_to_storage)
        .map(format_response)
    )
```

## Current Issues (Critical)

### 1. Monolithic Architecture

- **Issue**: 518 lines in single `__init__.py` file
- **Impact**: Violates Single Responsibility Principle, difficult to maintain
- **Resolution**: Refactor into Clean Architecture layers

### 2. Dependency Confusion

- **Issue**: pyproject.toml declares Django/FastAPI but uses Flask
- **Impact**: Bloated dependencies, architectural confusion
- **Resolution**: Clean up dependencies, choose single web framework

### 3. Template Inconsistency

- **Issue**: Django templates exist but Flask uses inline HTML
- **Impact**: Template system confusion, maintenance overhead
- **Resolution**: Implement consistent Flask template system

### 4. No Persistence Layer

- **Issue**: In-memory storage only, data lost on restart
- **Impact**: Not suitable for production deployment
- **Resolution**: Implement repository pattern with database

## Development Guidelines

### Code Quality Standards

- **Type Safety**: MyPy strict mode adoption; aiming for 95%+ coverage
- **Test Coverage**: 90%+ coverage required for all code
- **Documentation**: Comprehensive docstrings for all public APIs
- **Error Handling**: FlextResult patterns for all operations
- **Validation**: Domain rule validation for all entities

### Testing Approach

- **Unit Tests**: Domain entity and handler validation
- **Integration Tests**: API endpoint testing with Flask test client
- **End-to-End Tests**: Complete workflow validation
- **Performance Tests**: Load testing for production readiness

### Refactoring Priorities (Phase 1)

1. **Extract Domain Layer**: Move entities and value objects
2. **Extract Application Layer**: Move handlers and configuration
3. **Extract Infrastructure Layer**: Move Flask service and persistence
4. **Clean Dependencies**: Remove unused Django/FastAPI dependencies
5. **Implement Persistence**: Add repository pattern with database

## Integration Points

### FLEXT Ecosystem

- **flext-core**: Foundation patterns and utilities
- **flext-observability**: Monitoring and health checks
- **flext-auth**: Authentication and authorization (planned)
- **FlexCore**: Go runtime service integration (planned)
- **FLEXT Service**: Data platform service integration (planned)

### External Services

- **Database**: PostgreSQL for application persistence (planned)
- **Cache**: Redis for session management (planned)
- **Monitoring**: Integration with observability stack
- **Load Balancer**: Support for multiple instance deployment

## Version History

- **0.9.0**: Current development version with monolithic architecture
- **1.0.0**: Target production version with Clean Architecture (planned)

---

**Maintainers**: FLEXT Development Team  
**Architecture Review**: Required after Clean Architecture refactoring  
**Quality Gates**: All changes must pass `make validate` before merge
