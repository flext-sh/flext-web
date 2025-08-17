# Python Module Organization & Semantic Patterns - FLEXT Web Interface

**FLEXT Web Module Architecture & Standards for Enterprise Web Management Console**

---

## 🏗️ **Module Architecture Overview**

FLEXT Web Interface implements a **Clean Architecture module structure** integrated with **FLEXT Core patterns** for the enterprise web management console. This structure follows FLEXT ecosystem standards while providing specialized web interface capabilities for the 33-project distributed data integration platform.

### **Core Design Principles**

1. **FLEXT Core Integration**: Built on flext-core foundation patterns (FlextResult, FlextEntity, FlextConfig)
2. **Clean Architecture Layers**: Domain → Application → Infrastructure → Web Interface
3. **Single Responsibility**: Each module has one primary architectural concern
4. **Type-Safe Web Operations**: Complete type hints with strict MyPy compliance for web APIs
5. **Railway-Oriented Web APIs**: FlextResult[T] threading through all HTTP operations
6. **Ecosystem Consistency**: Web patterns work identically across FLEXT ecosystem

---

## 📁 **Current Module Structure & Critical Issues**

### **Current Implementation (Problematic Single-File Architecture)**

```python
# ⚠️ CURRENT STATE: Monolithic structure requiring refactoring
src/flext_web/
├── __init__.py              # 🚨 CRITICAL: 518 lines, all layers mixed
│   ├── Domain Models        # FlextWebApp, FlextWebAppStatus (lines 42-97)
│   ├── Configuration        # FlextWebConfig, validation (lines 98-151)
│   ├── Handlers            # FlextWebAppHandler, CQRS (lines 155-188)
│   ├── Web Service         # FlextWebService, Flask routes (lines 195-485)
│   └── Factory Functions   # Service creation (lines 449-485)
├── __main__.py             # ✅ CLI entry point (64 lines)
├── exceptions.py           # ✅ Exception hierarchy (311 lines)
├── py.typed               # ✅ Type checking marker
└── templates/             # ⚠️ UNUSED: Django templates (Flask uses inline HTML)
    ├── base.html          # Django syntax - not compatible with Flask
    └── dashboard.html     # Unused template
```

**Critical Issues**:

- **Monolithic**: 518 lines violate Single Responsibility Principle
- **Layer Mixing**: Domain, Application, Infrastructure all in one file
- **Template Confusion**: Django templates exist but Flask uses inline HTML
- **Dependency Bloat**: pyproject.toml includes unused Django/FastAPI/Celery

---

## 🎯 **Target Module Structure (Clean Architecture Implementation)**

### **Foundation Layer**

```python
# Web interface foundation
src/flext_web/
├── __init__.py              # 🎯 Public API gateway (FLEXT patterns)
├── version.py               # 🎯 Version management
├── constants.py             # 🎯 Web-specific constants
└── types.py                 # 🎯 Web interface type definitions
```

**Responsibility**: Establish web interface foundation using flext-core patterns.

**Import Pattern**:

```python
# FLEXT Web main imports
from flext_web import create_service, get_web_settings, FlextWebApp
from flext_web import FlextWebConfig, FlextWebService, FlextWebAppHandler
```

### **Domain Layer (Business Logic)**

```python
# Domain-driven design for web application management
src/flext_web/domain/
├── __init__.py              # Domain layer exports
├── entities.py              # 🏛️ FlextWebApp - Rich domain entity
├── value_objects.py         # 🏛️ WebAppStatus, HostPort - Value objects
├── services.py              # 🏛️ FlextWebDomainService - Domain services
├── events.py                # 🏛️ FlextWebEvent - Domain events
└── repositories.py          # 🏛️ Repository interfaces (protocols)
```

**Domain Entity Pattern**:

```python
from flext_core import FlextEntity, FlextResult
from flext_web.domain.value_objects import WebAppStatus, HostPort

class FlextWebApp(FlextEntity):
    """Rich domain entity for web application management"""
    name: str
    host_port: HostPort
    status: WebAppStatus = WebAppStatus.STOPPED

    def start(self) -> FlextResult['FlextWebApp']:
        """Business logic for starting application"""
        if self.status == WebAppStatus.RUNNING:
            return FlextResult.fail("Application already running")

        # Business validation and state transition
        new_status = WebAppStatus.RUNNING
        self.add_domain_event(AppStartedEvent(self.id, self.name))

        return FlextResult.ok(
            self.model_copy(update={"status": new_status})
        )

    def stop(self) -> FlextResult['FlextWebApp']:
        """Business logic for stopping application"""
        if self.status == WebAppStatus.STOPPED:
            return FlextResult.fail("Application already stopped")

        # Business rules and domain events
        new_status = WebAppStatus.STOPPED
        self.add_domain_event(AppStoppedEvent(self.id, self.name))

        return FlextResult.ok(
            self.model_copy(update={"status": new_status})
        )
```

**Value Object Pattern**:

```python
from flext_core import FlextValueObject

class HostPort(FlextValueObject):
    """Network address value object with validation"""
    host: str
    port: int

    def __post_init__(self):
        if not (1 <= self.port <= 65535):
            raise ValueError("Port must be between 1 and 65535")
        if not self.host.strip():
            raise ValueError("Host cannot be empty")

    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}"

class WebAppStatus(FlextValueObject):
    """Application status with business rules"""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"

    def can_start(self) -> bool:
        return self in [self.STOPPED, self.ERROR]

    def can_stop(self) -> bool:
        return self in [self.RUNNING, self.ERROR]
```

### **Application Layer (Use Cases & Handlers)**

```python
# CQRS commands and application services
src/flext_web/application/
├── __init__.py              # Application layer exports
├── commands.py              # 📤 FlextWebCommand - Command definitions
├── handlers.py              # 📤 FlextWebAppHandler - CQRS handlers
├── queries.py               # 📤 FlextWebQuery - Query definitions
├── use_cases.py             # 📤 Application use cases
├── config.py                # ⚙️ FlextWebConfig - Configuration management
└── services.py              # ⚙️ Application services
```

**CQRS Handler Pattern**:

```python
from flext_core import FlextHandlers, FlextResult, FlextCommand
from flext_web.domain.entities import FlextWebApp
from flext_web.domain.repositories import FlextWebAppRepository

class CreateAppCommand(FlextCommand):
    """Command to create new web application"""
    name: str
    host: str = "localhost"
    port: int = 8000

class FlextWebAppHandler(FlextHandlers.Handler[CreateAppCommand, FlextWebApp]):
    """CQRS command handler for web application operations"""

    def __init__(self, repository: FlextWebAppRepository):
        self.repository = repository

    def create_app(self, command: CreateAppCommand) -> FlextResult[FlextWebApp]:
        """Handle create application command"""
        # Domain entity creation with validation
        host_port = HostPort(host=command.host, port=command.port)
        app = FlextWebApp(
            id=f"app_{command.name}",
            name=command.name,
            host_port=host_port
        )

        # Domain validation
        validation = app.validate_domain_rules()
        if not validation.success:
            return validation

        # Persistence through repository
        return self.repository.save(app)

    def start_app(self, app_id: str) -> FlextResult[FlextWebApp]:
        """Handle start application command"""
        return (
            self.repository.find_by_id(app_id)
            .flat_map(lambda app: app.start())
            .flat_map(lambda updated_app: self.repository.save(updated_app))
        )
```

