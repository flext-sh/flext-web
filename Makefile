# flext-web - Web Framework
PROJECT_NAME := flext-web
ifneq ("$(wildcard ../base.mk)", "")
include ../base.mk
else
include base.mk
endif

# === PROJECT-SPECIFIC TARGETS ===
.PHONY: dev test-unit test-integration build shell

dev: ## Start development server
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_web

.DEFAULT_GOAL := help
