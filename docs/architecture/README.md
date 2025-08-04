# Architecture Guide - FLEXT Web Interface

**Architecture Style**: Clean Architecture + Domain-Driven Design (DDD)  
**Integration Pattern**: FLEXT Ecosystem + flext-core standardization  
**Implementation**: Single-file consolidation with layer separation

## 🏗️ Clean Architecture Overview

FLEXT Web follows **Clean Architecture** principles with **Domain-Driven Design** patterns, implementing clear separation of concerns across four distinct layers:

```
┌─────────────────────────────────────────────────────────┐
│                  Web Interface Layer                   │
│  Flask Routes • HTML Dashboard • API Endpoints         │
├─────────────────────────────────────────────────────────┤
│                 Application Layer                      │
│  FlextWebService • Handlers • Configuration            │
├─────────────────────────────────────────────────────────┤
│                   Domain Layer                         │
│  FlextWebApp • Business Rules • Domain Logic           │
├─────────────────────────────────────────────────────────┤
│                Infrastructure Layer                    │
│  flext-core Integration • Flask Framework • Exceptions │
└─────────────────────────────────────────────────────────┘
```

## 📁 Current Implementation Structure

### Current Implementation Architecture (1,200+ lines with enterprise documentation in `__init__.py`)

**Status**: ✅ **Documentation Complete** - 100% enterprise-grade docstrings with comprehensive business context

```python
src/flext_web/
├── __init__.py              # All layers consolidated (518 lines)
│   ├── Domain Models        # FlextWebApp, FlextWebAppStatus
│   ├── Configuration        # FlextWebConfig, environment settings
│   ├── Handlers            # FlextWebAppHandler (CQRS commands)
│   ├── Web Service         # FlextWebService (Flask integration)
│   └── Factory Functions   # Service creation and configuration
├── __main__.py             # CLI entry point (64 lines)
├── exceptions.py           # Exception hierarchy (311 lines)
└── templates/              # Django templates (unused)
    ├── base.html           # Django-style template (not used)
    └── dashboard.html      # Dashboard template (not used)
```

### Architectural Layers Breakdown

#### 1. **Domain Layer** (Lines 42-97 in `__init__.py`)

```python
# Domain Models
class FlextWebAppStatus(Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"

class FlextWebApp(FlextEntity, FlextTimestampMixin, FlextValidatableMixin):
    """Core domain entity with business rules"""
    name: str
    host: str
    port: int
    status: FlextWebAppStatus

    # Business logic methods
    def start(self) -> FlextResult[FlextWebApp]: ...
    def stop(self) -> FlextResult[FlextWebApp]: ...
    def validate_domain_rules(self) -> FlextResult[None]: ...
```

**Responsibilities**:

- Business entities and value objects
- Domain rules and validation logic
- Core business operations (start/stop lifecycle)
- State transitions and business invariants

#### 2. **Application Layer** (Lines 98-188 in `__init__.py`)

```python
# Configuration Management
class FlextWebConfig(BaseSettings, FlextConfig):
    """Application configuration with validation"""
    app_name: str = "FLEXT Web"
    host: str = "localhost"
    port: int = 8080
    debug: bool = True
    secret_key: str = Field(min_length=32)

# Command Handlers (CQRS Pattern)
class FlextWebAppHandler(FlextHandlers.Handler[FlextWebApp, FlextWebApp]):
    """CQRS command handlers for application operations"""
    def create(self, name: str, port: int, host: str) -> FlextResult[FlextWebApp]: ...
    def start(self, app: FlextWebApp) -> FlextResult[FlextWebApp]: ...
    def stop(self, app: FlextWebApp) -> FlextResult[FlextWebApp]: ...
```

**Responsibilities**:

- Application services and use cases
- Configuration management and validation
- CQRS command handling
- Orchestration of domain operations

#### 3. **Infrastructure Layer** (Lines 195-485 in `__init__.py`)

