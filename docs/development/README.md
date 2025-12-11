# Development Guide - FLEXT Web Interface

**Development Environment**: Python 3.13+ • Poetry • Flask • pytest  
**Quality Standards**: PEP8 • Type Hints • 90%+ Coverage • Clean Architecture  
**Integration**: FLEXT ecosystem patterns using flext-core standardization

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+** (required for latest type hints and performance)
- **Poetry** (dependency management and packaging)
- **Git** (version control)
- **Make** (build automation)
- **Access to flext-core and flext-observability** (local path dependencies)

### Initial Setup

```bash
# Clone the repository
git clone <repository-url>
cd flext-web

# Complete project setup
make setup                    # Install tools, dependencies, pre-commit hooks

# Verify installation
make diagnose                 # Check environment and dependencies
make doctor                   # Run health check (diagnose + check)
```

### First Development Session

```bash
# Install development dependencies
make install-dev

# Run quality gates
make validate                 # Complete validation (lint + type + security + test)

# Start development server
make runserver               # Flask dev server on localhost:8080

# In another terminal, test the API
curl http://localhost:8080/health
```

## 🏗️ Project Structure

### Current Structure (Single-File Architecture)

```
flext-web/
├── src/flext_web/
│   ├── __init__.py          # All components (518 lines)
│   ├── __main__.py          # CLI entry point
│   ├── exceptions.py        # Exception hierarchy (311 lines)
│   ├── py.typed
│   └── templates/          # Django templates (unused)
├── tests/                  # Comprehensive test suite
├── docs/                   # Documentation
├── Makefile               # Development commands
├── pyproject.toml         # Project configuration
└── poetry.lock           # Locked dependencies
```

### Recommended Target Structure (Phase 1 Refactoring)

```
flext-web/
├── src/flext_web/
│   ├── domain/
│   │   ├── entities.py     # FlextWebApp, FlextWebAppStatus
│   │   ├── repositories.py # Repository interfaces
│   │   └── services.py     # Domain services
│   ├── application/
│   │   ├── handlers.py     # CQRS handlers
│   │   ├── config.py       # Configuration management
│   │   └── use_cases.py    # Application use cases
│   ├── infrastructure/
│   │   ├── web/
│   │   │   ├── routes.py   # Flask routes
│   │   │   ├── middleware.py # Auth, CORS, etc.
│   │   │   └── templates/  # Jinja2 templates
│   │   ├── persistence/
│   │   │   ├── repositories.py # Repository implementations
│   │   │   └── models.py   # Data models
│   │   └── external/
│   │       ├── flexcore.py # FlexCore integration
│   │       └── observability.py # Monitoring
│   └── interfaces/
│       ├── api/
│       │   ├── v1/         # API version 1
│       │   └── schemas.py  # API schemas
│       └── web/
│           ├── static/     # CSS, JS, images
│           └── templates/  # HTML templates
├── tests/
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   ├── e2e/              # End-to-end tests
│   └── fixtures/         # Test data
└── docs/                 # Documentation
```

## 🔧 Development Commands

### Essential Daily Commands

```bash
# Development workflow
make check                   # Quick lint + type check
make test                    # Run tests with coverage
make format                  # Auto-format code
make runserver              # Start development server

# Quality gates (run before commit)
make validate               # Complete validation pipeline
make security               # Security scanning
make pre-commit             # Run pre-commit hooks
```

### Complete Command Reference

#### Setup & Installation

```bash
make setup                  # Complete project setup with hooks
make install                # Install dependencies only
make install-dev            # Install with development dependencies
make reset                  # Reset project (clean + setup)
```

#### Quality Gates

```bash
make validate              # Complete validation (lint + type + security + test)
make check                 # Quick health check (lint + type)
make lint                  # Run ruff linting
make type-check            # Run mypy type checking with strict mode
make security              # Run bandit security scanning and pip-audit
make format                # Auto-format code with ruff
make fix                   # Auto-fix linting issues and format
```

#### Testing

```bash
make test                  # Run all tests with coverage
make test-unit             # Run unit tests only
make test-integration      # Run integration tests only
make test-web              # Run web interface tests
make test-api              # Run API tests
make test-fast             # Run tests without coverage
make coverage-html         # Generate HTML coverage report
```

#### Web Development

```bash
make runserver            # Start Flask development server (localhost:8080)
make serve
make dev-server           # Start dev server with hot reload
make prod-server          # Start production server
make web-test             # Test web service creation
```

#### Build & Distribution

```bash
make build                # Build distribution packages
make build-clean          # Clean and build
make build-docker         # Build Docker image
make clean                # Clean build artifacts
make clean-all            # Deep clean including venv
```

#### Dependencies & Maintenance

```bash
make deps-update          # Update dependencies
make deps-show            # Show dependency tree
make deps-audit           # Security audit of dependencies
make shell                # Open Python shell
make diagnose            # Project diagnostics
make doctor              # Health check (diagnose + check)
```

### Aliases for Speed

```bash
# Short aliases for frequent commands
make t                    # test
make l                    # lint
make f                    # format
make tc
make c                    # clean
make i                    # install
make v                    # validate
make r                    # runserver
make s                    # serve
```

