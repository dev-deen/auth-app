from pydantic import BaseModel, ConfigDict, Field, NonNegativeFloat
from typing import Optional
from models import RoleEnum

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=6, max_length=100)
    role: Optional[RoleEnum] = RoleEnum.employee

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: RoleEnum

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[RoleEnum] = None

class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=18, le=65)
    department: str = Field(..., min_length=2, max_length=50)
    designation: str = Field(..., min_length=2, max_length=50)
    salary: NonNegativeFloat = Field(..., example=50000.0)

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)