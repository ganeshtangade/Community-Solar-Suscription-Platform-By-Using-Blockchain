from fastapi import (
    FastAPI,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from fastapi.middleware.cors import (
    CORSMiddleware
)

from app.database import (
    engine,
    Base,
    get_db
)

from app import (
    models,
    schemas,
    crud
)

from app.blockchain import (
    record_energy_allocation
)

from app.payment_router import (
    router as payment_router
)


# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(
    bind=engine
)


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(

    title="Community Solar Subscription Platform",

    description=(
        "Blockchain-based Community Solar "
        "Subscription Platform API"
    ),

    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://localhost:5173",

        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# =========================================================
# PAYMENT ROUTER
# =========================================================

app.include_router(
    payment_router
)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {

        "message":
            "Community Solar Subscription Platform API is running"
    }


# =========================================================
# USERS
# =========================================================

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


# ---------------------------------------------------------
# GET ALL USERS
# ---------------------------------------------------------

@app.get(

    "/users",

    response_model=list[schemas.UserResponse]
)
def get_users(

    db: Session = Depends(get_db)
):

    return crud.get_users(db)


# ---------------------------------------------------------
# GET USER
# ---------------------------------------------------------

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


# =========================================================
# SUBSCRIPTION PLANS
# =========================================================

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


# =========================================================
# SOLAR PROJECTS
# =========================================================

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


# =========================================================
# SUBSCRIPTIONS
# =========================================================

@app.post(

    "/subscriptions",

    response_model=schemas.SubscriptionResponse
)
def create_subscription(

    subscription: schemas.SubscriptionCreate,

    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # CHECK USER
    # -----------------------------------------------------

    user = crud.get_user(

        db,

        subscription.user_id
    )


    if not user:

        raise HTTPException(

            status_code=404,

            detail="User not found"
        )


    # -----------------------------------------------------
    # CHECK PROJECT
    # -----------------------------------------------------

    project = crud.get_project(

        db,

        subscription.project_id
    )


    if not project:

        raise HTTPException(

            status_code=404,

            detail="Solar project not found"
        )


    # -----------------------------------------------------
    # CHECK PLAN
    # -----------------------------------------------------

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


# ---------------------------------------------------------
# GET ALL SUBSCRIPTIONS
# ---------------------------------------------------------

@app.get(

    "/subscriptions",

    response_model=list[schemas.SubscriptionResponse]
)
def get_subscriptions(

    db: Session = Depends(get_db)
):

    return crud.get_subscriptions(db)


# ---------------------------------------------------------
# GET SUBSCRIPTION
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# DELETE SUBSCRIPTION
# ---------------------------------------------------------

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

        "message":
            "Subscription deleted successfully"
    }


# =========================================================
# ENERGY GENERATION
# =========================================================

@app.post(

    "/energy-generation",

    response_model=schemas.EnergyGenerationResponse
)
def create_energy_generation(

    generation: schemas.EnergyGenerationCreate,

    db: Session = Depends(get_db)
):

    project = crud.get_project(

        db,

        generation.project_id
    )


    if not project:

        raise HTTPException(

            status_code=404,

            detail="Solar project not found"
        )


    return crud.create_energy_generation(

        db,

        generation
    )


# ---------------------------------------------------------
# GET ALL GENERATION
# ---------------------------------------------------------

@app.get(

    "/energy-generation",

    response_model=list[schemas.EnergyGenerationResponse]
)
def get_energy_generations(

    db: Session = Depends(get_db)
):

    return crud.get_energy_generations(db)


# ---------------------------------------------------------
# GET GENERATION
# ---------------------------------------------------------

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


# =========================================================
# ENERGY ALLOCATION + BLOCKCHAIN
# =========================================================

@app.post(

    "/energy-allocation",

    response_model=schemas.EnergyAllocationResponse
)
def create_energy_allocation(

    allocation: schemas.EnergyAllocationCreate,

    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # CHECK GENERATION
    # -----------------------------------------------------

    generation = db.query(

        models.EnergyGeneration

    ).filter(

        models.EnergyGeneration.id
        == allocation.generation_id

    ).first()


    if not generation:

        raise HTTPException(

            status_code=404,

            detail="Energy generation record not found"
        )


    # -----------------------------------------------------
    # CHECK SUBSCRIPTION
    # -----------------------------------------------------

    subscription = crud.get_subscription(

        db,

        allocation.subscription_id
    )


    if not subscription:

        raise HTTPException(

            status_code=404,

            detail="Subscription not found"
        )


    # -----------------------------------------------------
    # CHECK SUBSCRIPTION STATUS
    # -----------------------------------------------------

    if subscription.status != "Active":

        raise HTTPException(

            status_code=400,

            detail="Subscription is not active"
        )


    # -----------------------------------------------------
    # CHECK PROJECT MATCH
    # -----------------------------------------------------

    if (
        subscription.project_id
        != generation.project_id
    ):

        raise HTTPException(

            status_code=400,

            detail=(
                "Subscription and energy generation "
                "belong to different projects"
            )
        )


    # -----------------------------------------------------
    # GET PLAN
    # -----------------------------------------------------

    plan = crud.get_plan(

        db,

        subscription.plan_id
    )


    if not plan:

        raise HTTPException(

            status_code=404,

            detail="Subscription plan not found"
        )


    # -----------------------------------------------------
    # CHECK DUPLICATE ALLOCATION
    # -----------------------------------------------------

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

            detail=(
                "Energy already allocated "
                "to this subscription"
            )
        )


    # -----------------------------------------------------
    # CALCULATE ALREADY ALLOCATED ENERGY
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # REMAINING ENERGY
    # -----------------------------------------------------

    remaining_energy = (

        generation.energy_kwh
        - already_allocated
    )


    if remaining_energy <= 0:

        raise HTTPException(

            status_code=400,

            detail="No energy available for allocation"
        )


    # -----------------------------------------------------
    # PLAN ENERGY SHARE
    # -----------------------------------------------------

    requested_energy = plan.energy_share


    # -----------------------------------------------------
    # ACTUAL ALLOCATION
    # -----------------------------------------------------

    actual_allocation = min(

        requested_energy,

        remaining_energy
    )


    # -----------------------------------------------------
    # CREATE DATABASE ALLOCATION
    # -----------------------------------------------------

    new_allocation = crud.create_energy_allocation(

        db,

        generation.id,

        subscription.id,

        actual_allocation
    )


    # -----------------------------------------------------
    # BLOCKCHAIN VERIFICATION
    # -----------------------------------------------------

    try:

        blockchain_result = record_energy_allocation(

            new_allocation.id,

            generation.id,

            subscription.id,

            actual_allocation
        )


        # -------------------------------------------------
        # SAVE TRANSACTION HASH
        # -------------------------------------------------

        new_allocation.blockchain_hash = (

            blockchain_result[
                "transaction_hash"
            ]
        )


        # -------------------------------------------------
        # CHECK BLOCKCHAIN STATUS
        # -------------------------------------------------

        if blockchain_result["status"] == 1:

            new_allocation.verification_status = (
                "Verified"
            )

        else:

            new_allocation.verification_status = (
                "Failed"
            )


        db.commit()

        db.refresh(new_allocation)


    except Exception as e:

        new_allocation.verification_status = (
            "Failed"
        )

        db.commit()

        db.refresh(new_allocation)


        raise HTTPException(

            status_code=500,

            detail=(
                "Blockchain verification failed: "
                f"{str(e)}"
            )
        )


    return new_allocation


# =========================================================
# GET ENERGY ALLOCATIONS
# =========================================================

@app.get(

    "/energy-allocation",

    response_model=list[
        schemas.EnergyAllocationResponse
    ]
)
def get_energy_allocations(

    db: Session = Depends(get_db)
):

    return crud.get_energy_allocations(db)


# ---------------------------------------------------------
# GET SINGLE ALLOCATION
# ---------------------------------------------------------

@app.get(

    "/energy-allocation/{allocation_id}",

    response_model=schemas.EnergyAllocationResponse
)
def get_energy_allocation(

    allocation_id: int,

    db: Session = Depends(get_db)
):

    allocation = crud.get_energy_allocation(

        db,

        allocation_id
    )


    if not allocation:

        raise HTTPException(

            status_code=404,

            detail="Energy allocation not found"
        )


    return allocation


# =========================================================
# DELETE FAILED ALLOCATION
# =========================================================

@app.delete(

    "/energy-allocation/{allocation_id}"
)
def delete_energy_allocation(

    allocation_id: int,

    db: Session = Depends(get_db)
):

    allocation = crud.get_energy_allocation(

        db,

        allocation_id
    )


    if not allocation:

        raise HTTPException(

            status_code=404,

            detail="Energy allocation not found"
        )


    if allocation.verification_status != "Failed":

        raise HTTPException(

            status_code=400,

            detail=(
                "Only failed allocations "
                "can be deleted"
            )
        )


    db.delete(allocation)

    db.commit()


    return {

        "message":
            "Failed energy allocation deleted successfully",

        "allocation_id":
            allocation_id
    }


# =========================================================
# PROJECT GENERATION ALLOCATIONS
# =========================================================

@app.get(

    "/projects/{project_id}/generation",

    response_model=list[
        schemas.EnergyAllocationResponse
    ]
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

        models.EnergyGeneration.project_id
        == project_id

    ).all()


    return allocations


# =========================================================
# USER DASHBOARD
# =========================================================

@app.get(
    "/dashboard/{user_id}"
)
def get_user_dashboard(

    user_id: int,

    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # FIND USER
    # -----------------------------------------------------

    user = db.query(

        models.User

    ).filter(

        models.User.id == user_id

    ).first()


    if not user:

        raise HTTPException(

            status_code=404,

            detail="User not found"
        )


    # -----------------------------------------------------
    # USER SUBSCRIPTIONS
    # -----------------------------------------------------

    subscriptions = db.query(

        models.Subscription

    ).filter(

        models.Subscription.user_id
        == user_id

    ).all()


    dashboard_data = []


    for subscription in subscriptions:

        # -------------------------------------------------
        # PLAN
        # -------------------------------------------------

        plan = db.query(

            models.SubscriptionPlan

        ).filter(

            models.SubscriptionPlan.plan_id
            == subscription.plan_id

        ).first()


        # -------------------------------------------------
        # PROJECT
        # -------------------------------------------------

        project = db.query(

            models.SolarProject

        ).filter(

            models.SolarProject.id
            == subscription.project_id

        ).first()


        # -------------------------------------------------
        # PAYMENTS
        # -------------------------------------------------

        payments = db.query(

            models.Payment

        ).filter(

            models.Payment.subscription_id
            == subscription.id

        ).all()


        # -------------------------------------------------
        # ALLOCATIONS
        # -------------------------------------------------

        allocations = db.query(

            models.EnergyAllocation

        ).filter(

            models.EnergyAllocation.subscription_id
            == subscription.id

        ).all()


        dashboard_data.append({

            "subscription_id":
                subscription.id,

            "subscription_status":
                subscription.status,

            "plan": {

                "plan_id":
                    plan.plan_id
                    if plan else None,

                "plan_name":
                    plan.plan_name
                    if plan else None,

                "monthly_fee":
                    plan.monthly_fee
                    if plan else None,

                "energy_share":
                    plan.energy_share
                    if plan else None
            },

            "solar_project": {

                "project_id":
                    project.id
                    if project else None,

                "project_name":
                    project.project_name
                    if project else None,

                "location":
                    project.location
                    if project else None,

                "capacity_kw":
                    project.capacity_kw
                    if project else None,

                "energy_rate":
                    project.energy_rate
                    if project else None
            },

            "payments": [

                {

                    "payment_id":
                        payment.id,

                    "amount":
                        payment.amount,

                    "currency":
                        payment.currency,

                    "status":
                        payment.payment_status,

                    "stripe_session_id":
                        payment.stripe_session_id
                }

                for payment in payments
            ],

            "energy_allocations": [

                {

                    "allocation_id":
                        allocation.id,

                    "generation_id":
                        allocation.generation_id,

                    "allocated_kwh":
                        allocation.allocated_kwh,

                    "verification_status":
                        allocation.verification_status,

                    "blockchain_hash":
                        allocation.blockchain_hash,

                    "allocated_at":
                        allocation.allocated_at
                }

                for allocation in allocations
            ]
        })


    return {

        "user": {

            "id":
                user.id,

            "name":
                user.name,

            "email":
                user.email,

            "phone":
                user.phone,

            "address":
                user.address
        },

        "subscriptions":
            dashboard_data
    }


# =========================================================
# PAYMENT SUCCESS
# =========================================================

@app.get(
    "/payment-success"
)
def payment_success():

    return {

        "message":
            "Payment successful. Please verify the payment."
    }


# =========================================================
# PAYMENT CANCEL
# =========================================================

@app.get(
    "/payment-cancel"
)
def payment_cancel():

    return {

        "message":
            "Payment was cancelled."
    }


@app.post("/login", response_model=schemas.UserResponse)
def login(
    data: schemas.LoginRequest,
    db: Session = Depends(get_db)
):

    user = crud.get_user_by_email(db, data.email)

    if not user or user.password != data.password:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return user