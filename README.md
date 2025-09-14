# flext-web

**Web application patterns for FLEXT projects requiring web interfaces.**

> **⚠️ STATUS**: Functional for imports and basic services - architectural improvements needed

**Version**: 0.9.0 | **Updated**: September 17, 2025

---

## Purpose and Role in FLEXT Ecosystem

### For the FLEXT Ecosystem

flext-web provides web interface patterns and Flask integration for FLEXT ecosystem projects that require web capabilities. Built on flext-core foundation patterns, it offers web-specific domain models, HTTP handling, and application lifecycle management.

### Key Responsibilities

1. **Web Application Management** - Flask app creation and lifecycle
2. **HTTP Request/Response Handling** - Structured web request processing
3. **Web Domain Models** - Web-specific entities and value objects
4. **Configuration Management** - Web service configuration patterns

### Integration Points

- **flext-core** → Foundation patterns (FlextResult, FlextContainer, FlextModels)
- **FLEXT projects** → Import web patterns from flext-web
- **Web frameworks** → Flask integration with Clean Architecture

---

## Current Status

**Recently Fixed**: Circular import issue resolved - basic imports now functional

**Architecture Implementation**:
- **4,441 lines** across **15 Python files**
- **Clean Architecture** with domain, application, and infrastructure layers
- **CQRS Pattern** implemented in handlers (691 lines)
- **Domain Modeling** using FlextModels.Entity patterns (279 lines)
- **Configuration System** comprehensive but needs enhancement (774 lines)

**Current Gaps**:
- Direct Flask imports (architectural violation of FLEXT patterns)
- Limited async/modern web framework support
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

### Basic Usage

```python
from flext_web import FlextWebServices, FlextWebModels

# Create web service
service = FlextWebServices()

# Available service methods
methods = [m for m in dir(service) if not m.startswith('_')]
print(f"Available methods: {methods}")

# Create web configuration (when methods are implemented)
# config = FlextWebModels.WebAppConfig(host="localhost", port=8080)
# result = service.create_web_application(config)
```

---

## Architecture and Patterns

### Foundation Integration

Built on flext-core patterns:
- **FlextResult[T]** - Railway-oriented error handling
- **FlextModels.Entity** - Domain modeling
- **FlextContainer** - Dependency injection
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
- Async web framework support research
- Production-ready web patterns

---

## Roadmap

### Phase 1: Foundation (Priority 1)
- Fix direct Flask imports through abstraction
- Complete FlextResult integration
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

**flext-web v0.9.0** - Web application patterns for FLEXT ecosystem projects, providing Flask integration with Clean Architecture and modern web development capabilities.