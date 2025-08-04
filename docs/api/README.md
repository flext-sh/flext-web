# API Reference - FLEXT Web Interface

**API Version**: v1  
**Base URL**: `http://localhost:8080`  
**Content Type**: `application/json`  
**Authentication**: None (open endpoints - security integration planned for v1.0.0)  
**Documentation Status**: ✅ **Complete** - Enterprise API documentation with comprehensive examples

## 🔗 API Overview

The FLEXT Web Interface provides RESTful API endpoints for managing applications within the FLEXT ecosystem. All endpoints follow consistent response patterns using flext-core standardization with comprehensive error handling and validation.

**Enterprise Features**:

- Structured JSON responses with consistent error handling
- Comprehensive input validation using business rules
- Integration with FlextResult railway-oriented programming
- CQRS command processing through FlextWebAppHandler
- Monitoring and observability integration ready

### Response Format

All API responses follow this standardized structure:

```json
{
  "success": boolean,
  "message": string,
  "data": object | null
}
```

### HTTP Status Codes

- `200 OK` - Successful request
- `400 Bad Request` - Invalid request data or validation errors
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## 🏥 Health & Management Endpoints

### GET /health

Returns service health status and ecosystem information.

**Response Example**:

```json
{
  "success": true,
  "message": "FLEXT Web Service is healthy",
  "data": {
    "status": "healthy",
    "version": "0.9.0",
    "apps_count": 3,
    "config": "FLEXT Web"
  }
}
```

**cURL Example**:

```bash
curl -X GET http://localhost:8080/health
```

### GET /

Returns HTML dashboard with real-time application metrics.

**Response**: HTML page with inline CSS and Bootstrap styling

**Features**:

- Total applications count
- Running applications count
- Service version and status
- Enterprise UI with responsive design

**cURL Example**:

```bash
curl -X GET http://localhost:8080/
```

## 📱 Application Management Endpoints

### GET /api/v1/apps

List all managed applications with their current status.

**Response Example**:

```json
{
  "success": true,
  "message": "Applications retrieved successfully",
  "data": {
    "apps": [
      {
        "id": "app_data-pipeline",
        "name": "data-pipeline",
        "port": 3000,
        "host": "localhost",
        "is_running": true,
        "status": "running"
      },
      {
        "id": "app_web-service",
        "name": "web-service",
        "port": 8000,
        "host": "0.0.0.0",
        "is_running": false,
        "status": "stopped"
      }
    ]
  }
}
```

**cURL Example**:

```bash
curl -X GET http://localhost:8080/api/v1/apps
```

### POST /api/v1/apps

Create a new application with specified configuration.

**Request Body**:

```json
{
  "name": "string (required)",
  "port": "integer (optional, default: 8000)",
  "host": "string (optional, default: localhost)"
}
```

**Request Example**:

```json
{
  "name": "data-pipeline",
  "port": 3000,
  "host": "localhost"
}
```

**Success Response** (201 Created):

```json
{
  "success": true,
  "message": "Application created successfully",
  "data": {
    "id": "app_data-pipeline",
    "name": "data-pipeline",
    "port": 3000,
    "host": "localhost",
    "is_running": false,
    "status": "stopped"
  }
}
```

**Error Response** (400 Bad Request):

```json
{
  "success": false,
  "message": "App name is required",
  "data": null
}
```

**Validation Rules**:

- `name`: Required, non-empty string
- `port`: Optional, integer between 1-65535
- `host`: Optional, non-empty string

**cURL Example**:

```bash
curl -X POST http://localhost:8080/api/v1/apps \
  -H "Content-Type: application/json" \
  -d '{
    "name": "data-pipeline",
    "port": 3000,
    "host": "localhost"
  }'
```

### GET /api/v1/apps/{app_id}

Get detailed information about a specific application.

**Path Parameters**:

- `app_id`: Application identifier (format: `app_{name}`)

**Success Response**:

```json
{
  "success": true,
  "message": "Application retrieved successfully",
  "data": {
    "id": "app_data-pipeline",
    "name": "data-pipeline",
    "port": 3000,
    "host": "localhost",
    "is_running": false,
    "status": "stopped"
  }
}
```

**Error Response** (404 Not Found):

