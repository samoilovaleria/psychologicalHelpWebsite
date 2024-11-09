from fastapi import HTTPException, APIRouter
from src.services.therapists_service import get_therapist_by_id
from src.schemas.therapist_schema import TherapistBase
from uuid import UUID

router = APIRouter(prefix="/therapists", tags=["therapists"])


@router.get("/{therapist_id}", response_model=TherapistBase)
async def read_appointment(therapist_id: UUID):
    appointment = await get_therapist_by_id(therapist_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Therapist not found")
    return appointment