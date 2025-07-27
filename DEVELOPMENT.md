# Nunyakata Development Setup

This document provides instructions for setting up the development environment and building the package.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Development Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/SeveighTech/nunyakata.git
   cd nunyakata
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package in development mode:**

   ```bash
   pip install -e ".[dev]"
   ```

   Or using the Makefile:

   ```bash
   make install-dev
   ```

## Development Workflow

### Running Tests

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov
```

### Code Formatting and Linting

```bash
# Format code
make format

# Lint code
make lint

# Type checking
make typecheck
```

### Building the Package

```bash
# Clean previous builds
make clean

# Build the package
make build
```

## Publishing

### Test PyPI (for testing)

```bash
# Build the package first
make build

# Upload to Test PyPI
make upload-test
```

### PyPI (production)

```bash
# Build the package first
make build

# Upload to PyPI
make upload
```

## Project Structure

```
nunyakata/
├── src/
│   └── nunyakata/
│       ├── __init__.py      # Package initialization
│       └── client.py        # Main client class
├── tests/
│   ├── __init__.py
│   └── test_client.py       # Tests for client
├── pyproject.toml           # Package configuration
├── Makefile                 # Development commands
├── README.md               # Project documentation
├── LICENSE                 # License file
└── DEVELOPMENT.md          # This file
```

## Adding New Services

When adding new Ghana-specific services:

1. Create new modules in `src/nunyakata/`
2. Add corresponding tests in `tests/`
3. Update the main `__init__.py` to export new classes
4. Update dependencies in `pyproject.toml` if needed
5. Run tests and ensure they pass

## Useful Commands

All available commands can be seen with:

```bash
make help
```
