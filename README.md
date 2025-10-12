# flext-web

**Web application patterns for FLEXT projects requiring web interfaces.**

> **⚠️ STATUS**: Functional for imports and basic services - architectural improvements needed

**Version**: 0.9.9 RC | **Updated**: September 17, 2025

---

## Purpose and Role in FLEXT Ecosystem

### For the FLEXT Ecosystem

flext-web provides **Web UI/Dashboard layer** for FLEXT ecosystem projects, focusing on Flask-based web interfaces and HTML rendering. It integrates with flext-auth for authentication and flext-api for REST API communication, creating a cohesive web application stack.

### Key Responsibilities

1. **Web UI/Dashboard** - Flask-based web dashboards and HTML rendering
2. **Session Management** - Flask session handling with secure cookies
3. **Authentication UI** - Login/logout/registration interfaces using flext-auth
4. **Frontend for REST APIs** - Uses flext-api client for backend communication

### Domain Separation in FLEXT Web Stack

- **flext-web** → Web UI layer (Flask dashboards, HTML rendering, sessions)
- **flext-api** → HTTP client layer (FlextApiClient for backend communication)
- **flext-auth** → Authentication layer (JWT, OAuth2, 10 providers + middleware)
- **flext-core** → Foundation patterns (FlextCore.Result, FlextCore.Container, FlextCore.Models)

**Phase 2 Status**: FastAPI application factory (FlextWebApp) migrated to flext-web ✅. Full server implementation (FlextWebServer) pending middleware/plugin migration.

### Integration Points (Phase 1 Complete)

✅ **flext-auth Integration Complete**:

- JWT-based authentication with 10 provider support
- WebAuthMiddleware integration for Flask session management
- Endpoints: `/auth/login`, `/auth/logout`, `/auth/register`
- User management with FlextCore.Result error handling

✅ **flext-api Integration Complete**:

- FlextApiClient initialized for backend HTTP communication
- Methods: `fetch_apps_from_api()`, `create_app_via_api()`, `delete_app_via_api()`
- Ready for backend integration when service available

✅ **flext-core Foundation**:

- FlextCore.Result[T] for railway-oriented error handling
- FlextCore.Logger for structured logging
- FlextCore.Container for dependency injection
- FlextCore.Models.Entity for domain modeling

### Phase 2 Progress: FastAPI Migration

✅ **Phase 2.1 Complete: FastAPI Application Factory**

- `FlextWebApp` - Enterprise-grade FastAPI application creation (242 lines)
- `create_fastapi_app()` - Helper function for quick app creation
- Health check endpoints with /health route
- OpenAPI documentation support (/docs, /redoc)
- Middleware support for authentication (flext-auth integration)
- Exported from flext-web and fully functional

🔄 **Phase 2.2 Pending: FastAPI Server**

- `FlextWebServer` - Full-featured server with protocol handlers (planned)
- Requires migration of BaseMiddleware and ProtocolPlugin from flext-api
- WebSocket, SSE, and GraphQL endpoint support (pending)
- Server lifecycle management (start/stop/restart) (pending)

**Migration Path**: Applications should use FlextWebApp for FastAPI app creation. The flext-api deprecation warnings already point to flext-web. Full server functionality will be completed in a future phase.

---

## Current Status

**Recently Fixed**: Circular import issue resolved - basic imports now functional

**Architecture Implementation**:

- **4,441 lines** across **15 Python files**
- **Clean Architecture** with domain, application, and infrastructure layers
- **CQRS Pattern** implemented in handlers (691 lines)
- **Domain Modeling** using FlextCore.Models.Entity patterns (279 lines)
- **Configuration System** comprehensive but needs enhancement (774 lines)

**Current Gaps**:

- Direct Flask imports (architectural violation of FLEXT patterns)
- Limited /modern web framework support
- Missing flext-cli integration for web commands

---

## Quick Start

### Installation

```bash
git clone https://github.com/flext-sh/flext-web.git
cd flext-web
make setup

# Verify imports work
python -c "from flext_web import FlextWebServices; print('Import successful')"
```

### Basic Usage - Flask Web Service

```python
from flext_web import FlextWebServices
from flext_auth import FlextAuth
from flext_api import FlextApiClient

# Create Flask web service with integrated auth and API client
config = {
    "secret_key": "your-secret-key-min-32-chars-long",
    "debug_bool": False,
    "api_base_url": "http://localhost:8000",  # Backend REST API
    "session_cookie_secure": True,
    "session_cookie_httponly": True,
    "session_cookie_samesite": "Lax"
}

# Initialize Flask web service (automatically integrates flext-auth and flext-api)
web_service = FlextWebServices.WebService(config)

# Start Flask application
web_service.start()

# Available endpoints:
# - POST /auth/login - User authentication
# - POST /auth/logout - User logout
# - POST /auth/register - User registration
# - GET / - Dashboard (requires authentication)
# - GET /health - Health check
```

### Basic Usage - FastAPI Application

```python
from flext_web import create_fastapi_app, FlextWebApp
from flext_web.models import FlextWebModels

# Quick FastAPI app creation
config = FlextWebModels.AppConfig(
    title="My Enterprise API",
    version="1.0.0",
    description="Enterprise-grade API with FLEXT patterns"
)

# Create FastAPI application
result = create_fastapi_app(config)
if result.is_success:
    app = result.unwrap()
    # app is ready to use with uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)

# With authentication middleware
from flext_auth import FlextAuthOAuth2Provider, WebAuthMiddleware

auth_provider = FlextAuthOAuth2Provider(
    client_id="your-client-id",
    client_secret="your-client-secret",
    authorization_url="https://auth.example.com/oauth/authorize",
    token_url="https://auth.example.com/oauth/token"
)
auth_middleware = WebAuthMiddleware(provider=auth_provider)

config_with_auth = FlextWebModels.AppConfig(
    title="Authenticated API",
    version="1.0.0",
    middlewares=[auth_middleware]
)
app_result = create_fastapi_app(config_with_auth)
```

