from pydantic import BaseModel,Field
from typing import Optional


# What we RECEIVE when creating a student
class StudentCreate(BaseModel):
    name:  str            = Field(min_length=2)
    age:   int            = Field(gt=0, le=100)
    grade: float          = 0.0
    email: Optional[str]  = None

# What we SEND BACK — adds id field
class StudentResponse(BaseModel):
    id: int
    name : str
    age:   int
    grade: float
    email: Optional[str]
    active: bool

class Config:
    from_attributes = True   # allows reading SQLAlchemy objects
