# python-environment-variable

Open-source package for loading environment variables easier and in a Pythonic way

## Getting Started

TBD (Pending https://github.com/bryanterichardson/python-environment-variable/issues/2)

## Development

> [!IMPORTANT]
> We `uv` for development, from environment setup to test and build/deploy.
>
> See official `uv` [documentation](https://docs.astral.sh/uv/) for more information.

### Initial setup

If it's your first time working on this project, you can run the following command to set up your environment:

```sh
make init
```

> [!TIP]
> We also provide a number of other `make` targets for convenience.
> Run `make` (or `make help`) to see what's available.

### Code format

We use `ruff` for code formatting and linting. You can run the following command to check your code.
A simple way to lint your code is to run the pre-commit hooks using the `format` target:

```sh
make format
```

### Unit tests

We use `pytest` for unit tests, and all tests are in the `tests` directory.

To quickly run unit tests using the development environment, you can run

```sh
make test
```

To make sure that the package works as expected in all supported `python` versions, you can run the `test-all` target.
Note that each `python` version will be tested in an isolated environment, and you can use the `-j, --jobs` option to run tests in parallel
(each `python` version in its own process). For example:

```sh
make -j5 test-all
```

> [!TIP]
> For the `test-all` target, both `stdout` and `stderr` from testing each `python` version are written to respective `.test-{version}.log` files.
