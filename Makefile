# flext-web - Web Framework
PROJECT_NAME := flext-web
COV_DIR := flext_web
MIN_COVERAGE := 90

include ../base.mk

# === PROJECT-SPECIFIC TARGETS ===
.PHONY: dev test-unit test-integration build shell

dev: ## Start development server
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_web

.DEFAULT_GOAL := help
