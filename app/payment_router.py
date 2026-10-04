from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.payment import create_checkout_session

import stripe


# =========================================================
# PAYMENT ROUTER
# =========================================================

router = APIRouter(
    prefix="/payment",
    tags=["Payment"]
)


# =========================================================
# CREATE STRIPE CHECKOUT SESSION
# =========================================================

@router.post("/create-checkout-session/{subscription_id}")
def create_payment(
    subscription_id: int,
    db: Session = Depends(get_db)
):
    try:

        # -------------------------------------------------
        # 1. FIND SUBSCRIPTION
        # -------------------------------------------------

        subscription = db.query(
            models.Subscription
        ).filter(
            models.Subscription.id == subscription_id
        ).first()

        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="Subscription not found"
            )


        # -------------------------------------------------
        # 2. CHECK SUBSCRIPTION STATUS
        # -------------------------------------------------

        if subscription.status != "Active":
            raise HTTPException(
                status_code=400,
                detail="Subscription is not active"
            )


        # -------------------------------------------------
        # 3. GET SUBSCRIPTION PLAN
        # -------------------------------------------------

        plan = db.query(
            models.SubscriptionPlan
        ).filter(
            models.SubscriptionPlan.plan_id == subscription.plan_id
        ).first()

        if not plan:
            raise HTTPException(
                status_code=404,
                detail="Subscription plan not found"
            )


        # -------------------------------------------------
        # 4. GET PAYMENT AMOUNT
        # -------------------------------------------------

        amount = plan.monthly_fee


        # -------------------------------------------------
        # 5. CHECK IF ALREADY PAID
        # -------------------------------------------------

        existing_payment = db.query(
            models.Payment
        ).filter(
            models.Payment.subscription_id == subscription_id,
            models.Payment.payment_status == "Paid"
        ).first()

        if existing_payment:

            raise HTTPException(
                status_code=400,
                detail="Payment already completed for this subscription"
            )


        # -------------------------------------------------
        # 6. CREATE STRIPE CHECKOUT SESSION
        # -------------------------------------------------

        session = create_checkout_session(
            amount=amount,
            subscription_id=subscription_id
        )


        # -------------------------------------------------
        # 7. SAVE PAYMENT
        # -------------------------------------------------

        new_payment = models.Payment(

            subscription_id=subscription_id,

            amount=amount,

            currency="INR",

            stripe_session_id=session.id,

            payment_status="Pending"
        )

        db.add(new_payment)

        db.commit()

        db.refresh(new_payment)


        # -------------------------------------------------
        # 8. RETURN PAYMENT INFORMATION
        # -------------------------------------------------

        return {
            "message": "Checkout session created successfully",

            "payment_id": new_payment.id,

            "subscription_id": subscription_id,

            "amount": amount,

            "currency": "INR",

            "payment_status": new_payment.payment_status,

            "checkout_url": session.url,

            "session_id": session.id
        }


    except HTTPException:
        raise


    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Payment creation failed: {str(e)}"
        )


# =========================================================
# VERIFY STRIPE PAYMENT
# =========================================================

@router.post("/verify/{session_id}")
def verify_payment(
    session_id: str,
    db: Session = Depends(get_db)
):
    try:

        # -------------------------------------------------
        # 1. FIND PAYMENT IN DATABASE
        # -------------------------------------------------

        payment = db.query(
            models.Payment
        ).filter(
            models.Payment.stripe_session_id == session_id
        ).first()

        if not payment:

            raise HTTPException(
                status_code=404,
                detail="Payment record not found"
            )


        # -------------------------------------------------
        # 2. GET SESSION FROM STRIPE
        # -------------------------------------------------

        session = stripe.checkout.Session.retrieve(
            session_id
        )


        # -------------------------------------------------
        # 3. CHECK PAYMENT STATUS
        # -------------------------------------------------

        if session.payment_status == "paid":

            # Update database payment status
            payment.payment_status = "Paid"

            db.commit()

            db.refresh(payment)

            return {
                "message": "Payment verified successfully",

                "payment_id": payment.id,

                "subscription_id": payment.subscription_id,

                "amount": payment.amount,

                "currency": payment.currency,

                "payment_status": payment.payment_status,

                "stripe_session_id": payment.stripe_session_id
            }


        # -------------------------------------------------
        # PAYMENT NOT COMPLETED
        # -------------------------------------------------

        return {
            "message": "Payment has not been completed",

            "payment_id": payment.id,

            "payment_status": payment.payment_status,

            "stripe_payment_status": session.payment_status
        }


    except HTTPException:
        raise


    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Payment verification failed: {str(e)}"
        )