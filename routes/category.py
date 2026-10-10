
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session  
from database import get_db
from models.category import Category
from utility import get_current_admin
from schemas.category import CreateCategorySchema, UpdateCategorySchema, CategorySchema

router = APIRouter(
    prefix="/category",
    tags=["category"],
    dependencies=[Depends(get_current_admin)]
)  


@router.post("/add", response_model=CategorySchema)
async def add_category(
    category_data: CreateCategorySchema,
    db: Session = Depends(get_db),
):
    new_category = Category(
        name=category_data.name,
        is_active=category_data.is_active,
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/list", response_model=list[CategorySchema])
async def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories

@router.put("/update/{category_id}", response_model=CategorySchema)
async def update_category(category_id:int,category:UpdateCategorySchema,db:Session = Depends(get_db)):

    update_category = db.query(Category).filter(Category.id==category_id).first()

    if not category_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "CATEGORY_NOT_FOUND", "message": "Category ID does not exist"}
        )

    update_category.name = category.name
    update_category.is_active = category.is_active

    db.commit()

    db.refresh(update_category)


    return{"message":"Category Updated"}

@router.delete("/delete/{category_id}")
def delete_category(cateory_id:int,db:Session = Depends(get_db)):

    category = db.query(Category).filter(Category.id == cateory_id).first()

    if not category:
         raise HTTPException(
                     status_code=status.HTTP_404_NOT_FOUND,
                     detail={"code": "CATEGORY_NOT_FOUND", "message": "Category ID does not exist"}
                 )

    db.delete(category)

    return{"message":"category Deleted"}  

