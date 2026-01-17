from sqlalchemy.orm import Session

from fastapi_app.models.users import User
from fastapi_app.models.professional_profiles import ProfessionalProfile
from fastapi_app.schemas.user import UserCreate, UserRole
from fastapi_app.core.security import get_password_hash


def create_user(db: Session, user_data: UserCreate) -> User:
    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        role=user_data.role
    )

    db.add(user)
    db.flush()  # 🔑 gera user.id antes do commit

    if user.role == UserRole.PROFESSIONAL:
        profile = ProfessionalProfile(
            user_id=user.id,
            appointment_duration=30  # valor padrão
        )
        db.add(profile)

    db.commit()
    db.refresh(user)
    return user