## 🧪 Testing Strategy

### Test Structure

```
tests/
├── conftest.py                      # Pytest configuration (358 lines)
├── test_config_comprehensive.py    # Configuration validation tests
├── test_domain_entities.py         # Entity and business logic tests
├── test_main_entry.py              # CLI entry point tests
├── test_simple_api_fixed.py        # API endpoint tests
├── test_simple_web_fixed.py        # Web interface tests
├── unit/                           # Unit tests
├── integration/                    # Integration tests
├── e2e/                           # End-to-end tests
└── fixtures/                      # Test fixtures
```

### Running Tests

```bash
# All tests with coverage
make test

# Specific test categories
pytest -m unit                      # Unit tests only
pytest -m integration               # Integration tests only
pytest -m "not slow"                # Fast tests for quick feedback

# Specific test files
pytest tests/test_simple_api_fixed.py -v
pytest tests/test_domain_entities.py::TestFlextWebApp::test_start_app

# Debug mode
pytest tests/test_name.py::test_function --pdb
```

### Test Configuration

```python
# pytest.ini_options in pyproject.toml
[tool.pytest.ini_options]
minversion = "8.0"
mode = "auto"
addopts = ["-ra", "--strict-markers", "--maxfail=1"]
testpaths = ["tests"]
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow tests",
    "e2e: End-to-end tests"
]
```

### Coverage Requirements

- **Minimum Coverage**: 90% (enforced by `make test`)
- **Coverage Report**: `make coverage-html` generates HTML report
- **Coverage Configuration**: Excludes tests, pycache, venv directories

## 🎨 Code Style & Quality

### Linting Configuration (Ruff)

```toml
# pyproject.toml - Ruff configuration
extend = "../.ruff-shared.toml"
lint.isort.known-first-party = ["flext_web"]
```

### Type Checking (MyPy)

```toml
# pyproject.toml - MyPy strict configuration
[tool.mypy]
strict = true
python_version = "3.13"
plugins = ["pydantic.mypy"]

# Strict checks beyond default
disallow_any_decorated = false
disallow_any_explicit = true
disallow_any_generics = true
warn_return_any = true
warn_unused_ignores = false
```

### Code Formatting

```bash
# Auto-format code
make format                  # Formats all code with ruff

# Manual formatting
poetry run ruff format src tests
poetry run ruff check src tests --fix
```

### Quality Metrics

- **Type Coverage**: 95% target with MyPy strict mode
- **Test Coverage**: 90%+ required for all new code
- **Complexity**: Monitored with radon (available in dev dependencies)
- **Security**: Bandit scanning + pip-audit for vulnerabilities

## 🔌 Development Environment

### Environment Variables

```bash
# Development configuration
export FLEXT_WEB_HOST=localhost
export FLEXT_WEB_PORT=8080
export FLEXT_WEB_DEBUG=true
export FLEXT_WEB_SECRET_KEY=development-secret-key-32-chars

# flext-core integration
export FLEXT_LOG_LEVEL=DEBUG
export FLEXT_ENVIRONMENT=development

# Future integration variables
export FLEXT_WEB_FLEXCORE_URL=http://localhost:8080
export FLEXT_WEB_FLEXT_SERVICE_URL=http://localhost:8081
```

### IDE Configuration

#### VS Code Settings

```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "mypy.dmypyExecutable": ".venv/bin/mypy"
}
```

#### PyCharm Configuration

- **Interpreter**: Use Poetry environment
- **Code Style**: Follow PEP8 with 88 character line length
- **Inspections**: Enable type checking and PEP8 compliance
- **Test Runner**: pytest with coverage

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml (automatically setup by make setup)
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.12.3
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        args: [--strict]
```

## 🏗️ Architecture Development

### Clean Architecture Layers

#### Domain Layer Development

```python
# src/flext_web/domain/entities.py (target)
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

class FlextWebApp(FlextModels.Entity):
    """Domain entity with business rules"""

    def start(self) -> FlextResult['FlextWebApp']:
        """Business logic for starting application"""
        if self.status == FlextWebAppStatus.RUNNING:
            return FlextResult[None].fail("Application already running")
        # Business validation here
        return FlextResult[None].ok(self.model_copy(update={"status": FlextWebAppStatus.RUNNING}))
```

#### Application Layer Development

```python
# src/flext_web/application/handlers.py (target)
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

class FlextWebAppHandler(FlextProcessors.Handler):
    """CQRS command handlers"""

    def __init__(self, repository: FlextWebAppRepository):
        self.repository = repository

    def create_app(self, command: CreateAppCommand) -> FlextResult[FlextWebApp]:
        """Handle create app command"""
        app = FlextWebApp(
            id=f"app_{command.name}",
            name=command.name,
            port=command.port,
            host=command.host
        )

        validation = app.validate_domain_rules()
        if not validation.success:
            return validation

        return self.repository.save(app)
```

#### Infrastructure Layer Development

```python
# src/flext_web/infrastructure/web/routes.py (target)
from flask import Blueprint, request, jsonify
from ...application.handlers import FlextWebAppHandler

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

