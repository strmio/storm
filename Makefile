.PHONY: test lint format check all

# Ejecutar todos los tests
test:
	pytest

# Linting con Ruff
lint:
	ruff check storm tests

# Formatear código con Ruff
format:
	ruff format storm tests

# Verifica y ejecuta tests
check: lint test

# Ejecuta todo
all: lint format test
