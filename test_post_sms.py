from nunyakata import NaloSolutions

# Test POST method
config = {
    "sms": {
        "username": "your_username",
        "password": "your_password",
        "sender_id": "your_sender_id",
    },
    "payment": {"public_key": "test", "private_key": "test"},
}

nalo = NaloSolutions(config)
print("✅ Package imported successfully!")

# Test SMS sending with POST method
test_number = "233265542141"
message = "POST method test - Nalo integration COMPLETED!"

print(f"\n📱 Testing SMS POST method to {test_number}...")
print(f"Message: {message}")

try:
    print(f"\n🚀 Sending SMS via POST to {test_number}...")
    result = nalo.send_sms(
        phone_number=test_number, message=message, method="POST"  # Use POST method
    )
    print(f"✅ SMS sent successfully via POST")
    print(f"Response: {result}")
except Exception as e:
    print(f"❌ Failed to send SMS via POST: {str(e)}")

print("\n🎉 POST method test completed!")
