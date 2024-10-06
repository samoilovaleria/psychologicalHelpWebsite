from fastapi import HTTPException, APIRouter
from src.services.roles_service import get_role_by_id
from src.schemas.roles_schema import RoleBase

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/{user_id}", response_model=RoleBase)
async def read_appointment(user_id: int):
    appointment = await get_role_by_id(user_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return appointment