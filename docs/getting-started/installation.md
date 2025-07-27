# Installation

## Requirements

- Python 3.8 or higher
- pip package manager

## Install from PyPI

The easiest way to install Nunyakata is using pip:

```bash
pip install nunyakata
```

## Install with Environment Variable Support

For projects that use environment variables for configuration:

```bash
pip install nunyakata[env]
```

This includes the `python-dotenv` package for loading environment variables from `.env` files.

## Install from Source

To install the latest development version:

```bash
git clone https://github.com/SeveighTech/nunyakata.git
cd nunyakata
pip install -e .
```

## Verify Installation

Test your installation:

```python
import nunyakata
print(f"Nunyakata version: {nunyakata.__version__}")

# Test imports
from nunyakata import NaloSolutions, load_nalo_client_from_env
print("✅ Nunyakata installed successfully!")
```

## Dependencies

Nunyakata automatically installs these required dependencies:

- `requests` - HTTP library for API calls
- `pyyaml` - YAML configuration support

Optional dependencies:

- `python-dotenv` - Environment variable support (install with `[env]` extra)