**Configuration Pattern**:

```python
from flext_core import FlextConfig, FlextResult
from pydantic_settings import BaseSettings

class FlextWebConfig(BaseSettings, FlextConfig):
    """Web interface configuration with FLEXT core integration"""

    model_config = {
        "env_prefix": "FLEXT_WEB_",
        "case_sensitive": False,
        "validate_assignment": True,
    }

    # Server settings
    app_name: str = Field(default="FLEXT Web", description="Application name")
    host: str = Field(default="localhost", description="Server host")
    port: int = Field(default=8080, ge=1, le=65535, description="Server port")
    debug: bool = Field(default=True, description="Debug mode")

    # Security settings
    secret_key: str = Field(
        min_length=32,
        description="Cryptographic secret key"
    )

    # FLEXT ecosystem integration
    flexcore_url: str = Field(
        default="http://localhost:8080",
        description="FlexCore service URL"
    )
    flext_service_url: str = Field(
        default="http://localhost:8081",
        description="FLEXT Service URL"
    )

    def validate_config(self) -> FlextResult[None]:
        """Validate configuration with business rules"""
        if not self.debug and "change-in-production" in self.secret_key:
            return FlextResult.fail("Secret key must be changed in production")

        return FlextResult.ok(None)
```

### **Infrastructure Layer (External Concerns)**

```python
# Infrastructure adapters and external integrations
src/flext_web/infrastructure/
├── __init__.py              # Infrastructure exports
├── persistence/
│   ├── __init__.py
│   ├── repositories.py      # 🔧 Repository implementations
│   ├── models.py            # 🔧 Database models
│   └── migrations.py        # 🔧 Database migrations
├── external/
│   ├── __init__.py
│   ├── flexcore.py          # 🔧 FlexCore service integration
│   ├── flext_service.py     # 🔧 FLEXT Service integration
│   └── observability.py     # 🔧 Monitoring integration
├── web/
│   ├── __init__.py
│   ├── middleware.py        # 🔧 Authentication, CORS, etc.
│   ├── serializers.py       # 🔧 Request/response serialization
│   └── templates.py         # 🔧 Template management
└── messaging/
    ├── __init__.py
    ├── events.py            # 🔧 Domain event handling
    └── publishers.py        # 🔧 Event publishing
```

**Repository Implementation Pattern**:

```python
from typing import Dict, Optional
from flext_core import FlextResult
from flext_web.domain.entities import FlextWebApp
from flext_web.domain.repositories import FlextWebAppRepository

class InMemoryFlextWebAppRepository(FlextWebAppRepository):
    """In-memory repository implementation for development"""

    def __init__(self):
        self._apps: Dict[str, FlextWebApp] = {}

    def save(self, app: FlextWebApp) -> FlextResult[FlextWebApp]:
        """Save application to storage"""
        try:
            self._apps[app.id] = app
            return FlextResult.ok(app)
        except Exception as e:
            return FlextResult.fail(f"Failed to save app: {e}")

    def find_by_id(self, app_id: str) -> FlextResult[FlextWebApp]:
        """Find application by ID"""
        app = self._apps.get(app_id)
        if app is None:
            return FlextResult.fail(f"Application {app_id} not found")
        return FlextResult.ok(app)

    def find_all(self) -> FlextResult[list[FlextWebApp]]:
        """Find all applications"""
        return FlextResult.ok(list(self._apps.values()))

class PostgreSQLFlextWebAppRepository(FlextWebAppRepository):
    """PostgreSQL repository implementation for production"""

    def __init__(self, connection_pool):
        self.pool = connection_pool

    def save(self, app: FlextWebApp) -> FlextResult[FlextWebApp]:
        """Save application to PostgreSQL"""
        try:
            # Implementation with connection pool and transactions
            return FlextResult.ok(app)
        except Exception as e:
            return FlextResult.fail(f"Database error: {e}")
```

### **Web Interface Layer (HTTP/REST)**

```python
# Web interface and REST API implementation
src/flext_web/interfaces/
├── __init__.py              # Interface exports
├── api/
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── apps.py          # 🌐 Application management endpoints
│   │   ├── health.py        # 🌐 Health check endpoints
│   │   └── schemas.py       # 🌐 API request/response schemas
│   ├── middleware.py        # 🌐 API middleware
│   └── exceptions.py        # 🌐 HTTP exception handling
├── web/
│   ├── __init__.py
│   ├── routes.py            # 🌐 Web dashboard routes
│   ├── templates/           # 🌐 Jinja2 templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   └── apps/
│   │       ├── list.html
│   │       └── detail.html
│   └── static/              # 🌐 CSS, JavaScript, images
│       ├── css/
│       ├── js/
│       └── img/
└── cli/
    ├── __init__.py
    ├── commands.py          # 🌐 CLI command definitions
    └── main.py              # 🌐 CLI entry point
```

**REST API Implementation Pattern**:

```python
from flask import Blueprint, request, jsonify
from flext_core import FlextResult
from flext_web.application.handlers import FlextWebAppHandler
from flext_web.application.commands import CreateAppCommand

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

class AppsAPI:
    """REST API for application management"""

    def __init__(self, app_handler: FlextWebAppHandler):
        self.app_handler = app_handler

    def create_app(self):
        """POST /api/v1/apps - Create new application"""
        data = request.get_json()

        # Input validation and command creation
        command_result = self._create_command(data)
        if command_result.is_failure:
            return self._error_response(command_result.error, 400)

        # Execute command through handler
        app_result = self.app_handler.create_app(command_result.data)

        if app_result.success:
            return self._success_response(
                "Application created successfully",
                app_result.data.dict()
            )

        return self._error_response(app_result.error, 400)

    def _create_command(self, data: dict) -> FlextResult[CreateAppCommand]:
        """Create and validate command from request data"""
        try:
            if not data or not data.get("name"):
                return FlextResult.fail("Application name is required")

            command = CreateAppCommand(
                name=data["name"],
                host=data.get("host", "localhost"),
                port=data.get("port", 8000)
            )
            return FlextResult.ok(command)
        except Exception as e:
            return FlextResult.fail(f"Invalid request data: {e}")

    def _success_response(self, message: str, data: dict = None):
        """Create standardized success response"""
        return jsonify({
            "success": True,
            "message": message,
            "data": data
        })

    def _error_response(self, error: str, status_code: int = 400):
        """Create standardized error response"""
        return jsonify({
            "success": False,
            "message": error,
            "data": None
        }), status_code

# Route registration
@api_v1.route('/apps', methods=['POST'])
def create_app():
    return apps_api.create_app()
```