### Integration Example: Authentication + API Client

```python
from flext_web import FlextWebServices
from flext_auth import FlextAuth
from flext_api import FlextApiClient

# Create web service with integrated auth and API client
config = {
    "secret_key": "your-secret-key-min-32-chars-long",
    "debug_bool": False,
    "api_base_url": "http://localhost:8000",
}

web_service = FlextWebServices.WebService(config)

# Authentication Example (flext-auth integration)
def login_user(username: str, password: str):
    """Login using flext-auth JWT authentication."""
    # POST /auth/login
    # Body: {"username": "user@example.com", "password": "password123"}
    # Response: Sets session cookie with JWT token
    # Handled automatically by FlextWebService with flext-auth

def logout_user():
    """Logout and clear session."""
    # POST /auth/logout
    # Response: Clears session cookie
    # Handled by FlextWebService

# API Client Example (flext-api integration)
def fetch_applications():
    """Fetch applications from backend using FlextApiClient."""
    apps_result = web_service.fetch_apps_from_api()
    if apps_result.is_failure:
        return {"error": apps_result.error}, 500

    return {"apps": apps_result.value}, 200

def create_application(app_data: dict):
    """Create application via backend API."""
    result = web_service.create_app_via_api(app_data)
    if result.is_failure:
        return {"error": result.error}, 400

    return {"app": result.value}, 201

# Dashboard Example (combined integration)
def protected_dashboard():
    """Dashboard showing authentication + API client integration.

    Integration demonstration:
    - Uses flext-auth for JWT authentication
    - Uses FlextApiClient for backend communication
    - FlextCore.Result error handling throughout
    """
    # Authentication handled by FlextWebService middleware
    # API calls available through fetch_apps_from_api() method
    # Current implementation uses local data, ready for backend
```

### Available Endpoints

**Authentication Endpoints** (flext-auth):

- `POST /auth/login` - User login with JWT token generation
- `POST /auth/logout` - User logout and session clearing
- `POST /auth/register` - User registration

**Application Endpoints**:

- `GET /` - Dashboard (requires authentication)
- `GET /health` - Health check endpoint

**API Client Methods** (flext-api):

- `fetch_apps_from_api()` - Fetch applications from backend
- `create_app_via_api(app_data)` - Create application via backend
- `delete_app_via_api(app_name)` - Delete application via backend

---

## Architecture and Patterns

### Foundation Integration

Built on flext-core patterns:

- **FlextCore.Result[T]** - Railway-oriented error handling
- **FlextCore.Models.Entity** - Domain modeling
- **FlextCore.Container** - Dependency injection
- **Clean Architecture** - Layer separation

### Web-Specific Components

**Domain Layer**:

- `models.py` - WebApp entities with business rules
- Domain events and validation

**Application Layer**:

- `handlers.py` - CQRS command handlers
- Web application use cases

**Infrastructure Layer**:

- `services.py` - Flask service implementations
- `config.py` - Configuration management

---

## Development

### Essential Commands

```bash
make setup          # Complete development setup
make validate       # All quality checks
make lint          # Code linting
make type-check    # Type validation
make format        # Auto-formatting
make test          # Run tests (when functional)
```

### Quality Standards

- **Type Safety**: Complete type annotations
- **Code Quality**: Zero Ruff violations
- **Testing**: Target 85% coverage (following flext-core standard)
- **Integration**: Seamless flext-core pattern usage

---

## Current Implementation

### What Works

```python
# Basic imports and service creation
from flext_web import FlextWebServices, FlextWebModels, FlextWebHandlers
service = FlextWebServices()  # Successfully creates service instance

# Component access
handlers = FlextWebHandlers()
models = FlextWebModels()
```

### What Needs Implementation

- Complete API methods (create_application, etc.)
- Flask abstraction layer
- flext-cli integration
- web framework support research
- Production-ready web patterns

---

## Roadmap

### Phase 1: Foundation (Priority 1)

- Fix direct Flask imports through abstraction
- Complete FlextCore.Result integration
- Implement single class per module pattern
- Achieve zero type errors

### Phase 2: Web Capabilities (Priority 2)

- HTTP request/response enhancement
- Security and authentication integration
- CLI command support
- Testing infrastructure

### Phase 3: Modern Patterns (Priority 3)

- Research FastAPI compatibility
- WebSocket support foundation
- Caching integration
- Developer experience tools

---

## Documentation

- **[TODO](TODO.md)** - Development roadmap and priorities
- **[Getting Started](docs/getting-started.md)** - Installation guide
- **[Development](docs/development.md)** - Development workflow
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues

---

## Contributing

### Development Areas

- Architectural compliance with FLEXT standards
- Modern web framework pattern implementation
- Testing and quality improvements
- Documentation enhancement

### Quality Requirements

- All changes must pass `make validate`
- Follow FLEXT ecosystem patterns
- Maintain Clean Architecture principles
- Complete type annotations required

---

**flext-web v0.9.9** - Web application patterns for FLEXT ecosystem projects, providing Flask integration with Clean Architecture and modern web development capabilities.
