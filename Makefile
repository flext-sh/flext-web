# =============================================================================
# FLEXT-WEB - PROJECT MAKEFILE
# =============================================================================
# Enterprise Django Web Application with Clean Architecture + DDD + Zero Tolerance Quality
# Python 3.13 + Django 5.1+ + Modern UI + Type Safety
# =============================================================================

# Project Configuration
PROJECT_NAME := flext-web
PROJECT_TYPE := python-library
PYTHON_VERSION := 3.13
POETRY := poetry
SRC_DIR := src
TESTS_DIR := tests
DOCS_DIR := docs

# Quality Gates Configuration
MIN_COVERAGE := 90
MYPY_STRICT := true
RUFF_CONFIG := pyproject.toml
PEP8_LINE_LENGTH := 79

# Django Configuration
DJANGO_HOST := 0.0.0.0
DJANGO_PORT := 8000
DJANGO_SETTINGS := flext_web.config.settings.development

# Export environment variables
export PYTHON_VERSION
export MIN_COVERAGE
export MYPY_STRICT
export DJANGO_HOST
export DJANGO_PORT
export DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS)

# =============================================================================
# HELP & INFORMATION
# =============================================================================

.PHONY: help
help: ## Show available commands
	@echo "$(PROJECT_NAME) - Django Enterprise Application"
	@echo "==============================================="
	@echo ""
	@echo "📋 AVAILABLE COMMANDS:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-18s %s\\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "🔧 PROJECT INFO:"
	@echo "  Type: $(PROJECT_TYPE)"
	@echo "  Python: $(PYTHON_VERSION)"
	@echo "  Coverage: $(MIN_COVERAGE)%"
	@echo "  Django Host: $(DJANGO_HOST):$(DJANGO_PORT)"
	@echo "  Line Length: $(PEP8_LINE_LENGTH)"

.PHONY: info
info: ## Show project information
	@echo "Project Information"
	@echo "=================="
	@echo "Name: $(PROJECT_NAME)"
	@echo "Type: $(PROJECT_TYPE)"
	@echo "Python Version: $(PYTHON_VERSION)"
	@echo "Source Directory: $(SRC_DIR)"
	@echo "Tests Directory: $(TESTS_DIR)"
	@echo "Django Host: $(DJANGO_HOST)"
	@echo "Django Port: $(DJANGO_PORT)"
	@echo "Django Settings: $(DJANGO_SETTINGS)"
	@echo "Quality Standards: Zero Tolerance"
	@echo "Architecture: Clean Architecture + DDD + Django"

# =============================================================================
# INSTALLATION & SETUP
# =============================================================================

.PHONY: install
install: ## Install project dependencies
	@echo "📦 Installing $(PROJECT_NAME) dependencies..."
	@$(POETRY) install

.PHONY: install-dev
install-dev: ## Install development dependencies
	@echo "📦 Installing development dependencies..."
	@$(POETRY) install --with dev,test,docs

.PHONY: setup
setup: ## Complete project setup
	@echo "🚀 Setting up $(PROJECT_NAME)..."
	@make install-dev
	@make pre-commit-install
	@make migrate
	@make collectstatic
	@echo "✅ Setup complete"

.PHONY: pre-commit-install
pre-commit-install: ## Install pre-commit hooks
	@echo "🔧 Installing pre-commit hooks..."
	@$(POETRY) run pre-commit install
	@$(POETRY) run pre-commit autoupdate

# =============================================================================
# QUALITY GATES & VALIDATION
# =============================================================================

.PHONY: validate
validate: ## Run complete validation (quality gate)
	@echo "🔍 Running complete validation for $(PROJECT_NAME)..."
	@make lint
	@make type-check
	@make security
	@make test
	@make pep8-check
	@make django-validate
	@echo "✅ Validation complete"

.PHONY: check
check: ## Quick health check
	@echo "🏥 Running health check..."
	@make lint
	@make type-check
	@echo "✅ Health check complete"

.PHONY: lint
lint: ## Run code linting
	@echo "🧹 Running linting..."
	@$(POETRY) run ruff check $(SRC_DIR) $(TESTS_DIR)