---

## 🎯 **Semantic Naming Conventions**

### **Public API Naming (FlextWebXxx)**

All public exports use the `FlextWeb` prefix for clear web interface identification:

```python
# Core web patterns
FlextWebApp                 # Domain entity for web application
FlextWebAppHandler          # CQRS handler for app operations
FlextWebAppStatus          # Value object for app status
FlextWebConfig             # Configuration management
FlextWebService            # Main web service implementation

# Web-specific patterns
FlextWebRoute              # Route definition pattern
FlextWebMiddleware         # Middleware pattern
FlextWebTemplate           # Template management pattern
FlextWebAPI                # REST API pattern
FlextWebDashboard          # Dashboard pattern

# Exception patterns
FlextWebError              # Base web error
FlextWebValidationError    # Web validation error
FlextWebAuthenticationError # Web authentication error
FlextWebRoutingError       # Web routing error
```

**Rationale**: Clear namespace separation for web interface concerns within FLEXT ecosystem.

### **Module-Level Naming**

```python
# Domain layer modules
entities.py                # Contains FlextWebApp and related entities
value_objects.py           # Contains WebAppStatus, HostPort value objects
repositories.py            # Contains repository interfaces
services.py                # Contains domain services

# Application layer modules
commands.py                # Contains command definitions
handlers.py                # Contains CQRS command handlers
queries.py                 # Contains query definitions
config.py                  # Contains configuration management

# Infrastructure layer modules
persistence/repositories.py # Repository implementations
web/middleware.py          # Web middleware implementations
external/flexcore.py       # FlexCore integration

# Interface layer modules
api/v1/apps.py            # Application management API
web/routes.py             # Web dashboard routes
cli/commands.py           # CLI command definitions
```

**Pattern**: One primary architectural concern per module with related utilities.

### **Internal Naming (\_xxx)**

```python
# Internal implementation modules
_web_base.py              # Internal web service base
_repository_base.py       # Internal repository base
_handler_base.py          # Internal handler base

# Internal functions and classes
def _validate_app_data(data: dict) -> bool:
    """Internal validation function"""

class _InternalWebService:
    """Internal web service implementation"""
```

**Rule**: Anything with `_` prefix is internal and not part of public API.

---

## 📦 **Import Patterns & Best Practices**

### **Recommended Import Styles**

#### **1. Primary Pattern (Recommended for FLEXT Ecosystem)**

```python
# Import from main package - gets web interface essentials
from flext_web import (
    FlextWebApp, FlextWebAppHandler, FlextWebConfig,
    create_service, get_web_settings
)

# Use patterns directly with type safety
def process_app_request(data: dict) -> FlextResult[FlextWebApp]:
    return FlextResult.ok(FlextWebApp(**data))
```

#### **2. Layer-Specific Pattern (For Advanced Usage)**

```python
# Import from specific layers for clarity
from flext_web.domain.entities import FlextWebApp
from flext_web.application.handlers import FlextWebAppHandler
from flext_web.infrastructure.persistence.repositories import InMemoryFlextWebAppRepository

# More explicit architectural boundaries
```

#### **3. Web API Pattern**

```python
# Import patterns for REST API development
from flext_web.interfaces.api.v1.schemas import CreateAppRequest, AppResponse
from flext_web.interfaces.api.middleware import authenticate, validate_json
from flext_web.application.commands import CreateAppCommand
```

#### **4. Type Annotation Pattern**

```python
# Import types for annotations
from typing import TYPE_CHECKING

from flext_web import FlextWebApp, FlextWebService
from flext_core import FlextResult

# Use in function signatures
def process_web_request(service: 'FlextWebService') -> 'FlextResult[FlextWebApp]':
    pass
```

### **Anti-Patterns (Forbidden)**

```python
# ❌ Don't import everything
from flext_web import *

# ❌ Don't import internal modules
from flext_web._web_base import _InternalWebService

# ❌ Don't use deep imports unnecessarily
from flext_web.infrastructure.persistence.repositories import InMemoryFlextWebAppRepository, _private_function

# ❌ Don't alias core web types
from flext_web import FlextWebApp as WebApp  # Confusing across ecosystem

# ❌ Don't import from current monolithic structure
from flext_web import FlextWebService  # Will break during refactoring
```

---

## 🏛️ **Architectural Patterns**

### **Clean Architecture Layer Separation**

```python
# Clear architectural boundaries with dependency direction
┌─────────────────────────────────────────────────────────┐
│              Web Interface Layer                        │  # Flask routes, REST API, HTML templates
│  (HTTP Endpoints, Templates, Static Assets)             │  # interfaces/api/, interfaces/web/
├─────────────────────────────────────────────────────────┤
│             Application Layer                           │  # CQRS handlers, use cases, config
│  (Commands, Handlers, Use Cases, Configuration)         │  # application/handlers.py, application/config.py
├─────────────────────────────────────────────────────────┤
│               Domain Layer                              │  # Business entities, value objects
│    (Business Logic, Domain Rules, Entities)             │  # domain/entities.py, domain/value_objects.py
├─────────────────────────────────────────────────────────┤
│            Infrastructure Layer                         │  # Database, external services, messaging
│  (Persistence, External APIs, Messaging)                │  # infrastructure/persistence/, infrastructure/external/
├─────────────────────────────────────────────────────────┤
│              Foundation Layer                           │  # FLEXT Core integration
│     (FlextResult, FlextEntity, FlextConfig)             │  # from flext_core import ...
└─────────────────────────────────────────────────────────┘
```

### **Dependency Direction (Clean Architecture)**

```python
# Dependencies flow inward (Clean Architecture principle)
Web Interface  →  Application  →  Domain  →  Foundation (flext-core)
     ↓                ↓           ↓           ↓
Infrastructure  →  Foundation   (OK - cross-cutting concerns)
```

**Rule**: Higher layers can depend on lower layers, never the reverse.

### **Web-Specific Cross-Cutting Concerns**

```python
# Handled via middleware and decorators
from flext_web.infrastructure.web.middleware import with_authentication, with_cors
from flext_web.interfaces.api.middleware import with_json_validation, with_rate_limiting

class AppsAPI:
    @with_authentication
    @with_json_validation(CreateAppRequest)
    @with_rate_limiting(requests_per_minute=60)
    def create_app(self, request: CreateAppRequest) -> FlextResult[AppResponse]:
        return self.handler.create_app(request.to_command())
```

---

## 🔄 **Railway-Oriented Programming for Web APIs**

### **FlextResult Chain Patterns for HTTP Operations**

