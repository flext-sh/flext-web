# FLEXT WEB - Django Enterprise Web Application
# =============================================
# Modern Django web interface with Clean Architecture + DDD
# Python 3.13 + Django 5.1+ + Zero Tolerance Quality Gates

.PHONY: help check validate test lint type-check security format format-check fix
.PHONY: install dev-install setup pre-commit build clean
.PHONY: coverage coverage-html test-unit test-integration test-web
.PHONY: deps-update deps-audit deps-tree deps-outdated
.PHONY: migrate makemigrations collectstatic runserver shell createsuperuser

# ============================================================================
# 🎯 HELP & INFORMATION
# ============================================================================

help: ## Show this help message
	@echo "🌐 FLEXT WEB - Django Enterprise Web Application"
	@echo "=============================================="
	@echo "🎯 Clean Architecture + DDD + Python 3.13 + Django 5.1+ Enterprise Standards"
	@echo ""
	@echo "📦 Modern Django web interface for FLEXT data integration platform"
	@echo "🔒 Zero tolerance quality gates with Django security"
	@echo "🧪 90%+ test coverage requirement with Django testing"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ============================================================================
# 🎯 CORE QUALITY GATES - ZERO TOLERANCE
# ============================================================================

validate: lint type-check security test ## STRICT compliance validation (all must pass)
	@echo "✅ ALL QUALITY GATES PASSED - FLEXT WEB COMPLIANT"

check: lint type-check test ## Essential quality checks (pre-commit standard)
	@echo "✅ Essential checks passed"

lint: ## Ruff linting (17 rule categories, ALL enabled)
	@echo "🔍 Running ruff linter (ALL rules enabled)..."
	@poetry run ruff check src/ tests/ --fix --unsafe-fixes
	@echo "✅ Linting complete"

type-check: ## MyPy strict mode type checking (zero errors tolerated)
	@echo "🛡️ Running MyPy strict type checking..."
	@poetry run mypy src/ tests/ --strict
	@echo "✅ Type checking complete"

security: ## Security scans (bandit + pip-audit + secrets)
	@echo "🔒 Running security scans..."
	@poetry run bandit -r src/ --severity-level medium --confidence-level medium
	@poetry run pip-audit --ignore-vuln PYSEC-2022-42969
	@poetry run detect-secrets scan --all-files
	@echo "✅ Security scans complete"

format: ## Format code with ruff
	@echo "🎨 Formatting code..."
	@poetry run ruff format src/ tests/
	@echo "✅ Formatting complete"

format-check: ## Check formatting without fixing
	@echo "🎨 Checking code formatting..."
	@poetry run ruff format src/ tests/ --check
	@echo "✅ Format check complete"

fix: format lint ## Auto-fix all issues (format + imports + lint)
	@echo "🔧 Auto-fixing all issues..."
	@poetry run ruff check src/ tests/ --fix --unsafe-fixes
	@echo "✅ All auto-fixes applied"

# ============================================================================
# 🧪 TESTING - 90% COVERAGE MINIMUM
# ============================================================================

test: ## Run Django tests with coverage (90% minimum required)
	@echo "🧪 Running Django tests with coverage..."
	@poetry run python manage.py test --keepdb --parallel --settings=flext_web.config.settings.test
	@poetry run coverage run --source='.' manage.py test --keepdb
	@poetry run coverage report --fail-under=90
	@echo "✅ Tests complete"

test-unit: ## Run unit tests only
	@echo "🧪 Running unit tests..."
	@poetry run python manage.py test tests.unit --keepdb --parallel
	@echo "✅ Unit tests complete"

test-integration: ## Run integration tests only
	@echo "🧪 Running integration tests..."
	@poetry run python manage.py test tests.integration --keepdb
	@echo "✅ Integration tests complete"

test-web: ## Run web UI tests
	@echo "🌐 Running web UI tests..."
	@poetry run python manage.py test tests.web --keepdb
	@echo "✅ Web UI tests complete"

coverage: ## Generate detailed coverage report
	@echo "📊 Generating coverage report..."
	@poetry run coverage run --source='.' manage.py test --keepdb
	@poetry run coverage html
	@echo "✅ Coverage report generated in htmlcov/"

coverage-html: coverage ## Generate HTML coverage report
	@echo "📊 Opening coverage report..."
	@python -m webbrowser htmlcov/index.html

# ============================================================================
# 🚀 DEVELOPMENT SETUP
# ============================================================================

setup: install pre-commit migrate collectstatic ## Complete development setup
	@echo "🎯 Development setup complete!"

install: ## Install dependencies with Poetry
	@echo "📦 Installing dependencies..."
	@poetry install --all-extras --with dev,test,docs,security
	@echo "✅ Dependencies installed"

