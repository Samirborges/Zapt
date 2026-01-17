import uuid
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from fastapi_app.core.database import Base


class ProfessionalProfile(Base):
    __tablename__ = "professional_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    specialty = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)

    appointment_duration = Column(Integer, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
