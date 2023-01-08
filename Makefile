init:
	python -m venv venv
	source venv/bin/activate; pip install -r requirements.txt

lint: ; @for py in *.py; do echo "Linting $$py"; pylint -rn $$py; done

black:
	black .

mypy:
	mypy --disallow-untyped-defs .

list:
	@grep '^[^#[:space:]].*:' Makefile

test:
	pytest

all: test black lint mypy
