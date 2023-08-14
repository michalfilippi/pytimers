.PHONY: test black mypy ruff all

test:
	python -m pytest

black:
	black pytimers tests --diff

mypy:
	mypy pytimers tests

ruff:
	ruff pytimers tests

all: test black mypy ruff
