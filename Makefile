.PHONY: test black mypy flake8 all

test:
	python -m pytest tests --cov pytimers --cov-report term-missing --no-cov-on-fail

black:
	black pytimers tests

mypy:
	mypy pytimers

flake8:
	flake8 pytimers tests

all: test black mypy flake8
