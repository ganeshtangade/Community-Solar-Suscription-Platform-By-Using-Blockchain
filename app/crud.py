from app import models


# =========================================================
# USER CRUD
# =========================================================

def create_user(db, user):

    db_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user


def get_user(db, user_id):

    return db.query(
        models.User
    ).filter(
        models.User.id == user_id
    ).first()


def get_all_users(db):

    return db.query(
        models.User
    ).all()


def update_user(db, user_id, user):

    db_user = get_user(
        db,
        user_id
    )

    if not db_user:
        return None

    if user.name is not None:
        db_user.name = user.name

    if user.email is not None:
        db_user.email = user.email

    if user.password is not None:
        db_user.password = user.password

    db.commit()

    db.refresh(db_user)

    return db_user


# =========================================================
# SUBSCRIPTION PLAN CRUD
# =========================================================

def create_plan(db, plan):

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


def get_all_plans(db):

    return db.query(
        models.SubscriptionPlan
    ).all()


def get_plan(db, plan_id):

    return db.query(
        models.SubscriptionPlan
    ).filter(
        models.SubscriptionPlan.plan_id == plan_id
    ).first()


def update_plan(db, plan_id, updated_plan):

    db_plan = get_plan(
        db,
        plan_id
    )

    if not db_plan:
        return None

    db_plan.plan_name = updated_plan.plan_name

    db_plan.monthly_fee = updated_plan.monthly_fee

    db_plan.energy_share = updated_plan.energy_share

    db_plan.description = updated_plan.description

    db.commit()

    db.refresh(db_plan)

    return db_plan


def delete_plan(db, plan_id):

    db_plan = get_plan(
        db,
        plan_id
    )

    if not db_plan:
        return None

    db.delete(db_plan)

    db.commit()

    return db_plan


# =========================================================
# SOLAR PROJECT CRUD
# =========================================================

def create_project(db, project):

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


def get_all_projects(db):

    return db.query(
        models.SolarProject
    ).all()


def get_project(db, project_id):

    return db.query(
        models.SolarProject
    ).filter(
        models.SolarProject.id == project_id
    ).first()


def update_project(db, project_id, updated_project):

    db_project = get_project(
        db,
        project_id
    )

    if not db_project:
        return None

    if updated_project.project_name is not None:
        db_project.project_name = updated_project.project_name

    if updated_project.description is not None:
        db_project.description = updated_project.description

    if updated_project.location is not None:
        db_project.location = updated_project.location

    if updated_project.capacity_kw is not None:
        db_project.capacity_kw = updated_project.capacity_kw

    if updated_project.total_panels is not None:
        db_project.total_panels = updated_project.total_panels

    if updated_project.energy_rate is not None:
        db_project.energy_rate = updated_project.energy_rate

    if updated_project.status is not None:
        db_project.status = updated_project.status

    db.commit()

    db.refresh(db_project)

    return db_project


def delete_project(db, project_id):

    db_project = get_project(
        db,
        project_id
    )

    if not db_project:
        return None

    db.delete(db_project)

    db.commit()

    return db_project


# =========================================================
# SUBSCRIPTION CRUD
# =========================================================

def create_subscription(db, subscription):

    db_subscription = models.Subscription(

        user_id=subscription.user_id,

        plan_id=subscription.plan_id,

        project_id=subscription.project_id,

        status=subscription.status
    )

    db.add(db_subscription)

    db.commit()

    db.refresh(db_subscription)

    return db_subscription


def get_all_subscriptions(db):

    return db.query(
        models.Subscription
    ).all()


def get_subscription(db, subscription_id):

    return db.query(
        models.Subscription
    ).filter(
        models.Subscription.id == subscription_id
    ).first()


def delete_subscription(db, subscription_id):

    db_subscription = get_subscription(
        db,
        subscription_id
    )

    if not db_subscription:
        return None

    db.delete(db_subscription)

    db.commit()

    return db_subscription


# =========================================================
# ENERGY GENERATION CRUD
# =========================================================

def create_energy_generation(db, generation):

    db_generation = models.EnergyGeneration(

        project_id=generation.project_id,

        power_kw=generation.power_kw,

        energy_kwh=generation.energy_kwh
    )

    db.add(db_generation)

    db.commit()

    db.refresh(db_generation)

    return db_generation


def get_project_generation(db, project_id):

    return db.query(
        models.EnergyGeneration
    ).filter(
        models.EnergyGeneration.project_id == project_id
    ).all()


# =========================================================
# ENERGY ALLOCATION CRUD
# =========================================================

def create_energy_allocation(
    db,
    generation_id,
    subscription_id,
    allocated_kwh
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


def get_energy_allocation(
    db,
    allocation_id
):

    return db.query(
        models.EnergyAllocation
    ).filter(
        models.EnergyAllocation.id == allocation_id
    ).first()


def get_generation_allocations(
    db,
    generation_id
):

    return db.query(
        models.EnergyAllocation
    ).filter(
        models.EnergyAllocation.generation_id == generation_id
    ).all()


def get_subscription_allocations(
    db,
    subscription_id
):

    return db.query(
        models.EnergyAllocation
    ).filter(
        models.EnergyAllocation.subscription_id == subscription_id
    ).all()