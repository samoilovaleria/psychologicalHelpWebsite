from src.repositories.appointment_repo import get_appointment
from uuid import UUID

def get_appointment_by_id(appointment_id: UUID):
    return get_appointment(appointment_id)
