from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import (
    engine,
    Base,
    get_db
)

from app import models, schemas, crud


# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(
    bind=engine
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Community Solar Subscription Platform",
    description="Backend API for community solar subscriptions",
    version="1.0.0"
)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "message": "Community Solar Subscription Platform API",
        "status": "running"
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

    existing_user = db.query(
        models.User
    ).filter(
        models.User.email == user.email
    ).first()

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
def get_all_users(
    db: Session = Depends(get_db)
):

    return crud.get_all_users(db)


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


@app.put(
    "/users/{user_id}",
    response_model=schemas.UserResponse
)
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db)
):

    updated_user = crud.update_user(
        db,
        user_id,
        user
    )

    if not updated_user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return updated_user


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
def get_all_plans(
    db: Session = Depends(get_db)
):

    return crud.get_all_plans(db)


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
            detail="Plan not found"
        )

    return plan


@app.put(
    "/plans/{plan_id}",
    response_model=schemas.SubscriptionPlanResponse
)
def update_plan(
    plan_id: int,
    plan: schemas.SubscriptionPlanCreate,
    db: Session = Depends(get_db)
):

    updated_plan = crud.update_plan(
        db,
        plan_id,
        plan
    )

    if not updated_plan:

        raise HTTPException(
            status_code=404,
            detail="Plan not found"
        )

    return updated_plan


@app.delete("/plans/{plan_id}")
def delete_plan(
    plan_id: int,
    db: Session = Depends(get_db)
):

    deleted_plan = crud.delete_plan(
        db,
        plan_id
    )

    if not deleted_plan:

        raise HTTPException(
            status_code=404,
            detail="Plan not found"
        )

    return {
        "message": "Plan deleted successfully"
    }


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
def get_all_projects(
    db: Session = Depends(get_db)
):

    return crud.get_all_projects(db)


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


@app.put(
    "/projects/{project_id}",
    response_model=schemas.SolarProjectResponse
)
def update_project(
    project_id: int,
    project: schemas.SolarProjectUpdate,
    db: Session = Depends(get_db)
):

    updated_project = crud.update_project(
        db,
        project_id,
        project
    )

    if not updated_project:

        raise HTTPException(
            status_code=404,
            detail="Solar project not found"
        )

    return updated_project


@app.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):

    deleted_project = crud.delete_project(
        db,
        project_id
    )

    if not deleted_project:

        raise HTTPException(
            status_code=404,
            detail="Solar project not found"
        )

    return {
        "message": "Solar project deleted successfully"
    }


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

    # Check user

    user = crud.get_user(
        db,
        subscription.user_id
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Check plan

    plan = crud.get_plan(
        db,
        subscription.plan_id
    )

    if not plan:

        raise HTTPException(
            status_code=404,
            detail="Subscription plan not found"
        )

    # Check solar project

    project = crud.get_project(
        db,
        subscription.project_id
    )

    if not project:

        raise HTTPException(
            status_code=404,
            detail="Solar project not found"
        )

    # Create subscription

    return crud.create_subscription(
        db,
        subscription
    )


@app.get(
    "/subscriptions",
    response_model=list[schemas.SubscriptionResponse]
)
def get_all_subscriptions(
    db: Session = Depends(get_db)
):

    return crud.get_all_subscriptions(db)


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


@app.delete("/subscriptions/{subscription_id}")
def delete_subscription(
    subscription_id: int,
    db: Session = Depends(get_db)
):

    deleted = crud.delete_subscription(
        db,
        subscription_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )

    return {
        "message": "Subscription deleted successfully"
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


@app.get(
    "/projects/{project_id}/generation",
    response_model=list[schemas.EnergyGenerationResponse]
)
def get_project_generation(
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

    return crud.get_project_generation(
        db,
        project_id
    )


# =========================================================
# ENERGY ALLOCATION
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
    # Check energy generation
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # Check subscription
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
    # Check subscription status
    # -----------------------------------------------------

    if subscription.status != "Active":

        raise HTTPException(
            status_code=400,
            detail="Subscription is not active"
        )

    # -----------------------------------------------------
    # Check project matching
    # -----------------------------------------------------

    if subscription.project_id != generation.project_id:

        raise HTTPException(
            status_code=400,
            detail="Subscription and energy generation belong to different projects"
        )

    # -----------------------------------------------------
    # Get subscription plan
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
    # Check existing allocation
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
            detail="Energy already allocated to this subscription"
        )

    # -----------------------------------------------------
    # Calculate already allocated energy
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
    # Calculate remaining energy
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
    # Requested energy from subscription plan
    # -----------------------------------------------------

    requested_energy = plan.energy_share

    # -----------------------------------------------------
    # Actual allocation
    # -----------------------------------------------------

    actual_allocation = min(
        requested_energy,
        remaining_energy
    )

    # -----------------------------------------------------
    # Create allocation
    # -----------------------------------------------------

    return crud.create_energy_allocation(
        db,
        generation.id,
        subscription.id,
        actual_allocation
    )


# =========================================================
# GET ALLOCATIONS FOR GENERATION
# =========================================================

@app.get(
    "/energy-generation/{generation_id}/allocations",
    response_model=list[schemas.EnergyAllocationResponse]
)
def get_generation_allocations(
    generation_id: int,
    db: Session = Depends(get_db)
):

    generation = db.query(
        models.EnergyGeneration
    ).filter(
        models.EnergyGeneration.id == generation_id
    ).first()

    if not generation:

        raise HTTPException(
            status_code=404,
            detail="Energy generation record not found"
        )

    return crud.get_generation_allocations(
        db,
        generation_id
    )


# =========================================================
# GET ALLOCATIONS FOR SUBSCRIPTION
# =========================================================

@app.get(
    "/subscriptions/{subscription_id}/allocations",
    response_model=list[schemas.EnergyAllocationResponse]
)
def get_subscription_allocations(
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

    return crud.get_subscription_allocations(
        db,
        subscription_id
    )