```python
# Web request processing pipeline
def process_create_app_request(request_data: dict) -> FlextResult[dict]:
    """Process web request through validation and business logic"""
    return (
        validate_request_data(request_data)  # Input validation
        .flat_map(create_command)           # Command creation
        .flat_map(execute_command)          # Business logic execution
        .map(serialize_response)            # Response serialization
    )

# Error aggregation for API validation
def validate_create_app_request(data: dict) -> FlextResult[dict]:
    """Validate web request with comprehensive error collection"""
    errors = []

    if not data.get('name'):
        errors.append("Application name is required")

    if 'port' in data and not (1 <= data['port'] <= 65535):
        errors.append("Port must be between 1 and 65535")

    if 'host' in data and not data['host'].strip():
        errors.append("Host cannot be empty")

    return FlextResult.fail(errors) if errors else FlextResult.ok(data)

# Async web operation with resource management
async def process_with_database_transaction(command: CreateAppCommand) -> FlextResult[FlextWebApp]:
    """Process command with database transaction"""
    async with database_transaction() as tx:
        return (
            await validate_app_uniqueness(tx, command.name)
            .flat_map_async(lambda _: create_app_entity(command))
            .flat_map_async(lambda app: save_app_to_database(tx, app))
            .map_async(lambda app: publish_app_created_event(app))
        )
```

### **HTTP Response Integration Patterns**

```python
from flask import jsonify
from flext_core import FlextResult

class APIResponseHandler:
    """Handle FlextResult to HTTP response conversion"""

    @staticmethod
    def to_json_response(result: FlextResult[Any], success_status: int = 200) -> tuple:
        """Convert FlextResult to Flask JSON response"""
        if result.success:
            return jsonify({
                "success": True,
                "message": "Operation completed successfully",
                "data": result.data
            }), success_status

        # Error response with appropriate HTTP status
        status_code = APIResponseHandler._get_error_status(result.error)
        return jsonify({
            "success": False,
            "message": result.error,
            "data": None
        }), status_code

    @staticmethod
    def _get_error_status(error_message: str) -> int:
        """Map error types to HTTP status codes"""
        if "not found" in error_message.lower():
            return 404
        elif "already exists" in error_message.lower():
            return 409
        elif "validation" in error_message.lower():
            return 400
        elif "unauthorized" in error_message.lower():
            return 401
        elif "forbidden" in error_message.lower():
            return 403
        else:
            return 400  # Default to bad request

# Usage in API endpoints
@api_v1.route('/apps', methods=['POST'])
def create_app():
    request_data = request.get_json()

    result = process_create_app_request(request_data)
    return APIResponseHandler.to_json_response(result, success_status=201)
```

---

## 🎯 **Domain-Driven Design Patterns for Web Applications**

### **Web Application Entity Pattern**

```python
from flext_core import FlextEntity, FlextResult
from flext_web.domain.value_objects import WebAppStatus, HostPort
from flext_web.domain.events import AppStartedEvent, AppStoppedEvent

class FlextWebApp(FlextEntity):
    """Rich domain entity for web application lifecycle management"""
    name: str
    host_port: HostPort
    status: WebAppStatus = WebAppStatus.STOPPED
    created_by: str = "system"
    environment: str = "development"
    _domain_events: list[dict] = field(default_factory=list, init=False)

    def start(self) -> FlextResult[None]:
        """Start application with business rules validation"""
        # Business rule: Can only start stopped or error state applications
        if not self.status.can_start():
            return FlextResult.fail(
                f"Cannot start application in {self.status} state"
            )

        # Business rule: Check port availability (would integrate with infrastructure)
        if self.environment == "production" and self.host_port.port < 1024:
            return FlextResult.fail(
                "Production applications cannot use privileged ports"
            )

        # State transition with domain event
        self.status = WebAppStatus.RUNNING
        self.add_domain_event(AppStartedEvent(
            app_id=self.id,
            app_name=self.name,
            host_port=self.host_port.address,
            started_by=self.created_by
        ))

        return FlextResult.ok(None)

    def stop(self, stopped_by: str = "system") -> FlextResult[None]:
        """Stop application with audit trail"""
        if not self.status.can_stop():
            return FlextResult.fail(
                f"Cannot stop application in {self.status} state"
            )

        # State transition with domain event
        self.status = WebAppStatus.STOPPED
        self.add_domain_event(AppStoppedEvent(
            app_id=self.id,
            app_name=self.name,
            stopped_by=stopped_by,
            reason="Manual stop"
        ))

        return FlextResult.ok(None)

    def update_configuration(self, new_host_port: HostPort) -> FlextResult[None]:
        """Update application configuration with validation"""
        if self.status == WebAppStatus.RUNNING:
            return FlextResult.fail(
                "Cannot update configuration of running application"
            )

        # Business rule: Port cannot conflict with existing apps
        # (This would be validated through domain service)

        old_host_port = self.host_port
        self.host_port = new_host_port

        self.add_domain_event(ConfigurationUpdatedEvent(
            app_id=self.id,
            old_config=old_host_port.address,
            new_config=new_host_port.address
        ))

        return FlextResult.ok(None)
```

### **Value Object Patterns for Web Concerns**

```python
from flext_core import FlextValueObject
from enum import Enum

class WebAppStatus(FlextValueObject):
    """Application status with state transition rules"""

    class Status(str, Enum):
        STOPPED = "stopped"
        STARTING = "starting"
        RUNNING = "running"
        STOPPING = "stopping"
        ERROR = "error"

    value: Status

    def can_start(self) -> bool:
        """Business rule: When application can be started"""
        return self.value in [self.Status.STOPPED, self.Status.ERROR]

    def can_stop(self) -> bool:
        """Business rule: When application can be stopped"""
        return self.value in [self.Status.RUNNING, self.Status.ERROR]

    def is_transitioning(self) -> bool:
        """Check if application is in transitional state"""
        return self.value in [self.Status.STARTING, self.Status.STOPPING]

class HostPort(FlextValueObject):
    """Network endpoint with validation and formatting"""
    host: str
    port: int

    def __post_init__(self):
        if not (1 <= self.port <= 65535):
            raise ValueError("Port must be between 1 and 65535")

        if not self.host.strip():
            raise ValueError("Host cannot be empty")

        # Additional validation for special hosts
        if self.host == "0.0.0.0" and self.port < 1024:
            raise ValueError("Privileged ports not allowed for wildcard binding")

    @property
    def address(self) -> str:
        """Full network address"""
        return f"{self.host}:{self.port}"

    @property
    def url(self) -> str:
        """HTTP URL representation"""
        return f"http://{self.host}:{self.port}"

    def is_localhost(self) -> bool:
        """Check if this is a localhost address"""
        return self.host in ["localhost", "127.0.0.1", "::1"]

    def is_wildcard(self) -> bool:
        """Check if this binds to all interfaces"""
        return self.host in ["0.0.0.0", "::"]

class Environment(FlextValueObject):
    """Environment specification with rules"""

    class Type(str, Enum):
        DEVELOPMENT = "development"
        TESTING = "testing"
        STAGING = "staging"
        PRODUCTION = "production"

    value: Type

    def allows_debug(self) -> bool:
        """Business rule: When debug mode is allowed"""
        return self.value in [self.Type.DEVELOPMENT, self.Type.TESTING]

    def requires_ssl(self) -> bool:
        """Business rule: When SSL is required"""
        return self.value in [self.Type.STAGING, self.Type.PRODUCTION]

    def allows_privileged_ports(self) -> bool:
        """Business rule: When privileged ports are allowed"""
        return self.value != self.Type.PRODUCTION
```

