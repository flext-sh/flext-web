# flext-web - FLEXT Infrastructure

**Hierarchy**: PROJECT
**Parent**: [../CLAUDE.md](../CLAUDE.md) - Workspace standards
**Last Update**: 2025-12-07

---

## Project Overview

**FLEXT-Web** is the Flask-based web interface and REST API foundation for the FLEXT ecosystem.

**Version**: 2.1.0  
**Status**: Production-ready  
**Python**: 3.13+

**Key Architecture**:

- Flask-based web interface
- REST API foundation
- Integration with flext-core patterns
- MANDATORY flext-cli usage for CLI and output

---

## Essential Commands

```bash
# Setup and validation
make setup                    # Complete development environment setup
make validate                 # Complete validation (lint + type + security + test)
make check                    # Quick check (lint + type)

# Quality gates
make lint                     # Ruff linting
make type-check               # Pyrefly type checking
make security                 # Bandit security scan
make test                     # Run tests

# Development
make dev                      # Start Flask development server
make format                   # Auto-format code
```

---

## Key Patterns

### Flask Integration with flext-core

```python
from flext_core import FlextResult
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    """Flask route using FlextResult pattern."""
    result = fetch_data_service()
    if result.is_success:
        return jsonify(result.unwrap()), 200
    return jsonify({"error": result.error}), 400
```

### flext-cli Integration (MANDATORY)

```python
from flext_cli import FlextCli

# ALL web CLI projects use flext-cli for CLI AND output
# NO direct Click/Rich imports allowed
cli = FlextCli()
cli.print("Success!", style="green")
```

---

## Critical Development Rules

### ZERO TOLERANCE Policies

**ABSOLUTELY FORBIDDEN**:

- ❌ Direct Click/Rich imports (use flext-cli)
- ❌ Exception-based error handling in web handlers (use FlextResult)
- ❌ Type ignores or `Any` types
- ❌ Mockpatch in tests

**MANDATORY**:

- ✅ Use `FlextResult[T]` for all operations
- ✅ Use flext-cli for all CLI and output operations
- ✅ Complete type annotations
- ✅ Zero Ruff violations
- ✅ Real fixtures in tests

---

**See Also**:

- [Workspace Standards](../CLAUDE.md)
- [flext-core Patterns](../flext-core/CLAUDE.md)
- [flext-api Patterns](../flext-api/CLAUDE.md)
- [flext-auth Patterns](../flext-auth/CLAUDE.md)
