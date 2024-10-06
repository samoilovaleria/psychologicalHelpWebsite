from src.repositories.roles_repo import get_role

def get_role_by_id(user_id: int):
    return get_role(user_id)
