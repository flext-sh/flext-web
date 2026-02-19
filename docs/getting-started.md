# Getting Started - flext-web


<!-- TOC START -->
- [Current Status](#current-status)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Integration with FLEXT Patterns](#integration-with-flext-patterns)
- [Development Priority](#development-priority)
- [Getting Help](#getting-help)
- [Related Documentation](#related-documentation)
<!-- TOC END -->

**Updated**: September 17, 2025 | **Version**: 0.9.9 RC

## Current Status

**flext-web is functional** for imports and basic service creation. Circular import issue has been resolved.

## Prerequisites

- Python 3.11+
- Access to flext-core (../flext-core)
- Poetry for dependency management

## Installation

```bash
# Clone FLEXT workspace if needed
cd flext/flext-web

# Install dependencies
poetry install
make setup

# Verify installation
python -c "from flext_web import FlextWebServices; print('Import successful')"
```

## Basic Usage

```python
from flext_web import FlextWebServices, FlextWebModels, FlextWebHandlers

# Create web service
service = FlextWebServices()
print(f"Service type: {type(service)}")

# Access components
handlers = FlextWebHandlers()
models = FlextWebModels()

# Check available methods
methods = [m for m in dir(service) if not m.startswith('_')]
print(f"Available methods: {methods}")
```

## Integration with FLEXT Patterns

flext-web uses patterns from flext-core:

- **FlextResult[T]** for error handling
- **FlextModels** for domain entities
- **Clean Architecture** layer separation

See [flext-core README](https://github.com/organization/flext/tree/main/flext-core/README.md) for foundation patterns.

## Development Priority

1. **Architecture Compliance**: Fix direct Flask imports and follow FLEXT standards
2. **API Implementation**: Complete web service methods
3. **Testing**: Implement comprehensive test coverage
4. **Modern Patterns**: Research FastAPI integration for support

## Getting Help

**Current State**: Basic imports functional, architectural improvements needed
**Next Steps**: See [TODO.md](../TODO.md) for development roadmap
**Architecture**: See [development.md](development.md) for development patterns

---

**Status**: Functional for imports - ready for architectural improvements · 1.0.0 Release Preparation

## Related Documentation

**Within Project**:

- [Architecture](architecture.md) - Architecture and design patterns
- [API Reference](api-reference.md) - Complete API documentation
- [Development](development.md) - Development patterns

**Across Projects**:

- [flext-core Foundation](https://github.com/organization/flext/tree/main/flext-core/docs/architecture/overview.md) - Clean architecture and CQRS patterns
- [flext-core Service Patterns](https://github.com/organization/flext/tree/main/flext-core/docs/guides/service-patterns.md) - Service patterns and dependency injection
- [flext-api HTTP Framework](https://github.com/organization/flext/tree/main/flext-api/CLAUDE.md) - HTTP foundation patterns

**External Resources**:

- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
