.PHONY: install lint format typecheck test all clean list

install:
	uv sync --group dev

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy .

test:
	uv run pytest

all: format lint typecheck test

clean:
	rm -rf .venv __pycache__ .pytest_cache htmlcov .coverage .mypy_cache .ruff_cache

list:
	@grep '^[^#[:space:]].*:' Makefile
