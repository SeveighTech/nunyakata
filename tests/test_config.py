"""Tests for Nunyakata configuration utilities."""

import os
from unittest.mock import MagicMock, patch

import pytest

from nunyakata.config import (
    create_nalo_client,
    get_env_config,
    load_nalo_client_from_env,
    validate_env_config,
)
from nunyakata.services.nalo_solutions import NaloSolutions


class TestLoadNaloClientFromEnv:
    """Test suite for load_nalo_client_from_env function."""

    def test_load_client_with_payment_credentials(self, monkeypatch):
        """Test loading client with payment credentials from environment."""
        # Set up environment variables
        monkeypatch.setenv("NALO_PAYMENT_USERNAME", "test_payment_user")
        monkeypatch.setenv("NALO_PAYMENT_PASSWORD", "test_payment_pass")
        monkeypatch.setenv("NALO_MERCHANT_ID", "test_merchant_123")

        client = load_nalo_client_from_env()

        assert isinstance(client, NaloSolutions)
        assert client.payment_username == "test_payment_user"
        assert client.payment_password == "test_payment_pass"
        assert client.payment_merchant_id == "test_merchant_123"

    def test_load_client_with_sms_username_password(self, monkeypatch):
        """Test loading client with SMS username/password credentials."""
        monkeypatch.setenv("NALO_SMS_USERNAME", "test_sms_user")
        monkeypatch.setenv("NALO_SMS_PASSWORD", "test_sms_pass")
        monkeypatch.setenv("NALO_SMS_SOURCE", "TEST_SENDER")

        client = load_nalo_client_from_env()

        assert isinstance(client, NaloSolutions)
        assert client.sms_username == "test_sms_user"
        assert client.sms_password == "test_sms_pass"
        assert client.sms_sender_id == "TEST_SENDER"

    def test_load_client_with_sms_auth_key(self, monkeypatch):
        """Test loading client with SMS auth key credentials."""
        monkeypatch.setenv("NALO_SMS_AUTH_KEY", "test_auth_key_12345")

        client = load_nalo_client_from_env()

        assert isinstance(client, NaloSolutions)
        assert client.sms_auth_key == "test_auth_key_12345"

    def test_load_client_with_email_credentials(self, monkeypatch):
        """Test loading client with email credentials."""
        monkeypatch.setenv("NALO_EMAIL_USERNAME", "test_email_user")
        monkeypatch.setenv("NALO_EMAIL_PASSWORD", "test_email_pass")

        client = load_nalo_client_from_env()

        assert isinstance(client, NaloSolutions)
        assert client.email_username == "test_email_user"
        assert client.email_password == "test_email_pass"

    def test_load_client_with_email_auth_key(self, monkeypatch):
        """Test loading client with email auth key."""
        monkeypatch.setenv("NALO_EMAIL_AUTH_KEY", "test_email_auth_key")

        client = load_nalo_client_from_env()

        assert isinstance(client, NaloSolutions)
        assert client.email_auth_key == "test_email_auth_key"

    def test_load_client_no_credentials_error(self):
        """Test that ValueError is raised when no credentials are found."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(
                ValueError, match="No valid Nalo Solutions credentials found"
            ):
                load_nalo_client_from_env()

    def test_load_client_without_dotenv(self, monkeypatch):
        """Test loading client when dotenv is not available."""

        # Mock ImportError for dotenv by patching the import
        def mock_import(name, *args, **kwargs):
            if name == "dotenv":
                raise ImportError("No module named 'dotenv'")
            return __import__(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            monkeypatch.setenv("NALO_SMS_USERNAME", "test_user")
            monkeypatch.setenv("NALO_SMS_PASSWORD", "test_pass")

            # Should still work without dotenv
            client = load_nalo_client_from_env()
            assert isinstance(client, NaloSolutions)


class TestGetEnvConfig:
    """Test suite for get_env_config function."""

    def test_get_config_default_values(self):
        """Test getting config with default values."""
        with patch.dict(os.environ, {}, clear=True):
            config = get_env_config()

            assert config["environment"] == "development"
            assert config["debug"] is False
            assert config["services"]["nalo_payments"] is False
            assert config["services"]["nalo_sms"] is False

    def test_get_config_with_environment_variables(self, monkeypatch):
        """Test getting config with environment variables set."""
        monkeypatch.setenv("ENVIRONMENT", "production")
        monkeypatch.setenv("DEBUG", "true")
        monkeypatch.setenv("NALO_PAYMENT_USERNAME", "payment_user")
        monkeypatch.setenv("NALO_PAYMENT_PASSWORD", "payment_pass")
        monkeypatch.setenv("NALO_MERCHANT_ID", "merchant_123")
        monkeypatch.setenv("NALO_SMS_AUTH_KEY", "sms_auth_key")

        config = get_env_config()

        assert config["environment"] == "production"
        assert config["debug"] is True
        assert config["services"]["nalo_payments"] is True
        assert config["services"]["nalo_sms"] is True

    def test_get_config_with_webhooks(self, monkeypatch):
        """Test getting config with webhook URLs."""
        monkeypatch.setenv("PAYMENT_CALLBACK_URL", "https://example.com/payment")
        monkeypatch.setenv("SMS_DELIVERY_CALLBACK_URL", "https://example.com/sms")
        monkeypatch.setenv("USSD_CALLBACK_URL", "https://example.com/ussd")

        config = get_env_config()

        assert config["webhooks"]["payment_callback"] == "https://example.com/payment"
        assert config["webhooks"]["sms_delivery_callback"] == "https://example.com/sms"
        assert config["webhooks"]["ussd_callback"] == "https://example.com/ussd"

    def test_get_config_with_testing_vars(self, monkeypatch):
        """Test getting config with testing variables."""
        monkeypatch.setenv("TEST_PHONE_NUMBER", "233501234567")
        monkeypatch.setenv("TEST_PAYMENT_AMOUNT", "10.50")

        config = get_env_config()

        assert config["testing"]["test_phone"] == "233501234567"
        assert config["testing"]["test_amount"] == "10.50"

    def test_get_config_sms_with_username_password(self, monkeypatch):
        """Test SMS service detection with username/password."""
        monkeypatch.setenv("NALO_SMS_USERNAME", "sms_user")
        monkeypatch.setenv("NALO_SMS_PASSWORD", "sms_pass")

        config = get_env_config()

        assert config["services"]["nalo_sms"] is True


class TestValidateEnvConfig:
    """Test suite for validate_env_config function."""

    def test_validate_config_all_valid(self, monkeypatch):
        """Test validation with all required variables present."""
        monkeypatch.setenv("NALO_PAYMENT_USERNAME", "payment_user")
        monkeypatch.setenv("NALO_PAYMENT_PASSWORD", "payment_pass")
        monkeypatch.setenv("NALO_MERCHANT_ID", "merchant_123")
        monkeypatch.setenv("NALO_SMS_AUTH_KEY", "sms_auth_key")

        is_valid, missing = validate_env_config()

        assert is_valid is True
        assert missing == []

    def test_validate_config_sms_username_password(self, monkeypatch):
        """Test validation with SMS username/password instead of auth key."""
        monkeypatch.setenv("NALO_PAYMENT_USERNAME", "payment_user")
        monkeypatch.setenv("NALO_PAYMENT_PASSWORD", "payment_pass")
        monkeypatch.setenv("NALO_MERCHANT_ID", "merchant_123")
        monkeypatch.setenv("NALO_SMS_USERNAME", "sms_user")
        monkeypatch.setenv("NALO_SMS_PASSWORD", "sms_pass")

        is_valid, missing = validate_env_config()

        assert is_valid is True
        assert missing == []

    def test_validate_config_missing_sms_credentials(self, monkeypatch):
        """Test validation with missing SMS credentials."""
        monkeypatch.setenv("NALO_PAYMENT_USERNAME", "payment_user")
        monkeypatch.setenv("NALO_PAYMENT_PASSWORD", "payment_pass")
        monkeypatch.setenv("NALO_MERCHANT_ID", "merchant_123")

        is_valid, missing = validate_env_config()

        assert is_valid is False
        assert (
            "NALO_SMS_AUTH_KEY or (NALO_SMS_USERNAME and NALO_SMS_PASSWORD)" in missing
        )

    def test_validate_config_partial_payment_credentials(self, monkeypatch):
        """Test validation with partial payment credentials."""
        monkeypatch.setenv("NALO_PAYMENT_USERNAME", "payment_user")
        # Missing password and merchant_id
        monkeypatch.setenv("NALO_SMS_AUTH_KEY", "sms_auth_key")

        is_valid, missing = validate_env_config()

        assert is_valid is False
        assert "NALO_PAYMENT_PASSWORD" in missing
        assert "NALO_MERCHANT_ID" in missing

    def test_validate_config_no_credentials(self):
        """Test validation with no credentials."""
        with patch.dict(os.environ, {}, clear=True):
            is_valid, missing = validate_env_config()

            assert is_valid is False
            assert (
                "NALO_SMS_AUTH_KEY or (NALO_SMS_USERNAME and NALO_SMS_PASSWORD)"
                in missing
            )


class TestCreateNaloClient:
    """Test suite for create_nalo_client function."""

    def test_create_client_with_explicit_params(self):
        """Test creating client with explicit parameters."""
        client = create_nalo_client(
            payment_username="explicit_user",
            payment_password="explicit_pass",
            merchant_id="explicit_merchant",
            sms_username="explicit_sms_user",
            sms_password="explicit_sms_pass",
        )

        assert isinstance(client, NaloSolutions)
        assert client.payment_username == "explicit_user"
        assert client.sms_username == "explicit_sms_user"

    def test_create_client_with_sms_auth_key(self):
        """Test creating client with SMS auth key."""
        client = create_nalo_client(sms_auth_key="explicit_auth_key")

        assert isinstance(client, NaloSolutions)
        assert client.sms_auth_key == "explicit_auth_key"

    def test_create_client_with_kwargs(self):
        """Test creating client with additional kwargs."""
        client = create_nalo_client(
            sms_username="test_user",
            sms_password="test_pass",
        )

        assert isinstance(client, NaloSolutions)
        assert client.sms_username == "test_user"
        assert client.sms_password == "test_pass"

    @patch("nunyakata.config.load_nalo_client_from_env")
    def test_create_client_fallback_to_env(self, mock_load_from_env, monkeypatch):
        """Test creating client falls back to environment when no params provided."""
        mock_client = MagicMock(spec=NaloSolutions)
        mock_load_from_env.return_value = mock_client

        # Call without any credentials
        client = create_nalo_client()

        mock_load_from_env.assert_called_once()
        assert client == mock_client

    @patch("nunyakata.config.load_nalo_client_from_env")
    def test_create_client_fallback_with_empty_params(self, mock_load_from_env):
        """Test creating client falls back to environment with None params."""
        mock_client = MagicMock(spec=NaloSolutions)
        mock_load_from_env.return_value = mock_client

        # Call with None values
        client = create_nalo_client(
            payment_username=None, sms_username=None, sms_auth_key=None
        )

        mock_load_from_env.assert_called_once()
        assert client == mock_client
