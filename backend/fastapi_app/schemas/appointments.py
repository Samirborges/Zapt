from pydantic import BaseModel

class AppointmentBase(BaseModel):
    date: str
    time: str
    description: str
    

class AppointmentResponse(AppointmentBase):
    id: int | None = None
    