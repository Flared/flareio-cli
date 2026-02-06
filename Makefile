.PHONY: test
test:
	uv run pytest

.PHONY: check
check:
	uv run ty check

.PHONY: ci
ci: test check
