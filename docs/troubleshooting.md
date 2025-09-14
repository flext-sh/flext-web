# Troubleshooting - flext-web

**Updated**: September 17, 2025 | **Version**: 0.9.0

## Primary Issue: Circular Import Error

**Problem**: Cannot import any classes from flext-web

```python
from flext_web import FlextWebServices
# ImportError: cannot import name 'FlextWebConfigs' from partially initialized module
# 'flext_web.config' (most likely due to a circular import)
# (/home/marlonsc/flext/flext-web/src/flext_web/config.py)
```

**Root Cause**: Circular dependency chain:
- `config.py` imports `FlextWebSettings` from `settings.py`
- `settings.py` imports `FlextWebConfigs` from `config.py`

**Impact**: Complete library non-functionality

## Diagnosis Steps

### Test Import Failure

```bash
# Confirm the issue exists
cd /home/marlonsc/flext/flext-web
python -c "from flext_web import FlextWebServices"
# Expected: ImportError with circular import message
```

### Analyze Dependency Chain

```bash
# Check actual imports in problematic files
grep -n "from.*settings" src/flext_web/config.py
grep -n "from.*config" src/flext_web/settings.py

# Look for the circular reference
grep -n "FlextWebConfigs" src/flext_web/settings.py
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
from flext_core import FlextContainer
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
- Any actual usage of the library

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
2. **Avoid import testing**: Cannot test actual functionality
3. **Plan refactoring**: Design solution for dependency structure
4. **Test incrementally**: Test imports after each structural change

## Getting Help

**Pattern reference**: See ../flext-core/README.md for dependency injection patterns
**Architecture guidance**: ../docs/architecture for Clean Architecture separation principles
**Issue priority**: This is the only blocking issue preventing all development