### **Domain Service Pattern for Web Operations**

```python
from flext_core import FlextDomainService, FlextResult
from flext_web.domain.repositories import FlextWebAppRepository

class WebAppPortConflictService(FlextDomainService):
    """Domain service for port conflict resolution"""

    def __init__(self, app_repository: FlextWebAppRepository):
        self.app_repository = app_repository

    def check_port_availability(self, host_port: HostPort, exclude_app_id: str = None) -> FlextResult[None]:
        """Check if port is available for use"""
        # Get all running applications
        apps_result = self.app_repository.find_by_status(WebAppStatus.Status.RUNNING)
        if apps_result.is_failure:
            return apps_result

        running_apps = apps_result.data

        # Check for conflicts
        for app in running_apps:
            if exclude_app_id and app.id == exclude_app_id:
                continue

            if app.host_port.port == host_port.port:
                # Same port - check host compatibility
                if (app.host_port.host == host_port.host or
                    app.host_port.is_wildcard() or
                    host_port.is_wildcard()):
                    return FlextResult.fail(
                        f"Port {host_port.port} already in use by application {app.name}"
                    )

        return FlextResult.ok(None)

    def suggest_available_port(self, preferred_port: int) -> FlextResult[int]:
        """Suggest next available port starting from preferred"""
        for port in range(preferred_port, 65536):
            host_port = HostPort(host="localhost", port=port)
            availability = self.check_port_availability(host_port)

            if availability.success:
                return FlextResult.ok(port)

        return FlextResult.fail("No available ports found")
```

---

## 🔧 **Configuration Patterns for Web Interface**

### **Hierarchical Web Configuration**

```python
from flext_core import FlextSettings
from pydantic import Field, validator

class ServerSettings(FlextSettings):
    """Web server configuration"""
    host: str = "localhost"
    port: int = 8080
    debug: bool = True
    worker_processes: int = 1
    max_connections: int = 1000

    class Config:
        env_prefix = "FLEXT_WEB_SERVER_"

    @validator('port')
    def validate_port(cls, v):
        if not (1 <= v <= 65535):
            raise ValueError('Port must be between 1 and 65535')
        return v

class SecuritySettings(FlextSettings):
    """Web security configuration"""
    secret_key: str = Field(min_length=32, repr=False)
    jwt_expiry: int = 3600
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])
    csrf_protection: bool = True

    class Config:
        env_prefix = "FLEXT_WEB_SECURITY_"

    @validator('secret_key')
    def validate_secret_key(cls, v):
        if 'change-in-production' in v:
            raise ValueError('Secret key must be changed from default')
        return v

class IntegrationSettings(FlextSettings):
    """FLEXT ecosystem integration configuration"""
    flexcore_url: str = "http://localhost:8080"
    flext_service_url: str = "http://localhost:8081"
    auth_service_url: str = "http://localhost:8082"
    observability_enabled: bool = True

    class Config:
        env_prefix = "FLEXT_WEB_INTEGRATION_"

class FlextWebConfig(FlextSettings):
    """Complete web interface configuration"""
    app_name: str = "FLEXT Web Interface"
    version: str = "0.9.0"
    environment: Environment.Type = Environment.Type.DEVELOPMENT

    server: ServerSettings = Field(default_factory=ServerSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    integration: IntegrationSettings = Field(default_factory=IntegrationSettings)

    class Config:
        env_prefix = "FLEXT_WEB_"
        env_nested_delimiter = "__"

    def validate_config(self) -> FlextResult[None]:
        """Comprehensive configuration validation"""
        # Environment-specific validation
        env = Environment(self.environment)

        if env.value == Environment.Type.PRODUCTION:
            if self.server.debug:
                return FlextResult.fail("Debug mode must be disabled in production")

            if not env.requires_ssl() and self.server.port == 80:
                return FlextResult.fail("Production should use HTTPS")

        # Port conflict validation
        integration_ports = [
            self._extract_port(self.integration.flexcore_url),
            self._extract_port(self.integration.flext_service_url),
            self._extract_port(self.integration.auth_service_url)
        ]

        if self.server.port in integration_ports:
            return FlextResult.fail(
                f"Web interface port {self.server.port} conflicts with integration services"
            )

        return FlextResult.ok(None)

    def _extract_port(self, url: str) -> int:
        """Extract port from URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.port or (443 if parsed.scheme == 'https' else 80)
        except:
            return 0

# Environment variables:
# FLEXT_WEB_APP_NAME="FLEXT Production Web"
# FLEXT_WEB_ENVIRONMENT="production"
# FLEXT_WEB_SERVER__HOST="0.0.0.0"
# FLEXT_WEB_SERVER__PORT="8080"
# FLEXT_WEB_SERVER__DEBUG="false"
# FLEXT_WEB_SECURITY__SECRET_KEY="production-secret-key-32-characters"
# FLEXT_WEB_INTEGRATION__FLEXCORE_URL="https://internal.invalid/REDACTED:8080"
```

### **Configuration Factory Pattern**

```python
from typing import Dict, Type
from flext_core import FlextResult

class ConfigurationFactory:
    """Factory for environment-specific configurations"""

    _configurations: Dict[str, Type[FlextWebConfig]] = {}

    @classmethod
    def register_config(cls, environment: str, config_class: Type[FlextWebConfig]):
        """Register configuration for specific environment"""
        cls._configurations[environment] = config_class

    @classmethod
    def create_config(cls, environment: str = None) -> FlextResult[FlextWebConfig]:
        """Create configuration for environment"""
        if environment is None:
            environment = os.getenv('FLEXT_WEB_ENVIRONMENT', 'development')

        config_class = cls._configurations.get(environment, FlextWebConfig)

        try:
            config = config_class()
            validation = config.validate_config()

            if validation.is_failure:
                return FlextResult.fail(f"Configuration validation failed: {validation.error}")

            return FlextResult.ok(config)
        except Exception as e:
            return FlextResult.fail(f"Configuration creation failed: {e}")

# Register environment-specific configurations
class DevelopmentConfig(FlextWebConfig):
    """Development-specific configuration"""
    class Config:
        env_file = ".env.development"

class ProductionConfig(FlextWebConfig):
    """Production-specific configuration"""
    class Config:
        env_file = ".env.production"

ConfigurationFactory.register_config("development", DevelopmentConfig)
ConfigurationFactory.register_config("production", ProductionConfig)

# Usage
config_result = ConfigurationFactory.create_config()
if config_result.success:
    web_service = FlextWebService(config_result.data)
```

