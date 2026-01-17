from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from uuid import UUID

from fastapi_app.core.database import get_db
from fastapi_app.models.users import User
from fastapi_app.appointments.schema import AppointmentBase, AppointmentResponse, AppointmentCreate
from fastapi_app.appointments.models import Appointment
from fastapi_app.appointments.service import create_appointment
from fastapi_app.schemas.user import UserRole

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.get("/", response_model=list[AppointmentResponse])
def list_by_user(user_id: UUID, db: Session = Depends(get_db)):
    """Retrieve all stored appointments.
    Returns:
        appoitnments: [{id: int, date: str, time: str, description: str}]
    """
    
    user_from_db = db.query(User).filter(User.id == user_id).first()
    if not user_from_db:
        raise HTTPException(status_code=400, detail="User not found")
    
    appointments = (
        db.query(Appointment)
        .filter(
            (Appointment.client_id == user_id) |
            (Appointment.professional_id == user_id)
        )
        .all()
    )

    return appointments


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_by_id(appointment_id: UUID, db: Session = Depends(get_db)):
    """Retrieve an appointment by its ID.

    Args:
        appointment_id (int): ID of the appointment to retrieve
        user_id (int): ID of the user 

    Returns:
        dict: {id: int, date: str, time: str, description: str}
    """
    
    appointment = (
        db.query(Appointment)
        .filter(Appointment.id == appointment_id)
        .first()
    )

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return appointment


@router.post("/", response_model=AppointmentResponse)
def create(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    """Create a new appointment

    Args:
        professional_id: UUID --> ID of the professional
        client_id: UUID  --> ID of the client
        start_time: str --> Start time of the appointment
        end_time: str --> End time of the appointment
        description: str --> Description of the appointment
        status: str --> Status of the appointment
        created_at: str --> Creation time of the appointment
    Returns:
        dict: {id: int, date: str, time: str, description: str}
    """
    
    try:
        new_appointment = create_appointment(
            db=db,
            appointment_data=appointment
        )
        return new_appointment

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
   
    
@router.delete("/delete-appointment/{appointment_id}", response_model=AppointmentResponse)
def delete_appointment(appointment_id: UUID, db: Session = Depends(get_db)):
    """Delete an appointment by its ID.

    Args:
        appointment_id (int): ID of the appointment to delete

    Returns:
        dict: {id: int, date: str, time: str, description: str}
    """
    
    appointment_db = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    
    db.delete(appointment_db)
    db.commit()

    return appointment_db
    

@router.put("/update-appointment/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(appointment_id: UUID, appointment: AppointmentBase, db: Session = Depends(get_db)):
    """Update an existing appointment by its ID.

    Args:
        appointment_id (int): ID of the appointment to update
        date (str): new date of the appointment
        time (str): new time of the appointment
        description (str): new description of the appointment

    Returns:
        dict: {id: int, date: str, time: str, description: str}
    """
    
    pass
