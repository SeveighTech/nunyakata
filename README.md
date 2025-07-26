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
from nunyakata import load_nalo_client_from_env

# Automatically loads credentials from environment
client = load_nalo_client_from_env()

# Send SMS
response = client.send_sms("233501234567", "Hello Ghana!")
print(client.explain_sms_response(response))

# Make payment
payment_response = client.make_payment(
    order_id="ORDER_123",
    key="1234",
    phone_number="233501234567",
    item_desc="Product purchase",
    amount="10.00",
    network="MTN",
    customer_name="John Doe"
)
```

### Method 2: Direct Initialization

```python
from nunyakata import NaloSolutionsClient

client = NaloSolutionsClient(
    # SMS credentials
    sms_auth_key="your_auth_key_here",
    sms_source="YOUR_SENDER_ID",

    # Payment credentials
    payment_username="your_username",
    payment_password="your_password",
    merchant_id="your_merchant_id"
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
# Required for SMS
NALO_SMS_AUTH_KEY=your_auth_key
NALO_SMS_SOURCE=YOUR_SENDER_ID

# Required for Payments
NALO_PAYMENT_USERNAME=your_username
NALO_PAYMENT_PASSWORD=your_password
NALO_MERCHANT_ID=your_merchant_id

# Required for Email
NALO_EMAIL_AUTH_KEY=your_email_auth_key
# OR
NALO_EMAIL_USERNAME=your_email_username
NALO_EMAIL_PASSWORD=your_email_password

# Optional
PAYMENT_CALLBACK_URL=https://yoursite.com/webhooks/payment
SMS_DELIVERY_CALLBACK_URL=https://yoursite.com/webhooks/sms
```

### Configuration Validation

```python
from nunyakata import validate_env_config, get_env_config

# Check if configuration is valid
is_valid, missing = validate_env_config()
if not is_valid:
    print(f"Missing variables: {missing}")

# Get current configuration status
config = get_env_config()
print(f"Available services: {config['services']}")
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

- ✅ **63 tests** with **100% pass rate**
- ✅ **85% code coverage** on core functionality
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
- **Email**: etsejoey@outlook.com

## Roadmap

- [ ] Additional payment providers
- [ ] Identity verification services
- [ ] Banking API integrations
- [ ] Government service APIs
- [ ] Utility payment services