---

## 🧪 **Testing Patterns for Web Interface**

### **Test Organization Structure**

```python
# Test structure mirrors Clean Architecture layers
tests/
├── unit/                        # Unit tests (isolated, fast)
│   ├── domain/
│   │   ├── test_entities.py     # FlextWebApp entity tests
│   │   ├── test_value_objects.py # WebAppStatus, HostPort tests
│   │   └── test_services.py     # Domain service tests
│   ├── application/
│   │   ├── test_handlers.py     # CQRS handler tests
│   │   ├── test_commands.py     # Command validation tests
│   │   └── test_config.py       # Configuration tests
│   └── infrastructure/
│       ├── test_repositories.py # Repository implementation tests
│       └── test_external.py     # External integration tests
├── integration/                 # Integration tests (with dependencies)
│   ├── test_api_endpoints.py    # REST API integration tests
│   ├── test_web_interface.py    # Web dashboard integration tests
│   ├── test_database.py         # Database integration tests
│   └── test_ecosystem.py        # FLEXT ecosystem integration tests
├── e2e/                        # End-to-end tests (full system)
│   ├── test_user_workflows.py   # Complete user workflows
│   ├── test_api_workflows.py    # API usage workflows
│   └── test_REDACTED_LDAP_BIND_PASSWORD_workflows.py  # Administrative workflows
├── performance/                # Performance tests
│   ├── test_load.py            # Load testing with Locust
│   ├── test_stress.py          # Stress testing
│   └── test_benchmarks.py      # Performance benchmarks
├── fixtures/                   # Test data and fixtures
│   ├── web_apps.py             # Sample web application data
│   ├── configurations.py       # Test configurations
│   └── mock_services.py        # Mock external services
└── conftest.py                 # Pytest configuration and fixtures
```

### **Domain Entity Testing Patterns**

```python
import pytest
from flext_core import FlextResult
from flext_web.domain.entities import FlextWebApp
from flext_web.domain.value_objects import WebAppStatus, HostPort

class TestFlextWebApp:
    """Test domain entity behavior with comprehensive scenarios"""

    def test_app_creation_success(self):
        """Test successful application creation with valid data"""
        # Arrange
        host_port = HostPort(host="localhost", port=3000)

        # Act
        app = FlextWebApp(
            id="app_test",
            name="test-app",
            host_port=host_port
        )

        # Assert
        assert app.name == "test-app"
        assert app.host_port.address == "localhost:3000"
        assert app.status == WebAppStatus.Status.STOPPED
        assert len(app.domain_events) == 0

    def test_app_start_success(self):
        """Test successful application start with state transition"""
        # Arrange
        app = FlextWebApp(
            id="app_test",
            name="test-app",
            host_port=HostPort(host="localhost", port=3000)
        )

        # Act
        result = app.start()

        # Assert
        assert result.success
        assert app.status == WebAppStatus.Status.RUNNING
        assert len(app.domain_events) == 1
        assert app.domain_events[0]["type"] == "AppStartedEvent"
        assert app.domain_events[0]["app_name"] == "test-app"

    def test_app_start_already_running(self):
        """Test starting already running application fails"""
        # Arrange
        app = FlextWebApp(
            id="app_test",
            name="test-app",
            host_port=HostPort(host="localhost", port=3000),
            status=WebAppStatus.Status.RUNNING
        )

        # Act
        result = app.start()

        # Assert
        assert result.is_failure
        assert "Cannot start application in running state" in result.error
        assert len(app.domain_events) == 0

    @pytest.mark.parametrize("status", [
        WebAppStatus.Status.STARTING,
        WebAppStatus.Status.STOPPING
    ])
    def test_app_start_transitioning_states(self, status):
        """Test starting application in transitioning states fails"""
        # Arrange
        app = FlextWebApp(
            id="app_test",
            name="test-app",
            host_port=HostPort(host="localhost", port=3000),
            status=status
        )

        # Act
        result = app.start()

        # Assert
        assert result.is_failure
        assert f"Cannot start application in {status} state" in result.error

    def test_production_privileged_port_restriction(self):
        """Test production environment blocks privileged ports"""
        # Arrange
        app = FlextWebApp(
            id="app_prod",
            name="prod-app",
            host_port=HostPort(host="0.0.0.0", port=80),
            environment="production"
        )

        # Act
        result = app.start()

        # Assert
        assert result.is_failure
        assert "Production applications cannot use privileged ports" in result.error
```

### **API Integration Testing Patterns**

```python
import pytest
from flask import Flask
from flext_web.interfaces.api.v1.apps import AppsAPI
from flext_web.application.handlers import FlextWebAppHandler
from flext_web.infrastructure.persistence.repositories import InMemoryFlextWebAppRepository

@pytest.fixture
def web_app():
    """Provide Flask test application"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def apps_api():
    """Provide configured AppsAPI for testing"""
    repository = InMemoryFlextWebAppRepository()
    handler = FlextWebAppHandler(repository)
    return AppsAPI(handler)

@pytest.fixture
def client(web_app, apps_api):
    """Provide test client with registered routes"""
    # Register API routes
    web_app.register_blueprint(apps_api.blueprint)

    with web_app.test_client() as client:
        yield client

class TestAppsAPI:
    """Test REST API endpoints with comprehensive scenarios"""

    def test_create_app_success(self, client):
        """Test successful application creation via API"""
        # Arrange
        app_data = {
            "name": "test-app",
            "host": "localhost",
            "port": 3000
        }

        # Act
        response = client.post('/api/v1/apps',
                             json=app_data,
                             content_type='application/json')

        # Assert
        assert response.status_code == 201
        data = response.get_json()
        assert data["success"] is True
        assert data["message"] == "Application created successfully"
        assert data["data"]["name"] == "test-app"
        assert data["data"]["id"] == "app_test-app"
        assert data["data"]["status"] == "stopped"

    def test_create_app_missing_name(self, client):
        """Test application creation fails without name"""
        # Arrange
        app_data = {
            "host": "localhost",
            "port": 3000
        }

        # Act
        response = client.post('/api/v1/apps',
                             json=app_data,
                             content_type='application/json')

        # Assert
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "Application name is required" in data["message"]
        assert data["data"] is None

    def test_create_app_invalid_port(self, client):
        """Test application creation fails with invalid port"""
        # Arrange
        app_data = {
            "name": "test-app",
            "host": "localhost",
            "port": 70000  # Invalid port
        }

        # Act
        response = client.post('/api/v1/apps',
                             json=app_data,
                             content_type='application/json')

        # Assert
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "Port must be between 1 and 65535" in data["message"]

    def test_start_app_success(self, client):
        """Test successful application start via API"""
        # Arrange - Create app first
        create_data = {"name": "test-app", "port": 3000}
        client.post('/api/v1/apps', json=create_data, content_type='application/json')

        # Act
        response = client.post('/api/v1/apps/app_test-app/start')

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["message"] == "Application started successfully"
        assert data["data"]["status"] == "running"
        assert data["data"]["is_running"] is True

    def test_start_nonexistent_app(self, client):
        """Test starting nonexistent application fails"""
        # Act
        response = client.post('/api/v1/apps/app_nonexistent/start')

        # Assert
        assert response.status_code == 404
        data = response.get_json()
        assert data["success"] is False
        assert "Application not found" in data["message"]
```

