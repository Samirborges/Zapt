from pydantic import BaseModel

class UserModel(BaseModel):
    email: str
    password: str


class UserResponseModel(BaseModel):
    id: int