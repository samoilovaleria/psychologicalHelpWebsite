from fastapi import HTTPException, APIRouter, Response, Request

from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)

from psychohelp.services.appointments import (
    get_appointment_by_id,
    create_appointment as srv_create_appointment,
    cancel_appointment_by_id,
    get_appointments_by_token,
    get_appointments_by_user_id,
    UUID,
)
from psychohelp.schemas.appointments import AppointmentBase, AppointmentCreateRequest


router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("/", response_model=list[AppointmentBase])
async def get_appointments(request: Request, user_id: UUID | None = None):
    if user_id is None:
        if "access_token" not in request.cookies:
            raise HTTPException(
                HTTP_401_UNAUTHORIZED, detail="Пользователь не авторизован"
            )
        token = request.cookies["access_token"]
        return await get_appointments_by_token(token)

    return await get_appointments_by_user_id(user_id)


@router.post("/create", response_model=AppointmentBase)
async def create_appointment(appointment: AppointmentCreateRequest, request: Request):
    try:
        appointment = await srv_create_appointment(**appointment.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return appointment


@router.get("/{id}", response_model=AppointmentBase)
async def get_appointment(id: UUID):
    appointment = await get_appointment_by_id(id)
    if appointment is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Встреча не найдена")
    return appointment


@router.put("/{id}/cancel")
async def cancel_appointment(id: UUID):
    try:
        await cancel_appointment_by_id(id)
    except ValueError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))

    return Response(None, status_code=HTTP_200_OK)