@api_v1.route('/apps', methods=['POST'])
def create_app():
    """Create application endpoint"""
    data = request.get_json()
    command = CreateAppCommand(
        name=data.get('name'),
        port=data.get('port', 8000),
        host=data.get('host', 'localhost')
    )

    result = app_handler.create_app(command)

    if result.success:
        return jsonify({
            "success": True,
            "message": "Application created successfully",
            "data": result.data.dict()
        })

    return jsonify({
        "success": False,
        "message": f"Failed: {result.error}"
    }), 400
```

### FLEXT Core Integration

```python
# Using flext-core patterns
from flext_core import (
    FlextResult,      # Railway-oriented programming
    FlextModels.Entity,      # Domain entity base class
    FlextSettings,      # Configuration management
    FlextProcessors,    # CQRS handlers
    FlextLogger        # Structured logging
)

# Example: Error handling with FlextResult
def create_application(name: str, port: int) -> FlextResult[FlextWebApp]:
    """Create application with proper error handling"""
    try:
        # Validation
        if not name:
            return FlextResult[None].fail("Application name is required")

        if not (1 <= port <= 65535):
            return FlextResult[None].fail("Port must be between 1 and 65535")

        # Create entity
        app = FlextWebApp(id=f"app_{name}", name=name, port=port)

        # Domain validation
        validation = app.validate_domain_rules()
        if not validation.success:
            return validation

        # Success
        return FlextResult[None].ok(app)

    except Exception as e:
        return FlextResult[None].fail(f"Unexpected error: {e}")
```

## 🔍 Debugging

### Flask Development Server

```bash
# Debug mode with auto-reload
make dev-server

# Or with environment variable
FLASK_ENV=development python -m flext_web --debug

# With custom host/port
python -m flext_web --host 0.0.0.0 --port 8080 --debug
```

### Testing Debug

```bash
# Debug failing tests
pytest tests/test_name.py::test_function --pdb

# Verbose output
pytest tests/test_name.py -v -s

# With coverage and debugging
pytest tests/test_name.py --cov=src --pdb
```

### Logging Configuration

```python
# Current logging (via flext-core)
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

logger = FlextLogger(__name__)

# Usage in code
logger.info("Application created", extra={"app_id": app.id})
logger.error("Validation failed", extra={"errors": validation.error})
```

## 🚨 Common Issues & Solutions

### Dependency Issues

```bash
# Poetry lock issues
poetry lock --no-update

# Clean install
rm -rf .venv poetry.lock
make setup

# Dependency conflicts
poetry show --tree
poetry deps-audit
```

### Test Issues

```bash
# Pytest collection issues
pytest --collect-only

# Coverage issues
pytest --cov=src --cov-report=html
# Check reports/coverage/index.html

# Fixture issues
pytest tests/test_name.py -v --fixtures
```

### Type Checking Issues

```bash
# MyPy errors
poetry run mypy src --show-error-codes

# Ignore specific errors (temporary)
# Add "

# Update type stubs
poetry add --group dev types-requests types-flask
```

### Development Server Issues

```bash
# Port already in use
netstat -tulpn | grep 8080
kill -9 <PID>

# Configuration issues
python -c "from flext_web import get_web_settings; print(get_web_settings())"

# Flask app factory issues
python -c "from flext_web import create_app; app = create_app(); print(app)"
```

## 📋 Development Checklist

### Before Starting Development

- [ ] Run `make setup` for complete environment setup
- [ ] Run `make diagnose` to verify environment
- [ ] Configure IDE with Python interpreter from `.venv/`
- [ ] Test API with `curl http://localhost:8080/health`

### Before Committing Changes

- [ ] Run `make validate` (lint + type + security + test)
- [ ] Check test coverage with `make coverage-html`
- [ ] Review changed files for code quality
- [ ] Update documentation if API changes
- [ ] Verify pre-commit hooks pass

### Before Creating PR

- [ ] All quality gates pass
- [ ] New features have tests
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (if applicable)
- [ ] No secrets or sensitive data in commits

## 🔄 Development Workflow

### Feature Development

1. **Create feature branch**: `git checkout -b feature/amazing-feature`
2. **Develop incrementally**: Small commits, frequent testing
3. **Run quality gates**: `make validate` before each commit
4. **Update documentation**: Keep docs in sync with code
5. **Create PR**: Follow PR template and guidelines

### Bug Fixes

1. **Reproduce issue**: Create failing test first
2. **Fix implementation**: Minimal change to fix issue
3. **Verify fix**: Ensure test passes and no regressions
4. **Document**: Update relevant documentation

### Refactoring

1. **Ensure test coverage**: Add tests before refactoring
2. **Refactor incrementally**: Small, focused changes
3. **Validate continuously**: Run tests after each change
4. **Update architecture docs**: Keep design docs current

---

**Development Standards**: Clean Architecture • DDD • FLEXT ecosystem patterns  
**Quality Gates**: 90%+ coverage • Strict typing • Comprehensive linting  
**Next Review**: After monolithic architecture refactoring