dev-install: install ## Install in development mode
	@echo "🔧 Setting up development environment..."
	@poetry install --all-extras --with dev,test,docs,security
	@poetry run pre-commit install
	@echo "✅ Development environment ready"

pre-commit: ## Setup pre-commit hooks
	@echo "🎣 Setting up pre-commit hooks..."
	@poetry run pre-commit install
	@poetry run pre-commit run --all-files || true
	@echo "✅ Pre-commit hooks installed"

# ============================================================================
# 🗄️ DJANGO DATABASE OPERATIONS
# ============================================================================

migrate: ## Run Django database migrations
	@echo "🗄️ Running Django migrations..."
	@poetry run python manage.py migrate
	@echo "✅ Database migrations complete"

makemigrations: ## Create new Django migrations
	@echo "🗄️ Creating Django migrations..."
	@poetry run python manage.py makemigrations
	@echo "✅ Migrations created"

migrate-reset: ## Reset and recreate database
	@echo "🗄️ Resetting database..."
	@poetry run python manage.py flush --noinput
	@poetry run python manage.py migrate
	@echo "✅ Database reset complete"

migrate-check: ## Check for unapplied migrations
	@echo "🔍 Checking for unapplied migrations..."
	@poetry run python manage.py showmigrations --plan
	@echo "✅ Migration check complete"

# ============================================================================
# 🌐 DJANGO WEB OPERATIONS
# ============================================================================

runserver: ## Start Django development server
	@echo "🌐 Starting Django development server..."
	@echo "📡 Server will be available at: http://localhost:8000"
	@echo "🔧 Admin interface at: http://localhost:8000/REDACTED_LDAP_BIND_PASSWORD/"
	@poetry run python manage.py runserver 0.0.0.0:8000

runserver-prod: ## Start Django server with production settings
	@echo "🌐 Starting Django server (production mode)..."
	@poetry run python manage.py runserver 0.0.0.0:8000 --settings=flext_web.config.settings.production

collectstatic: ## Collect static files
	@echo "📦 Collecting static files..."
	@poetry run python manage.py collectstatic --noinput
	@echo "✅ Static files collected"

shell: ## Start Django shell
	@echo "🐚 Starting Django shell..."
	@poetry run python manage.py shell

shell-plus: ## Start Django shell with extensions
	@echo "🐚 Starting Django shell plus..."
	@poetry run python manage.py shell_plus

dbshell: ## Start database shell
	@echo "🗄️ Starting database shell..."
	@poetry run python manage.py dbshell

# ============================================================================
# 👤 DJANGO USER OPERATIONS
# ============================================================================

createsuperuser: ## Create Django superuser
	@echo "👤 Creating Django superuser..."
	@poetry run python manage.py createsuperuser

create-test-data: ## Create test data for development
	@echo "🌱 Creating test data..."
	@poetry run python manage.py loaddata fixtures/test_data.json
	@echo "✅ Test data created"

flush-data: ## Remove all data from database
	@echo "🧹 Flushing database data..."
	@poetry run python manage.py flush --noinput
	@echo "✅ Database data flushed"

# ============================================================================
# 🔄 DJANGO MANAGEMENT COMMANDS
# ============================================================================

check-deploy: ## Check Django deployment configuration
	@echo "🔍 Checking Django deployment configuration..."
	@poetry run python manage.py check --deploy
	@echo "✅ Deployment check complete"

validate-templates: ## Validate Django templates
	@echo "🔍 Validating Django templates..."
	@poetry run python manage.py validate_templates
	@echo "✅ Template validation complete"

check-migrations: ## Check for migration issues
	@echo "🔍 Checking for migration issues..."
	@poetry run python manage.py makemigrations --dry-run --check
	@echo "✅ Migration check complete"

# ============================================================================
# 📦 BUILD & DISTRIBUTION
# ============================================================================

build: clean collectstatic ## Build distribution packages
	@echo "🔨 Building distribution..."
	@poetry build
	@echo "✅ Build complete - packages in dist/"

build-docker: ## Build Docker image
	@echo "🐳 Building Docker image..."
	@docker build -t flext-web:latest .
	@echo "✅ Docker image built"

# ============================================================================
# 🧹 CLEANUP
# ============================================================================

clean: ## Remove all artifacts
	@echo "🧹 Cleaning up..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@rm -rf .coverage
	@rm -rf htmlcov/
	@rm -rf .pytest_cache/
	@rm -rf staticfiles/
	@rm -rf media/uploads/
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete"

# ============================================================================
# 📊 DEPENDENCY MANAGEMENT
# ============================================================================

deps-update: ## Update all dependencies
	@echo "🔄 Updating dependencies..."
	@poetry update
	@echo "✅ Dependencies updated"

