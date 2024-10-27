from src.repositories.therapist_repo import get_therapist
from uuid import UUID

def get_therapist_by_id(therapist_id: UUID):
    return get_therapist(therapist_id)
