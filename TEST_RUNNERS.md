# Quick Test Runner

This directory contains convenient test runner scripts to validate your code quickly during development.

## Usage Options

### 1. Python Test Runner (Detailed)

```bash
# Run all tests and checks (comprehensive)
python3 run_tests.py

# Quick validation (skip slow checks like security, docs, build)
python3 run_tests.py --fast

# Run only tests with coverage
python3 run_tests.py --coverage

# Run only linting and formatting checks
python3 run_tests.py --lint

# Run tests without coverage (faster)
python3 run_tests.py --no-coverage

# Show help
python3 run_tests.py --help
```

### 2. Shell Script Wrapper (Simple)

```bash
# Run all tests (equivalent to python3 run_tests.py)
./test.sh

# Pass any arguments to the underlying Python script
./test.sh --fast
./test.sh --lint
./test.sh --coverage
```

### 3. Individual Commands (Manual)

```bash
# Code formatting and linting
python3 -m black --check src/ tests/
python3 -m isort --check-only src/ tests/
python3 -m flake8 src
python3 -m mypy src/nunyakata

# Tests with coverage
python3 -m pytest tests/ -v --cov=src/nunyakata --cov-report=term-missing --cov-fail-under=70

# Security and quality
python3 -m safety check
python3 -m bandit -r src

# Build package
python3 -m build
```

## What Each Test Runner Includes

### Full Test Suite (`python3 run_tests.py`)

1. **Dependency Check** - Ensures Python 3 and pip are available
2. **Install Dependencies** - Updates development dependencies
3. **Code Formatting** - Black and isort checks
4. **Linting** - Flake8 syntax and style checks
5. **Type Checking** - MyPy static type analysis
6. **Unit Tests** - Pytest with 70%+ coverage requirement
7. **Integration Tests** - If available
8. **Security Scans** - Safety and Bandit security checks
9. **Package Build** - Build and validate Python package
10. **Documentation** - Build docs if MkDocs config exists

### Fast Mode (`--fast`)

Skips slower checks:

- Security scans
- Package building
- Documentation building

### Coverage Only (`--coverage`)

Runs only:

- Dependency check
- Install dependencies
- Unit tests with coverage

### Lint Only (`--lint`)

Runs only:

- Dependency check
- Install dependencies
- Code formatting checks
- Linting checks
- Type checking

## Output Features

- **Color-coded output** for easy reading
- **Progress indicators** showing which check is running
- **Detailed summary** at the end with pass/fail counts
- **Success rate percentage**
- **Individual check status** (✅ passed, ❌ failed)

## Examples

```bash
# Quick development check (2-3 seconds)
python3 run_tests.py --lint

# Fast validation before commit (10-15 seconds)
python3 run_tests.py --fast

# Full CI/CD simulation (30-60 seconds)
python3 run_tests.py

# Just run tests to check coverage
python3 run_tests.py --coverage
```

## Integration with Development Workflow

1. **Before committing**: `./test.sh --fast`
2. **During development**: `python3 run_tests.py --lint`
3. **Before pushing**: `python3 run_tests.py`
4. **CI/CD validation**: All individual commands are available

The test runners ensure your code meets the same standards as the CI/CD pipeline, catching issues early in development.
