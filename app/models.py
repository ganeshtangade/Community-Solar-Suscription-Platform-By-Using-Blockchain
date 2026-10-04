from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database import Base


# =========================================================
# USER
# =========================================================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )

    subscriptions = relationship(
        "Subscription",
        back_populates="user"
    )


# =========================================================
# SUBSCRIPTION PLAN
# =========================================================

class SubscriptionPlan(Base):

    __tablename__ = "subscription_plans"

    plan_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    plan_name = Column(
        String(100),
        nullable=False
    )

    monthly_fee = Column(
        Float,
        nullable=False
    )

    energy_share = Column(
        Float,
        nullable=False
    )

    description = Column(
        String(500),
        nullable=True
    )

    subscriptions = relationship(
        "Subscription",
        back_populates="plan"
    )


# =========================================================
# SOLAR PROJECT
# =========================================================

class SolarProject(Base):

    __tablename__ = "solar_projects"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_name = Column(
        String(100),
        nullable=False
    )

    description = Column(
        String(500),
        nullable=True
    )

    location = Column(
        String(200),
        nullable=False
    )

    capacity_kw = Column(
        Float,
        nullable=False
    )

    total_panels = Column(
        Integer,
        nullable=False
    )

    energy_rate = Column(
        Float,
        nullable=False
    )

    status = Column(
        String(50),
        default="Active"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    subscriptions = relationship(
        "Subscription",
        back_populates="project"
    )

    energy_generations = relationship(
        "EnergyGeneration",
        back_populates="project"
    )


# =========================================================
# SUBSCRIPTION
# =========================================================

class Subscription(Base):

    __tablename__ = "subscriptions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    plan_id = Column(
        Integer,
        ForeignKey("subscription_plans.plan_id"),
        nullable=False
    )

    project_id = Column(
        Integer,
        ForeignKey("solar_projects.id"),
        nullable=False
    )

    status = Column(
        String(50),
        default="Active"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="subscriptions"
    )

    plan = relationship(
        "SubscriptionPlan",
        back_populates="subscriptions"
    )

    project = relationship(
        "SolarProject",
        back_populates="subscriptions"
    )

    allocations = relationship(
        "EnergyAllocation",
        back_populates="subscription"
    )


# =========================================================
# ENERGY GENERATION
# =========================================================

class EnergyGeneration(Base):

    __tablename__ = "energy_generations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey("solar_projects.id"),
        nullable=False
    )

    power_kw = Column(
        Float,
        nullable=False
    )

    energy_kwh = Column(
        Float,
        nullable=False
    )

    recorded_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    project = relationship(
        "SolarProject",
        back_populates="energy_generations"
    )

    allocations = relationship(
        "EnergyAllocation",
        back_populates="generation"
    )


# =========================================================
# ENERGY ALLOCATION
# =========================================================

class EnergyAllocation(Base):

    __tablename__ = "energy_allocations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    generation_id = Column(
        Integer,
        ForeignKey("energy_generations.id"),
        nullable=False
    )

    subscription_id = Column(
        Integer,
        ForeignKey("subscriptions.id"),
        nullable=False
    )

    allocated_kwh = Column(
        Float,
        nullable=False
    )

    allocated_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    verification_status = Column(
        String(50),
        default="Pending"
    )

    blockchain_hash = Column(
        String(255),
        nullable=True
    )

    generation = relationship(
        "EnergyGeneration",
        back_populates="allocations"
    )

    subscription = relationship(
        "Subscription",
        back_populates="allocations"
    )