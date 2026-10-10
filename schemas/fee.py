import enum
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class Months(str, enum.Enum):
    JANUARY = "January"
    FEBRUARY = "February"
    MARCH = "March"
    APRIL = "April"
    MAY = "May"
    JUNE = "June"
    JULY = "July"
    AUGUST = "August"
    SEPTEMBER = "September"
    OCTOBER = "October"
    NOVEMBER = "November"
    DECEMBER = "December"


# Base schema with shared fields
class FeeBase(BaseModel):
    student_id: int
    amount: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    month: Months
    year: int = Field(default_factory=lambda: datetime.now().year, ge=1901, le=2155)
    notes: Optional[str] = Field(None, max_length=255)
    is_paid: bool = False
    payment_date: Optional[date] = None


# Schema for CREATING a fee record
class FeeCreate(FeeBase):
    pass


# Schema for UPDATING a fee record (all fields optional for partial updates)
class FeeUpdate(BaseModel):
    
    amount: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2)
    month: Optional[Months] = None
    year: Optional[int] = Field(None, ge=1901, le=2155)
    notes: Optional[str] = Field(None, max_length=255)
    is_paid: Optional[bool] = None
    payment_date: Optional[date] = None


# Schema for GET / READ responses (includes DB-generated ID and timestamps)
class FeeResponse(FeeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)