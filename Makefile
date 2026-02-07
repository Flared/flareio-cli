.DEFAULT_GOAL := ci

.PHONY: test
test:
	uv run pytest

.PHONY: check
check:
	uv run ty check

.PHONY: ci
ci: test check format-check

.PHONY: format
format:
	uv run ruff check --fix
	uv run ruff format

.PHONY: format-check
format-check:
	uv run ruff format --check

.PHONY: clean
clean:
	rm -rf dist .venv

.PHONY: venv
venv:
	uv sync