```json
{
  "success": false,
  "message": "Application not found",
  "data": null
}
```

**cURL Example**:

```bash
curl -X GET http://localhost:8080/api/v1/apps/app_data-pipeline
```

### POST /api/v1/apps/{app_id}/start

Start a specific application, changing its status to running.

**Path Parameters**:

- `app_id`: Application identifier (format: `app_{name}`)

**Success Response**:

```json
{
  "success": true,
  "message": "Application started successfully",
  "data": {
    "id": "app_data-pipeline",
    "name": "data-pipeline",
    "is_running": true,
    "status": "running"
  }
}
```

**Error Responses**:

Application not found (404):

```json
{
  "success": false,
  "message": "Application not found",
  "data": null
}
```

Application already running (400):

```json
{
  "success": false,
  "message": "Failed to start app: Application already running",
  "data": null
}
```

**Business Rules**:

- Cannot start an application that is already running
- Cannot start an application that is currently starting
- Status transitions: `stopped` → `running`

**cURL Example**:

```bash
curl -X POST http://localhost:8080/api/v1/apps/app_data-pipeline/start
```

### POST /api/v1/apps/{app_id}/stop

Stop a specific application, changing its status to stopped.

**Path Parameters**:

- `app_id`: Application identifier (format: `app_{name}`)

**Success Response**:

```json
{
  "success": true,
  "message": "Application stopped successfully",
  "data": {
    "id": "app_data-pipeline",
    "name": "data-pipeline",
    "is_running": false,
    "status": "stopped"
  }
}
```

**Error Responses**:

Application not found (404):

```json
{
  "success": false,
  "message": "Application not found",
  "data": null
}
```

Application already stopped (400):

```json
{
  "success": false,
  "message": "Failed to stop app: Application already stopped",
  "data": null
}
```

**Business Rules**:

- Cannot stop an application that is already stopped
- Cannot stop an application that is currently stopping
- Status transitions: `running` → `stopped`

**cURL Example**:

```bash
curl -X POST http://localhost:8080/api/v1/apps/app_data-pipeline/stop
```

## 📊 Application Status States

Applications can be in one of the following states:

| Status     | Description                               | Can Start | Can Stop |
| ---------- | ----------------------------------------- | --------- | -------- |
| `stopped`  | Application is not running                | ✅        | ❌       |
| `starting` | Application is in the process of starting | ❌        | ❌       |
| `running`  | Application is actively running           | ❌        | ✅       |
| `stopping` | Application is in the process of stopping | ❌        | ❌       |
| `error`    | Application encountered an error          | ✅        | ✅       |

### State Transition Diagram

```
    [stopped] ──start──► [starting] ──success──► [running]
        ▲                    │                     │
        │                    └──fail──► [error]   │
        │                                         │
        └──stop──◄ [stopping] ◄──stop──────────────┘
                       │
                       └──fail──► [error]
```

## 🔧 SDK Examples

### Python SDK Example

```python
import requests
from typing import Dict, Any, Optional

class FlextWebClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def health_check(self) -> Dict[str, Any]:
        """Check service health"""
        response = self.session.get(f"{self.base_url}/health")
        return response.json()

    def list_apps(self) -> Dict[str, Any]:
        """List all applications"""
        response = self.session.get(f"{self.base_url}/api/v1/apps")
        return response.json()

    def create_app(self, name: str, port: int = 8000, host: str = "localhost") -> Dict[str, Any]:
        """Create new application"""
        data = {"name": name, "port": port, "host": host}
        response = self.session.post(f"{self.base_url}/api/v1/apps", json=data)
        return response.json()

    def get_app(self, app_id: str) -> Dict[str, Any]:
        """Get application details"""
        response = self.session.get(f"{self.base_url}/api/v1/apps/{app_id}")
        return response.json()

    def start_app(self, app_id: str) -> Dict[str, Any]:
        """Start application"""
        response = self.session.post(f"{self.base_url}/api/v1/apps/{app_id}/start")
        return response.json()

    def stop_app(self, app_id: str) -> Dict[str, Any]:
        """Stop application"""
        response = self.session.post(f"{self.base_url}/api/v1/apps/{app_id}/stop")
        return response.json()

# Usage Example
client = FlextWebClient()

# Create and manage application
result = client.create_app("my-service", port=3000)
if result["success"]:
    app_id = result["data"]["id"]

    # Start the application
    start_result = client.start_app(app_id)
    print(f"Started: {start_result['success']}")

    # Check status
    app_info = client.get_app(app_id)
    print(f"Status: {app_info['data']['status']}")
```

