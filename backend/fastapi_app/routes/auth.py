from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from fastapi_app.schemas.user import UserModel, UserLoginModel, UserResponseModel
from fastapi_app.models.users import User
from fastapi_app.core.database import get_db
from fastapi_app.core.security import get_password_hash, verify_password
from fastapi_app.users.service import create_user 

router = APIRouter()

@router.post("/login", response_model=UserResponseModel)
def login(user: UserLoginModel, db: Session = Depends(get_db)):
    """Authenticate a user and return their details."""
    
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    response_user: UserResponseModel = {
        "id": str(db_user.id),
        "name": db_user.name,
        "email": db_user.email,
        "role": db_user.role
    }
    
    return response_user


@router.post("/register", response_model=UserResponseModel)
def register(user: UserModel, db: Session = Depends(get_db)):
    """Register a new user"""
    
    return create_user(db=db, user_data=user)


@router.get("/get-user/{user_id}", response_model=UserResponseModel)
def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    """Retrieve a user by their ID.

    Args:
        user_id (str): ID of the user to retrieve

    Returns:
        dict: {id: str, username: str, email: str}
    """
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    response_user: UserResponseModel = {
        "id": str(user_db.id),
        "name": user_db.name,
        "email": user_db.email,
        "role": user_db.role
    }
    
    return response_user


@router.put("/update-user/{user_id}", response_model=UserResponseModel)
def update_user(user_id: UUID, user: UserModel, db: Session = Depends(get_db)):
    """Update user information.

    Args:
        user_id (str): ID of the user to update
        user (UserModel): Updated user data

    Returns:
        dict: {id: str, username: str, email: str}
    """
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_db.name = user.name
    user_db.email = user.email
   
    if user.password != "":
        user_db.password_hash = get_password_hash(user.password)
        
    user_db.role = user.role
    db.commit()
    db.refresh(user_db)
    
    response_user: UserResponseModel = {
        "id": str(user_db.id),
        "name": user_db.name,
        "email": user_db.email,
        "role": user_db.role
    }
    
    return user_db


@router.delete("/delete-user/{user_id}")
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    """Delete a user by their ID.

    Args:
        user_id (str): ID of the user to delete

    Returns:
        dict: {"detail": "User deleted successfully" , "user": UserResponseModel}
    """
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user_db)
    db.commit()
    
    return {
        "detail": "User deleted successfully",
        "user": user_db
    }
    
