from sqlalchemy.orm import Session
from uuid import UUID

from fastapi_app.professional_profiles.models import ProfessionalProfile
from fastapi_app.models.users import User
from fastapi_app.schemas.user import UserRole
from fastapi_app.professional_profiles.schema import ProfessionalProfilePatchModel

def get_professional_profile(user_id: UUID, db: Session) -> ProfessionalProfile | None:
    
    return (
        db.query(ProfessionalProfile)
        .filter(ProfessionalProfile.user_id == user_id)
        .first()
    )


def make_patch_on_profile(
    profile: ProfessionalProfile,
    data: ProfessionalProfilePatchModel, 
    db: Session
) -> ProfessionalProfile:
    
        
    profile.specialty = data.specialty
    profile.description = data.description
    profile.appointment_duration = data.appointment_duration
    
    db.commit()
    db.refresh(profile)
    
    return profile