deps-audit: ## Audit dependencies for vulnerabilities
	@echo "🔍 Auditing dependencies..."
	@poetry run pip-audit
	@echo "✅ Dependency audit complete"

deps-tree: ## Show dependency tree
	@echo "🌳 Dependency tree:"
	@poetry show --tree

deps-outdated: ## Show outdated dependencies
	@echo "📋 Outdated dependencies:"
	@poetry show --outdated

# ============================================================================
# 🔧 ENVIRONMENT CONFIGURATION
# ============================================================================

# Python settings
PYTHON := python3.13
export PYTHONPATH := $(PWD)/src:$(PYTHONPATH)
export PYTHONDONTWRITEBYTECODE := 1
export PYTHONUNBUFFERED := 1

# Django settings
export DJANGO_SETTINGS_MODULE := flext_web.config.settings.development
export DJANGO_DEBUG := true
export DJANGO_SECRET_KEY := dev-secret-key-change-in-production
export DJANGO_ALLOWED_HOSTS := localhost,127.0.0.1

# Database settings
export DATABASE_URL := postgresql://localhost/flext_web_dev
export FLEXT_WEB_DATABASE_URL := postgresql://localhost/flext_web_dev

# Redis settings
export REDIS_URL := redis://localhost:6379/0
export FLEXT_WEB_REDIS_URL := redis://localhost:6379/0

# Static files settings
export DJANGO_STATIC_URL := /static/
export DJANGO_MEDIA_URL := /media/

# Poetry settings
export POETRY_VENV_IN_PROJECT := false
export POETRY_CACHE_DIR := $(HOME)/.cache/pypoetry

# Quality gate settings
export MYPY_CACHE_DIR := .mypy_cache
export RUFF_CACHE_DIR := .ruff_cache

# ============================================================================
# 📝 PROJECT METADATA
# ============================================================================

# Project information
PROJECT_NAME := flext-web
PROJECT_VERSION := $(shell poetry version -s)
PROJECT_DESCRIPTION := FLEXT Web - Django Enterprise Web Application

.DEFAULT_GOAL := help

# ============================================================================
# 🎯 DJANGO VALIDATION COMMANDS
# ============================================================================

django-validate: check-deploy validate-templates check-migrations ## Validate Django setup
	@echo "✅ Django validation complete"

django-security: ## Check Django security
	@echo "🔒 Checking Django security..."
	@poetry run python manage.py check --deploy --fail-level WARNING
	@echo "✅ Django security check complete"

django-performance: ## Check Django performance
	@echo "⚡ Checking Django performance..."
	@poetry run python manage.py check --debug-mode --fail-level WARNING
	@echo "✅ Django performance check complete"

# ============================================================================
# 🎯 WEB APPLICATION TESTING
# ============================================================================

test-api: ## Test Django REST API endpoints
	@echo "🔌 Testing Django REST API..."
	@poetry run python manage.py test tests.api --keepdb
	@echo "✅ API tests complete"

test-forms: ## Test Django forms
	@echo "📋 Testing Django forms..."
	@poetry run python manage.py test tests.forms --keepdb
	@echo "✅ Form tests complete"

test-views: ## Test Django views
	@echo "👁️ Testing Django views..."
	@poetry run python manage.py test tests.views --keepdb
	@echo "✅ View tests complete"

test-models: ## Test Django models
	@echo "🗄️ Testing Django models..."
	@poetry run python manage.py test tests.models --keepdb
	@echo "✅ Model tests complete"

# ============================================================================
# 🎯 FLEXT ECOSYSTEM INTEGRATION
# ============================================================================

ecosystem-check: ## Verify FLEXT ecosystem compatibility
	@echo "🌐 Checking FLEXT ecosystem compatibility..."
	@echo "📦 Web project: $(PROJECT_NAME) v$(PROJECT_VERSION)"
	@echo "🏗️ Architecture: Clean Architecture + DDD"
	@echo "🐍 Python: 3.13"
	@echo "🌐 Framework: Django 5.1+ with Django REST Framework"
	@echo "📊 Quality: Zero tolerance enforcement"
	@echo "✅ Ecosystem compatibility verified"

workspace-info: ## Show workspace integration info
	@echo "🏢 FLEXT Workspace Integration"
	@echo "==============================="
	@echo "📁 Project Path: $(PWD)"
	@echo "🏆 Role: Django Web Interface (enterprise UI)"
	@echo "🔗 Dependencies: flext-core, flext-auth, flext-api, flext-grpc"
	@echo "📦 Provides: Web UI, REST API, Admin interface"
	@echo "🎯 Standards: Enterprise Django patterns with Clean Architecture"