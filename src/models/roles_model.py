from sqlalchemy import Column, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.config.database import Base
import enum
from sqlalchemy.dialects.postgresql import UUID

class UserRole(enum.Enum):
    Patient = 'Patient'
    Therapist = 'Therapist'
    Administrator = 'Administrator'

class Role(Base):
    __tablename__ = 'roles'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    role = Column(Enum(UserRole), primary_key=True)

    user = relationship("User", back_populates="roles")
