from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db

from utility import get_current_admin
from models.stclass import Stclass
from schemas.stclass import CreateStclass,StclassResponse,UpdateStclass
from typing import List

router = APIRouter(

    prefix="/stclass",
    tags=["Student Class"],
    dependencies=[Depends(get_current_admin)]

)

@router.post("/add")
def add_stclass(stcls:CreateStclass,db:Session = Depends(get_db)):

    new_stclass = Stclass(standard = stcls.standard,is_active = stcls.is_active)

    db.add(new_stclass)

    db.commit()
    db.refresh(new_stclass)

    return{new_stclass}

@router.get("/all", response_model=List[StclassResponse])
def get_all_stclass(db: Session = Depends(get_db)):
    stclasses = db.query(Stclass).all()
    return stclasses


@router.put("/update/{id}")
def update_stclass(id:int,stclass:UpdateStclass,db:Session=Depends(get_db)):

    update_stclass = db.query(Stclass).filter(Stclass.id == id).first()

    if not update_stclass:
        raise HTTPException

    update_stclass.standard = stclass.standard
    update_stclass.is_active = stclass.is_active

    db.commit()

    db.refresh(update_stclass)

    return{update_stclass}


@router.delete("/delete/{id}")
def delete_stclass(id:int,db:Session = Depends(get_db)):

    stclass = db.query(Stclass).filter(Stclass.id == id).first()

    if not update_stclass:
            raise HTTPException

    db.delete(stclass)

    return{"stclass Deleted"}

