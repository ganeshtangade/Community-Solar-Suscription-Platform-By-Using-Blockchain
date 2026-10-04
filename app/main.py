from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import (
    engine,
    Base,
    get_db
)

from app import models, schemas, crud

# Blockchain
from app.blockchain import record_energy_allocation

# Payment Router
from app.payment_router import router as payment_router


# =====================================================
# DATABASE
# =====================================================

# Create database tables if they do not already exist
Base.metadata.create_all(bind=engine)


# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(
    title="Community Solar Subscription Platform",
    description="Blockchain-based Community Solar Subscription Platform API",
    version="1.0.0"
)


# =====================================================
# PAYMENT ROUTER
# =====================================================

# Register the Payment Router
# All payment APIs will start with /payment
app.include_router(payment_router)


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():

    return {
        "message": "Community Solar Subscription Platform API is running"
    }


# =====================================================
# USERS
# =====================================================

@app.post(
    "/users",
    response_model=schemas.UserResponse
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = crud.get_user_by_email(
        db,
        user.email
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    return crud.create_user(
        db,
        user
    )


@app.get(
    "/users",
    response_model=list[schemas.UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):

    return crud.get_users(db)


@app.get(
    "/users/{user_id}",
    response_model=schemas.UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = crud.get_user(
        db,
        user_id
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# =====================================================
# SUBSCRIPTION PLANS
# =====================================================

@app.post(
    "/plans",
    response_model=schemas.SubscriptionPlanResponse
)
def create_plan(
    plan: schemas.SubscriptionPlanCreate,
    db: Session = Depends(get_db)
):

    return crud.create_plan(
        db,
        plan
    )


@app.get(
    "/plans",
    response_model=list[schemas.SubscriptionPlanResponse]
)
def get_plans(
    db: Session = Depends(get_db)
):

    return crud.get_plans(db)


@app.get(
    "/plans/{plan_id}",
    response_model=schemas.SubscriptionPlanResponse
)
def get_plan(
    plan_id: int,
    db: Session = Depends(get_db)
):

    plan = crud.get_plan(
        db,
        plan_id
    )

    if not plan:

        raise HTTPException(
            status_code=404,
            detail="Subscription plan not found"
        )

    return plan


# =====================================================
# SOLAR PROJECTS
# =====================================================

@app.post(
    "/projects",
    response_model=schemas.SolarProjectResponse
)
def create_project(
    project: schemas.SolarProjectCreate,
    db: Session = Depends(get_db)
):

    return crud.create_project(
        db,
        project
    )


@app.get(
    "/projects",
    response_model=list[schemas.SolarProjectResponse]
)
def get_projects(
    db: Session = Depends(get_db)
):

    return crud.get_projects(db)


@app.get(
    "/projects/{project_id}",
    response_model=schemas.SolarProjectResponse
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = crud.get_project(
        db,
        project_id
    )

    if not project:

        raise HTTPException(
            status_code=404,
            detail="Solar project not found"
        )

    return project


# =====================================================
# SUBSCRIPTIONS
# =====================================================

@app.post(
    "/subscriptions",
    response_model=schemas.SubscriptionResponse
)
def create_subscription(
    subscription: schemas.SubscriptionCreate,
    db: Session = Depends(get_db)
):

    # -------------------------------------------------
    # Check user
    # -------------------------------------------------

    user = crud.get_user(
        db,
        subscription.user_id
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # -------------------------------------------------
    # Check project
    # -------------------------------------------------

    project = crud.get_project(
        db,
        subscription.project_id
    )

    if not project:

        raise HTTPException(
            status_code=404,
            detail="Solar project not found"
        )

    # -------------------------------------------------
    # Check plan
    # -------------------------------------------------

    plan = crud.get_plan(
        db,
        subscription.plan_id
    )

    if not plan:

        raise HTTPException(
            status_code=404,
            detail="Subscription plan not found"
        )

    return crud.create_subscription(
        db,
        subscription
    )


@app.get(
    "/subscriptions",
    response_model=list[schemas.SubscriptionResponse]
)
def get_subscriptions(
    db: Session = Depends(get_db)
):

    return crud.get_subscriptions(db)


@app.get(
    "/subscriptions/{subscription_id}",
    response_model=schemas.SubscriptionResponse
)
def get_subscription(
    subscription_id: int,
    db: Session = Depends(get_db)
):

    subscription = crud.get_subscription(
        db,
        subscription_id
    )

    if not subscription:

        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )

    return subscription


@app.delete(
    "/subscriptions/{subscription_id}"
)
def delete_subscription(
    subscription_id: int,
    db: Session = Depends(get_db)
):

    subscription = crud.get_subscription(
        db,
        subscription_id
    )

    if not subscription:

        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )

    crud.delete_subscription(
        db,
        subscription_id
    )

    return {
        "message": "Subscription deleted successfully"
    }


# =====================================================
# ENERGY GENERATION
# =====================================================

@app.post(
    "/energy-generation",
    response_model=schemas.EnergyGenerationResponse
)
def create_energy_generation(
    generation: schemas.EnergyGenerationCreate,
    db: Session = Depends(get_db)
):

    # -------------------------------------------------
    # Check project
    # -------------------------------------------------

    project = crud.get_project(
        db,
        generation.project_id
    )

    if not project:

        raise HTTPException(
            status_code=404,
            detail="Solar project not found"
        )

    # -------------------------------------------------
    # Create generation
    # -------------------------------------------------

    return crud.create_energy_generation(
        db,
        generation
    )


@app.get(
    "/energy-generation",
    response_model=list[schemas.EnergyGenerationResponse]
)
def get_energy_generations(
    db: Session = Depends(get_db)
):

    return crud.get_energy_generations(db)


@app.get(
    "/energy-generation/{generation_id}",
    response_model=schemas.EnergyGenerationResponse
)
def get_energy_generation(
    generation_id: int,
    db: Session = Depends(get_db)
):

    generation = crud.get_energy_generation(
        db,
        generation_id
    )

    if not generation:

        raise HTTPException(
            status_code=404,
            detail="Energy generation record not found"
        )

    return generation


# =====================================================
# ENERGY ALLOCATION + BLOCKCHAIN
# =====================================================

@app.post(
    "/energy-allocation",
    response_model=schemas.EnergyAllocationResponse
)
def create_energy_allocation(
    allocation: schemas.EnergyAllocationCreate,
    db: Session = Depends(get_db)
):

    # -------------------------------------------------
    # Check energy generation
    # -------------------------------------------------

    generation = db.query(
        models.EnergyGeneration
    ).filter(
        models.EnergyGeneration.id == allocation.generation_id
    ).first()

    if not generation:

        raise HTTPException(
            status_code=404,
            detail="Energy generation record not found"
        )

    # -------------------------------------------------
    # Check subscription
    # -------------------------------------------------

    subscription = crud.get_subscription(
        db,
        allocation.subscription_id
    )

    if not subscription:

        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )

    # -------------------------------------------------
    # Check subscription status
    # -------------------------------------------------

    if subscription.status != "Active":

        raise HTTPException(
            status_code=400,
            detail="Subscription is not active"
        )

    # -------------------------------------------------
    # Check project matching
    # -------------------------------------------------

    if subscription.project_id != generation.project_id:

        raise HTTPException(
            status_code=400,
            detail="Subscription and energy generation belong to different projects"
        )

    # -------------------------------------------------
    # Get subscription plan
    # -------------------------------------------------

    plan = crud.get_plan(
        db,
        subscription.plan_id
    )

    if not plan:

        raise HTTPException(
            status_code=404,
            detail="Subscription plan not found"
        )

    # -------------------------------------------------
    # Check existing allocation
    # -------------------------------------------------

    existing_allocation = db.query(
        models.EnergyAllocation
    ).filter(
        models.EnergyAllocation.generation_id
        == allocation.generation_id,

        models.EnergyAllocation.subscription_id
        == allocation.subscription_id
    ).first()

    if existing_allocation:

        raise HTTPException(
            status_code=400,
            detail="Energy already allocated to this subscription"
        )

    # -------------------------------------------------
    # Calculate already allocated energy
    # -------------------------------------------------

    allocated_energy = db.query(
        models.EnergyAllocation
    ).filter(
        models.EnergyAllocation.generation_id
        == allocation.generation_id
    ).all()

    already_allocated = sum(
        item.allocated_kwh
        for item in allocated_energy
    )

    # -------------------------------------------------
    # Calculate remaining energy
    # -------------------------------------------------

    remaining_energy = (
        generation.energy_kwh
        - already_allocated
    )

    if remaining_energy <= 0:

        raise HTTPException(
            status_code=400,
            detail="No energy available for allocation"
        )

    # -------------------------------------------------
    # Requested energy from subscription plan
    # -------------------------------------------------

    requested_energy = plan.energy_share

    # -------------------------------------------------
    # Actual allocation
    # -------------------------------------------------

    actual_allocation = min(
        requested_energy,
        remaining_energy
    )

    # -------------------------------------------------
    # Create allocation in PostgreSQL
    # -------------------------------------------------

    new_allocation = crud.create_energy_allocation(
        db,
        generation.id,
        subscription.id,
        actual_allocation
    )

    # -------------------------------------------------
    # Blockchain verification
    # -------------------------------------------------

    try:

        blockchain_result = record_energy_allocation(
            new_allocation.id,
            generation.id,
            subscription.id,
            actual_allocation
        )

        # -------------------------------------------------
        # Save blockchain transaction hash
        # -------------------------------------------------

        new_allocation.blockchain_hash = (
            blockchain_result["transaction_hash"]
        )

        # -------------------------------------------------
        # Check blockchain status
        # -------------------------------------------------

        if blockchain_result["status"] == 1:

            new_allocation.verification_status = "Verified"

        else:

            new_allocation.verification_status = "Failed"

        # -------------------------------------------------
        # Save result
        # -------------------------------------------------

        db.commit()

        db.refresh(new_allocation)

    except Exception as e:

        # -------------------------------------------------
        # Blockchain verification failed
        # -------------------------------------------------

        new_allocation.verification_status = "Failed"

        db.commit()

        db.refresh(new_allocation)

        raise HTTPException(
            status_code=500,
            detail=f"Blockchain verification failed: {str(e)}"
        )

    # -------------------------------------------------
    # Return allocation
    # -------------------------------------------------

    return new_allocation


# =====================================================
# GET ENERGY ALLOCATIONS
# =====================================================

@app.get(
    "/energy-allocation",
    response_model=list[schemas.EnergyAllocationResponse]
)
def get_energy_allocations(
    db: Session = Depends(get_db)
):

    return db.query(
        models.EnergyAllocation
    ).all()


@app.get(
    "/energy-allocation/{allocation_id}",
    response_model=schemas.EnergyAllocationResponse
)
def get_energy_allocation(
    allocation_id: int,
    db: Session = Depends(get_db)
):

    allocation = db.query(
        models.EnergyAllocation
    ).filter(
        models.EnergyAllocation.id == allocation_id
    ).first()

    if not allocation:

        raise HTTPException(
            status_code=404,
            detail="Energy allocation not found"
        )

    return allocation


# =====================================================
# DELETE FAILED ENERGY ALLOCATION
# =====================================================

@app.delete(
    "/energy-allocation/{allocation_id}"
)
def delete_energy_allocation(
    allocation_id: int,
    db: Session = Depends(get_db)
):

    allocation = db.query(
        models.EnergyAllocation
    ).filter(
        models.EnergyAllocation.id == allocation_id
    ).first()

    if not allocation:

        raise HTTPException(
            status_code=404,
            detail="Energy allocation not found"
        )

    # Only failed allocations can be deleted
    if allocation.verification_status != "Failed":

        raise HTTPException(
            status_code=400,
            detail="Only failed allocations can be deleted"
        )

    db.delete(allocation)
    db.commit()

    return {
        "message": "Failed energy allocation deleted successfully",
        "allocation_id": allocation_id
    }


# =====================================================
# PROJECT GENERATION ALLOCATIONS
# =====================================================

@app.get(
    "/projects/{project_id}/generation",
    response_model=list[schemas.EnergyAllocationResponse]
)
def get_project_generation_allocations(
    project_id: int,
    db: Session = Depends(get_db)
):

    allocations = db.query(
        models.EnergyAllocation
    ).join(
        models.EnergyGeneration
    ).filter(
        models.EnergyGeneration.project_id == project_id
    ).all()

    return allocations


# =========================================================
# USER DASHBOARD
# =========================================================

@app.get("/dashboard/{user_id}")
def get_user_dashboard(
    user_id: int,
    db: Session = Depends(get_db)
):
    # Find user
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Get user's subscriptions
    subscriptions = db.query(
        models.Subscription
    ).filter(
        models.Subscription.user_id == user_id
    ).all()

    dashboard_data = []

    for subscription in subscriptions:

        # Get plan
        plan = db.query(
            models.SubscriptionPlan
        ).filter(
            models.SubscriptionPlan.plan_id == subscription.plan_id
        ).first()

        # Get project
        project = db.query(
            models.SolarProject
        ).filter(
            models.SolarProject.id == subscription.project_id
        ).first()

        # Get payments
        payments = db.query(
            models.Payment
        ).filter(
            models.Payment.subscription_id == subscription.id
        ).all()

        # Get energy allocations
        allocations = db.query(
            models.EnergyAllocation
        ).filter(
            models.EnergyAllocation.subscription_id == subscription.id
        ).all()

        dashboard_data.append({
            "subscription_id": subscription.id,
            "subscription_status": subscription.status,

            "plan": {
                "plan_id": plan.plan_id if plan else None,
                "plan_name": plan.plan_name if plan else None,
                "monthly_fee": plan.monthly_fee if plan else None,
                "energy_share": plan.energy_share if plan else None
            },

            "solar_project": {
                "project_id": project.id if project else None,
                "project_name": project.project_name if project else None,
                "location": project.location if project else None,
                "capacity_kw": project.capacity_kw if project else None,
                "energy_rate": project.energy_rate if project else None
            },

            "payments": [
                {
                    "payment_id": payment.id,
                    "amount": payment.amount,
                    "currency": payment.currency,
                    "status": payment.payment_status,
                    "stripe_session_id": payment.stripe_session_id
                }
                for payment in payments
            ],

            "energy_allocations": [
                {
                    "allocation_id": allocation.id,
                    "generation_id": allocation.generation_id,
                    "allocated_kwh": allocation.allocated_kwh,
                    "verification_status": allocation.verification_status,
                    "blockchain_hash": allocation.blockchain_hash,
                    "allocated_at": allocation.allocated_at
                }
                for allocation in allocations
            ]
        })

    return {
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        },
        "subscriptions": dashboard_data
    }