from sqlalchemy import Integer,ForeignKey,Numeric
from sqlalchemy.orm import Mapped,mapped_column
from database import Base
from decimal import Decimal
class FeeStructure(Base):
    __tablename__ ="fee_stucture"

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    st_class:Mapped[int] = mapped_column(Integer,ForeignKey("student_class.id"), nullable=False)
    amount:Mapped[Decimal] = mapped_column(Numeric(10,2),nullable=False)
    is_active:Mapped[bool] = mapped_column(default=True,nullable=False)

    

