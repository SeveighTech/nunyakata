# Nunyakata Documentation

Welcome to the official documentation for **Nunyakata** - Ghana's comprehensive API integration library.

## 🇬🇭 What is Nunyakata?

Nunyakata is a unified Python library that simplifies integration with popular Ghanaian service APIs. It provides a consistent interface for:

- **💳 Payment Services** - Mobile money, bank transfers, and payment gateways
- **📱 SMS Services** - Bulk SMS, notifications, and messaging
- **📧 Email Services** - Transactional emails, bulk emails, and templates
- **📞 USSD Services** - Interactive USSD applications and session management

## 🚀 Quick Start

Get started with Nunyakata in minutes:

```python
from nunyakata import NaloSolutions

# Initialize client
client = NaloSolutions(
    sms_username="your_username",
    sms_password="your_password",
    payment_username="your_payment_username",
    payment_password="your_payment_password",
    merchant_id="your_merchant_id"
)

# Send SMS
response = client.send_sms("233501234567", "Hello Ghana!")

# Make payment
payment = client.make_payment(
    amount=10.00,
    phone_number="233501234567",
    wallet_type="mtn"
)

# Send email
email = client.send_email(
    recipient="user@example.com",
    subject="Welcome!",
    message="Thank you for joining us!"
)
```

## 📦 Installation

Install Nunyakata using pip:

```bash
pip install nunyakata
```

For environment variable support:

```bash
pip install nunyakata[env]
```

## 🏗️ Currently Supported Services

### ✅ Completed Integrations
- **Nalo Solutions** - Payments, SMS, Email, USSD

### 🚧 Planned Integrations
- **Hubtel** - Payment gateway and messaging
- **ExpressPay** - Payment processing
- **PaySwitch** - Payment services
- **Flutterwave** - Payment gateway
- **Paystack** - Payment processing

[View all planned integrations →](https://github.com/SeveighTech/nunyakata/blob/main/integrations.yaml)

## 📖 Documentation Sections

- **[Getting Started](getting-started/installation.md)** - Installation and basic setup
- **[Services](services/nalo-solutions.md)** - Detailed service documentation
- **[API Reference](api/clients.md)** - Complete API documentation
- **[Examples](examples/payments.md)** - Code examples and tutorials
- **[Contributing](contributing/setup.md)** - How to contribute to the project

## 🤝 Contributing

Nunyakata is open source and welcomes contributions! Whether you want to:

- Add new service integrations
- Improve documentation
- Report bugs or suggest features
- Write tests

Check out our [Contributing Guide](contributing/setup.md) to get started.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/SeveighTech/nunyakata/blob/main/LICENSE) file for details.

## 🔗 Links

- **📦 PyPI Package**: [https://pypi.org/project/nunyakata/](https://pypi.org/project/nunyakata/)
- **🐙 GitHub Repository**: [https://github.com/SeveighTech/nunyakata](https://github.com/SeveighTech/nunyakata)
- **📋 Issue Tracker**: [https://github.com/SeveighTech/nunyakata/issues](https://github.com/SeveighTech/nunyakata/issues)
- **💬 Discussions**: [https://github.com/SeveighTech/nunyakata/discussions](https://github.com/SeveighTech/nunyakata/discussions)

---

*Built with ❤️ for the Ghanaian developer community*
