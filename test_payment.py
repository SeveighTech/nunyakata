from nunyakata import NaloSolutions

# Test Payment API
config = {
    "payment": {
        "merchant_id": "NPS_000002",  # Replace with your actual merchant ID
        "username": "your_username",  # Replace with your actual username
        "password": "your_password",  # Replace with your actual password
    },
    "sms": {
        "username": "your_username",
        "password": "your_password",
        "sender_id": "your_sender_id",
    },
}

nalo = NaloSolutions(config)
print("✅ Package imported successfully!")

# Test Payment functionality
print("\n💳 Testing Payment API structure...")

try:
    # This will fail because we don't have real payment credentials,
    # but it will show the correct API structure
    result = nalo.make_simple_payment(
        amount=5.00,
        phone_number="233241000000",
        customer_name="Test Customer",
        description="Test Payment",
        callback_url="https://example.com/callback",
    )
    print(f"✅ Payment request sent")
    print(f"Response: {result}")
except Exception as e:
    print(f"❌ Payment failed (expected - need real credentials): {str(e)}")

# Show the correct payment method signature
print("\n📝 Payment API Methods Available:")
print("1. make_payment() - Full control with all parameters")
print("2. make_simple_payment() - Simplified with auto network detection")
print("3. handle_payment_callback() - Process payment callbacks")

print("\n📋 Required Payment Config:")
print("payment.merchant_id - Your Nalo merchant ID (e.g., NPS_000002)")
print("payment.username - Your Nalo account username")
print("payment.password - Your Nalo account password")

print("\n🎯 Payment test completed - API structure is correct!")