```python
# Web Service Implementation
class FlextWebService:
    """Flask integration with REST API endpoints"""
    def __init__(self, config: FlextWebConfig | None = None):
        self.app = Flask(__name__)
        self.handler = FlextWebAppHandler()
        self.apps: dict[str, FlextWebApp] = {}  # In-memory storage

    # Route registration
    def _register_routes(self) -> None: ...

    # API endpoint handlers
    def health_check(self) -> ResponseReturnValue: ...
    def list_apps(self) -> ResponseReturnValue: ...
    def create_app(self) -> ResponseReturnValue: ...
```

**Responsibilities**:

- Flask framework integration
- HTTP request/response handling
- Route registration and API endpoint implementation
- External system integration points

#### 4. **Web Interface Layer** (Inline HTML in `dashboard()` method)

```python
def dashboard(self) -> str:
    """Serve inline HTML dashboard"""
    return f"""<!DOCTYPE html>
    <html>
    <head><title>{self.config.app_name}</title></head>
    <body>
        <div class="container">
            <h1>{self.config.app_name}</h1>
            <div class="stats">
                <div>Total Apps: {apps_count}</div>
                <div>Running: {running_count}</div>
            </div>
        </div>
    </body>
    </html>"""
```

**Responsibilities**:

- User interface presentation
- HTML rendering and styling
- Client-side interaction handling

## 🔧 FLEXT Ecosystem Integration

### flext-core Pattern Usage

```python
# FlextResult Pattern (Railway-Oriented Programming)
def create_app(self) -> ResponseReturnValue:
    app_result = self.handler.create(name, port, host)
    if app_result.success:
        return self._create_response(True, "Success", app_data)
    return self._create_response(False, f"Failed: {app_result.error}")

# FlextEntity Pattern
class FlextWebApp(FlextEntity, FlextTimestampMixin, FlextValidatableMixin):
    """Domain entity with standardized patterns"""

# FlextConfig Pattern
class FlextWebConfig(BaseSettings, FlextConfig):
    """Configuration with validation"""
    def validate_config(self) -> FlextResult[None]: ...
```

### Integration Points

1. **flext-core Foundation**:

   - `FlextResult` for error handling
   - `FlextEntity` for domain modeling
   - `FlextConfig` for configuration management
   - `FlextHandlers` for CQRS pattern implementation

2. **flext-observability** (planned):

   - Health check integration
   - Metrics collection
   - Distributed tracing support

3. **flext-auth** (planned):
   - Authentication middleware
   - Authorization for API endpoints
   - Session management

## 🚨 Architectural Issues & Technical Debt

### Critical Issues

1. **Monolithic Structure**:

   - 518 lines in single file violates SRP
   - Tight coupling between layers
   - Difficult to test and maintain

2. **Mixed Technology Stack**:

   - pyproject.toml declares Django/FastAPI but uses Flask
   - Django templates exist but not used
   - Dependency confusion and bloat

3. **No Persistence Layer**:
   - In-memory storage only (`dict[str, FlextWebApp]`)
   - Data lost on service restart
   - Not suitable for production

### Recommended Refactoring

```
# Target Structure
src/flext_web/
├── domain/
│   ├── entities.py         # FlextWebApp, FlextWebAppStatus
│   ├── repositories.py     # Repository interfaces
│   └── services.py         # Domain services
├── application/
│   ├── handlers.py         # CQRS handlers
│   ├── config.py          # Configuration management
│   └── use_cases.py       # Application use cases
├── infrastructure/
│   ├── web/
│   │   ├── routes.py      # Flask route definitions
│   │   ├── middleware.py  # Authentication, CORS, etc.
│   │   └── templates/     # Jinja2 templates
│   ├── persistence/
│   │   ├── repositories.py # Repository implementations
│   │   └── models.py      # Data models
│   └── external/
│       ├── flexcore.py    # FlexCore integration
│       └── observability.py # Monitoring integration
└── interfaces/
    ├── api/
    │   ├── v1/            # API version 1
    │   └── schemas.py     # API schemas
    └── web/
        ├── static/        # CSS, JS, images
        └── templates/     # HTML templates
```

