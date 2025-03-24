from fastapi import HTTPException, APIRouter, Query, Request

from psychohelp.services.therapists import (
    get_therapist_by_id,
    get_all_therapists,
)
from psychohelp.schemas.therapists import TherapistBase

from uuid import UUID

router = APIRouter(prefix="/therapists", tags=["therapists"])


@router.get("/{therapist_id}", response_model=TherapistBase)
async def read_appointment(therapist_id: UUID):
    appointment = await get_therapist_by_id(therapist_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Therapist not found")
    return appointment


@router.get("/", response_model=list[TherapistBase])
async def read_therapists(
    request: Request, skip: int = Query(0, ge=0), take: int = Query(10, gt=0)
):
    """
    Получить список психологов с пагинацией
    """
    therapists = await get_all_therapists(request, skip=skip, take=take)
    if not therapists:
        raise HTTPException(status_code=404, detail="No therapists found")
    return therapists
