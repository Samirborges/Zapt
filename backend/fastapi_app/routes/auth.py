from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from fastapi_app.schemas.user import UserModel
from fastapi_app.models.users import User
from fastapi_app.core.database import get_db
from fastapi_app.core.security import get_password_hash 

router = APIRouter()

@router.post("/login")
def login(user: UserModel):
    pass


@router.post("/register")
def register(user: UserModel, db: Session = Depends(get_db)):
    """Register a new user"""
    
    hashed_pwd = get_password_hash(user.password)
    
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_pwd,  # In a real app, hash the password!
        role=user.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user 


@router.get("/get-user/{user_id}")
def get_user_by_id(user_id: int):
    """Retrieve a user by their ID.

    Args:
        user_id (int): ID of the user to retrieve

    Returns:
        dict: {id: int, username: str, email: str}
    """
    pass


@router.put("/update-user/{user_id}")
def update_user(user_id: int, user: UserModel):
    """Update user information.

    Args:
        user_id (int): ID of the user to update
        user (UserModel): Updated user data

    Returns:
        dict: {id: int, username: str, email: str}
    """
    pass


