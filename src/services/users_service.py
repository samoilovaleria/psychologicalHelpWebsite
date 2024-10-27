from src.repositories.users_repo import get_user
from uuid import UUID

def get_user_by_id(user_id: UUID):
    return get_user(user_id)
