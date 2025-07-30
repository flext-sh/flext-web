# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**flext-web** is a modern Flask-based web interface for the FLEXT platform, implementing Clean Architecture patterns with flext-core standardization. The project provides both web UI and REST API endpoints for managing applications and services within the FLEXT ecosystem.

## Architecture

The project follows **Clean Architecture** with **Domain-Driven Design (DDD)** patterns, using the flext-core library for standardized patterns:

- **Domain Models**: `FlextWebApp` entity with status management and business rules
- **Configuration**: `FlextWebConfig` with environment-based settings and validation
- **Handlers**: `FlextWebAppHandler` for application lifecycle management
- **Web Service**: `FlextWebService` providing Flask integration with REST API
- **Error Handling**: Comprehensive exception hierarchy inheriting from flext-core

### Key Components

- **Flask Web Service** (`FlextWebService`): Main service class with route registration
- **Application Entity** (`FlextWebApp`): Domain model with start/stop lifecycle
- **Configuration Management** (`FlextWebConfig`): Type-safe configuration with validation
- **Exception Hierarchy**: Domain-specific exceptions extending flext-core patterns

## Development Commands

### Setup & Installation

```bash
make setup                   # Complete project setup with dependencies and hooks
make install                 # Install project dependencies only
make install-dev             # Install with development dependencies
```

### Quality Gates (run before committing)

```bash
make validate               # Complete validation (lint + type + security + test)
make check                  # Quick health check (lint + type)
make lint                   # Run ruff linting
make type-check             # Run mypy type checking with strict mode
make security               # Run bandit security scanning and pip-audit
make pep8-check             # Verify PEP8 compliance
make format                 # Auto-format code with ruff
make fix                    # Auto-fix linting issues and format
```

### Testing

```bash
make test                   # Run all tests with coverage
make test-unit              # Run unit tests only
make test-integration       # Run integration tests only
make coverage               # Generate HTML coverage report
```

### Web Development

```bash
make runserver              # Start Flask development server (localhost:8080)
make serve                  # Alias for runserver
make runserver-prod         # Start with production settings
```

### Individual Test Files

```bash
# Run specific test categories
pytest -m unit              # Unit tests only
pytest -m integration       # Integration tests only
pytest -m slow              # Slow tests only
pytest -m "not slow"        # Fast tests for quick feedback

# Run specific test files
pytest tests/test_config_comprehensive.py
pytest tests/test_domain_entities.py
pytest tests/test_simple_api_fixed.py
```

### Build & Distribution

```bash
make build                  # Build distribution packages
make build-docker           # Build Docker image
make clean                  # Clean build artifacts
make deps-update            # Update dependencies
make deps-audit             # Security audit of dependencies
```

## Configuration

The service uses environment-based configuration with the `FLEXT_WEB_` prefix:

```bash
FLEXT_WEB_HOST=localhost          # Server host (default: localhost)
FLEXT_WEB_PORT=8080              # Server port (default: 8080)
FLEXT_WEB_DEBUG=true             # Debug mode (default: true)
FLEXT_WEB_SECRET_KEY=your-key    # Cryptographic secret key
```

## Entry Points

### CLI Execution

```bash
# Direct module execution
python -m flext_web --host 0.0.0.0 --port 8080 --debug

# Using poetry
poetry run python -m flext_web --help

# Command options
--host HOST        # Override host address
--port PORT        # Override port number
--debug           # Enable debug mode
--no-debug        # Disable debug mode
```

### Programmatic Usage

```python
from flext_web import create_service, get_web_settings

# Create service with default config
service = create_service()
service.run()

# Create with custom configuration
config = get_web_settings()
config.port = 9000
service = create_service(config)
service.run(host="0.0.0.0", port=9000)
```

## API Endpoints

### Health & Management

- `GET /health` - Service health check
- `GET /` - Web dashboard

### Application Management

- `GET /api/v1/apps` - List all applications
- `POST /api/v1/apps` - Create new application
- `GET /api/v1/apps/<id>` - Get application details
- `POST /api/v1/apps/<id>/start` - Start application
- `POST /api/v1/apps/<id>/stop` - Stop application

### API Request Examples

```bash
# Create application
curl -X POST http://localhost:8080/api/v1/apps \
  -H "Content-Type: application/json" \
  -d '{"name": "test-app", "port": 3000, "host": "localhost"}'

# Start application
curl -X POST http://localhost:8080/api/v1/apps/app_test-app/start

# Check health
curl http://localhost:8080/health
```

## Project Structure

```
src/flext_web/
├── __init__.py          # Main library with service, entities, handlers
├── __main__.py          # CLI entry point with argument parsing
└── exceptions.py        # Domain-specific exception hierarchy

tests/
├── test_config_comprehensive.py    # Configuration validation tests
├── test_domain_entities.py         # Entity and business logic tests
├── test_main_entry.py              # CLI entry point tests
├── test_simple_api_fixed.py        # API endpoint tests
└── test_simple_web_fixed.py        # Web interface tests
```

