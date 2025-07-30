# FLEXT Web Interface

Enterprise web interface for FLEXT platform management built with Flask and Clean Architecture patterns. Provides comprehensive dashboard and API endpoints for monitoring and managing the distributed data integration ecosystem.

## Features

- FlexCore cluster management
- Plugin registry and execution
- Meltano and Ray job orchestration
- Real-time dashboard with monitoring
- REST API for programmatic access

## Usage

```bash
# Development
python -m flext_web.api --debug

# Production
python -m flext_web.api
```