## 🔄 CQRS Pattern Implementation

### Current Command Handlers

```python
class FlextWebAppHandler(FlextHandlers.Handler[FlextWebApp, FlextWebApp]):
    """CQRS command handlers"""

    # Commands
    def create(self, name: str, port: int, host: str) -> FlextResult[FlextWebApp]:
        """Create command with validation"""

    def start(self, app: FlextWebApp) -> FlextResult[FlextWebApp]:
        """Start command with business rules"""

    def stop(self, app: FlextWebApp) -> FlextResult[FlextWebApp]:
        """Stop command with state validation"""
```

### Query Handlers (Implicit)

Currently queries are handled directly in `FlextWebService`, but should be separated:

```python
# Planned Query Handlers
class FlextWebAppQueries:
    def get_app(self, app_id: str) -> FlextResult[FlextWebApp]: ...
    def list_apps(self) -> FlextResult[list[FlextWebApp]]: ...
    def get_app_status(self, app_id: str) -> FlextResult[FlextWebAppStatus]: ...
```

## 📊 Performance Characteristics

### Current Performance Profile

- **Memory Usage**: Low (in-memory dict storage)
- **Response Time**: Fast (no database I/O)
- **Scalability**: Limited (single instance, no persistence)
- **Reliability**: Poor (data loss on restart)

### Production Requirements

- **Persistence**: PostgreSQL or Redis for state storage
- **Caching**: Redis for session and application state
- **Load Balancing**: Multiple instances with shared state
- **Monitoring**: Integration with flext-observability

## 🔗 Service Communication Patterns

### Internal Communication

```python
# Current: Direct method calls
app_result = self.handler.create(name, port, host)

# Future: Event-driven communication
event = AppCreationRequested(name=name, port=port, host=host)
await self.event_bus.publish(event)
```

### External Communication (Planned)

```python
# FlexCore Integration
async def register_with_flexcore(self, app: FlextWebApp):
    flexcore_client = FlexCoreClient(self.config.flexcore_url)
    await flexcore_client.register_application(app)

# FLEXT Service Integration
async def deploy_to_flext_service(self, app: FlextWebApp):
    flext_client = FlextServiceClient(self.config.flext_service_url)
    await flext_client.deploy_application(app)
```

## 🧪 Testing Architecture

### Current Test Structure

```
tests/
├── test_config_comprehensive.py    # Configuration validation
├── test_domain_entities.py         # Domain model testing
├── test_main_entry.py              # CLI testing
├── test_simple_api_fixed.py        # API endpoint testing
└── test_simple_web_fixed.py        # Web interface testing
```

### Test Strategies by Layer

- **Domain Layer**: Unit tests for business logic and rules
- **Application Layer**: Integration tests for handlers and use cases
- **Infrastructure Layer**: Mock external dependencies, test adapters
- **Web Interface**: End-to-end tests with test client

## 📋 Next Steps

### Phase 1: Architecture Stabilization

1. **Dependency Cleanup**: Remove unused Django/FastAPI dependencies
2. **Layer Separation**: Extract domain, application, and infrastructure layers
3. **Persistence Layer**: Implement repository pattern with database

### Phase 2: Integration Enhancement

1. **flext-auth Integration**: Add authentication and authorization
2. **FlexCore Communication**: Implement service discovery and registration
3. **Event-Driven Architecture**: Replace direct calls with event bus

### Phase 3: Production Readiness

1. **Performance Optimization**: Caching, connection pooling, async operations
2. **Monitoring Integration**: Full observability with flext-observability
3. **Multi-tenancy**: Support for multiple organizations and environments

---

**Architecture Review**: Quarterly  
**Next Review**: After dependency stabilization  
**Maintainer**: FLEXT Architecture Team