## Dependencies

### Core Dependencies

- **flext-core**: Foundation library for standardized patterns
- **flext-observability**: Monitoring and observability
- **Flask**: Web framework for HTTP services
- **Pydantic**: Type validation and settings management

### Quality Tools

- **ruff**: Linting and code formatting
- **mypy**: Static type checking with strict mode
- **pytest**: Testing framework with coverage
- **bandit**: Security vulnerability scanning

## Testing Strategy

### Test Categories

- **Unit Tests**: Entity validation, handler logic, configuration
- **Integration Tests**: Service endpoints, Flask app integration
- **API Tests**: HTTP request/response validation
- **Configuration Tests**: Settings validation and environment handling

### Quality Standards

- **Coverage**: Minimum 90% test coverage required
- **Type Safety**: Strict mypy configuration with no untyped code
- **Security**: Bandit scanning and pip-audit for vulnerabilities
- **Code Quality**: Ruff with comprehensive rule set (ALL rules enabled)

## Common Development Workflows

### Adding New API Endpoints

1. Add route to `FlextWebService._register_routes()`
2. Implement handler method following naming pattern
3. Use `_create_response()` for consistent JSON responses
4. Add comprehensive tests in `tests/test_simple_api_fixed.py`
5. Run `make validate` to ensure quality gates pass

### Extending Domain Models

1. Add new entities inheriting from `FlextEntity`
2. Implement `validate_domain_rules()` method
3. Create corresponding handler class
4. Add unit tests for business logic validation
5. Update API endpoints to support new entity

### Configuration Changes

1. Update `FlextWebConfig` class with new fields
2. Add validation in `validate_config()` method
3. Update environment variable documentation
4. Add configuration tests with edge cases
5. Test both development and production scenarios

## Troubleshooting

### Service Won't Start

```bash
# Check port availability
netstat -tulpn | grep 8080

# Verify configuration
python -c "from flext_web import get_web_settings; print(get_web_settings())"

# Check dependencies
poetry show --tree
```

### Test Failures

```bash
# Run with verbose output
pytest tests/failing_test.py -v -s

# Check coverage issues
pytest --cov=src --cov-report=html

# Debug specific test
pytest tests/test_name.py::test_function --pdb
```

### Quality Gate Issues

```bash
# Fix formatting automatically
make format

# Check specific mypy errors
poetry run mypy src --show-error-codes

# Security audit
poetry run pip-audit
```

## TODO: GAPS DE ARQUITETURA IDENTIFICADOS - PRIORIDADE ALTA

### 🚨 GAP 1: Frontend Technology Gap

**Status**: ALTO - Web interface sem especificação de frontend technology
**Problema**:

- Flask mencionado mas frontend technology não especificada
- Dashboard mencionado (`GET /`) mas sem detalhes de implementação
- Não especifica se é SPA, server-side rendering, ou hybrid

**TODO**:

- [ ] Especificar frontend technology stack (React, Vue, vanilla JS, Jinja2)
- [ ] Documentar web dashboard architecture e components
- [ ] Definir API-first vs server-side rendering strategy
- [ ] Criar frontend development workflow

### 🚨 GAP 2: Autenticação e Autorização Missing

**Status**: ALTO - Web interface sem security integration
**Problema**:

- Endpoints API não protegidos por autenticação
- Não integra com flext-auth para security
- Session management não especificado

**TODO**:

- [ ] Integrar com flext-auth para authentication/authorization
- [ ] Implementar API security middleware
- [ ] Documentar user session management
- [ ] Criar role-based access control para web interface

### 🚨 GAP 3: Real-time Communication Gap

**Status**: ALTO - Falta real-time updates para web interface
**Problema**:

- Application status changes não refletidos em real-time
- Polling-based updates não implementado
- WebSocket ou SSE não especificado

**TODO**:

- [ ] Implementar WebSocket ou Server-Sent Events
- [ ] Criar real-time status updates para applications
- [ ] Documentar pub/sub patterns para web updates
- [ ] Integrar com flext-observability para live metrics

### 🚨 GAP 4: Integration com Ecosystem Services

**Status**: ALTO - Web interface não integrada com outros services
**Problema**:

- Não integra com FlexCore (Go) ou FLEXT Service
- API management isolado em vez de proxy para ecosystem
- Monitoring dashboard não conectado com flext-observability

**TODO**:

- [ ] Criar proxy patterns para ecosystem APIs
- [ ] Integrar monitoring dashboard com flext-observability
- [ ] Implementar service discovery integration
- [ ] Documentar cross-service communication patterns
