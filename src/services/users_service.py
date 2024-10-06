from src.repositories.users_repo import get_user

def get_user_by_id(user_id: int):
    return get_user(user_id)
