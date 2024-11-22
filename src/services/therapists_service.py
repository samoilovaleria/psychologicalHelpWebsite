from src.repositories.therapist_repo import get_therapist, get_therapists_with_pagination
from uuid import UUID

def get_therapist_by_id(therapist_id: UUID):
    return get_therapist(therapist_id)

async def get_all_therapists(skip: int = 0, take: int = 10):
    """
    Получить список всех психологов с пагинацией
    """
    therapists = await get_therapists_with_pagination(skip=skip, take=take)
    return therapists