from fastapi import FastAPI

app = FastAPI()

stored_appointments = [
    {"id": 1, "date": "2024-07-01", "time": "10:00", "description": "Dentist appointment"},
    {"id": 2, "date": "2024-07-02", "time": "14:00", "description": "Meeting with client"},
    {"id": 3, "date": "2024-07-03", "time": "09:00", "description": "Yoga class"},
]

@app.get("/")
def get_all_appoitnments():
    return {"appoitnments": stored_appointments}


@app.post("/create-appointment")
def create_appointment(date: str, time: str, description: str):
    stored_appointments.append({
        "id": len(stored_appointments) + 1,
        "date": date,
        "time": time,
        "description": description
    })
    return {
        "id": stored_appointments[-1]["id"],
        "date": date,
        "time": time,
        "description": description,
    }