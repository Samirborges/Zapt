from fastapi_app.core.database import Base
from sqlalchemy import (
    Column,
    Integer,
    Time,
    ForeignKey
)
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Availability (Base):
    __tablename__ = "availability"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    professional_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "professional_profiles.id",
            ondelete="CASCADE"
        ),
        nullable=False,
    )
    
    day_of_week = Column(
        Integer, 
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
    
    