### **Repository Testing Patterns**

```python
import pytest
from flext_web.infrastructure.persistence.repositories import InMemoryFlextWebAppRepository
from flext_web.domain.entities import FlextWebApp
from flext_web.domain.value_objects import HostPort

class TestInMemoryFlextWebAppRepository:
    """Test repository implementation with comprehensive scenarios"""

    @pytest.fixture
    def repository(self):
        """Provide clean repository for each test"""
        return InMemoryFlextWebAppRepository()

    @pytest.fixture
    def sample_app(self):
        """Provide sample application for testing"""
        return FlextWebApp(
            id="app_sample",
            name="sample-app",
            host_port=HostPort(host="localhost", port=3000)
        )

    def test_save_app_success(self, repository, sample_app):
        """Test successful application save"""
        # Act
        result = repository.save(sample_app)

        # Assert
        assert result.success
        assert result.data == sample_app

    def test_find_by_id_success(self, repository, sample_app):
        """Test successful application retrieval by ID"""
        # Arrange
        repository.save(sample_app)

        # Act
        result = repository.find_by_id("app_sample")

        # Assert
        assert result.success
        assert result.data.id == "app_sample"
        assert result.data.name == "sample-app"

    def test_find_by_id_not_found(self, repository):
        """Test application retrieval fails for nonexistent ID"""
        # Act
        result = repository.find_by_id("app_nonexistent")

        # Assert
        assert result.is_failure
        assert "Application app_nonexistent not found" in result.error

    def test_find_all_empty(self, repository):
        """Test finding all applications when repository is empty"""
        # Act
        result = repository.find_all()

        # Assert
        assert result.success
        assert result.data == []

    def test_find_all_with_apps(self, repository):
        """Test finding all applications with multiple apps"""
        # Arrange
        apps = [
            FlextWebApp(id="app_1", name="app-1", host_port=HostPort(host="localhost", port=3000)),
            FlextWebApp(id="app_2", name="app-2", host_port=HostPort(host="localhost", port=3001))
        ]

        for app in apps:
            repository.save(app)

        # Act
        result = repository.find_all()

        # Assert
        assert result.success
        assert len(result.data) == 2
        assert {app.name for app in result.data} == {"app-1", "app-2"}
```

---

## 📏 **Code Quality Standards for Web Interface**

### **Type Annotation Requirements**

```python
# ✅ Complete type annotations for web operations
from typing import Dict, List, Optional, Union
from flask import Response
from flext_core import FlextResult

def process_web_request(
    request_data: Dict[str, Any],
    handler: FlextWebAppHandler,
    validator: RequestValidator
) -> FlextResult[Dict[str, Any]]:
    """Process web request with complete type safety"""
    return (
        validator.validate(request_data)
        .flat_map(lambda data: handler.create_app(CreateAppCommand(**data)))
        .map(lambda app: app.dict())
    )

# ✅ Generic type usage for web responses
T = TypeVar('T')

class APIResponse(Generic[T]):
    """Type-safe API response wrapper"""
    success: bool
    message: str
    data: Optional[T]

    @classmethod
    def success_response(cls, data: T, message: str = "Success") -> 'APIResponse[T]':
        return cls(success=True, message=message, data=data)

    @classmethod
    def error_response(cls, message: str) -> 'APIResponse[None]':
        return cls(success=False, message=message, data=None)

# ✅ Flask route type annotations
@api_v1.route('/apps/<string:app_id>', methods=['GET'])
def get_app(app_id: str) -> Response:
    """Get application with proper typing"""
    result: FlextResult[FlextWebApp] = app_handler.get_app(app_id)
    return APIResponseHandler.to_json_response(result)

# ❌ Missing type annotations
def process_request(data):  # Missing types
    return validate_data(data)
```

### **Error Handling Standards for Web Operations**

```python
# ✅ Always use FlextResult for web error handling
def validate_create_app_request(data: Dict[str, Any]) -> FlextResult[CreateAppCommand]:
    """Validate web request with comprehensive error handling"""
    try:
        # Input validation with detailed errors
        if not data.get('name'):
            return FlextResult.fail("Application name is required")

        if 'port' in data and not isinstance(data['port'], int):
            return FlextResult.fail("Port must be an integer")

        # Create command with validation
        command = CreateAppCommand(
            name=data['name'],
            host=data.get('host', 'localhost'),
            port=data.get('port', 8000)
        )

        return FlextResult.ok(command)

    except ValueError as e:
        return FlextResult.fail(f"Validation error: {e}")
    except Exception as e:
        return FlextResult.fail(f"Unexpected error: {e}")

# ✅ Chain web operations safely
def complete_app_creation_workflow(request_data: Dict[str, Any]) -> FlextResult[Dict[str, Any]]:
    """Complete workflow with error propagation"""
    return (
        validate_create_app_request(request_data)
        .flat_map(lambda cmd: app_handler.create_app(cmd))
        .flat_map(lambda app: register_with_load_balancer(app))
        .flat_map(lambda app: update_service_discovery(app))
        .map(lambda app: serialize_app_response(app))
    )

# ❌ Never raise exceptions in web business logic
def create_app_bad(data: Dict[str, Any]) -> FlextWebApp:
    if not data.get('name'):
        raise ValueError("Name required")  # Breaks railway pattern
    return FlextWebApp(**data)
```

### **Documentation Standards for Web Interface**

