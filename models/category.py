from sqlalchemy import String,Integer

from sqlalchemy.orm import Mapped,mapped_column
from database import Base

class Category(Base):
    __tablename__ = "category"

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    name:Mapped[str] = mapped_column(String(50),nullable=False)
    is_active:Mapped[bool] = mapped_column(nullable=False,default=True)

    