"""
Nunyakata - A unified Python package for Ghana-specific services and APIs.

This package provides a unified interface to various Ghana-specific services
and APIs, making it easier for developers to integrate with Ghanaian services.
"""

__version__ = "0.1.0"
__author__ = "Joseph"
__email__ = "etsejoey@outlook.com"

from .client import NunyakataClient
from .services.nalo_solutions import NaloSolutionsClient
from .config import (
    load_nalo_client_from_env,
    get_env_config,
    validate_env_config,
    create_nalo_client,
)

__version__ = "0.1.0"

__all__ = [
    "NunyakataClient",
    "NaloSolutionsClient",
    "load_nalo_client_from_env",
    "get_env_config",
    "validate_env_config",
    "create_nalo_client",
]
