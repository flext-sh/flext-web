# Configuration Guide - FLEXT Web Interface


<!-- TOC START -->
- [🔧 Configuration Overview](#-configuration-overview)
  - [Configuration Architecture](#configuration-architecture)
  - [Key Features](#key-features)
- [🌍 Environment Variables](#-environment-variables)
  - [Server Configuration](#server-configuration)
  - [Security Configuration](#security-configuration)
  - [Integration Configuration (Planned)](#integration-configuration-planned)
  - [FLEXT Core Integration](#flext-core-integration)
- [📝 Configuration Examples](#-configuration-examples)
  - [Development Environment](#development-environment)
  - [Testing Environment](#testing-environment)
  - [Production Environment](#production-environment)
- [⚙️ Configuration Management](#-configuration-management)
  - [Configuration Class](#configuration-class)
  - [Configuration Usage](#configuration-usage)
  - [Configuration Validation](#configuration-validation)
- [🔒 Security Configuration](#-security-configuration)
  - [Secret Key Management](#secret-key-management)
  - [Security Validation Rules](#security-validation-rules)
- [🏗️ Environment-Specific Configuration](#-environment-specific-configuration)
  - [Development Setup](#development-setup)
  - [Testing Configuration](#testing-configuration)
  - [Production Deployment](#production-deployment)
- [🔍 Configuration Debugging](#-configuration-debugging)
  - [Configuration Inspection](#configuration-inspection)
  - [Environment Variable Debug](#environment-variable-debug)
  - [Configuration Validation Debug](#configuration-validation-debug)
- [📋 Configuration Checklist](#-configuration-checklist)
  - [Development Environment](#development-environment)
  - [Testing Environment](#testing-environment)
  - [Production Environment](#production-environment)
  - [Security Checklist](#security-checklist)
- [🚨 Common Configuration Issues](#-common-configuration-issues)
  - [Issue: Service Won't Start](#issue-service-wont-start)
  - [Issue: Secret Key Validation Failed](#issue-secret-key-validation-failed)
  - [Issue: Configuration Not Loading](#issue-configuration-not-loading)
- [🔄 Configuration Updates](#-configuration-updates)
  - [Development Configuration Changes](#development-configuration-changes)
  - [Production Configuration Updates](#production-configuration-updates)
<!-- TOC END -->

**Configuration System**: Pydantic Settings • Environment Variables • flext-core Integration  
**Validation**: Strict validation with business rules and security checks  
**Environment Support**: Development • Testing • Production with appropriate defaults  
**Documentation Status**: ✅ **Complete** - Configuration patterns with validation

## 🔧 Configuration Overview

FLEXT Web Interface uses **Pydantic Settings** with **flext-core configuration patterns** for type-safe, validated configuration management. All settings support environment variable overrides and have appropriate defaults for different environments.

**Enterprise Configuration Features**:

- Comprehensive business rule validation with detailed error messages
- Production safety checks and security validation
- Environment-specific behavior and deployment scenarios
- Integration with flext-core singleton patterns
- Type-safe configuration with 95%+ annotation coverage

### Configuration Architecture

```python
# Configuration hierarchy
FlextWebSettings(BaseSettings, FlextSettings)
├── Server Settings (host, port, debug)
├── Security Settings (secret_key, cors)
├── Integration Settings (flexcore_url, flext_service_url)
├── Logging Settings (via flext-core)
└── Validation Rules (business logic + security)
```

### Key Features

- **Type Safety**: Full Pydantic validation with Python 3.13 type hints
- **Environment Integration**: Automatic environment variable loading
- **Validation**: Business rules and security validation on startup
- **FLEXT Patterns**: Integration with flext-core configuration standards
- **Hot Reload**: Development mode configuration changes without restart

## 🌍 Environment Variables

### Server Configuration

| Variable             | Type   | Default     | Description                               |
| -------------------- | ------ | ----------- | ----------------------------------------- |
| `FLEXT_WEB_HOST`     | `str`  | `localhost` | Server bind address                       |
| `FLEXT_WEB_PORT`     | `int`  | `8080`      | Server listen port                        |
| `FLEXT_WEB_DEBUG`    | `bool` | `true`      | Debug mode (auto-reload, detailed errors) |
| `FLEXT_WEB_APP_NAME` | `str`  | `FLEXT Web` | Application display name                  |
| `FLEXT_WEB_VERSION`  | `str`  | `0.9.9`     | Application version                       |

### Security Configuration

| Variable               | Type  | Default                  | Description                     |
| ---------------------- | ----- | ------------------------ | ------------------------------- |
| `FLEXT_WEB_SECRET_KEY` | `str` | `change-in-production-*` | Flask secret key (min 32 chars) |

### Integration Configuration (Planned)

| Variable                      | Type   | Default                 | Description                            |
| ----------------------------- | ------ | ----------------------- | -------------------------------------- |
| `FLEXT_WEB_FLEXCORE_URL`      | `str`  | `http://localhost:8080` | FlexCore service URL                   |
| `FLEXT_WEB_FLEXT_SERVICE_URL` | `str`  | `http://localhost:8081` | FLEXT Service URL                      |
| `FLEXT_WEB_AUTH_ENABLED`      | `bool` | `false`                 | Enable authentication                  |
| `FLEXT_WEB_CORS_ORIGINS`      | `str`  | `*`                     | CORS allowed origins (comma-separated) |

### FLEXT Core Integration

| Variable             | Type  | Default       | Description                                 |
| -------------------- | ----- | ------------- | ------------------------------------------- |
| `FLEXT_LOG_LEVEL`    | `str` | `INFO`        | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `FLEXT_ENVIRONMENT`  | `str` | `development` | Environment name                            |
| `FLEXT_SERVICE_NAME` | `str` | `flext-web`   | Service identifier                          |

## 📝 Configuration Examples

### Development Environment

```bash
# .env.development
FLEXT_WEB_HOST=localhost
FLEXT_WEB_PORT=8080
FLEXT_WEB_DEBUG=true
FLEXT_WEB_SECRET_KEY=development-secret-key-32-characters-long
FLEXT_LOG_LEVEL=DEBUG
FLEXT_ENVIRONMENT=development
```

### Testing Environment

```bash
# .env.testing
FLEXT_WEB_HOST=localhost
FLEXT_WEB_PORT=8081
FLEXT_WEB_DEBUG=false
FLEXT_WEB_SECRET_KEY=testing-secret-key-32-characters-long-test
FLEXT_LOG_LEVEL=WARNING
FLEXT_ENVIRONMENT=testing
```

### Production Environment

```bash
# .env.production
FLEXT_WEB_HOST=0.0.0.0
FLEXT_WEB_PORT=8080
FLEXT_WEB_DEBUG=false
FLEXT_WEB_SECRET_KEY=${PRODUCTION_SECRET_KEY}  # From secure storage
FLEXT_WEB_FLEXCORE_URL=https://internal.invalid/REDACTED:8080
FLEXT_WEB_FLEXT_SERVICE_URL=https://internal.invalid/REDACTED:8081
FLEXT_LOG_LEVEL=INFO
FLEXT_ENVIRONMENT=production
```

## ⚙️ Configuration Management

### Configuration Class

```python
from pydantic_settings import BaseSettings
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
from pydantic import Field

class FlextWebSettings(BaseSettings, FlextSettings):
    """Web configuration using flext-core patterns"""

    model_config = {
        "env_prefix": "FLEXT_WEB_",
        "case_sensitive": False,
        "validate_assignment": True,
    }

    # Server settings
    app_name: str = Field(default="FLEXT Web", description="Application name")
    version: str = Field(default="0.9.9", description="Application version")
    debug: bool = Field(default=True, description="Debug mode")
    host: str = Field(default="localhost", description="Server host")
    port: int = Field(default=8080, ge=1, le=65535, description="Server port")

    # Security settings
    secret_key: str = Field(
        default="change-in-production-" + "x" * 32,
        min_length=32,
        description="Secret key for cryptographic operations"
    )

    def validate_config(self) -> FlextResult[bool]:
        """Validate configuration"""
        # Implementation includes business rules and security validation
        if not self.debug and "change-in-production" in self.secret_key:
            return FlextResult[bool].fail("Secret key must be changed")
        return FlextResult[bool].| ok(value=True)

    def get_server_url(self) -> str:
        """Get complete server URL"""
        return f"http://{self.host}:{self.port}"
```

### Configuration Usage

```python
from flext_web import get_web_settings, reset_web_settings

# Get configuration (singleton pattern)
config = get_web_settings()
print(f"Server URL: {config.get_server_url()}")

# Reset configuration (useful for testing)
reset_web_settings()

# Create service with custom configuration
from flext_web import create_service
custom_config = FlextWebSettings(port=9000, debug=False)
service = create_service(custom_config)
```

### Configuration Validation

```python
# Automatic validation on startup
try:
    config = get_web_settings()
    print("Configuration valid")
except ValueError as e:
    print(f"Configuration error: {e}")

# Manual validation
config = FlextWebSettings()
validation_result = config.validate_config()
if not validation_result.success:
    print(f"Validation failed: {validation_result.error}")
```

## 🔒 Security Configuration

### Secret Key Management

#### Development

```bash
# Generate secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Set in environment
export FLEXT_WEB_SECRET_KEY="your-generated-secret-key-here"
```

#### Production

```bash
# Using Kubernetes secrets
kubectl create secret generic flext-web-secrets \
  --from-literal=secret-key="$(openssl rand -base64 32)"

# Using Docker secrets
echo "$(openssl rand -base64 32)" | docker secret create flext_web_secret_key -

# Using AWS Systems Manager Parameter Store
aws ssm put-parameter \
  --name "/flext/web/secret-key" \
  --value "$(openssl rand -base64 32)" \
  --type "SecureString"
```

### Security Validation Rules

The configuration includes several security validation rules:

```python
def validate_config(self) -> FlextResult[bool]:
    """Security validation rules"""

    # Production secret key validation
    if not self.debug and "change-in-production" in self.secret_key:
        return FlextResult[bool].fail("Secret key must be changed in production")

    # Secret key length validation
    if len(self.secret_key) < 32:
        return FlextResult[bool].fail("Secret key must be at least 32 characters")

    # Port range validation
    if not (1 <= self.port <= 65535):
        return FlextResult[bool].fail("Port must be between 1 and 65535")

    # Host validation for production
    if not self.debug and self.host == "0.0.0.0":
        # Log warning for production binding to all interfaces
        logger.warning("Production service binding to all interfaces")

    return FlextResult[bool].| ok(value=True)
```

## 🏗️ Environment-Specific Configuration

### Development Setup

```bash
# Create development environment file
cat > .env.development << EOF
FLEXT_WEB_HOST=localhost
FLEXT_WEB_PORT=8080
FLEXT_WEB_DEBUG=true
FLEXT_WEB_SECRET_KEY=dev-secret-key-32-characters-long-dev
FLEXT_LOG_LEVEL=DEBUG
FLEXT_ENVIRONMENT=development
EOF

# Load and start
set -a; source .env.development; set +a
python -m flext_web
```

### Testing Configuration

```python
# tests/conftest.py
import os
import pytest
from flext_web import reset_web_settings

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment configuration"""
    os.environ["FLEXT_WEB_DEBUG"] = "true"
    os.environ["FLEXT_WEB_PORT"] = "8081"
    os.environ["FLEXT_WEB_SECRET_KEY"] = "test-secret-key-32-characters-long-test"
    os.environ["FLEXT_ENVIRONMENT"] = "testing"

    yield

    # Cleanup
    os.environ.pop("FLEXT_WEB_DEBUG", None)
    os.environ.pop("FLEXT_WEB_PORT", None)
    os.environ.pop("FLEXT_WEB_SECRET_KEY", None)
    reset_web_settings()
```

### Production Deployment

```yaml
# docker-compose.prod.yml
version: "3.8"
services:
  flext-web:
    image: flext-web:latest
    environment:
      - FLEXT_WEB_HOST=0.0.0.0
      - FLEXT_WEB_PORT=8080
      - FLEXT_WEB_DEBUG=false
      - FLEXT_WEB_SECRET_KEY_FILE=/run/secrets/secret_key
      - FLEXT_ENVIRONMENT=production
      - FLEXT_LOG_LEVEL=INFO
    secrets:
      - secret_key
    ports:
      - "8080:8080"

secrets:
  secret_key:
    external: true
```

## 🔍 Configuration Debugging

### Configuration Inspection

```python
# View current configuration
from flext_web import get_web_settings

config = get_web_settings()
print(f"App Name: {config.app_name}")
print(f"Server URL: {config.get_server_url()}")
print(f"Debug Mode: {config.debug}")

# View all settings (excluding secrets)
config_dict = config.dict()
config_dict.pop('secret_key', None)  # Remove secret from output
print(config_dict)
```

### Environment Variable Debug

```bash
# Check current environment variables
env | grep FLEXT_WEB_

# Test configuration loading
python -c "
from flext_web import get_web_settings
config = get_web_settings()
print(f'Host: {config.host}')
print(f'Port: {config.port}')
print(f'Debug: {config.debug}')
"
```

### Configuration Validation Debug

```bash
# Test configuration validation
python -c "
from flext_web.settings import FlextWebSettings
import os

# Test with invalid configuration
os.environ['FLEXT_WEB_SECRET_KEY'] = 'short'
os.environ['FLEXT_WEB_DEBUG'] = 'false'

try:
    config = FlextWebSettings()
    result = config.validate_config()
    if not result.success:
        print(f'Validation error: {result.error}')
except Exception as e:
    print(f'Configuration error: {e}')
"
```

## 📋 Configuration Checklist

### Development Environment

- [ ] Set `FLEXT_WEB_DEBUG=true` for development features
- [ ] Use `localhost` for host to prevent external access
- [ ] Set a development secret key (not production key)
- [ ] Enable debug logging with `FLEXT_LOG_LEVEL=DEBUG`

### Testing Environment

- [ ] Set `FLEXT_WEB_DEBUG=false` to test production-like behavior
- [ ] Use different port to avoid conflicts
- [ ] Set test-specific secret key
- [ ] Reduce logging noise with `FLEXT_LOG_LEVEL=WARNING`

### Production Environment

- [ ] **CRITICAL**: Set secure `FLEXT_WEB_SECRET_KEY` (never use default)
- [ ] Set `FLEXT_WEB_DEBUG=false` to disable debug features
- [ ] Configure appropriate host binding (`0.0.0.0` for containers)
- [ ] Set production logging level (`INFO` or `WARNING`)
- [ ] Configure integration URLs for FlexCore and FLEXT Service
- [ ] Enable security features (CORS, authentication when available)

### Security Checklist

- [ ] Secret key is at least 32 characters long
- [ ] Secret key is cryptographically secure (not predictable)
- [ ] Secret key is stored securely (secrets management system)
- [ ] Debug mode is disabled in production
- [ ] Environment variables don't contain sensitive defaults
- [ ] Configuration validation passes before service start

## 🚨 Common Configuration Issues

### Issue: Service Won't Start

```bash
# Check configuration validation
python -c "from flext_web import get_web_settings; get_web_settings()"

# Check port availability
netstat -tulpn | grep 8080

# Check environment variables
env | grep FLEXT_WEB_ | sort
```

### Issue: Secret Key Validation Failed

```bash
# Generate new secret key
python -c "import secrets; print('FLEXT_WEB_SECRET_KEY=' + secrets.token_urlsafe(32))"

# Check current secret key length
python -c "import os; key=os.getenv('FLEXT_WEB_SECRET_KEY', ''); print(f'Length: {len(key)}')"
```

### Issue: Configuration Not Loading

```bash
# Check environment variable prefix
env | grep FLEXT_WEB_

# Test direct configuration
python -c "
from flext_web.settings import FlextWebSettings
config = FlextWebSettings(host='test', port=9999)
print(f'Host: {config.host}, Port: {config.port}')
"
```

## 🔄 Configuration Updates

### Development Configuration Changes

```bash
# Update environment variables
export FLEXT_WEB_PORT=9000
export FLEXT_WEB_DEBUG=false

# Restart service to pick up changes
make runserver
```

### Production Configuration Updates

```bash
# Rolling update with new configuration
docker service update \
  --env-add FLEXT_WEB_SECRET_KEY="new-secret-key" \
  flext-web

# Kubernetes configuration update
kubectl set env deployment/flext-web \
  FLEXT_WEB_SECRET_KEY="new-secret-key"
```

---

**Configuration Standard**: Pydantic Settings + FLEXT patterns  
**Security**: Validated secrets management and production safety  
**Next Review**: After authentication system integration
