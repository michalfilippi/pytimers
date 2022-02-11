.PHONY: test black mypy flake8

test:
	python -m pytest tests --cov pytimers --cov-report term-missing --no-cov-on-fail

black:
	black pytimers tests

mypy:
	mypy pytimers

flake8:
	flake8 pytimers tests
