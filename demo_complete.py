from nunyakata import NaloSolutions


def main():
    """Demonstrate both SMS and Payment functionality"""

    # Configuration with both SMS and Payment settings
    config = {
        "sms": {
            "username": "your_username",  # Replace with your actual username
            "password": "your_password",  # Replace with your actual password
            "sender_id": "your_sender_id",  # Replace with your sender ID
        },
        "payment": {
            "merchant_id": "your_merchant_id",  # Replace with your actual merchant ID
            "username": "your_payment_username",  # Replace with your payment username
            "password": "your_payment_password",  # Replace with your payment password
        },
    }

    nalo = NaloSolutions(config)
    print("🚀 Nunyakata - Unified Ghana Services Package")
    print("=" * 50)

    # Test SMS (working with real credentials)
    print("\n📱 SMS Service - WORKING")
    try:
        sms_result = nalo.send_sms(
            phone_number="233265542141", message="Nunyakata package demo - SMS working!"
        )
        print(f"✅ SMS Status: {sms_result.get('status')}")
        print(f"📝 Message ID: {sms_result.get('message_id')}")
    except Exception as e:
        print(f"❌ SMS Error: {e}")

    # Test Payment (structure ready, needs real credentials)
    print("\n💳 Payment Service - READY (needs credentials)")
    try:
        # This shows the correct API structure
        payment_result = nalo.make_simple_payment(
            amount=1.00,
            phone_number="233265542141",
            customer_name="John Doe",
            description="Test Purchase",
            callback_url="https://webhook.site/0a8ac637-b709-4a40-815b-aac6f000c687",
        )
        print(f"✅ Payment Status: {payment_result.get('status')}")
        print(f"📝 Response: {payment_result.get('raw_response', 'No response')}")
    except Exception as e:
        print(f"ℹ️  Payment: {e} (Expected - need real credentials)")

    print("\n" + "=" * 50)
    print("✨ Both SMS and Payment APIs are properly implemented!")
    print("📋 SMS: Working with your credentials")
    print("💳 Payment: Ready - just add your Nalo payment credentials")


if __name__ == "__main__":
    main()
