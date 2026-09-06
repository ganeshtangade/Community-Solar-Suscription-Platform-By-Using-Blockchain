from sqlalchemy.orm import Session
from app import models, schemas


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
    return db.query(models.SubscriptionPlan).all()

def get_plan(db, plan_id):
    return db.query(models.SubscriptionPlan).filter(
        models.SubscriptionPlan.plan_id == plan_id
    ).first()


def update_plan(db, plan_id, updated_plan):
    db_plan = db.query(models.SubscriptionPlan).filter(
        models.SubscriptionPlan.plan_id == plan_id
    ).first()

    if db_plan:
        db_plan.plan_name = updated_plan.plan_name
        db_plan.monthly_fee = updated_plan.monthly_fee
        db_plan.energy_share = updated_plan.energy_share
        db_plan.description = updated_plan.description

        db.commit()
        db.refresh(db_plan)

    return db_plan

def delete_plan(db, plan_id):
    db_plan = db.query(models.SubscriptionPlan).filter(
        models.SubscriptionPlan.plan_id == plan_id
    ).first()

    if db_plan:
        db.delete(db_plan)
        db.commit()

    return db_plan


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
    return db.query(models.SolarProject).all()

def get_project(db, project_id):
    return db.query(models.SolarProject).filter(
        models.SolarProject.id == project_id
    ).first()

def update_project(db, project_id, updated_project):

    db_project = db.query(models.SolarProject).filter(
        models.SolarProject.id == project_id
    ).first()

    if db_project:

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

    db_project = db.query(models.SolarProject).filter(
        models.SolarProject.id == project_id
    ).first()

    if db_project:

        db.delete(db_project)
        db.commit()

    return db_project