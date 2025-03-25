from psychohelp.repositories.roles import (
    get_roles_by_user_id as repo_get_roles_by_user_id,
    add_roles_by_user_id as repo_add_roles_by_user_id,
    delete_roles_by_user_id as repo_delete_roles_by_user_id,
    UserRole,
    UUID,
)


async def get_roles_by_user_id(user_id: UUID):
    return await repo_get_roles_by_user_id(user_id)


async def add_roles_by_user_id(user_id: UUID, roles: list[UserRole]):
    await repo_add_roles_by_user_id(user_id, roles)


async def delete_roles_by_user_id(user_id: UUID, roles: list[UserRole]):
    await repo_delete_roles_by_user_id(user_id, roles)
