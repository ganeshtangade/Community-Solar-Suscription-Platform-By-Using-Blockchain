from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# =========================================================
# USER SCHEMAS
# =========================================================

class UserCreate(BaseModel):

    name: str

    email: str

    password: str


class UserUpdate(BaseModel):

    name: Optional[str] = None

    email: Optional[str] = None

    password: Optional[str] = None


class UserResponse(BaseModel):

    id: int

    name: str

    email: str

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# SUBSCRIPTION PLAN SCHEMAS
# =========================================================

class SubscriptionPlanCreate(BaseModel):

    plan_name: str

    monthly_fee: float

    energy_share: float

    description: Optional[str] = None


class SubscriptionPlanResponse(BaseModel):

    plan_id: int

    plan_name: str

    monthly_fee: float

    energy_share: float

    description: Optional[str]

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# SOLAR PROJECT SCHEMAS
# =========================================================

class SolarProjectCreate(BaseModel):

    project_name: str

    description: Optional[str] = None

    location: str

    capacity_kw: float

    total_panels: int

    energy_rate: float

    status: str = "Active"


class SolarProjectUpdate(BaseModel):

    project_name: Optional[str] = None

    description: Optional[str] = None

    location: Optional[str] = None

    capacity_kw: Optional[float] = None

    total_panels: Optional[int] = None

    energy_rate: Optional[float] = None

    status: Optional[str] = None


class SolarProjectResponse(BaseModel):

    id: int

    project_name: str

    description: Optional[str]

    location: str

    capacity_kw: float

    total_panels: int

    energy_rate: float

    status: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# SUBSCRIPTION SCHEMAS
# =========================================================

class SubscriptionCreate(BaseModel):

    user_id: int

    plan_id: int

    project_id: int

    status: str = "Active"


class SubscriptionResponse(BaseModel):

    id: int

    user_id: int

    plan_id: int

    project_id: int

    status: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# ENERGY GENERATION SCHEMAS
# =========================================================

class EnergyGenerationCreate(BaseModel):

    project_id: int

    power_kw: float

    energy_kwh: float


class EnergyGenerationResponse(BaseModel):

    id: int

    project_id: int

    power_kw: float

    energy_kwh: float

    recorded_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# ENERGY ALLOCATION SCHEMAS
# =========================================================

class EnergyAllocationCreate(BaseModel):

    generation_id: int

    subscription_id: int


class EnergyAllocationResponse(BaseModel):

    id: int

    generation_id: int

    subscription_id: int

    allocated_kwh: float

    allocated_at: datetime

    verification_status: str

    blockchain_hash: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# PAYMENT SCHEMAS
# =========================================================

class PaymentResponse(BaseModel):

    id: int

    subscription_id: int

    amount: float

    currency: str

    stripe_session_id: str

    payment_status: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )