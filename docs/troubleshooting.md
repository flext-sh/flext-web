# Troubleshooting - flext-web

<!-- TOC START -->

- [Primary Issue: Circular Import Error](#primary-issue-circular-import-error)
- [Diagnosis Steps](#diagnosis-steps)
  - [Test Import Failure](#test-import-failure)
  - [Analyze Dependency Chain](#analyze-dependency-chain)
- [Resolution Approaches](#resolution-approaches)
  - [Option 1: Move Shared Components](#option-1-move-shared-components)
  - [Option 2: Lazy Imports](#option-2-lazy-imports)
  - [Option 3: Dependency Injection](#option-3-dependency-injection)
- [Testing Resolution](#testing-resolution)
- [Related Issues](#related-issues)
  - [Development Commands Affected](#development-commands-affected)
  - [Quality Impact](#quality-impact)
- [Development Workflow](#development-workflow)
- [Getting Help](#getting-help)

<!-- TOC END -->

**Updated**: September 17, 2025 | **Version**: 0.9.9 RC

## Primary Issue: Circular Import Error

**Problem**: Cannot import any classes from flext-web

```python
from flext_web import FlextWebServices
# ImportError: cannot import name 'FlextWebSettings' from partially initialized module
# 'flext_web.config' (most likely due to a circular import)
# (..flext-web/src/flext_web/config.py)
```

**Root Cause**: Circular dependency chain:

- `config.py` imports `FlextWebSettings` from `settings.py`
- `settings.py` imports `FlextWebSettings` from `config.py`

**Impact**: Complete library non-functionality

## Diagnosis Steps

### Test Import Failure

```bash
# Confirm the issue exists
cd ..flext-web
python -c "from flext_web import FlextWebServices"
# Expected: ImportError with circular import message
```

### Analyze Dependency Chain

```bash
# Check actual imports in problematic files
grep -n "from.*settings" src/flext_web/config.py
grep -n "from.*config" src/flext_web/settings.py

# Look for the circular reference
grep -n "FlextWebSettings" src/flext_web/settings.py
grep -n "FlextWebSettings" src/flext_web/config.py
```

## Resolution Approaches

### Option 1: Move Shared Components

Move shared constants/types that both modules need into a separate module:

```bash
# Create shared module for common components
touch src/flext_web/shared.py
```

### Option 2: Lazy Imports

Use lazy imports to break the circular dependency:

```python
# In one of the files, import inside function instead of at module level
def get_config():
    from flext_web.settings import FlextWebSettings  # Import inside function
    return FlextWebSettings()
```

### Option 3: Dependency Injection

Use flext-core's FlextContainer to manage the dependencies:

```python
# Register components with container instead of direct imports
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import t
from flext_core import u
container = FlextContainer.get_global()
# Register and retrieve components through container
```

## Testing Resolution

Once a fix is implemented:

```bash
# Test basic import
python -c "from flext_web import FlextWebServices; print('Import successful')"

# Test component creation
python -c "
from flext_web import FlextWebServices
service = FlextWebServices()
print('Service creation successful')
"

# Test basic functionality
python -c "
from flext_web import FlextWebModels
app = FlextWebModels.WebApp(name='test', port=8080)
print(f'App created: {app.name}')
"
```

## Related Issues

### Development Commands Affected

**Works**:

- `make lint` - lints source files
- `make type-check` - type checks source files
- `make format` - formats source files

**Blocked**:

- `make test` - cannot import modules to test
- `make validate` - includes testing
- object actual usage of the library

### Quality Impact

Cannot measure:

- Test coverage (tests cannot import modules)
- Integration with flext-core (imports fail)
- Actual functionality (nothing works)

Can measure:

- Static analysis on source files
- Type checking on individual files
- Linting results

## Development Workflow

Until circular imports are resolved:

1. **Focus on static analysis**: Use lint and type-check on source files
1. **Avoid import testing**: Cannot test actual functionality
1. **Plan refactoring**: Design solution for dependency structure
1. **Test incrementally**: Test imports after each structural change

## Getting Help

**Pattern reference**: See ../flext-core/README.md for dependency injection patterns
**Architecture guidance**: ../docs/architecture for Clean Architecture separation principles
**Issue priority**: This is the only blocking issue preventing all development
