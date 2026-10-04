import os
import stripe
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Get Stripe secret key from .env
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


# =========================================================
# CREATE STRIPE CHECKOUT SESSION
# =========================================================

def create_checkout_session(
    amount: float,
    subscription_id: int
):

    # Check Stripe secret key
    if not stripe.api_key:
        raise Exception("STRIPE_SECRET_KEY is not configured")

    # Validate amount
    if amount <= 0:
        raise Exception("Amount must be greater than 0")

    # Convert INR to paise
    # Example:
    # ₹300 = 30000 paise
    amount_in_paise = int(round(amount * 100))

    # Create Stripe Checkout Session
    session = stripe.checkout.Session.create(

        # Stripe now manages payment methods
        # from the Stripe Dashboard.
        line_items=[
            {
                "price_data": {
                    "currency": "inr",

                    "product_data": {
                        "name": f"Solar Subscription #{subscription_id}"
                    },

                    "unit_amount": amount_in_paise,
                },

                "quantity": 1,
            }
        ],

        # One-time payment
        mode="payment",

        # Redirect after successful payment
        success_url="http://localhost:8000/payment-success",

        # Redirect if customer cancels payment
        cancel_url="http://localhost:8000/payment-cancel",
    )

    return session