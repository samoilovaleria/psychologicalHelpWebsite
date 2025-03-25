from fastapi import HTTPException, APIRouter

from starlette.status import HTTP_404_NOT_FOUND

from psychohelp.services.roles import get_roles_by_id
from psychohelp.models.roles import UserRole

from uuid import UUID

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/{user_id}", response_model=list[UserRole])
async def get_roles(user_id: UUID):
    roles = [r.role for r in await get_roles_by_id(user_id)]
    if not roles:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Роли не найдены")
    return roles
