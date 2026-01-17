import uuid
from sqlalchemy import (
    Column,
    Date,
    Time,
    DateTime,
    String,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from fastapi_app.core.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    professional_id = Column(
        UUID(as_uuid=True),
        ForeignKey("professional_profiles.id"),
        nullable=False
    )

    client_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    appointment_date = Column(
        Date,
        nullable=False
    )

    start_time = Column(
        Time,
        nullable=False
    )

    end_time = Column(
        Time,
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
