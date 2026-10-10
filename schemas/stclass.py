from pydantic import BaseModel


class CreateStclass(BaseModel):
    standard:str
    is_active:bool

    class Config:
        from_attributed=True

class StclassResponse(BaseModel):

    id:int
    standard:str
    is_active:bool
    
    class Config:
        from_attributed=True


class UpdateStclass(BaseModel):

    standard:str
    is_active:bool
      
    class Config:
        from_attributed=True