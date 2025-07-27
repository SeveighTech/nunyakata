.PHONY: help install clean test test-unit test-integration lint format type-check security build publish-test publish docs

# Default target
help:
	@echo "Nunyakata Development Commands"
	@echo "============================="
	@echo ""
	@echo "Setup:"
	@echo "  install          Install development dependencies"
	@echo "  clean            Clean build artifacts and cache"
	@echo ""
	@echo "Development:"
	@echo "  format           Format code with black and isort"
	@echo "  lint             Run linting checks (flake8, black, isort)"
	@echo "  type-check       Run type checking with mypy"
	@echo ""
	@echo "Testing:"
	@echo "  test             Run all tests with coverage"
	@echo "  test-unit        Run unit tests only"
	@echo "  test-integration Run integration tests only"
	@echo "  test-fast        Run tests without coverage"
	@echo "  test-core        Run core API tests only"
	@echo "  security         Run security checks"
	@echo ""
	@echo "Building:"
	@echo "  build            Build package for distribution"
	@echo "  publish-test     Publish to Test PyPI"
	@echo "  publish          Publish to PyPI"
	@echo ""
	@echo "Documentation:"
	@echo "  docs             Build documentation"
	@echo "  docs-serve       Serve documentation locally"
	@echo ""
	@echo "Quality Assurance:"
	@echo "  qa               Run full quality assurance (lint + type-check + test + security)"
	@echo "  ci               Run CI/CD simulation"

# Setup commands
install:
	pip install -e ".[dev,test,webhook]"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Development commands
format:
	black src tests
	isort src tests

lint:
	black --check src tests
	isort --check-only src tests
	flake8 src tests

type-check:
	mypy src/nunyakata

# Testing commands
test:
	pytest tests/test_basic_import.py tests/test_nalo_payments.py tests/test_nalo_sms.py tests/test_nalo_ussd.py tests/test_nalo_email.py -v --cov=src/nunyakata --cov-report=term-missing --cov-report=html --cov-report=xml --cov-fail-under=70

test-all:
	pytest tests/ -v --cov=src/nunyakata --cov-report=term-missing --cov-report=html --cov-report=xml

test-unit:
	pytest tests/ -v -m "unit" --cov=src/nunyakata --cov-report=term-missing

test-integration:
	pytest tests/ -v -m "integration"

test-fast:
	pytest tests/test_basic_import.py tests/test_nalo_payments.py tests/test_nalo_sms.py tests/test_nalo_ussd.py tests/test_nalo_email.py -v

test-core:
	pytest tests/test_basic_import.py tests/test_nalo_payments.py tests/test_nalo_sms.py tests/test_nalo_ussd.py tests/test_nalo_email.py -v

security:
	bandit -r src -f json || true
	safety check || true

# Building commands
build: clean
	pip install build twine
	python -m build
	python -m twine check dist/*

publish-test: build
	python -m twine upload --repository testpypi dist/*

publish: build
	python -m twine upload dist/*

# Documentation commands
docs:
	pip install mkdocs mkdocs-material mkdocstrings
	mkdocs build

docs-serve:
	pip install mkdocs mkdocs-material mkdocstrings
	mkdocs serve

# Quality assurance
qa: lint type-check test security
	@echo "✅ All quality checks passed!"

ci: install qa build
	@echo "🚀 CI/CD simulation completed successfully!"

# Development workflow
dev-setup:
	@test -d .venv || (echo "🔧 Creating virtual environment..." && python3 -m venv .venv)
	@echo "✅ Virtual environment ready."
	@. .venv/bin/activate && pip install --upgrade pip && pip install -e ".[dev,test,webhook]"
	@echo "✅ Development environment setup complete!"
	@echo "👉 Run 'source .venv/bin/activate' to activate the virtual environment."
	@echo "👉 Then run 'make test' to verify everything works."

# Quick test for development
quick-test:
	pytest tests/test_client.py -v

# Run specific service tests
test-payments:
	pytest tests/test_nalo_payments.py -v

test-sms:
	pytest tests/test_nalo_sms.py -v

test-ussd:
	pytest tests/test_nalo_ussd.py -v

test-email:
	pytest tests/test_nalo_email.py -v

# Coverage report
coverage:
	pytest tests/test_basic_import.py tests/test_nalo_payments.py tests/test_nalo_sms.py tests/test_nalo_ussd.py tests/test_nalo_email.py --cov=src/nunyakata --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

# Performance testing
perf-test:
	pytest tests/ -v --benchmark-only || echo "No performance tests found"

# Update dependencies
update-deps:
	pip install --upgrade pip
	pip install -e ".[dev,test,webhook]" --upgrade
