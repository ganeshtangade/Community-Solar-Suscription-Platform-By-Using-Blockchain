from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base #The classes that inherit from Base are database tables
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime



class User(Base):       #This creates a class named User.Because it inherits from Base, SQLAlchemy knows it should become a table in PostgreSQL.
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(255))


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    plan_name = Column(String(100))
    price = Column(Integer)
    duration_months = Column(Integer)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_id = Column(Integer, ForeignKey("plans.id"))
    status = Column(String(50))    



class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    plan_id = Column(Integer, primary_key=True, index=True)
    plan_name = Column(String, nullable=False)
    monthly_fee = Column(Float, nullable=False)
    energy_share = Column(Float, nullable=False)
    description = Column(String)


class SolarProject(Base):
    __tablename__ = "solar_projects"

    id = Column(Integer, primary_key=True, index=True)

    project_name = Column(String(100), nullable=False)

    description = Column(String(500), nullable=True)

    location = Column(String(200), nullable=False)

    capacity_kw = Column(Float, nullable=False)

    total_panels = Column(Integer, nullable=False)

    energy_rate = Column(Float, nullable=False)

    status = Column(String(50), default="Active")

    created_at = Column(DateTime, default=datetime.utcnow)