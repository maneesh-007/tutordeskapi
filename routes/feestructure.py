from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Replace 'database' and 'models' with your actual import paths
from database import get_db 
from models import FeeStructure
from schemas.feestructure import FeeStructureCreate, FeeStructureResponse, FeeStructureUpdate
from utility import get_current_admin

router = APIRouter(prefix="/fee-structures", tags=["Fee Structure"],
                dependencies=[Depends(get_current_admin)]
                   )


# 1. CREATE
@router.post("/", response_model=FeeStructureResponse, status_code=status.HTTP_201_CREATED)
def create_fee_structure(
    payload: FeeStructureCreate, 
    db: Session = Depends(get_db)
):
    db_fee_structure = FeeStructure(**payload.model_dump())
    db.add(db_fee_structure)
    db.commit()
    db.refresh(db_fee_structure)
    return db_fee_structure


# 2. READ (GET All)
@router.get("/", response_model=List[FeeStructureResponse])
def get_all_fee_structures(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return db.query(FeeStructure).offset(skip).limit(limit).all()


# 2b. READ (GET by ID)
@router.get("/{fee_structure_id}", response_model=FeeStructureResponse)
def get_fee_structure_by_id(
    fee_structure_id: int, 
    db: Session = Depends(get_db)
):
    fee_structure = db.query(FeeStructure).filter(FeeStructure.id == fee_structure_id).first()
    if not fee_structure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Fee structure with ID {fee_structure_id} not found"
        )
    return fee_structure


# 3. UPDATE (PATCH - Partial Update)
@router.patch("/{fee_structure_id}", response_model=FeeStructureResponse)
def update_fee_structure(
    fee_structure_id: int, 
    payload: FeeStructureUpdate, 
    db: Session = Depends(get_db)
):
    fee_structure = db.query(FeeStructure).filter(FeeStructure.id == fee_structure_id).first()
    if not fee_structure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Fee structure with ID {fee_structure_id} not found"
        )

    # Exclude unset fields so only provided fields are updated
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(fee_structure, field, value)

    db.commit()
    db.refresh(fee_structure)
    return fee_structure


# 4. DELETE
@router.delete("/{fee_structure_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fee_structure(
    fee_structure_id: int, 
    db: Session = Depends(get_db)
):
    fee_structure = db.query(FeeStructure).filter(FeeStructure.id == fee_structure_id).first()
    if not fee_structure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Fee structure with ID {fee_structure_id} not found"
        )

    db.delete(fee_structure)
    db.commit()
    return None