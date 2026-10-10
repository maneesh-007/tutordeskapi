from pydantic import BaseModel

class CreateCategorySchema(BaseModel):
    name: str
    is_active: bool = True

    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    id: int
    name: str
    is_active: bool

    class Config:
        from_attributes = True

class UpdateCategorySchema(BaseModel):
    name: str
    is_active: bool

    class Config:
        from_attributes = True