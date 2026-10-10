from sqlalchemy import BigInteger, String, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import List
class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Foreign key column
    student_class: Mapped[int] = mapped_column(Integer, ForeignKey("student_class.id"), nullable=False, index=True)
    
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(10), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationship (renamed variable so it does not overwrite student_class column)
    st_class: Mapped["Stclass"] = relationship("Stclass", back_populates="students")

    fees: Mapped[List["Fee"]] = relationship("Fee", back_populates="student", cascade="all, delete-orphan")