from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ProfessionalProfilePatchModel(BaseModel):
    specialty: str
    description: str
    appointment_duration: int
    
    model_config = {
        "from_attributes": True
    }


class ProfessionalProfileResponseModel(BaseModel):
    id: UUID
    user_id: UUID
    specialty: str
    description: str
    appointment_duration: int
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }
    
