from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.config.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(64), nullable=True)
    social_media = Column(String(50), nullable=False)
    password = Column(String(64), nullable=False)

    roles = relationship("Role", back_populates="user")
    appointments_as_patient = relationship("Appointment", foreign_keys="[Appointment.patient_id]", back_populates="patient")
    appointments_as_therapist = relationship("Appointment", foreign_keys="[Appointment.therapist_id]", back_populates="therapist")
    therapist_info = relationship("Therapist", back_populates="user", uselist=False)
