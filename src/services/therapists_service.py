from src.repositories.therapist_repo import get_therapist

def get_therapist_by_id(therapist_id: int):
    return get_therapist(therapist_id)
