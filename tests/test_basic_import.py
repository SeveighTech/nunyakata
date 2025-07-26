"""
Simple test to verify NaloSolutions can be imported and initialized.
"""

import pytest


def test_import_nalo_solutions():
    """Test that we can import NaloSolutions."""
    from nunyakata.services.nalo_solutions import NaloSolutions

    assert NaloSolutions is not None


def test_nalo_solutions_initialization():
    """Test that we can initialize NaloSolutions with config."""
    from nunyakata.services.nalo_solutions import NaloSolutions

    config = {
        "payment": {
            "public_key": "test_public_key",
            "private_key": "test_private_key",
            "environment": "sandbox",
        },
        "sms": {
            "sender_id": "TEST_SENDER",
            "username": "test_user",
            "password": "test_pass",
            "auth_key": "test_auth_key",
        },
    }

    client = NaloSolutions(config)
    assert client is not None
    assert client.config == config