.PHONY: format
format: ## Format code
	@echo "🎨 Formatting code..."
	@$(POETRY) run ruff format $(SRC_DIR) $(TESTS_DIR)

.PHONY: format-check
format-check: ## Check code formatting
	@echo "🎨 Checking code formatting..."
	@$(POETRY) run ruff format --check $(SRC_DIR) $(TESTS_DIR)

.PHONY: type-check
type-check: ## Run type checking
	@echo "🔍 Running type checking..."
	@$(POETRY) run mypy $(SRC_DIR) --strict

.PHONY: security
security: ## Run security scanning
	@echo "🔒 Running security scanning..."
	@$(POETRY) run bandit -r $(SRC_DIR)
	@$(POETRY) run pip-audit

.PHONY: pep8-check
pep8-check: ## Check PEP8 compliance
	@echo "📏 Checking PEP8 compliance..."
	@$(POETRY) run ruff check $(SRC_DIR) $(TESTS_DIR) --select E,W
	@echo "✅ PEP8 check complete"

.PHONY: fix
fix: ## Auto-fix code issues
	@echo "🔧 Auto-fixing code issues..."
	@$(POETRY) run ruff check $(SRC_DIR) $(TESTS_DIR) --fix
	@make format

# =============================================================================
# TESTING
# =============================================================================

.PHONY: test
test: ## Run Django tests with coverage
	@echo "🧪 Running Django tests with coverage..."
	@$(POETRY) run python manage.py test --keepdb --parallel
	@$(POETRY) run coverage run --source='.' manage.py test --keepdb
	@$(POETRY) run coverage report --fail-under=$(MIN_COVERAGE)

.PHONY: test-unit
test-unit: ## Run unit tests only
	@echo "🧪 Running unit tests..."
	@$(POETRY) run python manage.py test tests.unit --keepdb --parallel

.PHONY: test-integration
test-integration: ## Run integration tests only
	@echo "🧪 Running integration tests..."
	@$(POETRY) run python manage.py test tests.integration --keepdb

.PHONY: test-web
test-web: ## Run web UI tests
	@echo "🌐 Running web UI tests..."
	@$(POETRY) run python manage.py test tests.web --keepdb

.PHONY: test-api
test-api: ## Test Django REST API endpoints
	@echo "🔌 Testing Django REST API..."
	@$(POETRY) run python manage.py test tests.api --keepdb

.PHONY: test-forms
test-forms: ## Test Django forms
	@echo "📋 Testing Django forms..."
	@$(POETRY) run python manage.py test tests.forms --keepdb

.PHONY: test-views
test-views: ## Test Django views
	@echo "👁️ Testing Django views..."
	@$(POETRY) run python manage.py test tests.views --keepdb

.PHONY: test-models
test-models: ## Test Django models
	@echo "🗄️ Testing Django models..."
	@$(POETRY) run python manage.py test tests.models --keepdb

.PHONY: coverage
coverage: ## Generate coverage report
	@echo "📊 Generating coverage report..."
	@$(POETRY) run coverage run --source='.' manage.py test --keepdb
	@$(POETRY) run coverage html

.PHONY: coverage-html
coverage-html: ## Generate HTML coverage report
	@echo "📊 Generating HTML coverage report..."
	@$(POETRY) run coverage run --source='.' manage.py test --keepdb
	@$(POETRY) run coverage html
	@echo "📊 Coverage report: htmlcov/index.html"

# =============================================================================
# DJANGO OPERATIONS
# =============================================================================

.PHONY: runserver
runserver: ## Start Django development server
	@echo "🌐 Starting Django development server..."
	@echo "📡 Server will be available at: http://$(DJANGO_HOST):$(DJANGO_PORT)"
	@echo "🔧 Admin interface at: http://$(DJANGO_HOST):$(DJANGO_PORT)/REDACTED_LDAP_BIND_PASSWORD/"
	@$(POETRY) run python manage.py runserver $(DJANGO_HOST):$(DJANGO_PORT)

.PHONY: serve
serve: runserver ## Alias for runserver

.PHONY: runserver-prod
runserver-prod: ## Start Django server with production settings
	@echo "🌐 Starting Django server (production mode)..."
	@$(POETRY) run python manage.py runserver $(DJANGO_HOST):$(DJANGO_PORT) --settings=flext_web.config.settings.production

.PHONY: migrate
migrate: ## Run Django database migrations
	@echo "🗄️ Running Django migrations..."
	@$(POETRY) run python manage.py migrate

.PHONY: makemigrations
makemigrations: ## Create new Django migrations
	@echo "🗄️ Creating Django migrations..."
	@$(POETRY) run python manage.py makemigrations

.PHONY: migrate-reset
migrate-reset: ## Reset and recreate database
	@echo "🗄️ Resetting database..."
	@$(POETRY) run python manage.py flush --noinput
	@$(POETRY) run python manage.py migrate

.PHONY: migrate-check
migrate-check: ## Check for unapplied migrations
	@echo "🔍 Checking for unapplied migrations..."
	@$(POETRY) run python manage.py showmigrations --plan

.PHONY: collectstatic
collectstatic: ## Collect static files
	@echo "📦 Collecting static files..."
	@$(POETRY) run python manage.py collectstatic --noinput

.PHONY: shell
shell: ## Start Django shell
	@echo "🐚 Starting Django shell..."
	@$(POETRY) run python manage.py shell

.PHONY: shell-plus
shell-plus: ## Start Django shell with extensions
	@echo "🐚 Starting Django shell plus..."
	@$(POETRY) run python manage.py shell_plus

.PHONY: dbshell
dbshell: ## Start database shell
	@echo "🗄️ Starting database shell..."
	@$(POETRY) run python manage.py dbshell

.PHONY: createsuperuser
createsuperuser: ## Create Django superuser
	@echo "👤 Creating Django superuser..."
	@$(POETRY) run python manage.py createsuperuser

.PHONY: create-test-data
create-test-data: ## Create test data for development
	@echo "🌱 Creating test data..."
	@$(POETRY) run python manage.py loaddata fixtures/test_data.json

.PHONY: flush-data
flush-data: ## Remove all data from database
	@echo "🧹 Flushing database data..."
	@$(POETRY) run python manage.py flush --noinput

# =============================================================================
# DJANGO VALIDATION
# =============================================================================

.PHONY: django-validate
django-validate: ## Complete Django validation
	@echo "🔍 Running Django validation..."
	@make check-deploy
	@make validate-templates
	@make check-migrations
	@echo "✅ Django validation complete"

.PHONY: check-deploy
check-deploy: ## Check Django deployment configuration
	@echo "🔍 Checking Django deployment configuration..."
	@$(POETRY) run python manage.py check --deploy

.PHONY: validate-templates
validate-templates: ## Validate Django templates
	@echo "🔍 Validating Django templates..."
	@$(POETRY) run python manage.py validate_templates

.PHONY: check-migrations
check-migrations: ## Check for migration issues
	@echo "🔍 Checking for migration issues..."
	@$(POETRY) run python manage.py makemigrations --dry-run --check

.PHONY: django-security
django-security: ## Check Django security
	@echo "🔒 Checking Django security..."
	@$(POETRY) run python manage.py check --deploy --fail-level WARNING

.PHONY: django-performance
django-performance: ## Check Django performance
	@echo "⚡ Checking Django performance..."
	@$(POETRY) run python manage.py check --debug-mode --fail-level WARNING

# =============================================================================
# BUILD & DISTRIBUTION
# =============================================================================

.PHONY: build
build: ## Build distribution packages
	@echo "🏗️ Building $(PROJECT_NAME)..."
	@$(POETRY) build

.PHONY: build-clean
build-clean: ## Clean build and rebuild
	@echo "🏗️ Clean build..."
	@make clean
	@make build

.PHONY: build-docker
build-docker: ## Build Docker image
	@echo "🐳 Building Docker image..."
	@docker build -t flext-web:latest .

.PHONY: publish-test
publish-test: ## Publish to test PyPI
	@echo "📦 Publishing to test PyPI..."
	@$(POETRY) publish --repository testpypi

.PHONY: publish
publish: ## Publish to PyPI
	@echo "📦 Publishing to PyPI..."
	@$(POETRY) publish

# =============================================================================
# DOCUMENTATION
# =============================================================================

.PHONY: docs
docs: ## Build documentation
	@echo "📚 Building documentation..."
	@$(POETRY) run mkdocs build

.PHONY: docs-serve
docs-serve: ## Serve documentation locally
	@echo "📚 Serving documentation..."
	@$(POETRY) run mkdocs serve

.PHONY: docs-deploy
docs-deploy: ## Deploy documentation
	@echo "📚 Deploying documentation..."
	@$(POETRY) run mkdocs gh-deploy

# =============================================================================
# DEPENDENCY MANAGEMENT
# =============================================================================

.PHONY: deps-update
deps-update: ## Update dependencies
	@echo "🔄 Updating dependencies..."
	@$(POETRY) update

.PHONY: deps-show
deps-show: ## Show dependency tree
	@echo "📋 Showing dependency tree..."
	@$(POETRY) show --tree

.PHONY: deps-audit
deps-audit: ## Audit dependencies for security
	@echo "🔍 Auditing dependencies..."
	@$(POETRY) run pip-audit

.PHONY: deps-export
deps-export: ## Export requirements.txt
	@echo "📄 Exporting requirements..."
	@$(POETRY) export -f requirements.txt --output requirements.txt
	@$(POETRY) export -f requirements.txt --dev --output requirements-dev.txt

# =============================================================================
# DEVELOPMENT TOOLS
# =============================================================================

.PHONY: notebook
notebook: ## Start Jupyter notebook
	@echo "📓 Starting Jupyter notebook..."
	@$(POETRY) run jupyter lab

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks
	@echo "🔍 Running pre-commit hooks..."
	@$(POETRY) run pre-commit run --all-files

# =============================================================================
# MAINTENANCE & CLEANUP
# =============================================================================

.PHONY: clean
clean: ## Clean build artifacts and cache
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@rm -rf .coverage
	@rm -rf htmlcov/
	@rm -rf .pytest_cache/
	@rm -rf staticfiles/
	@rm -rf media/uploads/
	@rm -rf .mypy_cache/
	@rm -rf .ruff_cache/
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true

.PHONY: clean-all
clean-all: clean ## Deep clean including virtual environment
	@echo "🧹 Deep cleaning..."
	@rm -rf .venv/

.PHONY: reset
reset: clean-all ## Reset project to clean state
	@echo "🔄 Resetting project..."
	@make setup

# =============================================================================
# DIAGNOSTICS & TROUBLESHOOTING
# =============================================================================

.PHONY: diagnose
diagnose: ## Run project diagnostics
	@echo "🔬 Running project diagnostics..."
	@echo "Python version: $$(python --version)"
	@echo "Poetry version: $$($(POETRY) --version)"
	@echo "Django status: $$($(POETRY) run python -c 'import django; print(django.__version__)')"
	@echo "Project info:"
	@$(POETRY) show --no-dev
	@echo "Environment status:"
	@$(POETRY) env info

.PHONY: doctor
doctor: ## Check project health
	@echo "👩‍⚕️ Checking project health..."
	@make diagnose
	@make check
	@echo "✅ Health check complete"

# =============================================================================
# CONVENIENCE ALIASES
# =============================================================================

.PHONY: t
t: test ## Alias for test

.PHONY: l
l: lint ## Alias for lint

.PHONY: f
f: format ## Alias for format

.PHONY: tc
tc: type-check ## Alias for type-check

.PHONY: c
c: clean ## Alias for clean

.PHONY: i
i: install ## Alias for install

.PHONY: v
v: validate ## Alias for validate

.PHONY: r
r: runserver ## Alias for runserver

.PHONY: s
s: serve ## Alias for serve

.PHONY: m
m: migrate ## Alias for migrate

.PHONY: mm
mm: makemigrations ## Alias for makemigrations

# =============================================================================
# Default target
# =============================================================================

.DEFAULT_GOAL := help