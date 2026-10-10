from sqlalchemy import Integer,String,Boolean
from sqlalchemy.orm import Mapped,mapped_column,relationship

from database import Base

class Stclass(Base):
    __tablename__ = "student_class"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    standard: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Back relationship to Student
    students: Mapped[list["Student"]] = relationship("Student", back_populates="st_class")