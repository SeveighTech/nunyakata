# Quick Start

Get up and running with Nunyakata in just a few minutes!

## 1. Installation

```bash
pip install nunyakata
```

## 2. Basic Setup

### Option A: Direct Configuration
```python
from nunyakata import NaloSolutions

client = NaloSolutions(
    sms_username="your_username",
    sms_password="your_password",
    sms_source="YOUR_SENDER",
    payment_username="your_payment_username", 
    payment_password="your_payment_password",
    merchant_id="your_merchant_id"
)
```

### Option B: Environment Variables
```bash
# Create .env file
cat > .env << EOF
NALO_SMS_USERNAME=your_username
NALO_SMS_PASSWORD=your_password
NALO_SMS_SOURCE=YOUR_SENDER
NALO_PAYMENT_USERNAME=your_payment_username
NALO_PAYMENT_PASSWORD=your_payment_password
NALO_MERCHANT_ID=your_merchant_id
EOF
```

```python
from nunyakata import load_nalo_client_from_env

client = load_nalo_client_from_env()
```

## 3. Send Your First SMS

```python
response = client.send_sms(
    phone_number="233501234567",
    message="Hello from Nunyakata! 🇬🇭"
)

if response.get('status') == 'success':
    print(f"✅ SMS sent! Message ID: {response.get('message_id')}")
else:
    print(f"❌ Failed: {response.get('message')}")
```

## 4. Process a Payment

```python
payment_response = client.make_payment(
    amount=10.00,
    customer_number="233501234567",
    customer_name="John Doe",
    item_desc="Test Purchase",
    order_id="ORDER_001",
    payby="MTN"  # MTN, VODAFONE, or AIRTELTIGO
)

if payment_response.get('status') == 'success':
    print(f"💰 Payment initiated! Transaction ID: {payment_response.get('transaction_id')}")
```

## 5. Send an Email

```python
email_response = client.send_email(
    recipient="customer@example.com",
    sender="noreply@yourcompany.com",
    subject="Welcome to our service!",
    message="Thank you for choosing us. We're excited to serve you!"
)

if email_response.get('status') == 'success':
    print(f"📧 Email sent! Message ID: {email_response.get('message_id')}")
```

## 🎉 That's it!

You're now ready to integrate Ghanaian services into your application. 

## Next Steps

- **[Configuration Guide](configuration.md)** - Learn about all configuration options
- **[Nalo Solutions Guide](../services/nalo-solutions.md)** - Complete service documentation  
- **[Payment Examples](../examples/payments.md)** - Advanced payment integration
- **[SMS Examples](../examples/sms.md)** - Bulk SMS and advanced features
- **[Error Handling](../api/exceptions.md)** - How to handle errors gracefully

## Need Help?

- 📖 **Documentation**: [https://nunyakata.readthedocs.io/](https://nunyakata.readthedocs.io/)
- 🐛 **Issues**: [GitHub Issues](https://github.com/SeveighTech/nunyakata/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/SeveighTech/nunyakata/discussions)
- 📧 **Email**: info@seveightech.com
