# FLEXT-WEB Makefile
PROJECT_NAME := flext-web
PYTHON_VERSION := 3.13
POETRY := poetry
SRC_DIR := src
TESTS_DIR := tests

# Quality standards
MIN_COVERAGE := 90

# Flask configuration
FLASK_HOST := localhost
FLASK_PORT := 8080
FLASK_ENV := development

# Help
help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\\033[36m%-18s\\033[0m %s\\n", $$1, $$2}'

# Installation
install: ## Install dependencies
	$(POETRY) install

install-dev: ## Install dev dependencies
	$(POETRY) install --with dev,test,docs

setup: install-dev ## Complete project setup
	$(POETRY) run pre-commit install

# Quality gates
validate: lint type-check security test ## Run all quality gates

check: lint type-check ## Quick health check

lint: ## Run linting
	$(POETRY) run ruff check $(SRC_DIR) $(TESTS_DIR)

format: ## Format code
	$(POETRY) run ruff format $(SRC_DIR) $(TESTS_DIR)

type-check: ## Run type checking
	$(POETRY) run mypy $(SRC_DIR) --strict

security: ## Run security scanning
	$(POETRY) run bandit -r $(SRC_DIR)
	$(POETRY) run pip-audit

fix: ## Auto-fix issues
	$(POETRY) run ruff check $(SRC_DIR) $(TESTS_DIR) --fix
	$(POETRY) run ruff format $(SRC_DIR) $(TESTS_DIR)

# Testing
test: ## Run tests with coverage
	$(POETRY) run pytest $(TESTS_DIR) --cov=$(SRC_DIR) --cov-report=term-missing --cov-fail-under=$(MIN_COVERAGE)

test-unit: ## Run unit tests
	$(POETRY) run pytest $(TESTS_DIR) -m "not integration" -v

test-integration: ## Run integration tests
	$(POETRY) run pytest $(TESTS_DIR) -m integration -v

test-web: ## Run web interface tests
	$(POETRY) run pytest $(TESTS_DIR) -m web -v

test-api: ## Run API tests
	$(POETRY) run pytest $(TESTS_DIR) -m api -v

test-fast: ## Run tests without coverage
	$(POETRY) run pytest $(TESTS_DIR) -v

coverage-html: ## Generate HTML coverage report
	$(POETRY) run pytest $(TESTS_DIR) --cov=$(SRC_DIR) --cov-report=html

# Flask operations
runserver: ## Start Flask development server
	$(POETRY) run python -m flext_web --host $(FLASK_HOST) --port $(FLASK_PORT)

serve: runserver ## Alias for runserver

dev-server: ## Start dev server with hot reload
	FLASK_ENV=development $(POETRY) run python -m flext_web --debug

prod-server: ## Start production server
	FLASK_ENV=production $(POETRY) run python -m flext_web --no-debug

web-test: ## Test web service locally
	$(POETRY) run python -c "from flext_web import create_service; s = create_service(); print('Service created successfully')"

# Build
build: ## Build package
	$(POETRY) build

build-clean: clean build ## Clean and build

build-docker: ## Build Docker image
	docker build -t flext-web:latest .

# Documentation
docs: ## Build documentation
	$(POETRY) run mkdocs build

docs-serve: ## Serve documentation
	$(POETRY) run mkdocs serve

# Dependencies
deps-update: ## Update dependencies
	$(POETRY) update

deps-show: ## Show dependency tree
	$(POETRY) show --tree

deps-audit: ## Audit dependencies
	$(POETRY) run pip-audit

# Development
shell: ## Open Python shell
	$(POETRY) run python

pre-commit: ## Run pre-commit hooks
	$(POETRY) run pre-commit run --all-files

# Maintenance
clean: ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ htmlcov/ .coverage .mypy_cache/ .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

clean-all: clean ## Deep clean including venv
	rm -rf .venv/

reset: clean-all setup ## Reset project

# Diagnostics
diagnose: ## Project diagnostics
	@echo "Python: $$(python --version)"
	@echo "Poetry: $$($(POETRY) --version)"
	@echo "Flask: $$($(POETRY) run python -c 'import flask; print(flask.__version__)' 2>/dev/null || echo 'Not available')"
	@echo "Web Service: $$($(POETRY) run python -c 'import flext_web; print(getattr(flext_web, \"__version__\", \"dev\"))' 2>/dev/null || echo 'Not available')"
	@$(POETRY) env info

doctor: diagnose check ## Health check

# Aliases
t: test
l: lint
f: format
tc: type-check
c: clean
i: install
v: validate
r: runserver
s: serve

.DEFAULT_GOAL := help
.PHONY: help install install-dev setup validate check lint format type-check security fix test test-unit test-integration test-web test-api test-fast coverage-html runserver serve dev-server prod-server web-test build build-clean build-docker docs docs-serve deps-update deps-show deps-audit shell pre-commit clean clean-all reset diagnose doctor t l f tc c i v r s