```python
def create_web_application(
    app_data: Dict[str, Any],
    handler: FlextWebAppHandler,
    port_service: WebAppPortConflictService
) -> FlextResult[FlextWebApp]:
    """
    Create new web application through complete validation and conflict resolution.

    This function implements the complete web application creation workflow including
    request validation, port conflict checking, domain entity creation, and
    persistence. It follows railway-oriented programming for consistent error handling
    in web operations.

    Args:
        app_data: Raw application data from HTTP request containing name, host, port
        handler: CQRS handler for application lifecycle management operations
        port_service: Domain service for port conflict resolution and validation

    Returns:
        FlextResult[FlextWebApp]: Success contains created application with assigned
        ID and initial status, failure contains detailed error message explaining
        validation failure, port conflict, or persistence error

    Raises:
        None: This function uses FlextResult pattern and never raises exceptions

    Example:
        >>> app_data = {"name": "web-service", "host": "localhost", "port": 3000}
        >>> result = create_web_application(app_data, handler, port_service)
        >>> if result.success:
        ...     print(f"Created: {result.data.name} at {result.data.host_port.address}")
        ... else:
        ...     print(f"Creation failed: {result.error}")

    Web API Integration:
        This function is designed for integration with REST API endpoints:
        - POST /api/v1/apps - Create application
        - Returns appropriate HTTP status codes through APIResponseHandler
        - Integrates with Flask request validation middleware
    """
    return (
        validate_app_creation_request(app_data)
        .flat_map(lambda validated: create_app_command(validated))
        .flat_map(lambda command: port_service.check_port_availability(
            HostPort(command.host, command.port)
        ).map(lambda _: command))
        .flat_map(lambda command: handler.create_app(command))
    )
```

---

## 🔄 **Migration & Refactoring Plan**

### **Phase 1: Layer Separation (Week 1-2)**

```python
# Step 1: Extract Domain Layer
# Move from __init__.py lines 42-97 to domain/entities.py
class FlextWebApp(FlextEntity):
    # Current implementation

# Move to domain/value_objects.py
class FlextWebAppStatus(Enum):
    # Current implementation

# Step 2: Extract Application Layer
# Move from __init__.py lines 98-188 to application/
class FlextWebConfig(BaseSettings, FlextConfig):
    # Current implementation

class FlextWebAppHandler(FlextHandlers.Handler):
    # Current implementation

# Step 3: Extract Infrastructure Layer
# Move from __init__.py lines 195-485 to infrastructure/web/
class FlextWebService:
    # Current implementation
```

### **Phase 2: Template System Fix (Week 2-3)**

```python
# Remove Django templates, implement Flask templates
# templates/base.html (Jinja2 syntax)
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{{ config.app_name }}</title>
</head>
<body>
    <nav class="navbar">
        <a href="{{ url_for('dashboard') }}">{{ config.app_name }}</a>
    </nav>
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>

# templates/dashboard.html
{% extends "base.html" %}
{% block content %}
<div class="dashboard">
    <h1>Applications</h1>
    <div class="stats">
        <div class="stat">{{ apps|length }} Total Apps</div>
        <div class="stat">{{ apps|selectattr("is_running")|list|length }} Running</div>
    </div>
</div>
{% endblock %}
```

### **Phase 3: Persistence Layer (Week 3-4)**

```python
# Add database support
class PostgreSQLFlextWebAppRepository(FlextWebAppRepository):
    """Production repository with PostgreSQL"""

    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def save(self, app: FlextWebApp) -> FlextResult[FlextWebApp]:
        async with self.db_pool.acquire() as conn:
            try:
                await conn.execute(
                    "INSERT INTO web_apps (id, name, host, port, status) VALUES ($1, $2, $3, $4, $5)",
                    app.id, app.name, app.host_port.host, app.host_port.port, app.status.value
                )
                return FlextResult.ok(app)
            except Exception as e:
                return FlextResult.fail(f"Database error: {e}")
```

### **Phase 4: Dependency Cleanup (Week 4)**

```python
# Update pyproject.toml - remove unused dependencies
[project]
dependencies = [
    "flext-core @ file:///home/marlonsc/flext/flext-core",
    "flext-observability @ file:///home/marlonsc/flext/flext-observability",
    "flask (>=3.0.0)",
    "pydantic (>=2.11.7)",
    "pydantic-settings (>=2.10.1)",
    # Remove: django, fastapi, celery
]
```

---

## 📋 **Refactoring Checklist**

### **Pre-Refactoring Quality Gates**

- [ ] **Current Test Coverage**: Verify 90%+ coverage before changes
- [ ] **Type Check Pass**: `make type-check` passes with current code
- [ ] **Lint Clean**: `make lint` passes with current structure
- [ ] **Baseline Performance**: Benchmark current performance metrics

### **Domain Layer Extraction Checklist**

- [ ] **Extract FlextWebApp**: Move to `domain/entities.py`
- [ ] **Extract FlextWebAppStatus**: Move to `domain/value_objects.py`
- [ ] **Create HostPort**: New value object in `domain/value_objects.py`
- [ ] **Add Domain Events**: Create `domain/events.py`
- [ ] **Repository Interfaces**: Create `domain/repositories.py`
- [ ] **Update Imports**: Fix all import statements
- [ ] **Test Migration**: Move and update corresponding tests

### **Application Layer Extraction Checklist**

- [ ] **Extract FlextWebConfig**: Move to `application/config.py`
- [ ] **Extract FlextWebAppHandler**: Move to `application/handlers.py`
- [ ] **Create Commands**: New `application/commands.py`
- [ ] **Create Queries**: New `application/queries.py`
- [ ] **Update Dependencies**: Ensure proper dependency injection
- [ ] **Test Coverage**: Maintain 90%+ coverage during extraction

### **Infrastructure Layer Creation Checklist**

- [ ] **Repository Implementation**: Create `infrastructure/persistence/repositories.py`
- [ ] **Database Models**: Create `infrastructure/persistence/models.py`
- [ ] **External Services**: Create `infrastructure/external/` modules
- [ ] **Web Middleware**: Create `infrastructure/web/middleware.py`
- [ ] **Template Management**: Create `infrastructure/web/templates.py`

### **Web Interface Layer Creation Checklist**

- [ ] **API Routes**: Create `interfaces/api/v1/` modules
- [ ] **Web Routes**: Create `interfaces/web/routes.py`
- [ ] **Template System**: Create proper Jinja2 templates
- [ ] **Static Assets**: Organize CSS, JavaScript, images
- [ ] **CLI Interface**: Create `interfaces/cli/` modules

### **Post-Refactoring Validation**

- [ ] **All Tests Pass**: `make test` passes with new structure
- [ ] **Type Safety**: `make type-check` passes with strict mode
- [ ] **Lint Clean**: `make lint` passes with new organization
- [ ] **Performance**: No performance regression
- [ ] **API Compatibility**: All existing API endpoints work
- [ ] **Documentation**: Update all documentation for new structure
- [ ] **Integration**: Verify FLEXT ecosystem integration still works

---

**Last Updated**: January 27, 2025  
**Target Audience**: FLEXT Web Interface developers and contributors  
**Scope**: Python module organization for Clean Architecture web interface  
**Refactoring Status**: Phase 1 planning (dependency cleanup and layer separation)
