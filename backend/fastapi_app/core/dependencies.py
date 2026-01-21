from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID

from fastapi_app.core.database import get_db
from fastapi_app.models.users import User


def get_current_user(
    user_id: UUID = Query(...),
    db: Session = Depends(get_db)
) -> User:
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    return user
