# nunyakata

Núnyá kátã (All Knowledge in Ewe) is A unified Python library wrapping Ghanaian digital services like payments, identity verification, SMS, USSD, and more. Built to simplify integrations with providers such as appsNmobile, Nalo, and others, all in one place.

## Features

- **Nalo Solutions Integration**: Complete payment and SMS API support
- **Environment-based Configuration**: Easy credential management with `.env` files
- **Type Safety**: Full type hints and Pydantic validation
- **Comprehensive Error Handling**: Detailed error codes and explanations
- **Multiple Authentication Methods**: Support for various credential types
- **Production Ready**: Built for scalability and reliability

## Installation

```bash
pip install nunyakata
```

For environment variable support:

```bash
pip install nunyakata[env]
```

## Quick Start

### Method 1: Environment Variables (Recommended)

1. Copy the environment template:

```bash
cp .env.example .env
```

2. Fill in your credentials in `.env`:

```env
# SMS API (choose one method)
NALO_SMS_AUTH_KEY=your_auth_key_here
NALO_SMS_SOURCE=YOUR_SENDER_ID

# Payment API
NALO_PAYMENT_USERNAME=your_username
NALO_PAYMENT_PASSWORD=your_password
NALO_MERCHANT_ID=your_merchant_id
```

3. Use the client:

```python
from nunyakata import NaloSolutions, create_nalo_client

# Method 1: Using configuration dictionary
config = {
    "sms": {
        "username": "your_username",
        "password": "your_password",
        "sender_id": "YOUR_SENDER_ID"
    },
    "payment": {
        "merchant_id": "your_merchant_id",
        "username": "your_username",
        "password": "your_password"
    },
    "email": {
        "username": "your_username",
        "password": "your_password",
        "from_email": "sender@example.com"
    }
}

client = NaloSolutions(config)

# Send SMS
response = client.send_sms("233501234567", "Hello Ghana!")

# Make payment
payment_response = client.make_payment(
    amount=10.00,
    customer_number="233501234567",
    customer_name="John Doe",
    item_desc="Product purchase",
    order_id="ORDER_123",
    payby="MTN",
    callback_url="https://yoursite.com/callback"
)

# Send email
email_response = client.send_email(
    to_email="recipient@example.com",
    subject="Test Email",
    message="Hello from Ghana!"
)

# Handle USSD requests (for webhook endpoints)
ussd_response = client.handle_ussd_request({
    "USERID": "test_user",
    "MSISDN": "233501234567",
    "USERDATA": "",
    "MSGTYPE": True,
    "SESSIONID": "session_123"
})
```

### Method 2: Direct Initialization

```python
from nunyakata import NaloSolutions

client = NaloSolutions(
    # SMS credentials
    sms_username="your_username",
    sms_password="your_password",
    sms_sender_id="YOUR_SENDER_ID",

    # Payment credentials
    payment_username="your_username",
    payment_password="your_password",
    payment_merchant_id="your_merchant_id",

    # Email credentials
    email_username="your_email_username",
    email_password="your_email_password",
    email_from_email="sender@example.com"
)
)
```

## Supported Services

### Nalo Solutions

#### SMS Services

- ✅ Text SMS (GET/POST methods)
- ✅ Flash SMS
- ✅ Bulk SMS (individual and batch)
- ✅ Delivery reports and callbacks
- ✅ Username/password and auth key authentication
- ✅ Complete error code handling

#### Payment Services

- ✅ Mobile Money payments (MTN, Vodafone, AirtelTigo)
- ✅ Vodafone voucher and USSD payments
- ✅ Payment callbacks and webhooks
- ✅ Secure secret generation

#### USSD Services

- ✅ USSD request handling framework
- ✅ Session management utilities
- ✅ Menu creation and response formatting
- ✅ Flask webhook integration

#### Email Services

- ✅ JSON-based email sending
- ✅ Email with file attachments
- ✅ Bulk email support
- ✅ HTML email capabilities
- ✅ Template support with placeholders
- ✅ Username/password and auth key authentication
- ✅ Delivery status callbacks

## Examples

See the `examples/` directory for comprehensive usage examples:

