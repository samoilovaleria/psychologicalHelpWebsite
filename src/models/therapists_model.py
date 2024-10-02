from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base

class Therapist(Base):
    __tablename__ = 'therapists'

    id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    experience = Column(String(64), nullable=False)
    qualification = Column(String(128), nullable=False)
    consult_areas = Column(String(128), nullable=False)
    description = Column(String(256), nullable=False)
    office = Column(String(128), nullable=False)

    user = relationship("User", back_populates="therapist_info")
