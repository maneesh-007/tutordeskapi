from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from utility import get_current_admin
# Replace with your actual database and model/schema import paths
from database import get_db
from models import Fee
from schemas.fee import FeeCreate, FeeResponse, FeeUpdate

router = APIRouter(prefix="/fees", tags=["Fees"],
                   dependencies=[Depends(get_current_admin)]
                   )


# 1. CREATE
@router.post("/", response_model=FeeResponse, status_code=status.HTTP_201_CREATED)
def create_fee(
    payload: FeeCreate, 
    db: Session = Depends(get_db)
):
    db_fee = Fee(**payload.model_dump())
    
    # Auto-set payment_date if is_paid is passed as True without an explicit date
    if db_fee.is_paid and not db_fee.payment_date:
        db_fee.payment_date = date.today()

    db.add(db_fee)
    db.commit()
    db.refresh(db_fee)
    return db_fee


# 2. READ ALL (With Filtering Options)
@router.get("/", response_model=List[FeeResponse])
def get_all_fees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    student_id: Optional[int] = None,
    is_paid: Optional[bool] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Fee)
    
    if student_id is not None:
        query = query.filter(Fee.student_id == student_id)
    if is_paid is not None:
        query = query.filter(Fee.is_paid == is_paid)
    if year is not None:
        query = query.filter(Fee.year == year)

    return query.offset(skip).limit(limit).all()


# 2b. READ BY ID
@router.get("/{fee_id}", response_model=FeeResponse)
def get_fee_by_id(
    fee_id: int, 
    db: Session = Depends(get_db)
):
    fee = db.query(Fee).filter(Fee.id == fee_id).first()
    if not fee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Fee record with ID {fee_id} not found"
        )
    return fee


# 3. UPDATE (PATCH - Partial Update)
@router.patch("/{fee_id}", response_model=FeeResponse)
def update_fee(
    fee_id: int, 
    payload: FeeUpdate, 
    db: Session = Depends(get_db)
):
    fee = db.query(Fee).filter(Fee.id == fee_id).first()
    if not fee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Fee record with ID {fee_id} not found"
        )

    update_data = payload.model_dump(exclude_unset=True)
    
    # If is_paid is updated to True without a payment_date, auto-set today's date
    if update_data.get("is_paid") is True and "payment_date" not in update_data and not fee.payment_date:
        update_data["payment_date"] = date.today()

    for field, value in update_data.items():
        setattr(fee, field, value)

    db.commit()
    db.refresh(fee)
    return fee


# 4. DELETE
@router.delete("/{fee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fee(
    fee_id: int, 
    db: Session = Depends(get_db)
):
    fee = db.query(Fee).filter(Fee.id == fee_id).first()
    if not fee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Fee record with ID {fee_id} not found"
        )

    db.delete(fee)
    db.commit()
    return None