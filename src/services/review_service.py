from src.repositories.review_repo import get_review

def get_review_by_id(appointment_id: int):
    return get_review(appointment_id)
