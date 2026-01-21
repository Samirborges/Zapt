from fastapi import FastAPI
from fastapi_app.routes import auth
from fastapi_app.appointments.router import router as appointments_router
from fastapi_app.core.database import engine, Base
from fastapi_app.models import users # Isso registra o modelo no Base
from fastapi_app.appointments.models import Appointment  # Registrar o modelo de agendamento
from sqlalchemy import text
from fastapi_app.professional_profiles.models import ProfessionalProfile
from fastapi_app.professional_profiles.router import router as professional_router

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(appointments_router)
app.include_router(professional_router)

Base.metadata.create_all(bind=engine)


@app.get("/health/db")
def check_db():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "Banco conectado com sucesso"}
