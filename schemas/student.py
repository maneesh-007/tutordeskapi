from pydantic import BaseModel

class StclassResponse(BaseModel):
    id: int
    standard: str  # or whatever fields your Stclass model has
    is_active:bool

    class Config:
        from_attributes = True


class CreateStudent(BaseModel):

    name: str
    student_class: int  # Accepts foreign key integer ID when creating
    email: str
    phone_number: str
    is_active: bool

    class Config:
        from_attributes = True

class StudentResponse(BaseModel):
    id: int
    name: str
    student_class: StclassResponse  # Uses the nested Pydantic model for response
    email: str
    phone_number: str
    is_active: bool

    class Config:
        from_attributes = True


class UpdateStudent(BaseModel):

    name: str
    student_class: int  # Accepts foreign key integer ID when creating
    email: str
    phone_number: str
    is_active: bool
    
    class Config:
        from_attributes = True