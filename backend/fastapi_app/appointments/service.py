from sqlalchemy.orm import Session
from datetime import date, time
from uuid import UUID

from fastapi_app.appointments.models import Appointment
from fastapi_app.appointments.schema import AppointmentCreate, AppointmentStatus

def has_time_conflict(
    db: Session,
    professional_id: UUID,
    appointment_date: date,
    start_time: time,
    end_time: time,
) -> bool:
    conflict = (
        db.query(Appointment)
        .filter(
            Appointment.professional_id == professional_id,
            Appointment.appointment_date == appointment_date,
            Appointment.status == AppointmentStatus.SCHEDULED,
            Appointment.start_time < end_time,
            Appointment.end_time > start_time,
        )
        .first()
    )

    return conflict is not None


def create_appointment(
    db: Session,
    appointment_data: AppointmentCreate,
) -> Appointment:
    
    # Regra 1: horário válido
    if appointment_data.end_time <= appointment_data.start_time:
        raise ValueError("end_time must be greater than start_time")

    # Regra 2: conflito de horário
    if has_time_conflict(
        db=db,
        professional_id=appointment_data.professional_id,
        appointment_date=appointment_data.appointment_date,
        start_time=appointment_data.start_time,
        end_time=appointment_data.end_time,
    ):
        raise ValueError("Time slot is already booked")

    new_appointment = Appointment(
        professional_id=appointment_data.professional_id,
        client_id=appointment_data.client_id,
        appointment_date=appointment_data.appointment_date,
        start_time=appointment_data.start_time,
        end_time=appointment_data.end_time,
        status=AppointmentStatus.SCHEDULED,
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


