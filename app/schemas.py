from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserUpdate(BaseModel):
    name: str
    email: str
    password: str

from pydantic import BaseModel

class SubscriptionPlanCreate(BaseModel):
    plan_name: str
    monthly_fee: float
    energy_share: float
    description: str



from typing import Optional
from datetime import datetime


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

    class Config:
        from_attributes = True
