from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.config.database import Base

class Review(Base):
    __tablename__ = 'reviews'

    appointment_id = Column(Integer, ForeignKey('appointments.id', ondelete='CASCADE'), primary_key=True)
    time = Column(DateTime, nullable=False)
    content = Column(Text, nullable=False)

    appointment = relationship("Appointment", back_populates="review")
