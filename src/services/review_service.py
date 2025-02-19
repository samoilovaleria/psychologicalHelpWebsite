from repositories.review_repo import get_review
from uuid import UUID

def get_review_by_id(appointment_id: UUID):
    return get_review(appointment_id)
