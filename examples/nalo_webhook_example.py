"""
Example Flask webhook for handling Nalo Solutions payment callbacks.

This demonstrates how to set up a webhook endpoint to receive payment
status updates from Nalo Solutions.
"""

from flask import Flask, request, jsonify
from nunyakata import NaloSolutionsClient
import os

app = Flask(__name__)

# Initialize Nalo client
nalo_client = NaloSolutionsClient(
    payment_username=os.getenv("NALO_PAYMENT_USERNAME"),
    payment_password=os.getenv("NALO_PAYMENT_PASSWORD"),
    merchant_id=os.getenv("NALO_MERCHANT_ID"),
)


@app.route("/nalo-payment-callback", methods=["POST"])
def handle_payment_callback():
    """
    Handle payment callback from Nalo Solutions.

    Expected callback format:
    {
        "Timestamp": "2018-01-04 11:24:47",
        "Status": "PAID" or "FAILED",
        "InvoiceNo": "203343123",
        "Order_id": "myoder_15150"
    }
    """
    try:
        callback_data = request.get_json()

        # Validate required fields
        required_fields = ["Timestamp", "Status", "InvoiceNo", "Order_id"]
        if not all(field in callback_data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Extract callback information
        timestamp = callback_data["Timestamp"]
        status = callback_data["Status"]
        invoice_no = callback_data["InvoiceNo"]
        order_id = callback_data["Order_id"]

        print(f"Payment Callback Received:")
        print(f"  Order ID: {order_id}")
        print(f"  Status: {status}")
        print(f"  Invoice: {invoice_no}")
        print(f"  Timestamp: {timestamp}")

        # Handle payment status
        if status == "PAID":
            # Payment successful - update your database, send confirmation email, etc.
            handle_successful_payment(order_id, invoice_no, timestamp)

        elif status == "FAILED":
            # Payment failed - update status, notify user, etc.
            handle_failed_payment(order_id, invoice_no, timestamp)

        else:
            # Handle other statuses like "ACCEPTED"
            handle_other_payment_status(order_id, status, invoice_no, timestamp)

        # Use the client's callback handler
        response = nalo_client.handle_payment_callback(callback_data)
        return jsonify(response)

    except Exception as e:
        print(f"Error handling callback: {e}")
        # Still return OK to acknowledge receipt
        return jsonify({"Response": "OK"})


def handle_successful_payment(order_id: str, invoice_no: str, timestamp: str):
    """Handle successful payment processing."""
    print(f"✅ Payment successful for order {order_id}")

    # Example actions:
    # 1. Update database with payment confirmation
    # 2. Send confirmation email to customer
    # 3. Trigger order fulfillment process
    # 4. Update inventory
    # 5. Send SMS confirmation

    # Example database update (pseudo-code)
    # db.execute("UPDATE orders SET status = 'paid', invoice_no = ?, paid_at = ? WHERE order_id = ?",
    #           invoice_no, timestamp, order_id)

    # Example notification
    # send_payment_confirmation_email(order_id)


def handle_failed_payment(order_id: str, invoice_no: str, timestamp: str):
    """Handle failed payment processing."""
    print(f"❌ Payment failed for order {order_id}")

    # Example actions:
    # 1. Update database with failure status
    # 2. Send payment failure notification to customer
    # 3. Release any reserved inventory
    # 4. Log the failure for analysis

    # Example database update (pseudo-code)
    # db.execute("UPDATE orders SET status = 'failed', failed_at = ? WHERE order_id = ?",
    #           timestamp, order_id)

    # Example notification
    # send_payment_failure_email(order_id)


def handle_other_payment_status(
    order_id: str, status: str, invoice_no: str, timestamp: str
):
    """Handle other payment statuses like ACCEPTED."""
    print(f"ℹ️ Payment status '{status}' for order {order_id}")

    if status == "ACCEPTED":
        # Payment request accepted, waiting for user confirmation
        print(f"Payment request accepted, waiting for user confirmation...")

        # Update status to pending
        # db.execute("UPDATE orders SET status = 'pending' WHERE order_id = ?", order_id)


@app.route("/test-payment", methods=["POST"])
def test_payment():
    """Test endpoint to initiate a payment."""
    try:
        data = request.get_json()

        result = nalo_client.make_payment(
            order_id=data.get("order_id", "test_order_123"),
            key=data.get("key", "1234"),
            phone_number=data.get("phone_number", "233241000000"),
            item_desc=data.get("item_desc", "Test Payment"),
            amount=data.get("amount", "5.00"),
            network=data.get("network", "MTN"),
            customer_name=data.get("customer_name", "Test Customer"),
            callback_url="https://yoursite.com/nalo-payment-callback",
        )

        return jsonify({"success": True, "result": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/test-vodafone-voucher", methods=["POST"])
def test_vodafone_voucher():
    """Test endpoint for Vodafone voucher payment."""
    try:
        data = request.get_json()

        result = nalo_client.create_vodafone_voucher_payment(
            order_id=data.get("order_id", "voda_test_123"),
            key=data.get("key", "5678"),
            phone_number=data.get("phone_number", "233241000000"),
            voucher_code=data.get("voucher_code", "TEST123"),
            amount=data.get("amount", "10.00"),
            customer_name=data.get("customer_name", "Vodafone User"),
        )

        return jsonify({"success": True, "result": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/test-vodafone-ussd", methods=["POST"])
def test_vodafone_ussd():
    """Test endpoint for Vodafone USSD payment."""
    try:
        data = request.get_json()

        result = nalo_client.create_vodafone_ussd_payment(
            order_id=data.get("order_id", "voda_ussd_123"),
            key=data.get("key", "9012"),
            phone_number=data.get("phone_number", "233241000000"),
            item_desc=data.get("item_desc", "USSD Test Payment"),
            amount=data.get("amount", "15.00"),
            customer_name=data.get("customer_name", "USSD User"),
        )

        return jsonify({"success": True, "result": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "nalo-webhook"})


if __name__ == "__main__":
    print("🚀 Starting Nalo Solutions webhook server...")
    print("📝 Available endpoints:")
    print("  POST /nalo-payment-callback - Payment status webhook")
    print("  POST /test-payment - Test payment initiation")
    print("  POST /test-vodafone-voucher - Test Vodafone voucher payment")
    print("  POST /test-vodafone-ussd - Test Vodafone USSD payment")
    print("  GET  /health - Health check")
    print(
        "\n🔗 Make sure to set your callback URL to: https://yoursite.com/nalo-payment-callback"
    )
    print("\n⚠️  Remember to set environment variables:")
    print("   NALO_PAYMENT_USERNAME")
    print("   NALO_PAYMENT_PASSWORD")
    print("   NALO_MERCHANT_ID")

    app.run(debug=True, port=5000)
