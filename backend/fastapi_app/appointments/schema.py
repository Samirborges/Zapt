from pydantic import BaseModel
from uuid import UUID
from enum import Enum
from datetime import date, time, datetime

class AppointmentStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"

class AppointmentBase(BaseModel):
    professional_id: UUID
    client_id: UUID 
    appointment_date: date
    start_time: time
    end_time: time
    status: AppointmentStatus
    
    
class AppointmentCreate(AppointmentBase):
    pass
    

class AppointmentResponse(AppointmentBase):
    id: UUID | None = None
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }
    
    