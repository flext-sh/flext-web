# flext-web

**Type**: Application Service | **Status**: Active Development | **Dependencies**: flext-core

Web interface and REST API for managing FLEXT ecosystem services and applications.

> **⚠️ Development Status**: Flask service working, in-memory storage only, authentication missing, ecosystem integration incomplete

## Quick Start

```bash
# Install dependencies
poetry install

# Test basic functionality
python -c "from flext_web import create_service; service = create_service(); print('✅ Working')"

# Development setup
make setup

# Start web server
make runserver
```

## Current Reality

**What Actually Works:**

- Flask web service with REST API endpoints
- Application lifecycle management (start/stop states)
- HTML dashboard with real-time status
- Clean Architecture with flext-core patterns

**What Needs Work:**

- In-memory storage only (no persistence)
- No authentication or authorization
- Limited ecosystem service integration
- Basic HTML dashboard (needs frontend framework)

## Architecture Role in FLEXT Ecosystem

### **Application Service Component**

FLEXT Web provides management interface for ecosystem services:

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLEXT ECOSYSTEM (32 Projects)                 │
├─────────────────────────────────────────────────────────────────┤
│ Services: FlexCore(Go) | FLEXT Service(Go/Python) | Clients     │
├─────────────────────────────────────────────────────────────────┤
│ Applications: API | Auth | [FLEXT-WEB] | CLI | Quality | Observ │
├═════════════════════════════════════════════════════════════════┤
│ Infrastructure: Oracle | LDAP | LDIF | gRPC | Plugin | WMS      │
├─────────────────────────────────────────────────────────────────┤
│ Singer Ecosystem: Taps(5) | Targets(5) | DBT(4) | Extensions(1) │
├─────────────────────────────────────────────────────────────────┤
│ Foundation: FLEXT-CORE (FlextResult | DI | Domain Patterns)     │
└─────────────────────────────────────────────────────────────────┘
```

### **Core Responsibilities**

1. **Web Dashboard**: Management interface for FLEXT services
2. **REST API**: Programmatic access to ecosystem operations
3. **Application Management**: Service lifecycle and monitoring

## Key Features

### **Current Capabilities**

- **FlextWebService**: Flask-based web service with REST endpoints
- **Application Management**: Create, start, stop applications (in-memory)
- **Web Dashboard**: Real-time HTML interface
- **API Endpoints**: RESTful interface for programmatic access

### **API Endpoints**

```bash
# Health and status
GET /health              # Service health check
GET /                   # Web dashboard

# Application management
GET /api/v1/apps        # List applications
POST /api/v1/apps       # Create application
GET /api/v1/apps/<id>   # Get application details
POST /api/v1/apps/<id>/start  # Start application
POST /api/v1/apps/<id>/stop   # Stop application
```

## Installation & Usage

### Installation

```bash
# Clone and install
cd /path/to/flext-web
poetry install

# Development setup
make setup
```

### Basic Usage

```python
from flext_web import create_service, get_web_settings

# Start with default configuration
service = create_service()
service.run()

# Custom configuration
config = get_web_settings()
config.port = 9000
service = create_service(config)
service.run(host="0.0.0.0", port=9000)
```

### CLI Usage

```bash
# Start web server
python -m flext_web --host 0.0.0.0 --port 8080 --debug

# Using make commands
make runserver           # Start development server
make dev-server         # Start with hot reload
```

## Development Commands

### Quality Gates (Zero Tolerance)

```bash
# Complete validation pipeline (run before commits)
make validate              # Full validation (lint + type + security + test)
make check                 # Quick lint + type check + test
make test                  # Run all tests (90% coverage requirement)
make lint                  # Code linting
make type-check            # Type checking
make format                # Code formatting
make security              # Security scanning
```

### Web Development

```bash
# Server operations
make runserver             # Start Flask development server (localhost:8080)
make dev-server            # Start with hot reload
make web-test              # Test web service creation
```

### Testing

```bash
# Test categories
make test-unit             # Unit tests only
make test-integration      # Integration tests only
make test-api              # API endpoint tests
make test-web              # Web interface tests
make coverage-html         # Generate HTML coverage report
```

## Configuration

### Environment Variables

```bash
# Web service configuration
export FLEXT_WEB_HOST="localhost"
export FLEXT_WEB_PORT="8080"
export FLEXT_WEB_DEBUG="true"
export FLEXT_WEB_SECRET_KEY="your-secret-key"
```

## Quality Standards

### **Quality Targets**

- **Coverage**: 90% target (work in progress)
- **Type Safety**: MyPy strict mode adoption in progress
- **Linting**: Ruff with comprehensive rules (continuous improvement)
- **Security**: Bandit + pip-audit scanning

## Integration with FLEXT Ecosystem

### **FLEXT Core Patterns**

```python
# FlextResult for all operations
from flext_web import FlextWebService

service = FlextWebService()
result = service.create_app("test-app", 3000, "localhost")
if result.success:
    app = result.data
    print(f"Created app: {app.name}")
else:
    print(f"Error: {result.error}")
```

### **Service Integration**

- **flext-auth**: Authentication and authorization (planned)
- **flext-observability**: Monitoring and metrics collection
- **FlexCore (Go)**: Runtime service integration
- **FLEXT Service**: Data platform coordination

## Current Status

**Version**: 0.9.0 (Development)

**Completed**:

- ✅ Flask web service with REST API
- ✅ Application lifecycle management
- ✅ HTML dashboard interface
- ✅ Clean Architecture with flext-core patterns

**In Progress**:

- 🔄 Persistent storage implementation
- 🔄 Authentication and authorization
- 🔄 Ecosystem service integration

**Planned**:

- 📋 Frontend framework integration
- 📋 Real-time WebSocket updates
- 📋 Advanced monitoring dashboard

## Contributing

### Development Standards

- **FLEXT Core Integration**: Use established patterns
- **Type Safety**: All code must pass MyPy
- **Testing**: Maintain 90% coverage
- **Code Quality**: Follow linting rules

### Development Workflow

```bash
# Setup and validate
make setup
make validate
make test
make runserver
```

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Links

- **[flext-core](../flext-core)**: Foundation library
- **[CLAUDE.md](CLAUDE.md)**: Development guidance
- **[Documentation](docs/)**: Complete documentation

---

_Part of the FLEXT ecosystem - Enterprise data integration platform_
