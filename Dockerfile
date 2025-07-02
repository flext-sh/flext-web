# FLEXT Web - Django Dashboard Docker Image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_SETTINGS_MODULE=flext_web.settings.production

# Create non-root user
RUN groupadd -r flext && useradd -r -g flext flext

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY pyproject.toml .
COPY manage.py .

# Install the application
RUN pip install -e .

# Create directories and set permissions
RUN mkdir -p /app/logs /app/staticfiles /app/media \
    && chown -R flext:flext /app

# Collect static files
RUN python manage.py collectstatic --noinput

# Switch to non-root user
USER flext

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Start the Django application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--timeout", "120", "flext_web.wsgi:application"]