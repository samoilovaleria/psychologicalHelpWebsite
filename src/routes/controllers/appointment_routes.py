from fastapi import HTTPException, APIRouter, Response, Request

from src.services.appointment_service import (
    get_appointment_by_id,
    create_appointment as srv_create_appointment,
    cancel_appointment_by_id as srv_cancel_appointment_by_id
)

from src.schemas.appointment_schema import (
    AppointmentBase,
    AppointmentCreateRequest,
    AppointmentCreateResponse
)

from uuid import UUID


router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.get("/{appointment_id}", response_model=AppointmentBase)
async def read_appointment(appointment_id: UUID):
    appointment = await get_appointment_by_id(appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.post("/create", response_model=AppointmentCreateResponse)
async def create_appointment(appointment: AppointmentCreateRequest, request: Request):
    try:
        appointment_id = await srv_create_appointment(appointment)
    except:
        raise HTTPException(status_code=400, detail="Invalid data")

    return {"appointment_id": appointment_id}


@router.put("/{appointment_id}/cancel")
async def cancel_appointment(appointment_id: UUID):
    try:
        await srv_cancel_appointment_by_id(appointment_id)
        return {"message": "Встреча успешно отменена"}
    except HTTPException as e:
        raise e
    except:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
