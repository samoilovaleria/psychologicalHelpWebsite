from psychohelp.repositories.reviews import get_review, UUID


def get_review_by_id(appointment_id: UUID):
    return get_review(appointment_id)
