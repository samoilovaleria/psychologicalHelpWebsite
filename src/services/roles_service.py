from src.repositories.roles_repo import get_role
from uuid import UUID

def get_role_by_id(user_id: UUID):
    return get_role(user_id)
