from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, date, timedelta
from fastapi import HTTPException

from fastapi_app.availability.models import Availability
from fastapi_app.availability.schema import AvailabilityCreateModel
from fastapi_app.professional_profiles.models import ProfessionalProfile
from fastapi_app.models.users import User
from fastapi_app.schemas.user import UserRole


def create_availability(
    availability_data: AvailabilityCreateModel,
    user_id: UUID,
    db: Session
) -> Availability:

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role != UserRole.PROFESSIONAL:
        raise HTTPException(status_code=403, detail="Only professionals can create availability")

    # Verifica se o usuário possui um perfil na tabela de profissionais
    professional_profile = (
        db.query(ProfessionalProfile)
        .filter(ProfessionalProfile.user_id == user_id)
        .first()
    )

    if not professional_profile:
        raise HTTPException(status_code=404, detail="Professional profile not found")
    
    # Normalização de day_of_week
    if not 0 <= availability_data.day_of_week <= 6:
        raise HTTPException(status_code=422, detail="day_of_week must be between 0 and 6")
    
    # Verifica se o horário da disponibilidade faz sentido com a disponibilidade determinada no perfil do profissional
    
    if availability_data.start_time >= availability_data.end_time:
        raise HTTPException(status_code=422, detail="Invalid time range")
    
    start_time = datetime.combine(date.today(), availability_data.start_time)
    end_time = datetime.combine(date.today(), availability_data.end_time)
    duration = end_time - start_time
    
    minute_duration = timedelta(minutes=professional_profile.appointment_duration)
    
    if duration < minute_duration:
        raise HTTPException(status_code=422, detail="Availability duration is shorter than appointment duration")

    total_minutes = int(duration.total_seconds() / 60)

    if total_minutes % professional_profile.appointment_duration !=0:
        raise HTTPException(status_code=422, detail="Availability duration must be a multiple of appointment duration")


    # Verificar sobreposição
    conflicts = (
        db.query(Availability)
        .filter(
            Availability.professional_id == professional_profile.id,
            Availability.day_of_week == availability_data.day_of_week,
            Availability.start_time < availability_data.end_time,
            Availability.end_time > availability_data.start_time,
        )
        .first()
    )

    if conflicts:
        raise HTTPException(status_code=409, detail="There is a conflicting availability")

    availability = Availability(
        professional_id=professional_profile.id,
        day_of_week=availability_data.day_of_week,
        start_time=availability_data.start_time,
        end_time=availability_data.end_time
    )

    db.add(availability)
    db.commit()
    db.refresh(availability)

    return availability


def list_by_professional(
    user_id: UUID,
    day_of_week: int | None,
    db: Session
) -> list[Availability]:

    professional_profile = (
        db.query(ProfessionalProfile)
        .filter(ProfessionalProfile.user_id == user_id)
        .first()
    )

    if not professional_profile:
        raise ValueError("Professional profile not found")

    query = db.query(Availability).filter(
        Availability.professional_id == professional_profile.id
    )

    if day_of_week is not None:
        query = query.filter(Availability.day_of_week == day_of_week)

    return query.all()
