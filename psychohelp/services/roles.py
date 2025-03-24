from psychohelp.repositories.roles import get_role_by_user_id

from uuid import UUID


def get_role_by_id(user_id: UUID):
    return get_role_by_user_id(user_id)
