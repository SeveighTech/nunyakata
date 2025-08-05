"""
AppsNmobile Orchard API client for Ghana-based transactional services.

This module provides a client for interacting with the AppsNmobile Orchard platform,
which offers various transactional services including mobile money, airtime top-up,
and other payment services.
"""

import hashlib
import hmac
import json
from datetime import datetime
from typing import Any, Dict, Literal, Optional

import requests


class AppsNmobileOrchard:
    """
    Client for interacting with AppsNmobile Orchard APIs.

    The Orchard API uses HMAC-SHA256 authentication with client key and secret key.
    All requests must be signed using the JSON payload and secret key.
    """

    BASE_URL = "https://orchard-api.anmgw.com"

    def __init__(
        self,
        client_key: str,
        secret_key: str,
        environment: Literal["test", "production"] = "test",
        **kwargs: Any
    ) -> None:
        """
        Initialize AppsNmobile Orchard client.

        Args:
            client_key: Your client key from the Orchard Client Portal
            secret_key: Your secret key from the Orchard Client Portal
            environment: API environment ('test' or 'production')
            **kwargs: Additional configuration options
        """
        self.client_key = client_key
        self.secret_key = secret_key
        self.environment = environment

        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "Nunyakata-AppsNmobile-Client/0.1.0",
        })

    def _generate_signature(self, payload: str) -> str:
        """
        Generate HMAC-SHA256 signature for request authentication.

        Args:
            payload: JSON-encoded request payload

        Returns:
            Hex-encoded signature
        """
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def _make_request(
        self,
        endpoint: str,
        method: str = "POST",
        data: Optional[Dict[str, Any]] = None,
        base_url: Optional[str] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Make authenticated request to Orchard API.

        Args:
            endpoint: API endpoint (without base URL)
            method: HTTP method (default: POST)
            data: Request payload
            base_url: Custom base URL (defaults to self.BASE_URL)
            **kwargs: Additional request parameters

        Returns:
            API response as dictionary

        Raises:
            requests.RequestException: If request fails
        """
        url_base = base_url if base_url else self.BASE_URL
        url = f"{url_base}/{endpoint.lstrip('/')}"

        payload = json.dumps(data) if data else "{}"

        signature = self._generate_signature(payload)

        auth_header = f"{self.client_key}:{signature}"

        headers = {
            "Authorization": auth_header,
            "Content-Type": "application/json",
        }

        response = self.session.request(
            method=method,
            url=url,
            data=payload,
            headers=headers,
            **kwargs
        )

        response.raise_for_status()

        try:
            return response.json()
        except json.JSONDecodeError:
            return {"raw_response": response.text}

    def check_wallet_balance(self, service_id: int) -> Dict[str, Any]:
        """
        Check wallet balance for your Orchard account.
        
        This method retrieves information about the current balance on your Orchard account.
        The different types of accounts available are Collections and Payout.
        
        Args:
            service_id: The ID assigned to your service account (available on the dashboard of the Client Portal)
            
        Returns:
            Dictionary containing balance information with the following keys:
            - sms_bal: SMS balance
            - payout_bal: Payout balance
            - billpay_bal: Bill payment balance
            - available_collect_bal: Available collection balance
            - airtime_bal: Airtime balance
            - actual_collect_bal: Actual collection balance
            
        Raises:
            requests.RequestException: If the API request fails
        """

        utc_datetime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        payload = {
            "ts": utc_datetime,
            "service_id": service_id,
            "trans_type": "BLC"
        }

        return self._make_request("check_wallet_balance", data=payload)

    def check_transaction_status(self, exttrid: str, service_id: int) -> Dict[str, Any]:
        """
        Check the status of an existing transaction from Orchard.
        
        This feature is useful in cases where you did not receive the transaction status 
        from Orchard via your callback URL for a certain payment request.
        
        Args:
            exttrid: Unique identifier for an existing transaction from you that had 
                    already been sent to Orchard for processing (max 20 characters)
            service_id: The ID assigned to your service account
            
        Returns:
            Dictionary containing transaction status information with the following keys:
            - trans_status: Transaction status code (e.g., "000/01")
            - trans_ref: Transaction reference number
            - trans_id: Transaction ID
            - message: Status message (e.g., "SUCCESSFUL")
            
        Raises:
            requests.RequestException: If the API request fails
        """
        payload = {
            "exttrid": exttrid,
            "service_id": service_id,
            "trans_type": "TSC"
        }

        return self._make_request("transaction_status", data=payload)

    def send_sms(
        self,
        recipient_number: str,
        msg_body: str,
        unique_id: str,
        sender_id: str,
        service_id: int,
        msg_type: Literal["T", "F"] = "T",
        alert_type: str = "B"
    ) -> Dict[str, Any]:
        """
        Send SMS from the Orchard platform.
        
        Args:
            recipient_number: Mobile number of the recipient (ensure country code is added)
            msg_body: Content of the message to be delivered (max 160 characters per page)
            unique_id: Unique identifier for the SMS request (max 20 characters)
            sender_id: Sender name/alias that appears on the recipient's phone (max 9 characters)
            service_id: The ID assigned to your service account
            msg_type: Type of message ("T" for Text, "F" for Flash message)
            alert_type: Alert type recognized by Orchard platform (default: "B")
            
        Returns:
            Dictionary containing response information with the following keys:
            - resp_desc: Response description (e.g., "Message successfully queued for delivery")
            - resp_code: Response code (e.g., "082")
            
        Raises:
            requests.RequestException: If the API request fails
            
        Note:
            - Messages exceeding 160 characters will be considered multiple pages and attract multiple billing
            - The unique_id must be unique for each SMS request to track the SMS record on the Orchard platform
        """
        payload = {
            "recipient_number": recipient_number,
            "msg_body": msg_body,
            "unique_id": unique_id,
            "sender_id": sender_id,
            "trans_type": "SMS",
            "msg_type": msg_type,
            "service_id": service_id,
            "alert_type": alert_type
        }

        return self._make_request("sendSms", data=payload)

    def process_payment(
        self,
        customer_number: str,
        amount: float,
        exttrid: str,
        reference: str,
        network: Literal["AIR", "VOD", "MTN", "MAS", "BNK", "VIS"],
        trans_type: Literal["MTC", "CTM", "AUD", "AII"],
        callback_url: str,
        service_id: int,
        bank_code: Optional[str] = None,
        recipient_name: Optional[str] = None,
        nickname: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process payment transactions (debit/credit customer wallet).
        
        This API allows clients to make or receive payments for goods/services.
        Supports various transaction types including mobile money, bank transfers, and card payments.
        
        Args:
            customer_number: Mobile money wallet, bank account number, or card number (max 20 characters)
            amount: Transaction amount (max 6 digits, 2 decimal places)
            exttrid: Unique identifier for the transaction (max 20 characters)
            reference: Description for the payment request (max 10 characters, shown on USSD prompt)
            network: Customer's network ("AIR", "VOD", "MTN", "MAS", "BNK", "VIS")
            trans_type: Transaction type:
                - "MTC": Send money to customer's wallet/account
                - "CTM": Take money from customer's wallet/card
                - "AUD": Automatic debit from customer's wallet (subscription required)
                - "AII": Account inquiry information
            callback_url: URL for receiving transaction status updates (max 300 characters)
            service_id: Your service account ID
            bank_code: Bank code (required if trans_type="MTC" and network="BNK")
            recipient_name: Recipient name (required if trans_type="MTC" and network="BNK", max 100 characters)
            nickname: Alias for USSD authorization prompt (max 15 characters, useful for AirtelTigo)
            
        Returns:
            Dictionary containing response information with the following keys:
            - resp_desc: Response description (e.g., "Request successfully received for processing")
            - resp_code: Response code (e.g., "015")
            
        Raises:
            requests.RequestException: If the API request fails
            ValueError: If required parameters are missing for specific transaction types
            
        Note:
            - exttrid must be unique for each payment request for proper tracking
            - For bank transfers (MTC + BNK), both bank_code and recipient_name are mandatory
            - The callback_url will receive transaction status updates
        """
        if trans_type == "MTC" and network == "BNK":
            if not bank_code:
                raise ValueError("bank_code is required for bank transfers (MTC + BNK)")
            if not recipient_name:
                raise ValueError("recipient_name is required for bank transfers (MTC + BNK)")

        utc_datetime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        payload = {
            "customer_number": customer_number,
            "amount": str(amount),
            "exttrid": exttrid,
            "reference": reference,
            "nw": network,
            "trans_type": trans_type,
            "callback_url": callback_url,
            "service_id": service_id,
            "ts": utc_datetime
        }

        if bank_code:
            payload["bank_code"] = bank_code
        if recipient_name:
            payload["recipient_name"] = recipient_name
        if nickname:
            payload["nickname"] = nickname

        return self._make_request("sendRequest", data=payload)

    def process_ghipss_payment(
        self,
        amount: float,
        exttrid: str,
        network: str,
        trans_type: str,
        callback_url: str,
        service_id: int,
        landing_page_url: str
    ) -> Dict[str, Any]:
        """
        Process payment using a GHIPSS card.
        
        This API allows for payment processing using Ghana Interbank Payment and 
        Settlement Systems (GHIPSS) cards.
        
        Args:
            amount: Amount involved in the transaction
            exttrid: Unique identifier for the transaction from you
            network: Network type for the transaction
            trans_type: Transaction type (e.g., "CTM" for Customer to Money)
            callback_url: URL for receiving transaction status updates
            service_id: Your service account ID from the Client Portal Dashboard
            landing_page_url: Final page where customer will see transaction result
            
        Returns:
            Dictionary containing GHIPSS payment response with the following keys:
            - resp_code: Response code (e.g., "000")
            - form_url: URL to redirect customer for payment processing
            - form_details: Dictionary containing payment form details:
                - MerID: Merchant ID
                - AcqID: Acquirer ID
                - OrderID: Order ID
                - MerRespURL: Merchant response URL
                - PurchaseAmt: Purchase amount
                - PurchaseCurrency: Currency code (936 for GHS)
                - PurchaseCurrencyExponent: Currency exponent (2)
                - CaptureFlag: Capture flag ("A")
                - Signature: Payment signature
                - SignatureMethod: Signature method ("SHA1")
                - Version: API version ("1.0.0")
            
        Raises:
            requests.RequestException: If the API request fails
            
        Note:
            - The exttrid must be unique for each GHIPSS payment request
            - Customer will be redirected to form_url for payment processing
            - Transaction status updates will be sent to your callback_url
            - After payment completion, customer will be redirected to landing_page_url
        """
        utc_datetime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        payload = {
            "amount": str(amount),
            "exttrid": exttrid,
            "nw": network,
            "trans_type": trans_type,
            "callback_url": callback_url,
            "service_id": service_id,
            "landing_page_url": landing_page_url,
            "ts": utc_datetime
        }

        return self._make_request("sendRequest", data=payload)

    def pay_bill(
        self,
        amount: float,
        exttrid: str,
        network: Literal[
            "GOT", "GTM", "DST", "MPO", "MPP", "VPO", "VPP", "SFL", "TLS", "STT",
            "ECG", "VBB", "BXO", "EPP", "GHW", "SCP", "WRE"
        ],
        callback_url: str,
        service_id: int,
        account_number: str
    ) -> Dict[str, Any]:
        """
        Process bill payment for various services.
        
        This API allows payment of bills for multiple services including TV subscriptions,
        mobile data, utilities, and other services.
        
        Args:
            amount: Amount to pay (without currency format, e.g., 100.0)
            exttrid: Unique external transaction reference number
            network: Service provider network code:
                - TV Services: "GOT" (GoTV), "GTM" (GoTV Max), "DST" (DSTv), "STT" (Startimes)
                - Mobile Data: "MPP" (MTN Prepaid Data), "VPP" (Vodafone Prepaid Data)
                - Mobile Postpaid: "MPO" (MTN Postpaid), "VPO" (Vodafone Postpaid)
                - Internet: "SFL" (Surfline), "TLS" (Telesol), "VBB" (Vodafone Broadband)
                - Utilities: "ECG" (ECG Postpaid), "EPP" (ECG Prepaid), "GHW" (Ghana Water)
                - Education: "SCP" (School Placement), "WRE" (WAEC Result)
                - Entertainment: "BXO" (Box Office)
            callback_url: URL for receiving transaction status updates
            service_id: Your service account ID from the Client Portal Dashboard
            account_number: Smart card number or account number for the service
            
        Returns:
            Dictionary containing response information with the following keys:
            - resp_desc: Response description (e.g., "Request successfully completed")
            - resp_code: Response code (e.g., "027")
            
        Raises:
            requests.RequestException: If the API request fails
            
        Note:
            - The exttrid must be unique for each bill payment request
            - Transaction status updates will be sent to your callback_url
            - Account number format varies by service provider
            - Amount should be provided without currency symbol
        """
        utc_datetime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        payload = {
            "amount": str(amount),
            "exttrid": exttrid,
            "nw": network,
            "trans_type": "BLP",
            "callback_url": callback_url,
            "service_id": service_id,
            "ts": utc_datetime,
            "account_number": account_number
        }

        return self._make_request("sendRequest", data=payload)

    def create_hosted_checkout(
        self,
        amount: float,
        exttrid: str,
        reference: str,
        callback_url: str,
        service_id: int,
        landing_page: str,
        payment_mode: Literal["CRD", "MOM", "CRM"],
        currency_code: str = "GHS",
        currency_val: Optional[float] = None,
        nickname: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a hosted checkout session for Card and Mobile Money payments.
        
        This API provides a user interface for payments without direct integration complexity.
        It handles both Mobile Money and Card payments through a hosted interface.
        
        Args:
            amount: Transaction amount (max 6 digits, 2 decimal places)
            exttrid: Unique identifier for the transaction (max 20 characters)
            reference: Description for the payment request (max 10 characters, shown on USSD prompt)
            callback_url: URL for receiving transaction status updates (max 300 characters)
            service_id: Your service account ID from the Client Portal Dashboard
            landing_page: URL to redirect customer after payment completion (max 300 characters)
            payment_mode: Payment mode:
                - "CRD": Only display Card payment form
                - "MOM": Only display Mobile Money payment form
                - "CRM": Display both Mobile Money and Card payment forms
            currency_code: Currency code to display (e.g., "GHS", "EUR", "USD"), defaults to "GHS"
            currency_val: Amount in the specified currency (max 6 digits, 2 decimal places)
            nickname: Alias for USSD authorization prompt (max 15 characters, useful for AirtelTigo)
            
        Returns:
            Dictionary containing checkout response with the following keys:
            - resp_code: Response code (e.g., "000")
            - resp_desc: Response description (e.g., "Passed")
            - redirect_url: URL to redirect customer for payment processing
            
        Raises:
            requests.RequestException: If the API request fails
            
        Note:
            - This method provides a hosted payment interface, eliminating direct integration complexity
            - Card payment requires PCIDSS compliance proof for direct integration
            - The exttrid must be unique for each payment request
            - Customer will be redirected to the redirect_url for payment processing
            - Transaction status updates will be sent to your callback_url
        """
        utc_datetime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        payload = {
            "amount": str(amount),
            "exttrid": exttrid,
            "reference": reference,
            "callback_url": callback_url,
            "service_id": service_id,
            "ts": utc_datetime,
            "landing_page": landing_page,
            "payment_mode": payment_mode,
            "currency_code": currency_code
        }

        if currency_val is not None:
            payload["currency_val"] = str(currency_val)
        if nickname:
            payload["nickname"] = nickname

        return self._make_request("third_party_request", data=payload, base_url="https://payments.anmgw.com")

    def create_auto_debit_subscription(
        self,
        customer_number: str,
        amount: float,
        network: Literal["AIR", "VOD", "MTN"],
        cycle: Literal["DLY", "WKL", "MON"],
        start_date: str,
        reference: str,
        return_url: str,
        service_id: int,
        uniq_ref_id: str,
        end_date: Optional[str] = None,
        resumable: Optional[Literal["Y", "N"]] = None,
        cycle_skip: Optional[Literal["Y", "N"]] = None,
        apply_penalty: Optional[Literal["Y", "N"]] = None
    ) -> Dict[str, Any]:
        """
        Create an auto debit subscription for recurring payments from customer's mobile money wallet.
        
        This service enables automatic recurring debits from a customer's wallet without prior authorization
        after initial subscription. Suitable for loan repayment, hire purchase, insurance, etc.
        
        Args:
            customer_number: Customer's mobile money number (max 20 characters)
            amount: Recurring amount to be deducted (max 6 digits, 2 decimal places)
            network: Customer's network ("AIR", "VOD", "MTN")
            cycle: Frequency of recurring debit:
                - "DLY": Daily
                - "WKL": Weekly
                - "MON": Monthly
            start_date: Date and time when recurring debit will commence (format: YYYY-MM-DD)
            reference: Description for the subscription (max 10 characters, shows in all transactions)
            return_url: URL for receiving subscription status and transaction updates (max 300 characters)
            service_id: Your service account ID from the Client Portal Dashboard
            uniq_ref_id: Unique identifier for the subscription (max 20 characters, must be unique per customer)
            end_date: Optional end date for the subscription (format: YYYY-MM-DD, if not set, no end date)
            resumable: Allow customer to suspend/resume recurring debit ("Y" or "N")
            cycle_skip: Skip outstanding debits when current schedule is due ("Y" or "N")
            apply_penalty: Apply penalty amount upon customer default ("Y" or "N")
            
        Returns:
            Dictionary containing subscription response
            
        Raises:
            requests.RequestException: If the API request fails
            
        Note:
            - This triggers an SMS with OTP to the customer for validation
            - Customer needs an interface to enter and validate the OTP
            - After validation, automatic debits will occur according to the cycle
            - The uniq_ref_id must be unique for each customer subscription
            - All subsequent transaction statuses will be sent to the return_url
        """
        utc_datetime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        payload = {
            "service_id": service_id,
            "uniq_ref_id": uniq_ref_id,
            "ts": utc_datetime,
            "customer_number": customer_number,
            "amount": str(amount),
            "nw": network,
            "cycle": cycle,
            "start_date": start_date,
            "reference": reference,
            "return_url": return_url,
            "operation": "SUB"
        }

        if end_date:
            payload["end_date"] = end_date
        if resumable:
            payload["resumable"] = resumable
        if cycle_skip:
            payload["cycle_skip"] = cycle_skip
        if apply_penalty:
            payload["apply_penalty"] = apply_penalty

        return self._make_request("autoDebit", data=payload)

    def top_up_airtime(
        self,
        customer_number: str,
        amount: float,
        exttrid: str,
        reference: str,
        network: Literal["AIR", "VOD", "MTN", "GLO"],
        callback_url: str,
        service_id: int
    ) -> Dict[str, Any]:
        """
        Send airtime top-up to a customer's mobile number.
        
        This API allows airtime to be sent to a customer for electronic airtime refill.
        Supports all major mobile networks in Ghana.
        
        Args:
            customer_number: Customer's mobile number that will receive the airtime (max 20 characters)
            amount: Amount of airtime to top up (minimum GHS 0.2, max 6 digits, 2 decimal places)
            exttrid: Unique identifier for the transaction (max 20 characters)
            reference: Description for the top-up request (max 10 characters)
            network: Customer's network ("AIR", "VOD", "MTN", "GLO")
            callback_url: URL for receiving transaction status updates (max 300 characters)
            service_id: Your service account ID from the Client Portal Dashboard
            
        Returns:
            Dictionary containing response information with the following keys:
            - resp_desc: Response description (e.g., "Request successfully completed")
            - resp_code: Response code (e.g., "027")
            
        Raises:
            requests.RequestException: If the API request fails
            ValueError: If amount is less than minimum required (GHS 0.2)
            
        Note:
            - Minimum airtime amount allowed is GHS 0.2
            - The exttrid must be unique for each airtime top-up request
            - Transaction status updates will be sent to your callback_url
            - Supports AirtelTigo, Vodafone, MTN, and Glo networks
        """
        if amount < 0.2:
            raise ValueError("Minimum airtime amount allowed is GHS 0.2")
        
        utc_datetime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        payload = {
            "customer_number": customer_number,
            "amount": str(amount),
            "exttrid": exttrid,
            "reference": reference,
            "nw": network,
            "trans_type": "ATP",
            "callback_url": callback_url,
            "service_id": service_id,
            "ts": utc_datetime
        }

        return self._make_request("sendRequest", data=payload)

    def validate_auto_debit_otp(
        self,
        uniq_ref_id: str,
        service_id: int
    ) -> Dict[str, Any]:
        """
        Validate OTP for auto debit subscription activation.
        
        This method validates the OTP sent to the customer via SMS during subscription creation.
        A successful OTP validation activates the subscription and enables automatic recurring debits.
        
        Args:
            uniq_ref_id: Unique identifier for the recurring debit subscription (max 20 characters)
            service_id: Your service account ID from the Client Portal Dashboard
            
        Returns:
            Dictionary containing OTP validation response
            
        Raises:
            requests.RequestException: If the API request fails
            
        Note:
            - This validates the OTP sent to the customer during subscription creation
            - Successful validation activates the subscription and enables automatic debits
            - Status confirmation is sent to the return_url specified in the subscription
            - The uniq_ref_id must match the one used in the subscription creation
        """
        payload = {
            "service_id": service_id,
            "uniq_ref_id": uniq_ref_id,
            "operation": "OTP"
        }

        return self._make_request("autoDebit", data=payload)

    def suspend_auto_debit_subscription(
        self,
        uniq_ref_id: str,
        service_id: int
    ) -> Dict[str, Any]:
        """
        Suspend an active auto debit subscription.
        
        This method puts the recurring debit cycle on hold, temporarily stopping
        automatic payments from the customer's wallet.
        
        Args:
            uniq_ref_id: Unique identifier for the recurring debit subscription (max 20 characters)
            service_id: Your service account ID from the Client Portal Dashboard
            
        Returns:
            Dictionary containing suspension response
            
        Raises:
            requests.RequestException: If the API request fails
            
        Note:
            - This temporarily stops automatic recurring debits
            - The subscription can be resumed later using the resume operation
            - Only works if the subscription was created with resumable="Y"
            - The uniq_ref_id must match an existing active subscription
        """
        payload = {
            "service_id": service_id,
            "uniq_ref_id": uniq_ref_id,
            "operation": "SUS"
        }

        return self._make_request("autoDebit", data=payload)

    def resume_auto_debit_subscription(
        self,
        uniq_ref_id: str,
        service_id: int
    ) -> Dict[str, Any]:
        """
        Resume a suspended auto debit subscription.
        
        This method re-enables the recurring debit cycle, restarting automatic
        payments from the customer's wallet after a previous suspension.
        
        Args:
            uniq_ref_id: Unique identifier for the recurring debit subscription (max 20 characters)
            service_id: Your service account ID from the Client Portal Dashboard
            
        Returns:
            Dictionary containing resume response
            
        Raises:
            requests.RequestException: If the API request fails
            
        Note:
            - This re-enables automatic recurring debits after suspension
            - Only works on subscriptions that were previously suspended
            - The subscription must have been created with resumable="Y"
            - The uniq_ref_id must match a previously suspended subscription
        """
        payload = {
            "service_id": service_id,
            "uniq_ref_id": uniq_ref_id,
            "operation": "RES"
        }

        return self._make_request("autoDebit", data=payload)

    def verify_ghana_card(
        self,
        id_num: str,
        image: str,
        service_id: int,
        exttrid: str,
        id_type: str = "GCA"
    ) -> Dict[str, Any]:
        """
        Perform real-time live verification of a person using Ghana Card.
        
        This API verifies a person's identity by comparing their live photo with their Ghana Card data.
        
        Args:
            id_num: Ghana Card ID number (max 13 characters, format: GHA-xxxxxxxxx-x)
            image: Base64-encoded live photo of the person
            service_id: Your service account ID from the Client Portal Dashboard
            exttrid: Unique identifier for the verification request (max 20 characters)
            id_type: ID type (default: "GCA" for Ghana Card)
            
        Returns:
            Dictionary containing verification response with the following keys:
            - resp_code: Response code (e.g., "027")
            - resp_desc: Response description (e.g., "Request successfully completed")
            - data: Dictionary containing verification data:
                - name: Person's name
                - gender: Person's gender ("M" or "F")
                - verified: Verification status ("true" or "false")
                - card_valid_start: Card validity start date (YYYY-MM-DD)
                - card_valid_end: Card validity end date (YYYY-MM-DD)
            
        Raises:
            requests.RequestException: If the API request fails
            
        Note:
            - The exttrid must be unique for each verification request
            - The image must be a base64-encoded live photo
            - This is a real-time verification that compares live photo with card data
        """
        utc_datetime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        payload = {
            "service_id": service_id,
            "trans_type": "AII",
            "id_num": id_num,
            "id_type": id_type,
            "exttrid": exttrid,
            "image": image,
            "ts": utc_datetime
        }

        return self._make_request("verifyID", data=payload)

    def process_remittance(
        self,
        customer_number: str,
        amount: float,
        transf_amount: float,
        exttrid: str,
        reference: str,
        network: Literal["AIR", "VOD", "MTN", "BNK"],
        callback_url: str,
        service_id: int,
        sender_name: str,
        recipient_name: str,
        sender_number: str,
        recipient_address: str,
        ctry_origin_code: str,
        sender_gender: Literal["M", "F"],
        recipient_gender: Literal["M", "F"],
        transf_curr_code: str,
        transf_purpose: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process international remittance payments to Ghana.
        
        This API terminates payments from other countries into mobile money wallets 
        or bank accounts of persons in Ghana. Requires MTO licensing documentation.
        
        Args:
            customer_number: Receiving party account number (mobile money or bank account, max 20 chars)
            amount: Amount received by receiving party (max 6 digits, 2 decimal places)
            transf_amount: Amount the recipient will receive (max 10 digits, 2 decimal places)
            exttrid: Unique transaction identifier for tracing (max 25 characters)
            reference: Description for the payment request (max 10 characters)
            network: Network code of receiving party ("AIR", "VOD", "MTN", "BNK")
            callback_url: URL for transaction status updates (max 300 characters)
            service_id: Your service account ID from the Client Portal Dashboard
            sender_name: Sender's name (max 15 characters)
            recipient_name: Recipient's name (max 200 characters)
            sender_number: Sender's number (max 200 characters)
            recipient_address: Receiving party contact address (max 9 characters)
            ctry_origin_code: Three-letter ISO country code (e.g., "GBR", "USA")
            sender_gender: Gender of sending party ("M" or "F")
            recipient_gender: Recipient's gender ("M" or "F")
            transf_curr_code: Three-letter ISO currency code (e.g., "GBP", "USD")
            transf_purpose: Purpose of fund transfer (optional, max 25 characters)
            
        Returns:
            Dictionary containing response information with the following keys:
            - resp_desc: Response description (e.g., "Request successfully received for processing")
            - resp_code: Response code (e.g., "015")
            
        Raises:
            requests.RequestException: If the API request fails
            
        Note:
            - This service requires MTO (Money Transfer Operator) licensing documentation
            - The exttrid must be unique for each remittance transaction
            - Callback URL will receive transaction status updates
            - Supports both mobile money wallets and bank accounts in Ghana
        """
        utc_datetime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        payload = {
            "customer_number": customer_number,
            "amount": str(amount),
            "transf_amount": str(transf_amount),
            "exttrid": exttrid,
            "reference": reference,
            "nw": network,
            "trans_type": "RMT",
            "callback_url": callback_url,
            "service_id": service_id,
            "ts": utc_datetime,
            "sender_name": sender_name,
            "recipient_name": recipient_name,
            "sender_number": sender_number,
            "recipient_address": recipient_address,
            "ctry_origin_code": ctry_origin_code,
            "sender_gender": sender_gender,
            "recipient_gender": recipient_gender,
            "transf_curr_code": transf_curr_code
        }

        if transf_purpose:
            payload["transf_purpose"] = transf_purpose

        return self._make_request("sendRequest", data=payload)

    def inquire_account_info(
        self,
        customer_number: str,
        service_id: int,
        bank_code: str,
        exttrid: str
    ) -> Dict[str, Any]:
        """
        Retrieve the name on customer's bank account.
        
        This method performs an account information inquiry to get the account holder's name
        for a given bank account number.
        
        Args:
            customer_number: Customer's bank account number (max 20 characters)
            service_id: Your service account ID from the Client Portal Dashboard
            bank_code: Bank code for the customer's bank (3 characters)
            exttrid: Unique identifier for the inquiry operation (max 20 characters)
            
        Returns:
            Dictionary containing response information with the following keys:
            - resp_code: Response code (e.g., "027")
            - resp_desc: Response description (e.g., "Request successfully completed")
            - name: Account holder's name (e.g., "John Doe")
            
        Raises:
            requests.RequestException: If the API request fails
            
        Note:
            - This method is specifically for bank account inquiries (network is automatically set to "BNK")
            - The exttrid must be unique for each inquiry operation
            - Only works with bank accounts, not mobile money wallets
        """
        utc_datetime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        payload = {
            "customer_number": customer_number,
            "service_id": service_id,
            "trans_type": "AII",
            "bank_code": bank_code,
            "nw": "BNK",  # Bank network is required for account inquiry
            "ts": utc_datetime,
            "exttrid": exttrid
        }

        return self._make_request("sendRequest", data=payload)

    def cancel_auto_debit_subscription(
        self,
        uniq_ref_id: str,
        service_id: int
    ) -> Dict[str, Any]:
        """
        Cancel an auto debit subscription permanently.
        
        This method permanently cancels the recurring debit subscription.
        This operation is not reversible and will stop all future automatic payments.
        
        Args:
            uniq_ref_id: Unique identifier for the recurring debit subscription (max 20 characters)
            service_id: Your service account ID from the Client Portal Dashboard
            
        Returns:
            Dictionary containing cancellation response
            
        Raises:
            requests.RequestException: If the API request fails
            
        Note:
            - This permanently cancels the subscription and stops all future payments
            - This operation is NOT reversible - use suspend/resume for temporary stops
            - The uniq_ref_id must match an existing active or suspended subscription
            - Consider using suspend operation instead if you need temporary stoppage
        """
        payload = {
            "service_id": service_id,
            "uniq_ref_id": uniq_ref_id,
            "operation": "CAN"
        }

        return self._make_request("autoDebit", data=payload)

    def get_auto_debit_status(
        self,
        uniq_ref_id: str,
        service_id: int
    ) -> Dict[str, Any]:
        """
        Retrieve the status of a recurring debit subscription.
        
        This method returns comprehensive information about the subscription including
        profile details and transaction history.
        
        Args:
            uniq_ref_id: Unique identifier for the recurring debit subscription (max 20 characters)
            service_id: Your service account ID from the Client Portal Dashboard
            
        Returns:
            Dictionary containing subscription status with the following structure:
            - profile: Dictionary containing subscription profile information:
                - amount: Subscription amount
                - callback_url: Callback URL for notifications
                - cancel_date: Date when subscription was canceled (if applicable)
                - completed: Whether subscription is completed
                - customer_number: Customer's mobile number
                - cycle: Payment cycle (Daily, Weekly, Monthly)
                - cycle_skip: Whether cycle skipping is enabled
                - end_date: Subscription end date
                - nw: Network (MTN, VOD, AIR)
                - resumable: Whether subscription is resumable
                - service_id: Service account ID
                - service_name: Name of the service
                - start_date: Subscription start date
                - status: Current status (Active, Suspended, Canceled, etc.)
                - subscription_date: Date when subscription was created
                - uniq_ref_id: Unique reference ID
            - transactions: List of transaction records with:
                - prev_schedule: Previous schedule date
                - processing_id: Processing ID
                - trans_date: Transaction date
                - trans_id: Transaction ID
                - trans_msg: Transaction message
                - trans_ref: Transaction reference
                - trans_status: Transaction status
            
        Raises:
            requests.RequestException: If the API request fails
            
        Note:
            - Provides complete subscription profile and transaction history
            - Useful for monitoring subscription health and payment status
            - Can be used to verify subscription details and troubleshoot issues
        """
        payload = {
            "service_id": service_id,
            "uniq_ref_id": uniq_ref_id,
            "operation": "STA"
        }

        return self._make_request("autoDebit", data=payload)

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.session.close()
