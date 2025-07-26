# Development and Build Scripts

## Install in development mode
install-dev:
	pip install -e ".[dev]"

## Run tests
test:
	pytest

## Run tests with coverage
test-cov:
	pytest --cov=nunyakata --cov-report=html --cov-report=term-missing

## Format code
format:
	black src/ tests/
	isort src/ tests/

## Lint code
lint:
	flake8 src/ tests/
	mypy src/

## Type check
typecheck:
	mypy src/

## Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

## Build package
build:
	python -m build

## Upload to PyPI (production)
upload:
	python -m twine upload dist/*

## Upload to Test PyPI
upload-test:
	python -m twine upload --repository testpypi dist/*

## Help
help:
	@echo "Available commands:"
	@echo "  install-dev  - Install package in development mode"
	@echo "  test         - Run tests"
	@echo "  test-cov     - Run tests with coverage"
	@echo "  format       - Format code with black and isort"
	@echo "  lint         - Lint code with flake8 and mypy"
	@echo "  typecheck    - Run type checking with mypy"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build package"
	@echo "  upload       - Upload to PyPI"
	@echo "  upload-test  - Upload to Test PyPI"

.PHONY: install-dev test test-cov format lint typecheck clean build upload upload-test help
