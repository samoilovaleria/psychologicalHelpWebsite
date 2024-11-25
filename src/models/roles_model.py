import uuid
import enum

from sqlalchemy import Column, ForeignKey, Enum, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from src.config.database import Base
from sqlalchemy.dialects.postgresql import UUID

class UserRole(enum.Enum):
    Student = 'Student'
    Therapist = 'Therapist'
    Administrator = 'Administrator'
    Stuff = 'Stuff'

class Role(Base):
    __tablename__ = 'roles'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    role = Column(Enum(UserRole), nullable=False)

    __table_args__ = (PrimaryKeyConstraint("user_id", "role"),)
    user = relationship("User", back_populates="roles")
