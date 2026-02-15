from pydantic import BaseModel, Field
from uuid import UUID
from datetime import time

class AvailabilityBaseModel(BaseModel):
    day_of_week: int = Field(ge=0, le=6)
    start_time: time
    end_time: time
    
    
    model_config = {
        "from_attributes": True
    }
    
    
class AvailabilityCreateModel(AvailabilityBaseModel):
    professional_id: UUID


class AvailabilityResponseModel(BaseModel): 
    id: UUID
    professional_id: UUID
    day_of_week: int
    start_time: time
    end_time: time

    model_config = {
        "from_attributes": True
    }