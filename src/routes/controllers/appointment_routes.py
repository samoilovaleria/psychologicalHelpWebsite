from fastapi import HTTPException, APIRouter
from src.services.appointment_service import get_appointment_by_id
from src.schemas.appointment_schema import AppointmentBase
from uuid import UUID

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("/{appointment_id}", response_model=AppointmentBase)
async def read_appointment(appointment_id: UUID):
    appointment = await get_appointment_by_id(appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment