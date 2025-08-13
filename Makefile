# =============================================================================
# FLEXT-WEB - Flask Web Interface & Dashboard Makefile
# =============================================================================
# Python 3.13+ Web Framework - Clean Architecture + DDD + Zero Tolerance
# =============================================================================

# Project Configuration
PROJECT_NAME := flext-web
PYTHON_VERSION := 3.13
POETRY := poetry
SRC_DIR := src
TESTS_DIR := tests
COV_DIR := flext_web

# Quality Standards
MIN_COVERAGE := 90

# Flask Configuration
FLASK_HOST := localhost
FLASK_PORT := 8080
FLASK_ENV := development
FLASK_SECRET_KEY := dev-key-change-in-production

# Export Configuration
export PROJECT_NAME PYTHON_VERSION MIN_COVERAGE FLASK_HOST FLASK_PORT FLASK_ENV FLASK_SECRET_KEY

# =============================================================================
# HELP & INFORMATION
# =============================================================================

.PHONY: help
help: ## Show available commands
	@echo "FLEXT-WEB - Flask Web Interface & Dashboard"
	@echo "=========================================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \\\\033[36m%-18s\\\\033[0m %s\\\\n", $$1, $$2}'

.PHONY: info
info: ## Show project information
	@echo "Project: $(PROJECT_NAME)"
	@echo "Python: $(PYTHON_VERSION)+"
	@echo "Poetry: $(POETRY)"
	@echo "Coverage: $(MIN_COVERAGE)% minimum"
	@echo "Flask Host: $(FLASK_HOST)"
	@echo "Flask Port: $(FLASK_PORT)"
	@echo "Flask Environment: $(FLASK_ENV)"
	@echo "Architecture: Clean Architecture + DDD + Flask + REST API"

# =============================================================================
# SETUP & INSTALLATION
# =============================================================================

.PHONY: install
install: ## Install dependencies
	$(POETRY) install

.PHONY: install-dev
install-dev: ## Install dev dependencies
	$(POETRY) install --with dev,test,docs

.PHONY: setup
setup: install-dev ## Complete project setup
	$(POETRY) run pre-commit install

# =============================================================================
# QUALITY GATES (MANDATORY)
# =============================================================================

.PHONY: validate
validate: lint type-check security test ## Run all quality gates

.PHONY: check
check: lint type-check ## Quick health check

.PHONY: lint
lint: ## Run linting
	$(POETRY) run ruff check $(SRC_DIR) $(TESTS_DIR)

.PHONY: format
format: ## Format code
	$(POETRY) run ruff format $(SRC_DIR) $(TESTS_DIR)

.PHONY: type-check
type-check: ## Run type checking
	$(POETRY) run mypy $(SRC_DIR) --strict

.PHONY: security
security: ## Run security scanning
	$(POETRY) run bandit -r $(SRC_DIR)
	$(POETRY) run pip-audit

.PHONY: fix
fix: ## Auto-fix issues
	$(POETRY) run ruff check $(SRC_DIR) $(TESTS_DIR) --fix
	$(POETRY) run ruff format $(SRC_DIR) $(TESTS_DIR)

# =============================================================================
# TESTING
# =============================================================================

.PHONY: test
test: ## Run tests with coverage
	$(POETRY) run pytest $(TESTS_DIR) --cov=$(COV_DIR) --cov-report=term-missing --cov-fail-under=$(MIN_COVERAGE)

.PHONY: test-unit
test-unit: ## Run unit tests
	$(POETRY) run pytest $(TESTS_DIR) -m "not integration" -v

.PHONY: test-integration
test-integration: ## Run integration tests
	$(POETRY) run pytest $(TESTS_DIR) -m integration -v

.PHONY: test-web
test-web: ## Run web interface tests
	$(POETRY) run pytest $(TESTS_DIR) -m web -v

.PHONY: test-api
test-api: ## Run API tests
	$(POETRY) run pytest $(TESTS_DIR) -m api -v

.PHONY: test-e2e
test-e2e: ## Run end-to-end tests
	$(POETRY) run pytest $(TESTS_DIR) -m e2e -v

.PHONY: test-fast
test-fast: ## Run tests without coverage
	$(POETRY) run pytest $(TESTS_DIR) -v

.PHONY: coverage-html
coverage-html: ## Generate HTML coverage report
	$(POETRY) run pytest $(TESTS_DIR) --cov=$(COV_DIR) --cov-report=html

# =============================================================================
# BUILD & DISTRIBUTION
# =============================================================================

.PHONY: build
build: ## Build package
	$(POETRY) build

.PHONY: build-clean
build-clean: clean build ## Clean and build

.PHONY: build-docker
build-docker: ## Build Docker image
	docker build -t flext-web:latest .

# =============================================================================
# FLASK WEB OPERATIONS
# =============================================================================

.PHONY: runserver
runserver: ## Start Flask development server
	$(POETRY) run python -m flext_web --host $(FLASK_HOST) --port $(FLASK_PORT)

.PHONY: serve
serve: runserver ## Alias for runserver

.PHONY: dev-server
dev-server: ## Start dev server with hot reload
	FLASK_ENV=development $(POETRY) run python -m flext_web --debug

.PHONY: prod-server
prod-server: ## Start production server
	FLASK_ENV=production $(POETRY) run python -m flext_web --no-debug

.PHONY: web-test
web-test: ## Test web service locally
	$(POETRY) run python -c "from flext_web import create_service; s = create_service(); print('Service created successfully')"

.PHONY: web-health
web-health: ## Check web service health
	curl -f http://$(FLASK_HOST):$(FLASK_PORT)/health || echo "Web service not available"

# =============================================================================
# DOCUMENTATION
# =============================================================================

.PHONY: docs
docs: ## Build documentation
	$(POETRY) run mkdocs build

.PHONY: docs-serve
docs-serve: ## Serve documentation
	$(POETRY) run mkdocs serve

# =============================================================================
# DEPENDENCIES
# =============================================================================

.PHONY: deps-update
deps-update: ## Update dependencies
	$(POETRY) update

.PHONY: deps-show
deps-show: ## Show dependency tree
	$(POETRY) show --tree

.PHONY: deps-audit
deps-audit: ## Audit dependencies
	$(POETRY) run pip-audit

# =============================================================================
# DEVELOPMENT
# =============================================================================

.PHONY: shell
shell: ## Open Python shell
	$(POETRY) run python

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks
	$(POETRY) run pre-commit run --all-files

# =============================================================================
# MAINTENANCE
# =============================================================================

.PHONY: clean
clean: ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ htmlcov/ .coverage .mypy_cache/ .ruff_cache/
	rm -rf static/build/ templates/build/ instance/ logs/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

.PHONY: clean-all
clean-all: clean ## Deep clean including venv
	rm -rf .venv/

.PHONY: reset
reset: clean-all setup ## Reset project

# =============================================================================
# DIAGNOSTICS
# =============================================================================

.PHONY: diagnose
diagnose: ## Project diagnostics
	@echo "Python: $$(python --version)"
	@echo "Poetry: $$($(POETRY) --version)"
	@echo "Flask: $$($(POETRY) run python -c 'import flask; print(flask.__version__)' 2>/dev/null || echo 'Not available')"
	@echo "Web Service: $$($(POETRY) run python -c 'import flext_web; print(getattr(flext_web, \"__version__\", \"dev\"))' 2>/dev/null || echo 'Not available')"
	@$(POETRY) env info

.PHONY: doctor
doctor: diagnose check ## Health check

# =============================================================================
# ALIASES (SINGLE LETTER SHORTCUTS)
# =============================================================================

.PHONY: t l f tc c i v r s
t: test
l: lint
f: format
tc: type-check
c: clean
i: install
v: validate
r: runserver
s: serve

# =============================================================================
# CONFIGURATION
# =============================================================================

.DEFAULT_GOAL := help

.PHONY: help install install-dev setup validate check lint format type-check security fix test test-unit test-integration test-web test-api test-e2e test-fast coverage-html build build-clean build-docker runserver serve dev-server prod-server web-test web-health docs docs-serve deps-update deps-show deps-audit shell pre-commit clean clean-all reset diagnose doctor t l f tc c i v r s
