from fastapi import FastAPI
from fastapi_app.routes import auth, appointments
from fastapi_app.core.database import engine, Base
from fastapi_app.models import users # Isso registra o modelo no Base
from sqlalchemy import text

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])

Base.metadata.create_all(bind=engine)


@app.get("/health/db")
def check_db():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "Banco conectado com sucesso"}
