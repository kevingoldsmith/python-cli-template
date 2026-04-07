# python-cli-template

A template for personal Python CLI projects. Includes config file parsing,
argument handling, logging, and a complete dev toolchain.

## Toolchain

| Tool | Purpose |
|---|---|
| **uv** | Package management and virtual environments |
| **ruff** | Linting and formatting (replaces black + pylint) |
| **mypy** | Static type checking (strict mode) |
| **pytest** + **pytest-cov** | Testing with coverage reporting |
| **pre-commit** | Git hooks for ruff and mypy |
| **GitHub Actions** | CI across Python 3.12 and 3.13 |

## Prerequisites

Install [uv](https://docs.astral.sh/uv/getting-started/installation/).

## Setup

```sh
make install                      # install dev dependencies via uv
uv run pre-commit install         # enable git hooks
make all                          # format, lint, typecheck, test
```

## Make targets

```
install     install dev dependencies
format      run ruff formatter
lint        run ruff linter
typecheck   run mypy (strict)
test        run pytest with coverage
all         format + lint + typecheck + test
clean       remove build/cache artifacts
list        show all make targets
```

## Adapting this template

1. Rename `template.py` to your module name (e.g. `myscript.py`)
2. Rename `tests/test_template.py` accordingly
3. Update `_CONFIG_FILE` and `_LOG_FILE` constants in your module
4. Update `[project.name]` and `[project.scripts]` in `pyproject.toml`
5. Add your business logic in `main()`

## What's included

- **Config file** — INI-based config via `configparser`; auto-loaded on startup
- **Argument parsing** — `--verbose`/`-v` and `--verbose_log`/`-V` flags; extend in `parse_args()`
- **Logging** — dual console + file handlers with configurable levels; pass `logfile_name=None` to skip file logging

> For production services that emit structured/JSON logs, consider replacing the stdlib `logging` setup with [structlog](https://www.structlog.org/).
