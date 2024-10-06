from sqlalchemy import Column, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.config.database import Base
import enum

class AppointmentType(enum.Enum):
    Offline = 'Offline'
    Online = 'Online'

class AppointmentStatus(enum.Enum):
    Approved = 'Approved'
    Accepted = 'Accepted'
    Cancelled = 'Cancelled'
    Done = 'Done'

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    therapist_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    type = Column(Enum(AppointmentType), nullable=False)
    reason = Column(String(64), nullable=True)
    status = Column(Enum(AppointmentStatus), nullable=False)
    remind_time = Column(DateTime, nullable=True)
    last_change_time = Column(DateTime, nullable=False)
    venue = Column(String(128), nullable=False)

    patient = relationship("User", foreign_keys=[patient_id], back_populates="appointments_as_patient")
    therapist = relationship("User", foreign_keys=[therapist_id], back_populates="appointments_as_therapist")
    review = relationship("Review", back_populates="appointment", uselist=False)
