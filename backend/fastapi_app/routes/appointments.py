from fastapi import APIRouter, HTTPException

from fastapi_app.schemas.appointments import AppointmentBase, AppointmentResponse

router = APIRouter()

stored_appointments = [
    {"id": 1, "date": "2024-07-01", "time": "10:00", "description": "Dentist appointment"},
    {"id": 2, "date": "2024-07-02", "time": "14:00", "description": "Meeting with client"},
    {"id": 3, "date": "2024-07-03", "time": "09:00", "description": "Yoga class"},
]

@router.get("/get-all-appointments")
def get_all_appoitnments(user_id: int):
    """Retrieve all stored appointments.
    Returns:
        appoitnments: [{id: int, date: str, time: str, description: str}]
    """
    
    # TODO Realizar a validação do usuário no banco de dados
    
    return {"appointments": stored_appointments}


@router.get("/get-appointment/{appointment_id}")
def get_appointment_by_id(appointment_id: int, user_id: int):
    """Retrieve an appointment by its ID.

    Args:
        appointment_id (int): ID of the appointment to retrieve
        user_id (int): ID of the user 

    Returns:
        dict: {id: int, date: str, time: str, description: str}
    """
    
    # TODO Realizar a validação e busca do agendamento com o id do usuário e do agendamento no banco
    
    appointment: AppointmentResponse = next((appt for appt in stored_appointments if appt["id"] == appointment_id), None)
    return appointment


@router.post("/create-appointment")
def create_appointment(appointment: AppointmentResponse):
    """Create a new appointment

    Args:
        date (str): date of the appointment
        time (str): time of the appointment
        description (str): description of the appointment

    Returns:
        dict: {id: int, date: str, time: str, description: str}
    """

    appointment.id = len(stored_appointments) + 1
    
    stored_appointments.append(appointment)
    return appointment
   
    
@router.delete("/delete-appointment/{appointment_id}")
def delete_appointment(appointment_id: int):
    """Delete an appointment by its ID.

    Args:
        appointment_id (int): ID of the appointment to delete

    Returns:
        dict: {id: int, date: str, time: str, description: str}
    """
    delete_appointment: AppointmentBase = next((appt for appt in stored_appointments if appt["id"] == appointment_id), None)
    if delete_appointment:
        stored_appointments.remove(delete_appointment)
        
        return delete_appointment

@router.put("/update-appointment/{appointment_id}")
def update_appointment(appointment_id: int, appointment: AppointmentBase):
    """Update an existing appointment by its ID.

    Args:
        appointment_id (int): ID of the appointment to update
        date (str): new date of the appointment
        time (str): new time of the appointment
        description (str): new description of the appointment

    Returns:
        dict: {id: int, date: str, time: str, description: str}
    """
    update_appointment: AppointmentBase = next((appt for appt in stored_appointments if appt["id"] == appointment_id), None)
    if update_appointment:
        update_appointment["date"] = appointment.date
        update_appointment["time"] = appointment.time
        update_appointment["description"] = appointment.description
        
        return update_appointment
    
    raise HTTPException(status_code=404, detail="Appointment not found")
