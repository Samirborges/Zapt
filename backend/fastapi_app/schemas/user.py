from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class UserModel(BaseModel):
    name: str
    email: str
    password: str
    role: str | None = "CLIENT"

    model_config = {
        "from_attributes": True  # Pydantic V2 substitui orm_mode
    }