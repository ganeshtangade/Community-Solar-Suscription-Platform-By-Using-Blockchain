from fastapi import FastAPI, Depends, HTTPException
from app.database import SessionLocal, engine, Base
from app import models, crud, schemas
from sqlalchemy.orm import Session


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Create User Detail

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "id": new_user.id
    }


# Get Single User Detail


@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        return {"message": "User not found"}

    return user

# Get all Users Detail


@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.put("/users/{user_id}")
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if db_user is None:
        return {"message": "User not found"}

    db_user.name = user.name
    db_user.email = user.email
    db_user.password = user.password

    db.commit()
    db.refresh(db_user)

    return {
        "message": "User updated successfully",
        "user": db_user
    }


#Subscription

# post

@app.post("/plans")
def create_plan(plan: schemas.SubscriptionPlanCreate, db: Session = Depends(get_db)):
    return crud.create_plan(db, plan)

#Get all

@app.get("/plans")
def get_all_plans(db: Session = Depends(get_db)):
    return crud.get_all_plans(db)

# Get from ID

@app.get("/plans/{plan_id}")
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = crud.get_plan(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

#Put

@app.put("/plans/{plan_id}")
def update_plan(plan_id: int, plan: schemas.SubscriptionPlanCreate, db: Session = Depends(get_db)):
    updated = crud.update_plan(db, plan_id, plan)
    if not updated:
        raise HTTPException(status_code=404, detail="Plan not found")
    return updated

#delete

@app.delete("/plans/{plan_id}")
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_plan(db, plan_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"message": "Plan deleted successfully"}


# =========================
# Solar Project
# =========================

# Create Solar Project

@app.post("/projects")
def create_project(
    project: schemas.SolarProjectCreate,
    db: Session = Depends(get_db)
):
    return crud.create_project(db, project)


# Get All Solar Projects

@app.get("/projects")
def get_all_projects(db: Session = Depends(get_db)):
    return crud.get_all_projects(db)


# Get Solar Project by ID

@app.get("/projects/{project_id}")
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = crud.get_project(db, project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Solar project not found"
        )

    return project


# Update Solar Project

@app.put("/projects/{project_id}")
def update_project(
    project_id: int,
    project: schemas.SolarProjectUpdate,
    db: Session = Depends(get_db)
):
    updated = crud.update_project(
        db,
        project_id,
        project
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Solar project not found"
        )

    return updated


# Delete Solar Project

@app.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.delete_project(
        db,
        project_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Solar project not found"
        )

    return {
        "message": "Solar project deleted successfully"
    }
