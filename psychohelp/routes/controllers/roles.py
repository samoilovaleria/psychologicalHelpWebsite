from fastapi import HTTPException, APIRouter

from psychohelp.services.roles import get_roles_by_id
from psychohelp.schemas.roles import RoleBase

from uuid import UUID

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/{user_id}", response_model=list[RoleBase])
async def get_roles(user_id: UUID):
    roles = await get_roles_by_id(user_id)
    if roles is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return roles