### JavaScript/Node.js SDK Example

```javascript
class FlextWebClient {
  constructor(baseUrl = "http://localhost:8080") {
    this.baseUrl = baseUrl;
  }

  async request(method, path, data = null) {
    const url = `${this.baseUrl}${path}`;
    const options = {
      method,
      headers: { "Content-Type": "application/json" },
    };

    if (data) {
      options.body = JSON.stringify(data);
    }

    const response = await fetch(url, options);
    return response.json();
  }

  async healthCheck() {
    return this.request("GET", "/health");
  }

  async listApps() {
    return this.request("GET", "/api/v1/apps");
  }

  async createApp(name, port = 8000, host = "localhost") {
    return this.request("POST", "/api/v1/apps", { name, port, host });
  }

  async getApp(appId) {
    return this.request("GET", `/api/v1/apps/${appId}`);
  }

  async startApp(appId) {
    return this.request("POST", `/api/v1/apps/${appId}/start`);
  }

  async stopApp(appId) {
    return this.request("POST", `/api/v1/apps/${appId}/stop`);
  }
}

// Usage Example
const client = new FlextWebClient();

async function manageApplication() {
  try {
    // Create application
    const createResult = await client.createApp("web-service", 8080);
    if (createResult.success) {
      const appId = createResult.data.id;

      // Start application
      const startResult = await client.startApp(appId);
      console.log("Started:", startResult.success);

      // Check status
      const appInfo = await client.getApp(appId);
      console.log("Status:", appInfo.data.status);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}
```

## 🚨 Current Limitations

### Security

- **No Authentication**: All endpoints are publicly accessible
- **No Authorization**: No role-based access control
- **No Rate Limiting**: Vulnerable to abuse and DoS attacks
- **No Input Sanitization**: Basic validation only

### Functionality

- **In-Memory Storage**: Applications lost on service restart
- **No Real Management**: Status changes don't affect actual processes
- **No Persistence**: No database or file-based storage
- **Single Instance**: No support for clustering or load balancing

### Integration

- **No FlexCore Integration**: Not connected to actual FLEXT ecosystem
- **No Observability**: Limited monitoring and metrics
- **No Event System**: No publish/subscribe or webhook support

## 🗺️ API Roadmap

### Phase 1: Security & Persistence

- [ ] **Authentication**: JWT or session-based authentication
- [ ] **Authorization**: Role-based access control (REDACTED_LDAP_BIND_PASSWORD, operator, viewer)
- [ ] **Persistence**: Database storage for applications and state
- [ ] **Input Validation**: Comprehensive request validation and sanitization

### Phase 2: Real Management

- [ ] **Process Management**: Actual application lifecycle management
- [ ] **Docker Integration**: Container-based application deployment
- [ ] **Health Monitoring**: Real health checks for managed applications
- [ ] **Log Aggregation**: Application log collection and streaming

### Phase 3: Advanced Features

- [ ] **WebSocket Support**: Real-time updates and notifications
- [ ] **Batch Operations**: Bulk application management
- [ ] **Scheduling**: Cron-like scheduling for application operations
- [ ] **Backup/Restore**: Application configuration backup and restore

### Phase 4: Ecosystem Integration

- [ ] **FlexCore Integration**: Communication with Go runtime service
- [ ] **FLEXT Service Integration**: Data platform service connectivity
- [ ] **Event Streaming**: Kafka or Redis-based event system
- [ ] **API Gateway**: Rate limiting, caching, and request transformation

## 📚 Additional Resources

- **[Architecture Guide](../architecture/README.md)** - System design and patterns
- **[Development Guide](../development/README.md)** - Development setup and workflows
- **[Configuration Guide](../configuration/README.md)** - Environment and settings
- **[Testing Guide](../testing/README.md)** - API testing strategies

---

**API Version**: 1.0  
**Last Updated**: January 2025  
**Next Review**: After authentication implementation
