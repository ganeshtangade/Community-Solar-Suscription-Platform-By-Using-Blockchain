import os

import stripe

from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


stripe.api_key = os.getenv(
    "STRIPE_SECRET_KEY"
)


# =========================================================
# CREATE CHECKOUT SESSION
# =========================================================

def create_checkout_session(

    amount: float,

    subscription_id: int

):

    # -----------------------------------------------------
    # CHECK STRIPE KEY
    # -----------------------------------------------------

    if not stripe.api_key:

        raise Exception(
            "STRIPE_SECRET_KEY is not configured"
        )


    # -----------------------------------------------------
    # VALIDATE AMOUNT
    # -----------------------------------------------------

    if amount <= 0:

        raise Exception(
            "Amount must be greater than 0"
        )


    # -----------------------------------------------------
    # CONVERT INR TO PAISE
    # -----------------------------------------------------

    amount_in_paise = int(
        round(
            amount * 100
        )
    )


    # -----------------------------------------------------
    # CREATE STRIPE CHECKOUT SESSION
    # -----------------------------------------------------

    session = stripe.checkout.Session.create(

        line_items=[

            {

                "price_data": {

                    "currency": "inr",

                    "product_data": {

                        "name":
                            f"Solar Subscription #{subscription_id}"
                    },

                    "unit_amount":
                        amount_in_paise
                },

                "quantity": 1
            }
        ],

        mode="payment",

        success_url=(
            "http://localhost:5173/payment-success"
            "?session_id={CHECKOUT_SESSION_ID}"
        ),

        cancel_url=(
            "http://localhost:5173/payment-cancel"
        ),

        metadata={

            "subscription_id":
                str(subscription_id)
        }
    )


    return session