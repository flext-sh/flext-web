# Private project handlers for flext-web.
# Strict extension: only `_custom_<verb>_<what>` handlers and `(pre|post)-<verb>[-<what>]`
# hooks. Public targets, toolchain vars, .DEFAULT_GOAL, includes, and help are
# invalid (base.mk owns those). Each handler maps to `make <verb> WHAT=<what>`.
.PHONY: _custom_run_dev
_custom_run_dev: ## make run WHAT=dev — start dev server
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_web
