from src.repositories.appointment_repo import get_appointment

def get_appointment_by_id(appointment_id: int):
    return get_appointment(appointment_id)
