from fastapi import APIRouter, HTTPException, Depends 
from sqlalchemy.orm import Session
from uuid import UUID

from fastapi_app.schemas.user import UserResponseModel, UserRole
from fastapi_app.core.database import get_db
from fastapi_app.models.users import User 
from fastapi_app.professional_profiles.schema import ProfessionalProfilePatchModel, ProfessionalProfileResponseModel
from fastapi_app.professional_profiles.service import get_professional_profile, make_patch_on_profile
from fastapi_app.core.dependencies import get_current_user

router = APIRouter(prefix="/professionals", tags=["Professionals"])

@router.get("/professional", response_model=list[UserResponseModel])
def get_all_professional_users(db: Session = Depends(get_db)):
    
    return db.query(User).filter(User.role == UserRole.PROFESSIONAL).all()
    

@router.patch("/professional-profile/me", response_model=ProfessionalProfileResponseModel)
def professional_patch(
    professional_profile: ProfessionalProfilePatchModel,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user.role != UserRole.PROFESSIONAL:
        raise HTTPException(status_code=403, detail="Only professionals can edit this profile")
    
    profile = get_professional_profile(user.id, db=db)
    
    if not profile:
        raise HTTPException(status_code=404, detail="Professional profile was not found")
    

    
    return make_patch_on_profile(profile, professional_profile, db=db)
    