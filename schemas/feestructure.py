from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


# Base schema with shared fields
class FeeStructureBase(BaseModel):
    st_class: int = Field(..., alias="stclass", description="Student Class ID")
    amount: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    is_active: bool = True

    model_config = ConfigDict(populate_by_name=True)


# Schema for CREATING a fee structure
class FeeStructureCreate(FeeStructureBase):
    pass


# Schema for UPDATING a fee structure (all fields optional for partial updates)
class FeeStructureUpdate(BaseModel):
    st_class: Optional[int] = Field(None, alias="stclass")
    amount: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2)
    is_active: Optional[bool] = None

    model_config = ConfigDict(populate_by_name=True)


# Schema for GET / READ responses (includes DB-generated ID)
class FeeStructureResponse(FeeStructureBase):
    id: int

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)