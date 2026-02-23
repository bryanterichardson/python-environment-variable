.PHONY: \
	clean \
	clean-venv \
	format \
	init \
	test \

init: format test

clean: clean-venv

clean-venv:
	rm -rf .venv

format: .git/hooks/pre-commit
	uv tool run pre-commit run --all-files

test:
	uv run pytest


# Concrete Targets

.git/hooks/pre-commit: .pre-commit-config.yaml
	uvx pre-commit install
