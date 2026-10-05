from sqlalchemy.orm import Session

from app import models, schemas


# =========================================================
# USERS
# =========================================================

def create_user(
    db: Session,
    user: schemas.UserCreate
):

    db_user = models.User(

        name=user.name,

        email=user.email,

        phone=user.phone,

        address=user.address,

        password=user.password
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user


def get_users(
    db: Session
):

    return db.query(
        models.User
    ).all()


def get_user(
    db: Session,
    user_id: int
):

    return db.query(
        models.User
    ).filter(
        models.User.id == user_id
    ).first()


def get_user_by_email(
    db: Session,
    email: str
):

    return db.query(
        models.User
    ).filter(
        models.User.email == email
    ).first()


# =========================================================
# SUBSCRIPTION PLANS
# =========================================================

def create_plan(
    db: Session,
    plan: schemas.SubscriptionPlanCreate
):

    db_plan = models.SubscriptionPlan(

        plan_name=plan.plan_name,

        monthly_fee=plan.monthly_fee,

        energy_share=plan.energy_share,

        description=plan.description
    )

    db.add(db_plan)

    db.commit()

    db.refresh(db_plan)

    return db_plan


def get_plans(
    db: Session
):

    return db.query(
        models.SubscriptionPlan
    ).all()


def get_plan(
    db: Session,
    plan_id: int
):

    return db.query(
        models.SubscriptionPlan
    ).filter(
        models.SubscriptionPlan.plan_id == plan_id
    ).first()


# =========================================================
# SOLAR PROJECTS
# =========================================================

def create_project(
    db: Session,
    project: schemas.SolarProjectCreate
):

    db_project = models.SolarProject(

        project_name=project.project_name,

        description=project.description,

        location=project.location,

        capacity_kw=project.capacity_kw,

        total_panels=project.total_panels,

        energy_rate=project.energy_rate,

        status=project.status
    )

    db.add(db_project)

    db.commit()

    db.refresh(db_project)

    return db_project


def get_projects(
    db: Session
):

    return db.query(
        models.SolarProject
    ).all()


def get_project(
    db: Session,
    project_id: int
):

    return db.query(
        models.SolarProject
    ).filter(
        models.SolarProject.id == project_id
    ).first()


# =========================================================
# SUBSCRIPTIONS
# =========================================================

def create_subscription(
    db: Session,
    subscription: schemas.SubscriptionCreate
):

    db_subscription = models.Subscription(

        user_id=subscription.user_id,

        project_id=subscription.project_id,

        plan_id=subscription.plan_id,

        status=subscription.status
    )

    db.add(db_subscription)

    db.commit()

    db.refresh(db_subscription)

    return db_subscription


def get_subscriptions(
    db: Session
):

    return db.query(
        models.Subscription
    ).all()


def get_subscription(
    db: Session,
    subscription_id: int
):

    return db.query(
        models.Subscription
    ).filter(
        models.Subscription.id == subscription_id
    ).first()


def delete_subscription(
    db: Session,
    subscription_id: int
):

    subscription = db.query(
        models.Subscription
    ).filter(
        models.Subscription.id == subscription_id
    ).first()

    if subscription:

        db.delete(subscription)

        db.commit()

    return subscription


# =========================================================
# ENERGY GENERATION
# =========================================================

def create_energy_generation(
    db: Session,
    generation: schemas.EnergyGenerationCreate
):

    db_generation = models.EnergyGeneration(

        project_id=generation.project_id,

        power_kw=generation.power_kw,

        energy_kwh=generation.energy_kwh
    )

    db.add(db_generation)

    db.commit()

    db.refresh(db_generation)

    return db_generation


def get_energy_generations(
    db: Session
):

    return db.query(
        models.EnergyGeneration
    ).all()


def get_energy_generation(
    db: Session,
    generation_id: int
):

    return db.query(
        models.EnergyGeneration
    ).filter(
        models.EnergyGeneration.id == generation_id
    ).first()


# =========================================================
# ENERGY ALLOCATION
# =========================================================

def create_energy_allocation(
    db: Session,
    generation_id: int,
    subscription_id: int,
    allocated_kwh: float
):

    db_allocation = models.EnergyAllocation(

        generation_id=generation_id,

        subscription_id=subscription_id,

        allocated_kwh=allocated_kwh,

        verification_status="Pending"
    )

    db.add(db_allocation)

    db.commit()

    db.refresh(db_allocation)

    return db_allocation


def get_energy_allocations(
    db: Session
):

    return db.query(
        models.EnergyAllocation
    ).all()


def get_energy_allocation(
    db: Session,
    allocation_id: int
):

    return db.query(
        models.EnergyAllocation
    ).filter(
        models.EnergyAllocation.id == allocation_id
    ).first()