from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.config.database import Base
import enum

class UserRole(enum.Enum):
    Patient = 'Patient'
    Therapist = 'Therapist'
    Administrator = 'Administrator'

class Role(Base):
    __tablename__ = 'roles'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    role = Column(Enum(UserRole), primary_key=True)

    user = relationship("User", back_populates="roles")
