import uuid
from sqlalchemy import Column, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.config.database import Base
import enum
from sqlalchemy.dialects.postgresql import UUID

class UserRole(enum.Enum):
    Student = 'Student'
    Therapist = 'Therapist'
    Administrator = 'Administrator'
    Stuff = 'University employee'

class Role(Base):
    __tablename__ = 'roles'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    role = Column(Enum(UserRole), primary_key=True, nullable=False)

    user = relationship("User", back_populates="roles")
