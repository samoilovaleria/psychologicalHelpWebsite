from psychohelp.repositories import create_access_token, verify_password, hash_password
from psychohelp.repositories.users import (
    get_user_by_id as repo_get_user_by_id,
    get_user_by_email as repo_get_user_by_email,
    get_user_by_token as repo_get_user_by_token,
    create_user,
    UserRole,
    UUID,
)
from psychohelp.repositories.roles import add_roles_by_user_id


async def get_user_by_id(user_id: UUID):
    return await repo_get_user_by_id(user_id)


async def get_user_by_email(email: str):
    return await repo_get_user_by_email(email)


async def get_user_by_token(token: str):
    return await repo_get_user_by_token(token)


async def register_user(
    first_name: str,
    last_name: str,
    phone_number: str,
    email: str,
    password: str,
    middle_name: str | None = None,
    social_media: str | None = None,
):
    new_user = await create_user(
        first_name,
        last_name,
        phone_number,
        email,
        hash_password(password),
        middle_name,
        social_media,
    )
    return create_access_token(new_user.id)


async def login_user(email: str, password: str):
    user = await repo_get_user_by_email(email)
    if user is None or not verify_password(password, user.password):
        return None

    return create_access_token(user.id)
