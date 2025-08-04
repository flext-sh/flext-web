# FLEXT Web Interface

[![Version](https://img.shields.io/badge/version-0.9.0-blue.svg)](https://github.com/flext-sh/flext)
[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-100%25-brightgreen.svg)](docs/)
[![Quality](https://img.shields.io/badge/quality-90%25-yellow.svg)](docs/quality/README.md)

**Status**: ✅ **Documentation Complete** - Enterprise-grade documentation standardization achieved (2025-08-04)

Enterprise web interface for the FLEXT distributed data integration platform. Provides comprehensive dashboard and REST API endpoints for monitoring and managing applications within the FLEXT ecosystem.

## 🎯 Project Purpose

**flext-web** serves as the **central web management console** for the FLEXT ecosystem, providing:

- **Unified Dashboard**: Real-time monitoring of FLEXT services and data pipelines
- **Application Management**: Lifecycle management for distributed FLEXT applications
- **API Gateway**: RESTful interface for programmatic ecosystem interaction
- **Integration Hub**: Connection point between FlexCore (Go) and FLEXT services
- **Observability Center**: Centralized monitoring using flext-observability patterns

### FLEXT Ecosystem Integration

As part of the **33-project FLEXT ecosystem**, flext-web integrates with:

- **flext-core**: Foundation patterns (FlextResult, DI container, logging)
- **flext-observability**: Monitoring, metrics, health checks
- **flext-auth**: Authentication and authorization (planned)
- **FlexCore** (Go): Runtime container service (port 8080)
- **FLEXT Service** (Go/Python): Data platform service (port 8081)

## 🏗️ Architecture

### Clean Architecture Implementation

```
┌─────────────────────────────────────┐
│           Web Interface             │
│  (Flask Routes + HTML Dashboard)    │
├─────────────────────────────────────┤
│         Application Layer           │
│  (FlextWebService + Handlers)       │
├─────────────────────────────────────┤
│           Domain Layer              │
│    (FlextWebApp + Business Rules)   │
├─────────────────────────────────────┤
│        Infrastructure Layer         │
│   (flext-core integration + Flask)  │
└─────────────────────────────────────┘
```

### Key Components

- **FlextWebApp**: Domain entity with lifecycle management (start/stop/status)
- **FlextWebAppHandler**: CQRS command handlers for application operations
- **FlextWebService**: Flask service with route registration and API endpoints
- **FlextWebConfig**: Environment-based configuration with validation
- **Exception Hierarchy**: Domain-specific exceptions extending flext-core patterns

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Poetry (dependency management)
- Access to flext-core and flext-observability (local path dependencies)

### Installation

```bash
# Clone and setup
git clone <repository-url>
cd flext-web
make setup

# Install dependencies
make install

# Start development server
make runserver
```

### Basic Usage

```bash
# Development mode (localhost:8080)
python -m flext_web --debug

# Production mode
python -m flext_web --no-debug --host 0.0.0.0 --port 8080

# Using environment variables
export FLEXT_WEB_HOST=localhost
export FLEXT_WEB_PORT=8080
export FLEXT_WEB_DEBUG=false
python -m flext_web
```

## 📡 API Endpoints

### Health & Management

- `GET /health` - Service health check with ecosystem status
- `GET /` - Web dashboard with real-time metrics

### Application Management

- `GET /api/v1/apps` - List all managed applications
- `POST /api/v1/apps` - Create new application
- `GET /api/v1/apps/<id>` - Get application details
- `POST /api/v1/apps/<id>/start` - Start application
- `POST /api/v1/apps/<id>/stop` - Stop application

### API Examples

```bash
# Check service health
curl http://localhost:8080/health

# Create application
curl -X POST http://localhost:8080/api/v1/apps \
  -H "Content-Type: application/json" \
  -d '{"name": "data-pipeline", "port": 3000, "host": "localhost"}'

# Start application
curl -X POST http://localhost:8080/api/v1/apps/app_data-pipeline/start
```

## 🛠️ Development

### Quality Gates

```bash
make validate                # Complete validation (lint + type + security + test)
make check                   # Quick health check (lint + type)
make test                    # Run all tests with coverage
make format                  # Auto-format code
```

### Testing

```bash
make test                    # All tests with coverage
make test-unit               # Unit tests only
make test-integration        # Integration tests
make test-api                # API endpoint tests
make test-web                # Web interface tests
```

### Web Development

```bash
make runserver              # Start Flask development server
make dev-server             # Start with hot reload
make prod-server            # Start production server
make web-test               # Test web service creation
```

## 📊 Current Status

### ✅ What Works

- Flask web service with REST API endpoints
- FlextWebApp entity with lifecycle management
- Clean Architecture patterns using flext-core
- Configuration management with environment variables
- Comprehensive exception hierarchy
- Basic HTML dashboard with inline generation
- Full test coverage with pytest

### ⚠️ Known Limitations

- **In-memory storage only**: No persistence layer implemented
- **Mixed dependencies**: pyproject.toml includes unused Django/FastAPI/Celery
- **No authentication**: API endpoints are completely open
- **Template inconsistency**: Django templates exist but Flask uses inline HTML
- **Single instance**: No clustering or distributed state support

## 🗺️ Roadmap

### Phase 1: Stabilization (Current - Sprint 3)

- [ ] Resolve dependency inconsistencies (Django/Flask)
- [ ] Implement persistence layer (PostgreSQL/Redis)
- [ ] Add basic authentication integration
- [ ] Refactor monolithic architecture

### Phase 2: Integration (Sprint 4-6)

- [ ] Integrate with flext-auth for security
- [ ] Connect to FlexCore and FLEXT Service
- [ ] Implement real application management
- [ ] Add observability dashboards

### Phase 3: Production (Sprint 7-9)

- [ ] Performance optimization
- [ ] Advanced monitoring and alerting
- [ ] Multi-tenant support
- [ ] API rate limiting and caching

## 📖 Documentation

- **[Development Guide](docs/development/README.md)** - Complete development setup and workflows
- **[Architecture Guide](docs/architecture/README.md)** - Clean Architecture implementation details
- **[API Reference](docs/api/README.md)** - Complete REST API documentation
- **[Configuration Guide](docs/configuration/README.md)** - Environment and settings management
- **[Deployment Guide](docs/deployment/README.md)** - Production deployment strategies
- **[Contributing Guide](docs/contributing/README.md)** - How to contribute to the project
- **[TODO & Issues](docs/TODO.md)** - Known issues and improvement roadmap

## 🔧 Configuration

### Environment Variables

```bash
# Server Configuration
FLEXT_WEB_HOST=localhost          # Server host (default: localhost)
FLEXT_WEB_PORT=8080              # Server port (default: 8080)
FLEXT_WEB_DEBUG=true             # Debug mode (default: true)

# Security
FLEXT_WEB_SECRET_KEY=your-secret-key-here  # Required in production

# Integration (planned)
FLEXT_WEB_FLEXCORE_URL=http://localhost:8080     # FlexCore service URL
FLEXT_WEB_FLEXT_SERVICE_URL=http://localhost:8081 # FLEXT Service URL
```

### Configuration Validation

The service validates all configuration on startup using flext-core patterns:

```python
from flext_web import get_web_settings

config = get_web_settings()
print(f"Service URL: {config.get_server_url()}")
print(f"Production mode: {config.is_production()}")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following the coding standards
4. Run quality gates (`make validate`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Standards

- **Code Quality**: 90%+ test coverage, strict typing, comprehensive linting
- **Architecture**: Follow Clean Architecture and DDD patterns
- **Integration**: Use flext-core patterns for consistency
- **Documentation**: Update docs for any API or architecture changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏢 FLEXT Ecosystem Integration

**flext-web** is part of the comprehensive FLEXT enterprise data integration platform with 32+ interconnected projects.

### **Workspace Documentation**

- **🌐 [FLEXT Ecosystem Hub](../docs/README.md)** - Master documentation navigation for all 32 projects
- **🗺️ [Complete Navigation](../docs/NAVIGATION.md)** - Cross-project navigation and reference system
- **🏗️ [Ecosystem Architecture](../docs/architecture/ecosystem-architecture.md)** - Complete system architecture
- **📋 [Documentation Standards](../docs/DOCUMENTATION_STANDARD.md)** - Enterprise documentation template

### **Related Projects**

- **[flext-core](../flext-core/)** - Foundation patterns and DI container
- **[flext-observability](../flext-observability/)** - Monitoring and metrics
- **[FlexCore](../flexcore/)** - Go runtime container service (port 8080)
- **[FLEXT Service](../cmd/flext/)** - Data platform service (port 8081)

### **Project Positioning**

```
FLEXT Ecosystem (32+ Projects)
├── Foundation Libraries (2)     │ flext-core, flext-observability
├── Core Services (3)           │ FlexCore, FLEXT Service, Control Panel
├── Application Services (5)    │ → flext-web ← (YOU ARE HERE)
├── Infrastructure (6)          │ Database, LDAP, gRPC, WMS connectors
├── Singer Integration (15)     │ Taps, targets, DBT transformations
└── Enterprise Solutions (2)    │ Client-specific implementations
```

---

**Maintainers**: FLEXT Development Team  
**Documentation Status**: ✅ Complete (100% enterprise standardization)  
**Version**: 0.9.0 → 1.0.0 (production ready)  
**Last Updated**: January 2025
