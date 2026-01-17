from pydantic import BaseModel
from enum import Enum
from uuid import UUID

class UserRole(str, Enum):
    CLIENT = "CLIENT"
    PROFESSIONAL = "PROFESSIONAL"


class UserModel(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole = UserRole.CLIENT 

    model_config = {
        "from_attributes": True  # Pydantic V2 substitui orm_mode
    }
    
    
class UserLoginModel(BaseModel):
    email: str
    password: str

    model_config = {
        "from_attributes": True  # Pydantic V2 substitui orm_mode
    }
    
    
class UserResponseModel(BaseModel):
    id: UUID
    name: str
    email: str
    role: UserRole

    model_config = {
        "from_attributes": True  # Pydantic V2 substitui orm_mode
    }
    
    
class UserCreate(BaseModel):
    email: str
    password: str
    role: UserRole
    
    model_config = {
        "from_attributes": True
    }
