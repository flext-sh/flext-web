# Development Guide - flext-web

**Updated**: September 17, 2025 | **Version**: 0.9.0

## Development Focus

**Primary objective**: Implement architectural improvements while maintaining functional imports.

Circular import issue resolved - focus on FLEXT compliance and modern web patterns.

## Current Development Status

**Functional**: Basic imports and service creation work
**Architecture Gaps**: Direct Flask imports, nested classes need refactoring
**Quality Status**: Source files pass linting and type checking

## Development Setup

```bash
# Complete setup
cd flext/flext-web
poetry install
make setup

# Verify functionality
python -c "from flext_web import FlextWebServices; print('Import successful')"
make lint      # ✅ Source files pass
make type-check # ✅ Source files pass
```

## Development Commands

### Quality Gates

```bash
make lint          # Ruff linting
make type-check    # MyPy/PyRight type checking
make format        # Auto-format code
make validate      # Complete validation (when tests work)
```

### Testing (Implementation Needed)

```bash
make test          # Run test suite (needs implementation)
make coverage      # Test coverage report
make test-web      # Web-specific functionality tests
```

## Architecture Context

**flext-web design** follows patterns from:

- **flext-core**: Foundation patterns (FlextResult, FlextModels, Clean Architecture)
- **FLEXT workspace**: Overall architecture guidance (see ../docs/architecture)

**flext-web specific concerns**:

- Web application lifecycle management
- Flask integration patterns
- HTTP request/response handling
- Web-specific domain models

**Not duplicated here**: flext-core already documents FlextResult, FlextContainer, domain modeling, and Clean Architecture patterns.

## Code Organization

**Current structure** (4,441 lines across 15 files):

```
src/flext_web/
├── services.py (818 lines)    # Flask web services
├── config.py (774 lines)      # Configuration management
├── handlers.py (691 lines)    # CQRS handlers
├── protocols.py (439 lines)   # Interface definitions
├── models.py (279 lines)      # Domain models
├── settings.py (54 lines)     # Settings
└── Other modules...
```

## Development Priorities

### Priority 1: Architectural Compliance

- **Fix Direct Flask Imports**: Abstract Flask through flext-web interfaces
- **Single Class Pattern**: Refactor services.py nested classes
- **Enhanced flext-core Integration**: Complete FlextResult usage
- **Type Safety**: Achieve zero MyPy errors in strict mode

### Priority 2: Web Framework Enhancement

- **HTTP Interface**: Create framework-agnostic request/response handling
- **Error Handling**: Standardize FlextResult patterns
- **Middleware System**: Request/response pipeline
- **Configuration**: Environment-based configuration management

### Priority 3: Modern Web Patterns

- **Async Research**: Investigate FastAPI compatibility
- **API Documentation**: Auto-generated documentation
- **Testing Infrastructure**: Web-specific test utilities
- **CLI Integration**: flext-cli command support

## Quality Standards

**Static analysis** (works on source files):

- Ruff linting: Zero violations
- MyPy strict mode: Zero errors
- Type annotations: Complete coverage

**Functional testing** (needs implementation):

- Web service functionality tests
- HTTP request/response testing
- Integration tests with flext-core
- Performance and security testing

## Integration Guidelines

**flext-core integration patterns**:

- Use FlextResult[T] for all operations returning values
- Use FlextModels.Entity for domain entities (WebApp, etc.)
- Use FlextContainer for dependency injection
- Follow Clean Architecture layer separation

**Web-specific patterns**:

- Flask application factory patterns
- HTTP request/response handling
- Web application lifecycle management
- Configuration management for web services

## Contributing Workflow

**Current focus**: Architectural compliance and quality improvement

1. **Analyze current architecture**: Understand existing patterns
2. **Plan incremental changes**: Small, focused improvements
3. **Implement FLEXT compliance**: Fix architectural violations
4. **Add web functionality**: Implement missing API methods
5. **Add comprehensive tests**: Web-specific testing
6. **Performance optimization**: Benchmark and improve
7. **Documentation updates**: Keep docs current with code

## Getting Help

**Architecture reference**: ../docs/architecture (Clean Architecture patterns)
**Foundation patterns**: ../flext-core/README.md (FlextResult, domain modeling)
**Development roadmap**: See TODO.md for priorities and implementation plan

**Current status**: Foundation functional, architectural improvements in progress.