- `examples/nalo_solutions_demo.py` - Basic usage examples
- `examples/environment_config_demo.py` - Environment configuration
- `examples/sms_comprehensive_demo.py` - All SMS features
- `examples/email_comprehensive_demo.py` - All email features
- `examples/ussd_comprehensive_demo.py` - USSD application with Flask
- `examples/nalo_webhook_example.py` - Webhook handling

## Documentation

Detailed API documentation available in the `docs/` directory:

- `docs/nalo_solutions.md` - Nalo Solutions API guide
- `docs/nalo_api_compliance.md` - API compliance details
- `docs/sms_api_compliance.md` - SMS API implementation details
- `docs/ussd_api_compliance.md` - USSD API implementation details
- `docs/email_api_compliance.md` - Email API implementation details
- `docs/setup_guide.md` - Complete setup guide

## Configuration

### Environment Variables

See `.env.example` for all available configuration options:

```env
# SMS Configuration
NALO_SMS_USERNAME=your_sms_username
NALO_SMS_PASSWORD=your_sms_password
NALO_SMS_SENDER_ID=YOUR_SENDER_ID

# Payment Configuration
NALO_PAYMENT_USERNAME=your_payment_username
NALO_PAYMENT_PASSWORD=your_payment_password
NALO_PAYMENT_MERCHANT_ID=your_merchant_id

# Email Configuration
NALO_EMAIL_USERNAME=your_email_username
NALO_EMAIL_PASSWORD=your_email_password
NALO_EMAIL_FROM_EMAIL=sender@example.com
NALO_EMAIL_FROM_NAME=Your Name

# USSD Configuration
NALO_USSD_USERID=your_ussd_userid
NALO_USSD_MSISDN=233501234567

# Optional Callbacks
PAYMENT_CALLBACK_URL=https://yoursite.com/webhooks/payment
SMS_DELIVERY_CALLBACK_URL=https://yoursite.com/webhooks/sms
EMAIL_CALLBACK_URL=https://yoursite.com/webhooks/email
```

### Configuration Validation

```python
from nunyakata import NaloSolutions

# Initialize client with configuration
config = {
    "sms": {"username": "test", "password": "test"},
    "payment": {"merchant_id": "123", "username": "test", "password": "test"}
}

client = NaloSolutions(config)
print("Client initialized successfully!")
```

## Development

### Setup

```bash
git clone https://github.com/SeveighTech/nunyakata.git
cd nunyakata
pip install -e ".[dev]"
```

### Testing

```bash
pytest
pytest --cov=nunyakata tests/
```

### Code Quality

```bash
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Development

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/SeveighTech/nunyakata.git
cd nunyakata

# Install in development mode
pip install -e ".[dev,test]"

# Run tests
pytest

# Run with coverage
pytest --cov=src/nunyakata --cov-report=html
```

### Publishing to PyPI

This project uses automated publishing through GitHub Actions. To release:

1. **Prepare the release:**

   ```bash
   python release.py 0.1.0  # Replace with your version
   ```

2. **Commit and tag:**

   ```bash
   git add .
   git commit -m "Release v0.1.0"
   git tag v0.1.0
   git push origin main --tags
   ```

3. **Create GitHub Release:**

   - Go to GitHub Releases
   - Create a new release with the tag
   - The GitHub Action will automatically publish to PyPI

4. **Manual publishing (if needed):**

   ```bash
   # Test PyPI first
   python release.py test

   # Then PyPI
   python release.py publish
   ```

### Test Coverage

Our comprehensive test suite includes:

- ✅ **56 tests** with **100% pass rate**
- ✅ **66% code coverage** on core functionality
- ✅ All four Nalo APIs (Payments, SMS, USSD, Email)
- ✅ Error handling and edge cases
- ✅ Network resilience testing
- ✅ Multiple authentication methods
- ✅ Input validation

## License

MIT License - see LICENSE file for details.

## Support

- **Documentation**: See `docs/` directory
- **Examples**: See `examples/` directory
- **Issues**: GitHub Issues
- **Email**: nunyakata@seveightech.com

## Roadmap

- [ ] Additional payment providers
- [ ] Identity verification services
- [ ] Banking API integrations
- [ ] Government service APIs
- [ ] Utility payment services
