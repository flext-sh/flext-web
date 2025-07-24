# FLEXT Web Interface - Flask API Docker Image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    FLEXT_WEB_PORT=5000 \
    FLEXT_SERVICE_URL=http://flext-service:8080

# Create non-root user
RUN groupadd -r flext && useradd -r -g flext flext

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements for dependency caching
COPY requirements.txt .
COPY README.md .

# Install the application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Create directories and set permissions
RUN mkdir -p /app/logs /app/staticfiles \
    && chown -R flext:flext /app

# Switch to non-root user
USER flext

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Set environment variables for FLEXT integration
ENV FLEXT_BINARY_PATH=/usr/local/bin/flext \
    FLEXT_CONFIG_PATH=/etc/flext/config.yaml

# Start the Flask web interface
CMD ["python", "-m", "flext_web.api"]