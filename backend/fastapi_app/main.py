from fastapi import FastAPI
from fastapi_app.routes import auth, appointments

from pydantic import BaseModel

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])

