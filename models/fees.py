import enum
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, Boolean, Date, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.mysql import YEAR  # <--- Import MySQL's YEAR type
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Months(enum.Enum):
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


class Fee(Base):
    __tablename__ = "fees"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("students.id"), nullable=False, index=True)
    notes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    month: Mapped[Months] = mapped_column(Enum(Months), nullable=False)
    
    # Maps to MySQL's native YEAR column
    # Python type hint is int (e.g., 2026), default dynamically gets current year
    year: Mapped[int] = mapped_column(YEAR, nullable=False, default=lambda: datetime.now().year)

    is_paid: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    payment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    student: Mapped["Student"] = relationship("Student", back_populates="fees")