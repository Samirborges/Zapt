from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from fastapi_app.core.dependencies import get_current_user
from fastapi_app.core.database import get_db

from fastapi_app.availability.schema import (
    AvailabilityResponseModel,
    AvailabilityCreateModel
)
from fastapi_app.availability.service import (
    list_by_professional,
    create_availability
)
from fastapi_app.availability.models import Availability

from fastapi_app.models.users import User


router = APIRouter(
    prefix="/availability",
    tags=["Availability"]
)


@router.get(
    "/me",
    response_model=list[AvailabilityResponseModel]
)
def get_my_availability(
    day_of_week: int | None = Query(None, ge=0, le=6),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List availability of the authenticated professional.
    Optional filter by day_of_week (0–6).
    """

    try:
        return list_by_professional(
            user_id=user.id,
            day_of_week=day_of_week,
            db=db
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/",
    response_model=AvailabilityResponseModel,
    status_code=201
)
def create_my_availability(
    availability_data: AvailabilityCreateModel,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create availability for the authenticated professional.
    """

    try:
        return create_availability(
            availability_data=availability_data,
            user_id=user.id,
            db=db
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{availability_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_availability(
    availability_id: UUID,
    db: Session = Depends(get_db)
):
    availability_db = (
        db.query(Availability)
        .filter(Availability.id == availability_id)
        .first()
    )

    if not availability_db:
        raise HTTPException(
            status_code=404,
            detail="Availability not found"
        )

    db.delete(availability_db)
    db.commit()
    