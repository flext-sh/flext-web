# FLEXT-Web

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**FLEXT-Web** provides the web application layer for the FLEXT ecosystem, offering a unified interface for building web dashboards and REST APIs. It integrates seamlessly with `flext-auth` for security and `flext-api` for backend communication, providing a robust foundation for enterprise web interfaces.

**Reviewed**: 2026-02-17 | **Version**: 0.10.0-dev

Part of the [FLEXT](https://github.com/flext/flext) ecosystem.

## 🚀 Key Features

- **Unified Web Interface**: abstract both Flask and FastAPI patterns into a cohesive web application model.
- **FastAPI Application Factory**: Production-ready FastAPI application creation with built-in middleware configuration and health checks.
- **Integrated Authentication**: Seamless integration with `flext-auth` for JWT handling, OAuth2 flows, and session management.
- **Backend Communication**: Built-in support for `flext-api` clients to communicate with downstream services.
- **CQRS Pattern**: Implements Command Query Responsibility Segregation for clean separation of read and write operations.
- **Railway-Oriented**: All web operations return `FlextResult[T]`, ensuring consistent error handling and response formatting.

## 📦 Installation

To install `flext-web`:

```bash
pip install flext-web
```

Or with Poetry:

```bash
poetry add flext-web
```

## 🛠️ Usage

### Creating a FastAPI Application

Use the factory pattern to create production-ready FastAPI applications.

```python
from flext_web import create_fastapi_app, FlextWebModels

# 1. Configure the Application
config = FlextWebModels.AppConfig(
    title="My Enterprise Service",
    version="1.0.0",
    description="A robust microservice built with FLEXT",
    debug=True
)

# 2. Create the App
# Returns a configured FastAPI instance ready for Uvicorn
result = create_fastapi_app(config)

if result.is_success:
    app = result.unwrap()
    
    # 3. Add Routes
    @app.get("/")
    def read_root():
        return {"status": "online"}
else:
    print(f"Failed to create app: {result.error}")
```

### Flask Web Service with Auth Integration

Initialize a Flask-based web service with automatic authentication handling.

```python
from flext_web import FlextWebServices

# 1. Configuration
config = {
    "secret_key": "your-secure-secret-key",
    "api_base_url": "http://backend-api:8000",
    "session_cookie_secure": True
}

# 2. Initialize Service
# Automatically configures auth routes (/auth/login, /auth/logout)
web_service = FlextWebServices.WebService(config)

# 3. Start the Service
web_service.start()
```

### Using the API Client

Interact with backend services using the integrated client.

```python
# Fetch applications from the configured backend
apps_result = web_service.fetch_apps_from_api()

if apps_result.is_success:
    apps = apps_result.unwrap()
    print(f"Retrieved {len(apps)} applications")
```

## 🏗️ Architecture

FLEXT-Web is built on Clean Architecture principles to ensure scalability and maintainability:

- **Domain Layer**: Defines entities (`WebApp`, `UserSession`) and business rules independent of the web framework.
- **Application Layer**: Uses CQRS (`FlextWebHandlers`) to separate command logic from query logic.
- **Infrastructure Layer**: Provides concrete implementations for Flask and FastAPI, along with configuration adapters.
- **Presentation Layer**: Handles HTTP requests and responses, delegating business logic to the application layer.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/development.md) for details on setting up your environment and submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
