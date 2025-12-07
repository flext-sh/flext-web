# Getting Started - flext-web

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
