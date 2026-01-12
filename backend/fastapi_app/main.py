from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AppointmentModel(BaseModel):
    id: int | None = None
    date: str
    time: str
    description: str

stored_appointments = [
    {"id": 1, "date": "2024-07-01", "time": "10:00", "description": "Dentist appointment"},
    {"id": 2, "date": "2024-07-02", "time": "14:00", "description": "Meeting with client"},
    {"id": 3, "date": "2024-07-03", "time": "09:00", "description": "Yoga class"},
]

@app.get("/get-all-appointments")
def get_all_appoitnments():
    """Retrieve all stored appointments.
    Returns:
        appoitnments: [{id: int, date: str, time: str, description: str}]
    """
    return {"appoitnments": stored_appointments}


@app.get("/get-appointment/{appointment_id}")
def get_appointment_by_id(appointment_id: int):
    """Retrieve an appointment by its ID.

    Args:
        appointment_id (int): ID of the appointment to retrieve

    Returns:
        dict: {id: int, date: str, time: str, description: str}
    """
    appointment: AppointmentModel = next((appt for appt in stored_appointments if appt["id"] == appointment_id), None)
    return appointment


@app.post("/create-appointment")
def create_appointment(appointment: AppointmentModel):
    """Create a new appointment

    Args:
        date (str): date of the appointment
        time (str): time of the appointment
        description (str): description of the appointment

    Returns:
        dict: {id: int, date: str, time: str, description: str}
    """
    stored_appointments.append(appointment)
    return {
        "id": appointment.id,
        "date": appointment.date,
        "time": appointment.time,
        "description": appointment.description,
    }
    
@app.delete("/delete-appointment/{appointment_id}")
def delete_appointment(appointment_id: int):
    """Delete an appointment by its ID.

    Args:
        appointment_id (int): ID of the appointment to delete

    Returns:
        dict: {id: int, date: str, time: str, description: str}
    """
    delete_appointment: AppointmentModel = next((appt for appt in stored_appointments if appt["id"] == appointment_id), None)
    if delete_appointment:
        stored_appointments.remove(delete_appointment)
        return {
            "id": delete_appointment["id"],
            "date": delete_appointment["date"],
            "time": delete_appointment["time"],
            "description": delete_appointment["description"],
        }
        

@app.put("/update-appointment/{appointment_id}")
def update_appointment(appointment_id: int, appointment: AppointmentModel):
    """Update an existing appointment by its ID.

    Args:
        appointment_id (int): ID of the appointment to update
        date (str): new date of the appointment
        time (str): new time of the appointment
        description (str): new description of the appointment

    Returns:
        dict: {id: int, date: str, time: str, description: str}
    """
    update_appointment: AppointmentModel = next((appt for appt in stored_appointments if appt["id"] == appointment_id), None)
    if update_appointment:
        update_appointment["date"] = appointment.date
        update_appointment["time"] = appointment.time
        update_appointment["description"] = appointment.description
        return update_appointment