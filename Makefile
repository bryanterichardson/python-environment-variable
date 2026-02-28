.PHONY: \
	clean \
	clean-venv \
	format \
	init \
	test \


## Show this help.
help:
	@awk '/^## .*$$/,/^[~\/\.a-zA-Z_-]+:/' ${MAKEFILE_LIST} | \
	awk '!(NR%2){print $$0p}{p=$$0}' |  \
	awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' | \
	sort

init: format test

## Clean up all artifacts
clean: \
	clean-build \
	clean-tests \
	clean-venv

clean-build:
	rm -rfv build
	rm -rfv dist
	rm -rfv src/*.egg-info

clean-tests:
	rm -rfv .coverage*
	rm -rfv .pytest_cache
	rm -rfv coverage

clean-venv:
	rm -rf .venv

## Force-run pre-commit hooks
format: .git/hooks/pre-commit
	uvx pre-commit run --all-files

## Run quick and simple test with coverage using .venv
test:
	uv run pytest

## Run tests for all supported Python versions
test-all: \
	_test-3.10 \
	_test-3.11 \
	_test-3.12 \
	_test-3.13 \
	_test-3.14
	cat .pytest_cache/.test-*-log

_test-%:
	@uv run \
		-q \
		--isolated \
		--python $* \
		--group test \
		pytest --no-cov > .pytest_cache/.test-$*-log 2>&1

## Get the (would-be) version of the current commit
version:
	@uv run -q python -m setuptools_scm


# Concrete Targets

.git/hooks/pre-commit: .pre-commit-config.yaml
	uvx pre-commit install
